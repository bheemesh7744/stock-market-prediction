// API Base URL - Automatically detects local vs remote Render backend
const API_BASE_URL = window.__API_BASE_URL__ || (
    (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'))
    ? ''
    : 'https://agentic-ai-trader-y0xx.onrender.com'
);

// Helper to get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('jwt_token');
    const headers = { 'Content-Type': 'application/json' };
    if (token && token !== 'null' && token !== 'undefined') {
        headers['Authorization'] = 'Bearer ' + token;
    }
    return headers;
}

// Helper for authenticated fetch
function apiFetch(path, options = {}) {
    const url = path.startsWith('http') ? path : API_BASE_URL + path;
    options.headers = { ...getAuthHeaders(), ...(options.headers || {}) };
    return fetch(url, options);
}

// Check if user is logged in
function isLoggedIn() {
    const token = localStorage.getItem('jwt_token');
    if (!token || token === 'null' || token === 'undefined') return false;
    try {
        const parts = token.split('.');
        if (parts.length === 3) {
            const payload = JSON.parse(atob(parts[1]));
            if (payload.exp && payload.exp * 1000 < Date.now()) {
                localStorage.removeItem('jwt_token');
                return false;
            }
        }
        return true;
    } catch (e) {
        return !!token;
    }
}

function getCurrentUser() {
    try {
        const token = localStorage.getItem('jwt_token');
        if (!token || token === 'null' || token === 'undefined') return null;
        const payload = JSON.parse(atob(token.split('.')[1]));
        return { id: payload.user_id, username: payload.username };
    } catch(e) { return null; }
}

function logout() {
    localStorage.removeItem('jwt_token');
    window.location.href = '/login';
}
