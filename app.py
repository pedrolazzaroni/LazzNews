import streamlit as st
from news_collector import get_news_from_feeds, get_tech_feeds
from summarizer import summarize_text

# CSS customizado inspirado no design do site pedrolazzaroni.com.br
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
      body, .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
    }
    .main-header {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 140, 0, 0.2);
        border: 1px solid rgba(255, 140, 0, 0.3);
    }
    .main-title {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #ff8c00, #ffa500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .subtitle {
        color: #7f8c8d;
        font-size: 1.2rem;
        font-weight: 400;
    }
    .news-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .news-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
    }
    .news-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .news-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.8rem;
        line-height: 1.3;
    }
    .news-summary {
        color: #5a6c7d;
        font-size: 1rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    .news-actions {
        display: flex;
        gap: 1rem;
        align-items: center;
    }    .news-link {
        background: linear-gradient(45deg, #ff8c00, #ffa500);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        display: inline-block;
    }
    .news-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 140, 0, 0.4);
        color: white;
        text-decoration: none;
    }
    .tech-badge {
        background: linear-gradient(45deg, #ff8c00, #ffa500);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 1rem;
        display: inline-block;
    }
    .stats-container {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stSidebar > div:first-child {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    </style>
''', unsafe_allow_html=True)

st.markdown('''
    <div class="main-header">
        <div class="main-title">🚀 LazzNews</div>
        <div class="subtitle">Agregador de Notícias de Tecnologia</div>
    </div>
''', unsafe_allow_html=True)

# Usar feeds de tecnologia por padrão
DEFAULT_TECH_FEEDS = get_tech_feeds()

st.sidebar.header("🔧 Configurações")
use_default = st.sidebar.checkbox("Usar feeds de tecnologia pré-configurados", value=True)

if use_default:
    feeds = DEFAULT_TECH_FEEDS
    st.sidebar.success(f"Usando {len(feeds)} feeds de tecnologia")
else:
    feeds = st.sidebar.text_area(
        "Cole os links dos feeds RSS (um por linha):",
        value="\n".join(DEFAULT_TECH_FEEDS),
        height=120
    ).splitlines()

if st.sidebar.button("🔄 Atualizar Notícias", type="primary"):
    with st.spinner("Buscando notícias..."):
        st.session_state["news"] = get_news_from_feeds(feeds)

news = st.session_state.get("news", get_news_from_feeds(feeds))

st.markdown(f'''
    <div class="stats-container">
        <h3>📊 {len(news)} notícias de tecnologia encontradas</h3>
    </div>
''', unsafe_allow_html=True)

# Grid de notícias
cols = st.columns(2)
for idx, article in enumerate(news):
    with cols[idx % 2]:
        card_html = f'''
        <div class="news-card">
            <span class="tech-badge">TECH</span>
        '''
        
        # Renderização de imagem
        image_url = article.get('image', None)
        if image_url:
            card_html += f'<img src="{image_url}" class="news-img" alt="imagem da notícia">'
        
        card_html += f'''
            <div class="news-title">{article["title"]}</div>
            <div class="news-summary">{article["summary"][:200]}...</div>
            <div class="news-actions">
                <a href="{article["link"]}" class="news-link" target="_blank">Ler Notícia</a>
            </div>
        </div>
        '''
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Botão de sumarização
        if st.button("📝 Sumarizar", key=f"summ_{idx}"):
            resumo = summarize_text(article['summary'])
            st.info(f"📄 **Resumo:** {resumo}")
