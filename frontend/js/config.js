// API Base URL - Update this to your Render backend URL
const API_BASE_URL = window.__API_BASE_URL__ || 'https://agentic-ai-trader-y0xx.onrender.com';

// Helper to get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('jwt_token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = 'Bearer ' + token;
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
    return !!localStorage.getItem('jwt_token');
}

function getCurrentUser() {
    try {
        const token = localStorage.getItem('jwt_token');
        if (!token) return null;
        const payload = JSON.parse(atob(token.split('.')[1]));
        return { id: payload.user_id, username: payload.username };
    } catch(e) { return null; }
}

function logout() {
    localStorage.removeItem('jwt_token');
    window.location.href = '/login';
}
