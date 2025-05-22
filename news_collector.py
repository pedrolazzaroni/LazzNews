import feedparser

def get_news_from_feeds(feed_urls):
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                'title': entry.get('title', 'Sem título'),
                'summary': entry.get('summary', 'Sem resumo'),
                'link': entry.get('link', '#'),
                'published': entry.get('published', '')
            })
    return articles
