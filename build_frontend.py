import sys
import os
import re

# Add current directory to path to import html_template
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from html_template import HTML_TEMPLATE

def build_index():
    html = HTML_TEMPLATE

    # 1. Add config.js to head and redirect if not logged in
    head_addition = """
    <script src="/js/config.js"></script>
    <script>
        // Protect the dashboard
        if (!isLoggedIn()) {
            window.location.href = '/login';
        }
    </script>
"""
    html = html.replace('</head>', f'{head_addition}\n</head>')

    # 2. Add logout button to navbar (look for a known class like profile-btn or user-menu)
    # Just to be safe, append it near a closing div in the header, or replace user placeholder
    # Let's replace some jinja variables and inject the logout button
    logout_btn = """
    <button class="nav-btn" onclick="logout()" style="color: #ef4444; border-color: #ef4444; margin-left: 10px;">
        <i class="fas fa-sign-out-alt"></i> Logout
    </button>
    """
    if 'class="profile-btn"' in html:
        html = html.replace('<button class="profile-btn">', f'{logout_btn}\n<button class="profile-btn">')
    else:
        # fallback, add it right before </nav> or </header>
        html = html.replace('</header>', f'{logout_btn}\n</header>')

    # 3. Replace all fetch calls with apiFetch for /api routes
    html = html.replace("fetch('/api/", "apiFetch('/api/")
    html = html.replace('fetch("/api/', 'apiFetch("/api/')
    
    # Also fix relative endpoints that might not start with /api/ but are backend endpoints
    # (assuming all backend are prefixed with /api based on instructions)

    # 4. Remove Jinja template placeholders
    html = re.sub(r'\{\{\s*app_title.*\}\}', 'Stock Market Prediction Dashboard', html)
    html = re.sub(r'\{\{\s*csrf_token\(\)\s*\}\}', '', html)
    html = re.sub(r'\{\{\s*initial_market_data.*\}\}', 'null', html)
    html = re.sub(r'\{\{\s*stocks_config.*\}\}', 'null', html)
    html = re.sub(r'\{\{\s*is_logged_in.*\}\}', 'false', html)
    html = re.sub(r'\{\{\s*current_user.*\}\}', 'null', html)
    html = re.sub(r'\{\{\s*request\.url_root\s*\}\}', '', html)
    html = re.sub(r'\{\{.*?\}\}', '""', html)

    # 5. Fix Socket.IO connection
    # Replace io() with io(API_BASE_URL)
    html = re.sub(r'io\([^)]*\)', 'io(API_BASE_URL, {transports: ["websocket"]})', html)
    
    # 6. Any other JS auth headers
    # Ensure Authorization is passed if there are raw fetch calls left
    # (Config.js handles apiFetch, so we are good if we replaced fetch with apiFetch)

    # Write the result
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'index.html')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated {out_path} successfully.")

if __name__ == "__main__":
    build_index()
