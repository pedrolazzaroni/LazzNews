import feedparser
from datetime import datetime, date
import re
from html import unescape

def clean_html(raw_html):
    """Remove tags HTML e limpa o texto"""
    if not raw_html:
        return ''
    # Remove tags HTML
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Decodifica entidades HTML
    cleantext = unescape(cleantext)
    # Remove quebras de linha excessivas e espaços
    cleantext = re.sub(r'\s+', ' ', cleantext).strip()
    return cleantext

def get_news_from_feeds(feeds):
    articles = []
    today = date.today()
    
    for feed_info in feeds:
        # Se feed_info for um dicionário com name e url
        if isinstance(feed_info, dict):
            feed_name = feed_info['name']
            feed_url = feed_info['url']
        else:
            # Fallback para compatibilidade com URLs simples
            feed_url = feed_info
            feed_name = "Fonte Desconhecida"
        
        try:
            feed = feedparser.parse(feed_url)
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
                
                # Verificar se a notícia é de hoje
                article_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    article_date = date(*entry.published_parsed[:3])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    article_date = date(*entry.updated_parsed[:3])
                
                # Só adicionar se for notícia de hoje
                if article_date == today:
                    # Limpar HTML do título e resumo
                    clean_title = clean_html(entry.get('title', 'Sem título'))
                    clean_summary = clean_html(entry.get('summary', 'Sem resumo'))
                    
                    articles.append({
                        'title': clean_title,
                        'summary': clean_summary,
                        'link': entry.get('link', '#'),
                        'published': entry.get('published', ''),
                        'image': image_url,
                        'source': feed_name
                    })
        except Exception as e:
            print(f"Erro ao processar feed {feed_url}: {e}")
            continue
    
    return articles

def get_tech_feeds():
    """Retorna uma lista de feeds RSS de sites BRASILEIROS de tecnologia"""
    return [
        {"name": "Olhar Digital", "url": "https://olhardigital.com.br/feed/"},
        {"name": "Tecnoblog", "url": "https://tecnoblog.net/feed/"},
        {"name": "TechTudo", "url": "https://www.techtudo.com.br/rss/"},
        {"name": "Canaltech", "url": "https://canaltech.com.br/rss/"},
        {"name": "Hardware.com.br", "url": "https://www.hardware.com.br/rss/noticias.xml"},
        {"name": "Adrenaline", "url": "https://www.adrenaline.com.br/rss/"},
        {"name": "ShowMeTech", "url": "https://www.showmetech.com.br/feed/"},
        {"name": "TudoCelular", "url": "https://www.tudocelular.com/rss/noticias.xml"},
        {"name": "MeioBit", "url": "https://feeds.feedburner.com/MeioBit"},
        {"name": "MobileTime", "url": "https://www.mobiletime.com.br/feed/"},
        {"name": "TecMundo", "url": "https://www.tecmundo.com.br/rss"},
        {"name": "UOL Tilt", "url": "https://www.uol.com.br/tilt/rss.xml"}
    ]
