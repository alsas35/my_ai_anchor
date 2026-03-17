from duckduckgo_search import DDGS
from newspaper import Article

class NewsToolkit:
    def search_topics(self, query):
        with DDGS() as ddgs:
            results = ddgs.news(query, region='wt-wt', safesearch='off', timelimit='h', max_results=5)
            if not results:
                results = ddgs.news(query, region='wt-wt', safesearch='off', timelimit='d', max_results=3)
            return [{"title": r['title'], "url": r['url']} for r in results]

    def fetch_article_content(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except:
            return ""