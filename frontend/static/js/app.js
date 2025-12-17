// app.js - минимальная версия для HTMX
console.log("App.js loaded");

// Инициализация HTMX
document.addEventListener('DOMContentLoaded', function() {
    initHTMX();
});

// Переинициализация после HTMX загрузки
document.addEventListener('htmx:afterSwap', function() {
    setTimeout(initHTMX, 50);
});

function initHTMX() {
    // Показываем индикатор загрузки для всех HTMX запросов
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        document.body.addEventListener('htmx:beforeRequest', function() {
            spinner.classList.remove('d-none');
        });

        document.body.addEventListener('htmx:afterRequest', function() {
            spinner.classList.add('d-none');
        });
    }

    // Инициализируем Bootstrap компоненты для новых элементов
    if (typeof bootstrap !== 'undefined') {
        // Инициализируем все тултипы
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(el) {
            new bootstrap.Tooltip(el);
        });

        // Инициализируем все попапы
        document.querySelectorAll('[data-bs-toggle="popover"]').forEach(function(el) {
            new bootstrap.Popover(el);
        });
    }
}

// Утилитарные функции
function formatDate(dateString) {
    if (!dateString) return '';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU');
    } catch (e) {
        return dateString;
    }
}

function formatPoints(points) {
    if (!points && points !== 0) return '0';
    return points.toLocaleString('ru-RU');
}

// Показ уведомлений (опционально)
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;

    const toastId = 'toast-' + Date.now();
    const bgClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    }[type] || 'bg-info';

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    if (toastElement && typeof bootstrap !== 'undefined') {
        const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
        toast.show();

        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }
}

// Делегирование событий для пагинации (если все еще не работает)
document.addEventListener('click', function(e) {
    const paginationLink = e.target.closest('.page-link');
    if (paginationLink && paginationLink.href && paginationLink.href.includes('/athletes?')) {
        // Если HTMX не сработал, запускаем вручную
        if (!e.defaultPrevented && !htmx.find(paginationLink)) {
            console.log('Manually triggering HTMX for pagination');
            htmx.ajax('GET', paginationLink.href, {
                target: 'body',
                swap: 'innerHTML',
                pushUrl: true
            });
            e.preventDefault();
        }
    }
});

// Инициализация при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHTMX);
} else {
    initHTMX();
}