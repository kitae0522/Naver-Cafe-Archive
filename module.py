from typing import Final, Generator, Iterator, Optional
from datetime import datetime
import requests as req
import pandas as pd
import itertools
import time
import re
import os


class SortByData:
    NEWEST: str = 'date'
    SIMILARITY: str = 'sim'


class DownloadPath:
    def __init__(self, cafe_id: int):
        self.cafe_id: int = cafe_id

    def article_list(self, menu_id: int) -> str:
        return f'{os.getcwd()}/articles/{self.cafe_id}/{menu_id}'

    def menu_list(self) -> str:
        return f'{os.getcwd()}/menus/{self.cafe_id}'

    def search_article_list(self, query: str) -> str:
        return f'{os.getcwd()}/search/{self.cafe_id}/{query}'

    @staticmethod
    def make_directory(callback_path: str) -> None:
        if not os.path.exists(callback_path):
            os.makedirs(callback_path)


class NaverCafeArchive(DownloadPath):
    def __init__(self, cafe_id: int) -> None:
        self.api_host: Final[str] = 'https://apis.naver.com'
        self.cafe_id: Final[int] = cafe_id
        super().__init__(cafe_id=cafe_id)

    @staticmethod
    def request_get(url: str) -> Optional[Iterator]:
        try:
            api_get: req.models.Response = req.get(url)
            api_get.raise_for_status()
            api_get_json: Iterator = api_get.json()
            return api_get_json
        except req.exceptions.Timeout as err_timeout:
            print(f'Timeout Error: {err_timeout}')
        except req.exceptions.ConnectionError as err_conn:
            print(f'Connection Error: {err_conn}')
        except req.exceptions.JSONDecodeError as err_json:
            print(f'JSON Decode Error: {err_json}')
        except req.exceptions.HTTPError as err_http:
            print(f'HTTP Error: {err_http}')
        return None

    @staticmethod
    def unix_time_to_datetime(datetime_stamp: str) -> str:
        preprocess_datetime: int = int(datetime_stamp[:-3])
        return datetime.fromtimestamp(preprocess_datetime).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def convert_date_string_to_datetime(date_string: str) -> datetime:
        return datetime.strptime(date_string, '%a %b %d %H:%M:%S %Z %Y')

    def get_article_list(self, cafe_menu_id: int, per_page: int = 50, page: int = 1) -> Generator:
        URL: Final[str] = f'{self.api_host}/cafe-web/cafe2/ArticleList.json?' \
                          f'search.clubid={self.cafe_id}&' \
                          f'search.menuid={cafe_menu_id}&' \
                          f'boardType=L&search.perPage={per_page}&' \
                          f'search.page={page}'
        api_get_json: Iterator = self.request_get(URL)
        articles = api_get_json['message']['result']['articleList']
        return (
            dict(article_id=article['articleId'],
                 article_title=article['subject'],
                 article_writer=article['writerId'],
                 article_is_open=article['openArticle'],
                 article_view=article['readCount'],
                 article_like=article['likeItCount'],
                 article_comment=article['commentCount'],
                 article_datetime=self.unix_time_to_datetime(str(article['writeDateTimestamp'])))
            for article in articles
        )

    def get_menu_list(self) -> Generator:
        URL: Final[str] = f'{self.api_host}/cafe-web/cafe2/SideMenuList?' \
                          f'cafeId={self.cafe_id}'
        api_get_json: Iterator = self.request_get(URL)
        menu_list = api_get_json['message']['result']['menus']
        return (
            dict(menu_name=menu['menuName'],
                 menu_type=menu['menuType'],
                 menu_id=menu['menuId'],
                 is_menu_updated=menu['hasNewArticle'])
            for menu in menu_list
            if menu['menuType'] != 'F' and menu['menuType'] != 'S'
        )

    def get_article_content(self, article_id: str):
        URL: Final[str] = f'{self.api_host}/cafe-web/cafe-articleapi/v2/cafes/{self.cafe_id}/articles/{article_id}'
        api_get_json: Iterator = self.request_get(URL)
        return (
            dict(article_menu_id=api_get_json['result']['article']['menu']['id'],
                 article_title=api_get_json['result']['article']['subject'],
                 article_writer_nickname=api_get_json['result']['article']['writer']['nick'],
                 article_writer_id=api_get_json['result']['article']['writer']['id'],
                 article_view=api_get_json['result']['article']['readCount'],
                 article_datetime=self.unix_time_to_datetime(str(api_get_json['result']['article']['writeDate'])),
                 article_content_html=api_get_json['result']['article']['contentHtml'])
        )

    def search_articles(self, query: str, sort_by: str, result_count: int):
        URL: Final[str] = f'{self.api_host}/cafe-web/cafe-mobile/CafeMobileWebArticleSearchListV3?' \
                          f'cafeId={self.cafe_id}&' \
                          f'query={query}&' \
                          f'sortBy={sort_by}&' \
                          f'perPage={result_count}&' \
                          f'adUnit=MW_CAFE_BOARD'
        api_get_json: Iterator = self.request_get(URL)
        articles = api_get_json['message']['result']['articleList']
        return (
            dict(article_id=article['articleId'],
                 article_title=re.sub('<.+?>', '', article['subject']),
                 article_writer_nickname=article['memberNickName'],
                 article_writer_key=article['memberKey'],
                 article_view=article['readCount'],
                 article_like=article['likeItCount'],
                 article_comment=article['commentCount'],
                 article_datetime=self.convert_date_string_to_datetime(article['addDate']))
            for article in articles
        )

    def download_article_list_csv(self, cafe_menu_id: int, per_page: int, max_page: int) -> None:
        start_time: float = time.time()
        result: Generator = (self.get_article_list(cafe_menu_id, per_page, page)
                             for page in range(1, max_page + 1)
                             if time.sleep(0.5) is None)
        result: Iterator = list(itertools.chain.from_iterable(result))
        save_directory_path = self.article_list(cafe_menu_id)
        self.make_directory(save_directory_path)
        time_string: str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        pd.DataFrame(result).to_csv(f'{save_directory_path}/{time_string}.csv')
        end_time: float = time.time()
        print(f'✅ Article List Download Finished in {end_time - start_time} seconds')

    def download_menu_list_csv(self) -> None:
        start_time: float = time.time()
        result: Generator = self.get_menu_list()
        save_directory_path = self.menu_list()
        self.make_directory(save_directory_path)
        time_string: str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        pd.DataFrame(result).to_csv(f'{save_directory_path}/{time_string}.csv')
        end_time: float = time.time()
        print(f'✅ Menu List Download Finished in {end_time - start_time} seconds')

    def download_search_article_list_csv(self, query: str, sort_by: str, result_count: int) -> None:
        start_time: float = time.time()
        result: Generator = self.search_articles(query, sort_by, result_count)
        save_directory_path = self.search_article_list(query)
        self.make_directory(save_directory_path)
        time_string: str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        pd.DataFrame(result).to_csv(
            f'{save_directory_path}/{"NEWEST" if sort_by == SortByData.NEWEST else "SIMILARITY"}_{time_string}.csv')
        end_time: float = time.time()
        print(f'✅ Article List Of User Search Query Download Finished in {end_time - start_time} seconds')
