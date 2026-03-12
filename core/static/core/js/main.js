// ══════════════════════════════════════════════════════════════════════════════
// TimeBank – Main JavaScript
// ══════════════════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initToasts();
    initSearch();
});

// ─── Mobile Navigation ──────────────────────────────────────────────────────
function initNavbar() {
    const toggle = document.getElementById('nav-toggle');
    const links = document.getElementById('nav-links');
    const navbar = document.getElementById('main-nav');

    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('active');
            toggle.classList.toggle('active');
        });

        // Close on link click
        links.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                links.classList.remove('active');
                toggle.classList.remove('active');
            });
        });
    }

    // Navbar scroll effect
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
}

// ─── Toast Auto-dismiss ─────────────────────────────────────────────────────
function initToasts() {
    const toasts = document.querySelectorAll('.toast[data-auto-dismiss]');
    toasts.forEach((toast, index) => {
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000 + (index * 500));
    });
}

// Slide out animation (added dynamically)
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// ─── Search & Filter ────────────────────────────────────────────────────────
function initSearch() {
    const searchForm = document.getElementById('search-form');
    const filterSelect = document.getElementById('category-filter');

    if (filterSelect && searchForm) {
        filterSelect.addEventListener('change', () => {
            searchForm.submit();
        });
    }
}

// ─── Confirm Actions ────────────────────────────────────────────────────────
function confirmAction(message) {
    return confirm(message);
}
