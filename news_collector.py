import feedparser

def get_news_from_feeds(feed_urls):
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Buscar imagem em diferentes campos possíveis
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                image_url = entry.media_content[0].get('url')
            elif hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if 'image' in enclosure.get('type', ''):
                        image_url = enclosure.get('href')
                        break
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')
            
            articles.append({
                'title': entry.get('title', 'Sem título'),
                'summary': entry.get('summary', 'Sem resumo'),
                'link': entry.get('link', '#'),
                'published': entry.get('published', ''),
                'image': image_url
            })
    return articles

def get_tech_feeds():
    """Retorna uma lista de feeds RSS de sites de tecnologia"""
    return [
        "https://feeds.feedburner.com/oreilly/radar",
        "https://techcrunch.com/feed/",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://www.wired.com/feed/rss",
        "https://feeds.mashable.com/Mashable",
        "https://www.theverge.com/rss/index.xml",
        "https://olhardigital.com.br/feed/",
        "https://tecnoblog.net/feed/"
    ]
