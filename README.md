# Naver Cafe Archive

🇰🇷 Naver Cafe Archive Module

<a href="https://pypi.org/project/spdlqj/">
  <img alt="PyPI Module Version" src="https://img.shields.io/pypi/v/spdlqj?style=for-the-badge&labelColor=000" />
</a>
<a href="https://opensource.org/licenses/MIT">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge&labelColor=000" />
</a>

# `NaverCafeArchive`

## installation
```bash
pip3 install spdlqj 
```

```python
from spdlqj import NaverCafeArchive

app: NaverCafeArchive = NaverCafeArchive(cafe_id=10050146)  # 중고나라
```

### Parameters

- cafe_id: `Union[str, int]`
    - The target cafe ID to archive

### Properties

- `NaverCafeArchive.sort_by`
- `NaverCafeArchive.download`

### Methods

- `get_article_list()`
- `get_menu_list()`
- `get_article_content()`
- `search_articles()`
- `download_article_list_csv()`
- `download_menu_list_csv()`
- `download_search_article_list_csv()`

## NaverCafeArchive.sort_by

### Properties

- `app.sort_by.NEWEST`: `str`
    - The newest sort option for `NaverCafeArchive.search_articles()` result

- `app.sort_by.SIMILARITY`: `str`
    - The similarity sort option for `NaverCafeArchive.search_articles()` result

## NaverCafeArchive.download

### Methods

- `app.article_list(menu_id: Union[str, int]) -> str`
    - The path of article list csv file.
    - Path Rule: `{current_path}/articles/{cafe_id}/{menu_id}`

- `app.menu_list() -> str`
    - The path of menu list csv file.
    - Path Rule: `{current_path}/menus/{menus}`

- `app.search_article_list(query: str) -> str`
    - The path of search list csv file.
    - Path Rule: `{current_path}/search/{cafe_id}/{query}`

- `app.make_directory(callback_path: str) -> None`
    - Create a directory with 'callback_path' received as a parameter.

## NaverCafeArchive.get_article_list()

> The method of extract articles.

### Parameters

- cafe_menu_id: `Union[str, int]`
    - Cafe menu ID to extract articles

- per_page (default: 50): `int`
    - Number of articles per page

- page (default: 1): `int`

> The number of articles extracted is calculated by the formula `per_page`*`page`

### Return Value

- Optional[Generator]
    - `article_id`: The article id.
    - `article_title`: The article title.
    - `article_writer`: The writer of the article.
    - `article_is_open`: The permission of target cafe members to open the article.
    - `article_view`: The views of the article.
    - `article_like`: The like count of the article.
    - `article_comment`: The comment count of the article.
    - `article_datetime`: The datetime that the article was published.

## NaverCafeArchive.get_menu_list()

> The method of extract menu list.

### Return Value

- Optional[Generator]
    - `menu_name`: The menu title.
    - `menu_type`: The type of the menu.
    - `menu_id`: The menu id.
    - `is_menu_updated`: The state to determine if this menu has been updated.

## NaverCafeArchive.get_article_content()

> The method of extract article content.

### Parameters

- article_id: `Union[str, int]`
    - Cafe menu ID to extract articles

### Return Value

- Optional[dict]
    - `article_menu_id`: The article id.
    - `article_title`: The article title.
    - `article_writer_nickname`: The writer nickname of the article.
    - `article_writer_id`: The writer id of the article.
    - `article_view`: The views of the article.
    - `article_datetime`: The datetime that the article was published.
    - `article_content_html`: The html of the article.

## NaverCafeArchive.search_articles()

> The method of extract articles based on query results.

### Parameters

- query: `str`
- sort_by: `str` (based `NaverCafeArchive.sort_by`)
- result_count: int

### Return Value

- Optional[Generator]
    - `article_id`: The article id.
    - `article_title`: The article title.
    - `article_writer_nickname`: The writer nickname of the article.
    - `article_writer_key`: The writer UUID of the article.
    - `article_view`: The views of the article.
    - `article_like`: The like count of the article.
    - `article_comment`: The comment count of the article.
    - `article_datetime`: The datetime that the article was published.

## NaverCafeArchive.download_article_list_csv()

> The method of download csv file based on `NaverCafeArchive.get_article_list()`.

### Parameters

- cafe_menu_id: `Union[str, int]`
    - Cafe menu ID to extract articles

- per_page (default: 50): `int`
    - Number of articles per page

- page (default: 1): `int`

### Return Value

- None, but the csv file is saved to the specified path. (refer `NaverCafeArchive.download.search_article_list`)

## NaverCafeArchive.download_menu_list_csv()

> The method of download csv file based on `NaverCafeArchive.get_menu_list()`.

### Return Value

- None, but the csv file is saved to the specified path. (refer `NaverCafeArchive.download.menu_list()`)

## NaverCafeArchive.download_search_article_list_csv()

> The method of download csv file based on `NaverCafeArchive.search_articles()`.

### Parameters

- query: `str`
- sort_by: `str` (based `NaverCafeArchive.sort_by`)
- result_count: int

### Return Value

- None, but the csv file is saved to the specified path. (refer `NaverCafeArchive.download.search_article_list`)