from flask import Flask, render_template, jsonify
from news_collector import get_news_from_feeds, get_tech_feeds
from summarizer import summarize_text
import threading
import time

app = Flask(__name__)

# Cache global de notícias
news_cache = []
last_update = 0

def update_news():
    """Atualiza o cache de notícias em background"""
    global news_cache, last_update
    feeds = get_tech_feeds()
    news_cache = get_news_from_feeds(feeds)
    last_update = time.time()

def get_cached_news():
    """Retorna notícias do cache, atualizando se necessário"""
    global news_cache, last_update
    # Atualiza se não há cache ou se passou 30 minutos
    if not news_cache or (time.time() - last_update) > 1800:
        threading.Thread(target=update_news, daemon=True).start()
        if not news_cache:  # Se ainda não há cache, busca sincronamente
            update_news()
    return news_cache

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    """API para buscar notícias"""
    news = get_cached_news()
    return jsonify({
        'news': news,
        'count': len(news),
        'last_update': last_update
    })

@app.route('/api/refresh')
def api_refresh():
    """API para forçar atualização das notícias"""
    global news_cache, last_update
    feeds = get_tech_feeds()
    news_cache = get_news_from_feeds(feeds)
    last_update = time.time()
    return jsonify({
        'success': True,
        'news': news_cache,
        'count': len(news_cache),
        'last_update': last_update
    })

@app.route('/api/sources')
def api_sources():
    """API para obter lista de fontes"""
    # Usar a mesma lista de feeds para manter consistência
    feeds = get_tech_feeds()
    sources = [{"name": feed["name"], "url": feed["url"].replace("/feed/", "").replace("/rss/", "").replace("/rss", "")} for feed in feeds]
    return jsonify({'sources': sources})

@app.route('/api/summarize')
def api_summarize():
    """API para sumarizar texto"""
    from flask import request
    text = request.args.get('text', '')
    summary = summarize_text(text)
    return jsonify({'summary': summary})
if __name__ == '__main__':
    # Carrega notícias na inicialização
    update_news()
    app.run(debug=True, host='0.0.0.0', port=5000)
