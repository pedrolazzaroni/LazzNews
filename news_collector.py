import feedparser
from datetime import datetime, date

def get_news_from_feeds(feed_urls):
    articles = []
    today = date.today()
    
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:            # Buscar imagem em diferentes campos possíveis
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
            
            # Verificar se a notícia é de hoje
            article_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                article_date = date(*entry.published_parsed[:3])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                article_date = date(*entry.updated_parsed[:3])
            
            # Só adicionar se for notícia de hoje
            if article_date == today:
                articles.append({
                    'title': entry.get('title', 'Sem título'),
                    'summary': entry.get('summary', 'Sem resumo'),
                    'link': entry.get('link', '#'),
                    'published': entry.get('published', ''),
                    'image': image_url
                })
    return articles

def get_tech_feeds():
    """Retorna uma lista de feeds RSS de sites BRASILEIROS de tecnologia"""
    return [
        "https://olhardigital.com.br/feed/",
        "https://tecnoblog.net/feed/",
        "https://www.techtudo.com.br/rss/",
        "https://canaltech.com.br/rss/",
        "https://www.hardware.com.br/rss/noticias.xml",
        "https://www.adrenaline.com.br/rss/",
        "https://www.showmetech.com.br/feed/",
        "https://www.tudocelular.com/rss/noticias.xml",
        "https://feeds.feedburner.com/MeioBit",
        "https://www.mobiletime.com.br/feed/",
        "https://www.tecmundo.com.br/rss",
        "https://www.uol.com.br/tilt/rss.xml"
    ]
