// Variáveis globais
let newsData = [];
let lastUpdate = 0;
let sourcesData = [];
let currentPage = 1;
const itemsPerPage = 20;
let totalPages = 1;
let sourcesVisible = false;

// Elementos DOM
const newsGrid = document.getElementById('newsGrid');
const loading = document.getElementById('loading');
const refreshBtn = document.getElementById('refreshBtn');
const sourcesBtn = document.getElementById('sourcesBtn');
const newsCount = document.getElementById('newsCount');
const newsCountDisplay = document.getElementById('newsCountDisplay');
const lastUpdateEl = document.getElementById('lastUpdate');
const lastUpdateTime = document.getElementById('lastUpdateTime');
const summaryModal = document.getElementById('summaryModal');
const summaryContent = document.getElementById('summaryContent');
const closeModal = document.querySelector('.close');
const sourcesSection = document.getElementById('sourcesSection');
const sourcesList = document.getElementById('sourcesList');
const pagination = document.getElementById('pagination');
const currentPageEl = document.getElementById('currentPage');
const totalPagesEl = document.getElementById('totalPages');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    loadNews();
    loadSources();
    updateCurrentYear();
    
    // Adicionar event listeners após DOM carregado
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshNews);
    }
    if (sourcesBtn) {
        sourcesBtn.addEventListener('click', toggleSources);
    }
    if (closeModal) {
        closeModal.addEventListener('click', closeSummaryModal);
    }
});

window.addEventListener('click', (e) => {
    if (e.target === summaryModal) {
        closeSummaryModal();
    }
});

// Atualizar ano no footer
function updateCurrentYear() {
    const currentYearEl = document.getElementById('currentYear');
    if (currentYearEl) {
        currentYearEl.textContent = new Date().getFullYear();
    }
}

// Função para alternar seção de fontes com animação melhorada
function toggleSources() {
    if (!sourcesSection) return;
    
    // Prevenir cliques múltiplos
    if (sourcesBtn) sourcesBtn.disabled = true;
    
    if (sourcesVisible) {
        // Esconder com animação
        sourcesSection.style.animation = 'slideUp 0.3s ease forwards';
        setTimeout(() => {
            sourcesSection.style.display = 'none';
            sourcesSection.style.animation = '';
            sourcesVisible = false;
            if (sourcesBtn) sourcesBtn.disabled = false;
        }, 300);
        
        if (sourcesBtn) {
            sourcesBtn.innerHTML = '<span class="btn-icon"><i class="fas fa-rss"></i></span>';
            sourcesBtn.style.background = 'linear-gradient(135deg, rgba(255, 140, 0, 0.15), rgba(255, 165, 0, 0.1))';
            sourcesBtn.style.borderColor = 'rgba(255, 140, 0, 0.4)';
        }
    } else {
        // Mostrar com animação
        sourcesSection.style.display = 'block';
        sourcesSection.style.animation = 'slideDown 0.3s ease forwards';
        sourcesVisible = true;
        
        if (sourcesBtn) {
            sourcesBtn.innerHTML = '<span class="btn-icon"><i class="fas fa-times"></i></span>';
            sourcesBtn.style.background = 'linear-gradient(135deg, rgba(255, 140, 0, 0.25), rgba(255, 165, 0, 0.2))';
            sourcesBtn.style.borderColor = 'rgba(255, 140, 0, 0.7)';
            sourcesBtn.disabled = false;
        }
        
        if (sourcesData.length === 0) {
            loadSources();
        }
    }
}

// Função para carregar fontes
async function loadSources() {
    try {
        const response = await fetch('/api/sources');
        const data = await response.json();
        sourcesData = data.sources;
        renderSources();
    } catch (error) {
        console.error('Erro ao carregar fontes:', error);
    }
}

// Função para renderizar fontes
function renderSources() {
    sourcesList.innerHTML = sourcesData.map(source => `
        <div class="source-card">
            <div class="source-name">${source.name}</div>
            <a href="${source.url}" target="_blank" class="source-url">
                <i class="fas fa-external-link-alt"></i>
                ${source.url.replace('https://', '').replace('www.', '')}
            </a>
        </div>
    `).join('');
}

// Funções principais
async function loadNews() {
    showLoading(true);
    try {
        const response = await fetch('/api/news');
        const data = await response.json();
        newsData = data.news;
        lastUpdate = data.last_update;
        updateStatsAnimated();
        renderNews();
    } catch (error) {
        console.error('Erro ao carregar notícias:', error);
        showError('Erro ao carregar notícias. Tente novamente.');
    } finally {
        showLoading(false);
    }
}

async function refreshNews() {
    if (!refreshBtn) return;
    
    // Prevenir múltiplos cliques
    if (refreshBtn.disabled) return;
    
    refreshBtn.disabled = true;
    refreshBtn.classList.add('loading');
    
    try {
        const response = await fetch('/api/refresh');
        const data = await response.json();
        newsData = data.news;
        lastUpdate = data.last_update;
        currentPage = 1; // Reset para primeira página
        updateStatsAnimated();
        renderNews();
        
        // Mostrar notificação de sucesso
        showNotification('Notícias atualizadas com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao atualizar notícias:', error);
        showNotification('Erro ao atualizar notícias. Tente novamente.', 'error');
    } finally {
        // Pequeno delay para que o usuário veja o efeito
        setTimeout(() => {
            refreshBtn.disabled = false;
            refreshBtn.classList.remove('loading');
        }, 500);
    }
}

function renderNews() {
    const paginatedNews = getPaginatedNews();

    if (paginatedNews.length === 0) {
        newsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <i class="fas fa-newspaper" style="font-size: 4rem; color: #ff8c00; margin-bottom: 1rem;"></i>
                <h3>Nenhuma notícia de hoje encontrada</h3>
                <p style="color: #b0b0b0;">Todas as notícias exibidas são apenas do dia atual. Tente atualizar ou volte amanhã!</p>
            </div>
        `;
        return;
    }    newsGrid.innerHTML = paginatedNews.map((article, index) => `
        <article class="news-card" data-index="${index}">
            ${article.image ? `<img src="${article.image}" alt="Imagem da notícia" class="news-image" onerror="this.style.display='none'">` : ''}
            <div class="news-content">
                <span class="source-badge">${escapeHtml(article.source || 'Fonte Desconhecida')}</span>
                <h3 class="news-title">${escapeHtml(article.title)}</h3>
                <p class="news-summary">${escapeHtml(truncateText(article.summary, 150))}</p>
                <div class="news-meta">
                    <small><i class="fas fa-calendar"></i> Hoje</small>
                </div>
                <div class="news-actions">
                    <a href="${article.link}" target="_blank" class="news-link">
                        <i class="fas fa-external-link-alt"></i>
                        Ler Notícia
                    </a>
                    <button class="summary-btn" onclick="showSummary('${escapeHtml(article.summary).replace(/'/g, "&#39;")}')">
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

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
        ${message}
    `;
    
    // Adicionar estilos inline
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)'};
        color: ${type === 'success' ? '#00ff00' : '#ff6b6b'};
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border: 1px solid ${type === 'success' ? 'rgba(0, 255, 0, 0.5)' : 'rgba(255, 0, 0, 0.5)'};
        backdrop-filter: blur(10px);
        z-index: 1001;
        animation: slideIn 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
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
    // Atualizar contadores
    if (newsCount) newsCount.textContent = newsData.length;
    if (newsCountDisplay) newsCountDisplay.textContent = newsData.length;
    
    // Atualizar status de última atualização
    if (lastUpdate) {
        const date = new Date(lastUpdate * 1000);
        const timeString = date.toLocaleTimeString('pt-BR');
        
        if (lastUpdateEl) lastUpdateEl.textContent = timeString;
        if (lastUpdateTime) lastUpdateTime.textContent = timeString;
    }
    
    // Calcular paginação
    if (totalPagesEl && currentPageEl && pagination) {
        totalPages = Math.ceil(newsData.length / itemsPerPage);
        totalPagesEl.textContent = totalPages;
        currentPageEl.textContent = currentPage;
        
        // Mostrar/ocultar paginação
        if (totalPages > 1) {
            pagination.style.display = 'flex';
        } else {
            pagination.style.display = 'none';
        }
        
        updatePaginationButtons();
    }
}

// Função para animar a atualização do contador
function animateCounterUpdate(element, newValue) {
    if (!element) return;
    
    const currentValue = parseInt(element.textContent) || 0;
    const increment = newValue > currentValue ? 1 : -1;
    const duration = 800; // ms
    const steps = Math.abs(newValue - currentValue);
    const stepDuration = duration / Math.max(steps, 1);
    
    let current = currentValue;
    
    const updateCounter = () => {
        if (current !== newValue) {
            current += increment;
            element.textContent = current;
            element.style.transform = 'scale(1.1)';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 100);
            setTimeout(updateCounter, stepDuration);
        }
    };
    
    if (currentValue !== newValue) {
        updateCounter();
    }
}

// Função melhorada para atualizar stats com animação
function updateStatsAnimated() {
    // Animar contadores
    if (newsCount) animateCounterUpdate(newsCount, newsData.length);
    if (newsCountDisplay) animateCounterUpdate(newsCountDisplay, newsData.length);
    
    // Atualizar status de última atualização com efeito
    if (lastUpdate) {
        const date = new Date(lastUpdate * 1000);
        const timeString = date.toLocaleTimeString('pt-BR');
        
        if (lastUpdateEl) {
            lastUpdateEl.style.opacity = '0.5';
            setTimeout(() => {
                lastUpdateEl.textContent = timeString;
                lastUpdateEl.style.opacity = '1';
            }, 200);
        }
        if (lastUpdateTime) {
            lastUpdateTime.style.opacity = '0.5';
            setTimeout(() => {
                lastUpdateTime.textContent = timeString;
                lastUpdateTime.style.opacity = '1';
            }, 200);
        }
    }
    
    // Calcular paginação
    totalPages = Math.ceil(newsData.length / itemsPerPage);
    totalPagesEl.textContent = totalPages;
    currentPageEl.textContent = currentPage;
    
    // Mostrar/ocultar paginação
    if (totalPages > 1) {
        pagination.style.display = 'flex';
    } else {
        pagination.style.display = 'none';
    }
    
    updatePaginationButtons();
}

function changePage(direction) {
    const newPage = currentPage + direction;
    if (newPage >= 1 && newPage <= totalPages) {
        currentPage = newPage;
        currentPageEl.textContent = currentPage;
        renderNews();
        updatePaginationButtons();
        
        // Scroll suave para o topo das notícias
        document.getElementById('noticias').scrollIntoView({ 
            behavior: 'smooth' 
        });
    }
}

function updatePaginationButtons() {
    if (prevPageBtn && nextPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    }
}

function showLoading(show) {
    if (loading) loading.classList.toggle('show', show);
    if (newsGrid) newsGrid.style.display = show ? 'none' : 'grid';
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

// Função para paginar notícias
function getPaginatedNews() {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return newsData.slice(startIndex, endIndex);
}

// Auto-refresh a cada 30 minutos
setInterval(loadNews, 30 * 60 * 1000);