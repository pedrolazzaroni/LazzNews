import streamlit as st
from news_collector import get_news_from_feeds
from summarizer import summarize_text

# CSS customizado inspirado no design do site pedrolazzaroni.com.br
st.markdown('''
    <style>
    body, .stApp {
        background: #f7f7f7;
        font-family: 'Montserrat', Arial, sans-serif;
    }
    .main-title {
        color: #1a1a1a;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5em;
        letter-spacing: -1px;
    }
    .news-card {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        padding: 1.5em 2em;
        margin-bottom: 2em;
        display: flex;
        gap: 1.5em;
        align-items: flex-start;
    }
    .news-img {
        width: 140px;
        height: 100px;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    }
    .news-content {
        flex: 1;
    }
    .news-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.3em;
    }
    .news-summary {
        color: #444;
        font-size: 1.05rem;
        margin-bottom: 0.7em;
    }
    .news-link {
        color: #0072ff;
        font-weight: 500;
        text-decoration: none;
        margin-right: 1em;
    }
    .summ-btn {
        background: #0072ff;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.4em 1.2em;
        font-size: 1rem;
        cursor: pointer;
        margin-top: 0.2em;
    }
    .summ-btn:hover {
        background: #005bb5;
    }
    .sidebar .sidebar-content {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 1em;
    }
    </style>
''', unsafe_allow_html=True)

st.markdown('<div class="main-title">📰 LazzNews - Agregador Pessoal de Notícias</div>', unsafe_allow_html=True)

DEFAULT_FEEDS = [
    "https://g1.globo.com/rss/g1/",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://feeds.bbci.co.uk/news/rss.xml"
]

st.sidebar.header("Fontes de Notícias")
feeds = st.sidebar.text_area(
    "Cole os links dos feeds RSS (um por linha):",
    value="\n".join(DEFAULT_FEEDS),
    height=120
).splitlines()

if st.sidebar.button("Atualizar Notícias"):
    st.session_state["news"] = get_news_from_feeds(feeds)

news = st.session_state.get("news", get_news_from_feeds(feeds))

st.markdown(f"<p style='color:#888;font-size:1.1rem;'>Foram encontradas <b>{len(news)}</b> notícias.</p>", unsafe_allow_html=True)

for idx, article in enumerate(news):
    # Renderização de imagem (se disponível)
    image_url = article.get('image', None)
    card_html = f'<div class="news-card">'
    if image_url:
        card_html += f'<img src="{image_url}" class="news-img" alt="imagem da notícia">'
    else:
        card_html += f'<img src="https://pedrolazzaroni.com.br/assets/img/news-default.jpg" class="news-img" alt="imagem padrão">'
    card_html += '<div class="news-content">'
    card_html += f'<div class="news-title">{article["title"]}</div>'
    card_html += f'<div class="news-summary">{article["summary"]}</div>'
    card_html += f'<a href="{article["link"]}" class="news-link" target="_blank">Leia mais</a>'
    card_html += '</div></div>'
    st.markdown(card_html, unsafe_allow_html=True)
    # Botão de sumarização
    if st.button("Sumarizar", key=f"summ_{idx}"):
        resumo = summarize_text(article['summary'])
        st.info(resumo)
    st.markdown("<hr style='border:0;border-top:1px solid #eee;margin:1.5em 0;'>", unsafe_allow_html=True)
