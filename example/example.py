from spdlqj import NaverCafeArchive


def main():
    if __name__ == '__main__':
        # <-- INITIALIZE -->
        app: NaverCafeArchive = NaverCafeArchive(cafe_id=10050146)

        # <-- DOWNLOAD A LIST OF ARTICLES FOR THAT USER PARAMETER -->
        app.download_article_list_csv(cafe_menu_id=47, per_page=10, max_page=1)

        # <-- GET DETAIL ARTICLE CONTENT -->
        print(app.get_article_content(article_id=336033175)['article_content_html'])

        # <-- DOWNLOAD A LIST OF MENU IN CAFE -->
        app.download_menu_list_csv()

        # <-- DOWNLOAD A LIST OF ARTICLES FOR THAT USER SEARCH QUERY -->
        app.download_search_article_list_csv(query='BMW', sort_by=app.sort_by.NEWEST, result_count=30)
        app.download_search_article_list_csv(query='BMW', sort_by=app.sort_by.SIMILARITY, result_count=30)


main()
