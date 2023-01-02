from module import NaverCafeArchive
from module import SortByData


def main():
    if __name__ == '__main__':
        # <-- INITIALIZE -->
        NCA = NaverCafeArchive(cafe_id=27842958)
        # <-- DOWNLOAD A LIST OF ARTICLES FOR THAT USER PARAMETER -->
        # NCA.download_article_list_csv(cafe_menu_id=362, per_page=10, max_page=1)
        # <-- GET DETAIL ARTICLE CONTENT -->
        # print(NCA.get_article_content(963354665)['article_content_html'])
        # <-- DOWNLOAD A LIST OF MENU IN CAFE -->
        # NCA.download_menu_list_csv()
        # <-- DOWNLOAD A LIST OF ARTICLES FOR THAT USER SEARCH QUERY -->
        NCA.download_search_article_list_csv('BMW', SortByData.NEWEST, 30)


main()