import streamlit as st
from news_collector import get_news_from_feeds
from summarizer import summarize_text

st.set_page_config(page_title="LazzNews - Agregador de Notícias", layout="wide")

st.title("📰 LazzNews - Agregador Pessoal de Notícias")

# Lista de feeds RSS sugeridos
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

st.write(f"Foram encontradas {len(news)} notícias.")

for article in news:
    st.subheader(article['title'])
    st.write(article['summary'])
    st.markdown(f"[Leia mais]({article['link']})")
    if st.button(f"Sumarizar", key=article['link']):
        resumo = summarize_text(article['summary'])
        st.info(resumo)
    st.markdown("---")
