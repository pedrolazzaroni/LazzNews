# LazzNews - Agregador de Notícias de Tecnologia

## 🚀 Instalação e Execução

### 1. Instalar Dependências

Execute no terminal dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

Ou instale individualmente:
```bash
pip install Flask feedparser requests python-dateutil
```

### 2. Executar o Projeto

```bash
python app.py
```

O servidor será iniciado em: `http://localhost:5000`

## 📦 Dependências

- **Flask**: Framework web para Python
- **feedparser**: Parser de feeds RSS/Atom
- **requests**: Biblioteca para requisições HTTP
- **python-dateutil**: Utilitários para manipulação de datas

## 🔧 Estrutura do Projeto

```
LazzNews/
├── app.py              # Aplicação Flask principal
├── news_collector.py   # Coleta de notícias dos feeds RSS
├── summarizer.py       # Geração de resumos com IA
├── requirements.txt    # Dependências do projeto
├── templates/
│   └── index.html      # Template principal
└── static/
    ├── style.css       # Estilos CSS
    └── script.js       # JavaScript do frontend
```

## 🌐 Fontes de Notícias

- Olhar Digital
- Tecnoblog  
- TechTudo
- Canaltech
- Hardware.com.br
- Adrenaline
- ShowMeTech
- TudoCelular
- MeioBit
- MobileTime
- TecMundo
- UOL Tilt