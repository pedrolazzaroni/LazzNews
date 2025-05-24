import re
from html import unescape

def summarize_text(text):
    """Sumariza o texto de forma mais inteligente"""
    if not text:
        return "Não foi possível gerar um resumo."
    
    # Limpar HTML e entidades
    clean_text = unescape(text)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Se o texto é muito curto, retorna como está
    if len(clean_text) <= 150:
        return clean_text
    
    # Dividir em sentenças
    sentences = re.split(r'[.!?]+', clean_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Pegar as 2 primeiras sentenças ou até 200 caracteres
    summary = ""
    for sentence in sentences[:2]:
        if len(summary + sentence) < 200:
            summary += sentence + ". "
        else:
            break
    
    # Se ainda está muito longo, corta
    if len(summary) > 200:
        summary = summary[:197] + "..."
    
    return summary.strip() or "Resumo não disponível."
