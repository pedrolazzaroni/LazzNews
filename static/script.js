// Variáveis globais
let newsData = [];
let lastUpdate = 0;

// Elementos DOM
const newsGrid = document.getElementById('newsGrid');
const loading = document.getElementById('loading');
const refreshBtn = document.getElementById('refreshBtn');
const newsCount = document.getElementById('newsCount');
const lastUpdateEl = document.getElementById('lastUpdate');
const summaryModal = document.getElementById('summaryModal');
const summaryContent = document.getElementById('summaryContent');
const closeModal = document.querySelector('.close');

// Event listeners
document.addEventListener('DOMContentLoaded', loadNews);
refreshBtn.addEventListener('click', refreshNews);
closeModal.addEventListener('click', closeSummaryModal);
window.addEventListener('click', (e) => {
    if (e.target === summaryModal) {
        closeSummaryModal();
    }
});

// Funções principais
async function loadNews() {
    showLoading(true);
    try {
        const response = await fetch('/api/news');
        const data = await response.json();
        newsData = data.news;
        lastUpdate = data.last_update;
        updateStats();
        renderNews();
    } catch (error) {
        console.error('Erro ao carregar notícias:', error);
        showError('Erro ao carregar notícias. Tente novamente.');
    } finally {
        showLoading(false);
    }
}

async function refreshNews() {
    refreshBtn.disabled = true;
    refreshBtn.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Atualizando...';
    
    await loadNews();
    
    refreshBtn.disabled = false;
    refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Atualizar Notícias';
}

function renderNews() {
    if (newsData.length === 0) {
        newsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <i class="fas fa-newspaper" style="font-size: 4rem; color: #ff8c00; margin-bottom: 1rem;"></i>
                <h3>Nenhuma notícia encontrada</h3>
                <p style="color: #b0b0b0;">Tente atualizar as notícias.</p>
            </div>
        `;
        return;
    }

    newsGrid.innerHTML = newsData.map((article, index) => `
        <article class="news-card" data-index="${index}">
            ${article.image ? `<img src="${article.image}" alt="Imagem da notícia" class="news-image" onerror="this.style.display='none'">` : ''}
            <div class="news-content">
                <span class="tech-badge">TECH</span>
                <h3 class="news-title">${escapeHtml(article.title)}</h3>
                <p class="news-summary">${escapeHtml(truncateText(article.summary, 150))}</p>
                <div class="news-actions">
                    <a href="${article.link}" target="_blank" class="news-link">
                        <i class="fas fa-external-link-alt"></i>
                        Ler Notícia
                    </a>
                    <button class="summary-btn" onclick="showSummary('${escapeHtml(article.summary)}')">
                        <i class="fas fa-file-alt"></i>
                        Resumir
                    </button>
                </div>
            </div>
        </article>
    `).join('');

    // Adicionar animação escalonada
    const cards = document.querySelectorAll('.news-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

async function showSummary(text) {
    summaryModal.classList.add('show');
    summaryContent.innerHTML = `
        <div class="summary-loading">
            <div class="spinner"></div>
            <p>Gerando resumo...</p>
        </div>
    `;

    try {
        const response = await fetch(`/api/summarize?text=${encodeURIComponent(text)}`);
        const data = await response.json();
        
        summaryContent.innerHTML = `
            <div style="color: #ffffff; line-height: 1.6; font-size: 1.1rem;">
                ${escapeHtml(data.summary)}
            </div>
        `;
    } catch (error) {
        summaryContent.innerHTML = `
            <div style="color: #ff6b6b; text-align: center;">
                <i class="fas fa-exclamation-triangle" style="margin-right: 0.5rem;"></i>
                Erro ao gerar resumo. Tente novamente.
            </div>
        `;
    }
}

function closeSummaryModal() {
    summaryModal.classList.remove('show');
}

function updateStats() {
    newsCount.textContent = newsData.length;
    if (lastUpdate) {
        const date = new Date(lastUpdate * 1000);
        lastUpdateEl.textContent = formatDate(date);
    }
}

function showLoading(show) {
    loading.classList.toggle('show', show);
    newsGrid.style.display = show ? 'none' : 'grid';
}

function showError(message) {
    newsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: #ff6b6b;">
            <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
            <h3>${message}</h3>
        </div>
    `;
}

// Funções utilitárias
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}

function formatDate(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    
    if (diff < 60) return 'Agora';
    if (diff < 3600) return `${Math.floor(diff / 60)}min atrás`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h atrás`;
    return date.toLocaleDateString('pt-BR');
}

// Auto-refresh a cada 30 minutos
setInterval(loadNews, 30 * 60 * 1000);