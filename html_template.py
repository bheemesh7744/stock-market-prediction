HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Primary SEO Meta Tags -->
    <title>Stock Market Prediction — AI-Powered Indian Stock Market Trading & Analysis</title>
    <meta name="description" content="Stock by Bheemesh: Real-time Indian stock market analysis with AI-powered predictions for NIFTY 50, Bank NIFTY, SENSEX, and 20+ NSE stocks. Free technical indicators, candlestick charts, and intelligent trading signals by Bheemesh.">
    <meta name="keywords" content="stock by bheemesh, bheemesh stock market, indian stock market, nifty 50 live, bank nifty analysis, sensex today, AI stock prediction, NSE trading, BSE live, stock market india, agentic ai trader, bheemesh trader, indian market intelligence, nifty prediction, stock analysis india, free stock signals">
    <meta name="author" content="Bheemesh">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <link rel="canonical" href="{{ request.url_root }}">
    
    <!-- Favicon (inline SVG — no external file needed) -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%232563eb'/%3E%3Cstop offset='100%25' stop-color='%237c3aed'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100' height='100' rx='20' fill='url(%23g)'/%3E%3Cpath d='M25 65 L40 35 L55 50 L70 25 L80 25' stroke='white' stroke-width='6' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3Ccircle cx='80' cy='25' r='5' fill='%2310b981'/%3E%3C/svg%3E">
    <link rel="apple-touch-icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%232563eb'/%3E%3Cstop offset='100%25' stop-color='%237c3aed'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100' height='100' rx='20' fill='url(%23g)'/%3E%3Cpath d='M25 65 L40 35 L55 50 L70 25 L80 25' stroke='white' stroke-width='6' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3Ccircle cx='80' cy='25' r='5' fill='%2310b981'/%3E%3C/svg%3E">


    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ request.url_root }}">
    <meta property="og:title" content="Stock Market Prediction — AI Indian Market Intelligence">
    <meta property="og:description" content="Free real-time Indian stock market analysis with AI predictions for NIFTY 50, Bank NIFTY, SENSEX & 20+ NSE stocks. Technical indicators, charts & trading signals.">
    <meta property="og:site_name" content="Stock Market Prediction">
    <meta property="og:locale" content="en_IN">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Stock by Bheemesh — AI Indian Market Intelligence">
    <meta name="twitter:description" content="Free real-time Indian stock market analysis with AI predictions for NIFTY 50, Bank NIFTY, SENSEX & 20+ NSE stocks.">
    
    <!-- Additional SEO -->
    <meta name="theme-color" content="#06080f">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Stock by Bheemesh">
    <meta name="application-name" content="Stock by Bheemesh">
    
    <!-- Structured Data (JSON-LD) for Google Rich Results -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "Stock by Bheemesh",
      "alternateName": "Agentic AI Trader by Bheemesh",
      "url": "{{ request.url_root }}",
      "description": "AI-powered Indian stock market trading platform with real-time analysis for NIFTY 50, Bank NIFTY, SENSEX and 20+ NSE stocks",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "Web Browser",
      "author": {
        "@type": "Person",
        "name": "Bheemesh"
      },
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "INR"
      },
      "featureList": [
        "Real-time Indian stock market data",
        "AI-powered stock predictions",
        "Technical analysis indicators",
        "Candlestick charts with multiple timeframes",
        "NIFTY 50, Bank NIFTY, SENSEX tracking",
        "20+ NSE stock analysis",
        "RSI, MACD, Bollinger Bands indicators"
      ]
    }
    </script>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script defer src="https://unpkg.com/plotly.js-dist@2.35.3/plotly.js" crossorigin="anonymous"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">

    <style>
        :root {
            --bg-primary: #040807; /* Darker, slightly greenish base */
            --bg-secondary: #08110e;
            --bg-card: rgba(10, 17, 15, 0.45);
            --border-subtle: rgba(255,255,255,0.06);
            --border-glow-blue: rgba(56, 189, 248, 0.45);
            --border-glow-purple: rgba(45, 212, 191, 0.45);
            --border-glow-emerald: rgba(16, 185, 129, 0.45);
            --text-primary: #f0fdf4; /* Very light green tint */
            --text-secondary: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-purple: #2dd4bf;
            --accent-emerald: #10b981;
            --accent-red: #f43f5e;
            --accent-amber: #f59e0b;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        html { scroll-behavior:smooth; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 45%),
                radial-gradient(circle at 90% 80%, rgba(20, 184, 166, 0.05) 0%, transparent 45%),
                radial-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 20px 20px;
            background-attachment: fixed;
        }

        /* ── Ambient background blobs ── */
        body::before, body::after {
            content: ''; position: fixed; border-radius: 50%; pointer-events: none; z-index: 0; filter: blur(150px); opacity: 0.12;
        }
        body::before { width: 600px; height: 600px; background: #059669; top: -150px; left: -100px; animation: floatBlob1 15s ease-in-out infinite alternate; }
        body::after  { width: 500px; height: 500px; background: #0d9488; bottom: -100px; right: -80px; animation: floatBlob2 18s ease-in-out infinite alternate; }

        @keyframes floatBlob1 {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(40px, 30px) scale(1.08); }
        }
        @keyframes floatBlob2 {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(-30px, -40px) scale(1.05); }
        }

        /* ── Glass card ── */
        .glass-card {
            background: var(--bg-card);
            backdrop-filter: blur(20px) saturate(1.4);
            -webkit-backdrop-filter: blur(20px) saturate(1.4);
            border: 1px solid var(--border-subtle);
            border-radius: 24px;
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), border-color 0.3s ease;
            position: relative;
            z-index: 1;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border-color: rgba(255,255,255,0.12);
        }

        /* Border indicator top accents without breaking rounded corners */
        .glass-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: transparent;
            z-index: 2;
            transition: opacity 0.3s ease;
        }
        .glass-card.card-emerald::after { background: linear-gradient(90deg, #059669, #34d399); }
        .glass-card.card-purple::after { background: linear-gradient(90deg, #0d9488, #2dd4bf); }
        .glass-card.card-blue::after { background: linear-gradient(90deg, #0284c7, #38bdf8); }

        .glass-card.card-blue:hover  { border-color: var(--border-glow-blue); box-shadow: 0 15px 45px rgba(56,189,248,0.1); }
        .glass-card.card-purple:hover { border-color: var(--border-glow-purple); box-shadow: 0 15px 45px rgba(45,212,191,0.1); }
        .glass-card.card-emerald:hover { border-color: var(--border-glow-emerald); box-shadow: 0 15px 45px rgba(16,185,129,0.1); }

        /* ── Header ── */
        .header-glass {
            background: rgba(4,8,7,0.7);
            backdrop-filter: blur(24px) saturate(1.4);
            -webkit-backdrop-filter: blur(24px) saturate(1.4);
            border-bottom: 1px solid var(--border-subtle);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
        }

        /* ── Buttons ── */
        .btn {
            display: inline-flex; align-items: center; gap: 6px;
            font-family: 'Inter',sans-serif; font-weight: 600; font-size: 0.8125rem;
            padding: 9px 18px; border-radius: 10px; border: none;
            cursor: pointer; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); color: #fff; position: relative; overflow: hidden;
        }
        .btn::after {
            content: ''; position: absolute; inset: 0; background: rgba(255,255,255,0); transition: background 0.2s ease; border-radius: inherit;
        }
        .btn:hover::after { background: rgba(255,255,255,0.08); }
        .btn:hover { transform: translateY(-1px); }
        .btn:active { transform: scale(0.97) translateY(0); }
        .btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
        .btn-blue   { background: linear-gradient(135deg, #059669, #10b981); box-shadow: 0 4px 15px rgba(16,185,129,0.25); }
        .btn-purple { background: linear-gradient(135deg, #0d9488, #14b8a6); box-shadow: 0 4px 15px rgba(13,148,136,0.25); }
        .btn-ghost  { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: var(--text-secondary); }
        .btn-ghost:hover { border-color: rgba(255,255,255,0.2); color: #fff; background: rgba(255,255,255,0.03); }

        /* ── Tags ── */
        .tag { display: inline-flex; align-items: center; gap: 4px; font-size: 0.6875rem; font-weight: 600; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.4px; }
        .tag-blue    { background: rgba(56,189,248,0.1); color: var(--accent-blue); }
        .tag-purple  { background: rgba(45,212,191,0.1); color: var(--accent-purple); }
        .tag-emerald { background: rgba(16,185,129,0.1); color: var(--accent-emerald); }
        .tag-red     { background: rgba(244,63,94,0.1);  color: var(--accent-red); }
        .tag-amber   { background: rgba(245,158,11,0.1); color: var(--accent-amber); }

        /* ── Prediction pills ── */
        .pill-up   { background: linear-gradient(135deg, #059669, #10b981); box-shadow: 0 2px 10px rgba(16,185,129,0.2); }
        .pill-down { background: linear-gradient(135deg, #dc2626, #ef4444); box-shadow: 0 2px 10px rgba(220,38,38,0.2); }
        .pill-hold { background: linear-gradient(135deg, #4b5563, #6b7280); }

        /* ── Profit/Loss ── */
        .profit { color: var(--accent-emerald); }
        .loss   { color: var(--accent-red); }

        /* ── Animated data flash ── */
        @keyframes dataFlash {
            0% { background: rgba(16,185,129,0.15); }
            100% { background: transparent; }
        }
        .data-flash { animation: dataFlash 0.6s ease-out; }

        /* ── Pulse dot ── */
        @keyframes pulse-ring {
            0% { transform: scale(0.8); opacity: 1; }
            100% { transform: scale(2.2); opacity: 0; }
        }
        .live-dot { position: relative; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--accent-emerald); }
        .live-dot::before { content:''; position:absolute; inset:-3px; border-radius:50%; border:2px solid var(--accent-emerald); animation: pulse-ring 1.8s ease-out infinite; }

        /* ── Skeleton shimmer ── */
        @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
        .skeleton {
            background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.07) 50%, rgba(255,255,255,0.03) 75%);
            background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 6px;
        }

        /* ── Mono font ── */
        .mono { font-family: 'JetBrains Mono', 'SF Mono', monospace; font-size: 0.8125rem; }

        /* ── Advanced Animations ── */
        @keyframes fade-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in { animation: fade-in 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
        
        @keyframes slide-up {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-slide-up { animation: slide-up 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        .animate-float { animation: float 4s ease-in-out infinite; }

        /* ── Grid layout ── */
        .market-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
        @media (min-width: 640px) { .market-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (min-width: 1024px) { .market-grid { grid-template-columns: repeat(3, 1fr); } }

        /* ── Select styling ── */
        select.styled-select {
            appearance: none; background: rgba(255,255,255,0.04); color: var(--text-primary);
            border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
            padding: 8px 32px 8px 12px; font-size: 0.8125rem; font-family: 'Inter',sans-serif; font-weight: 500;
            cursor: pointer; transition: all 0.2s;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%238b949e' viewBox='0 0 16 16'%3E%3Cpath d='M4.5 6l3.5 4 3.5-4z'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 10px center;
        }
        select.styled-select:focus { outline: none; border-color: var(--accent-emerald); background: rgba(255,255,255,0.08); }

        /* ── Table ── */
        .data-table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 0.8125rem; }
        .data-table th { 
            padding: 12px 16px; 
            text-align: left; 
            color: var(--text-secondary); 
            font-weight: 600; 
            border-bottom: 1.5px solid rgba(255,255,255,0.06); 
            background: rgba(255,255,255,0.02); 
            backdrop-filter: blur(8px);
        }
        .data-table td { padding: 12px 16px; border-bottom: 1px solid rgba(255,255,255,0.03); transition: all 0.2s; }
        .data-table tbody tr { transition: background 0.2s; position: relative; }
        .data-table tbody tr:hover { 
            background: rgba(16, 185, 129, 0.04); 
        }
        .data-table tbody tr:hover td {
            color: #fff;
        }

        /* ── Modal ── */
        .modal-overlay {
            display: none; position: fixed; z-index: 1000; inset: 0;
            background: rgba(0,0,0,0.75); backdrop-filter: blur(12px);
            justify-content: center; align-items: flex-start; padding: 40px 16px; overflow-y: auto;
        }
        .modal-overlay.active { display: flex; }
        .modal-panel {
            background: rgba(10, 17, 15, 0.85); border: 1px solid var(--border-subtle);
            backdrop-filter: blur(24px) saturate(1.4);
            -webkit-backdrop-filter: blur(24px) saturate(1.4);
            border-radius: 24px; width: 100%; max-width: 640px;
            animation: modalIn 0.35s cubic-bezier(0.16, 1, 0.3, 1); position: relative;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        }
        @keyframes modalIn {
            from { opacity: 0; transform: translateY(24px) scale(0.97); }
            to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* ── Options Chain ── */
        .oc-tabs {
            display: flex; gap: 2px; padding: 2px;
            background: rgba(255,255,255,0.03); border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.06); margin-bottom: 16px;
        }
        .oc-tab {
            flex: 1; padding: 8px 16px; border-radius: 10px;
            font-size: 0.75rem; font-weight: 600; cursor: pointer;
            transition: all 0.2s; color: #9ca3af; text-align: center;
            background: transparent; border: none;
        }
        .oc-tab.active {
            background: linear-gradient(135deg, rgba(16,185,129,0.8), rgba(20,184,166,0.8));
            color: #fff; box-shadow: 0 2px 8px rgba(16,185,129,0.2);
        }
        .oc-tab:hover:not(.active) { color: #fff; background: rgba(255,255,255,0.04); }

        .oc-expiry-btn {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 6px 14px; border-radius: 8px; font-size: 0.75rem;
            font-weight: 600; cursor: pointer; transition: all 0.2s;
            background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
            color: #e5e7eb;
        }
        .oc-expiry-btn:hover { background: rgba(255,255,255,0.08); border-color: rgba(16,185,129,0.3); }

        .oc-expiry-sheet {
            position: absolute; left: 0; right: 0; top: 100%;
            background: rgba(10,17,15,0.98); border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px; padding: 16px; margin-top: 8px;
            z-index: 10; backdrop-filter: blur(20px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            animation: modalIn 0.25s ease-out;
        }
        .oc-expiry-option {
            display: flex; align-items: center; gap: 12px;
            padding: 12px 16px; border-radius: 10px; cursor: pointer;
            transition: all 0.15s; font-size: 0.85rem; color: #d1d5db;
        }
        .oc-expiry-option:hover { background: rgba(255,255,255,0.04); }
        .oc-expiry-option.selected { color: #10b981; font-weight: 600; }
        .oc-expiry-radio {
            width: 20px; height: 20px; border-radius: 50%;
            border: 2px solid rgba(255,255,255,0.15); display: flex;
            align-items: center; justify-content: center; flex-shrink: 0;
        }
        .oc-expiry-option.selected .oc-expiry-radio {
            border-color: #10b981; background: rgba(16,185,129,0.1);
        }
        .oc-expiry-option.selected .oc-expiry-radio::after {
            content: ''; width: 10px; height: 10px; border-radius: 50%;
            background: #10b981;
        }

        .oc-table { width: 100%; border-collapse: separate; border-spacing: 0; }
        .oc-table th {
            padding: 8px 6px; font-size: 0.65rem; font-weight: 600;
            text-transform: uppercase; color: #6b7280; letter-spacing: 0.05em;
            position: sticky; top: 0; background: rgba(10,17,15,0.95);
            backdrop-filter: blur(8px); z-index: 2;
        }
        .oc-table td {
            padding: 10px 6px; font-size: 0.8rem; font-weight: 500;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            transition: background 0.15s;
        }
        .oc-table tr:hover td { background: rgba(255,255,255,0.02); }
        .oc-table .strike-col {
            text-align: center; font-weight: 700; color: #e5e7eb;
            background: rgba(255,255,255,0.02); position: relative;
        }
        .oc-table .call-col { text-align: left; }
        .oc-table .put-col { text-align: right; }
        .oc-table .atm-row td {
            background: rgba(234,179,8,0.08) !important;
            border-top: 1px solid rgba(234,179,8,0.3);
            border-bottom: 1px solid rgba(234,179,8,0.3);
        }
        .oc-table .atm-row .strike-col { color: #eab308; }
        .oc-table .itm-call { background: rgba(16,185,129,0.03); }
        .oc-table .itm-put { background: rgba(16,185,129,0.03); }

        .oc-oi-bar {
            height: 3px; border-radius: 2px; margin-top: 3px;
            transition: width 0.3s ease;
        }

        .oc-legend {
            border-radius: 12px; overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
        }
        .oc-legend-toggle {
            display: flex; align-items: center; gap: 8px;
            padding: 10px 14px; cursor: pointer; width: 100%;
            background: rgba(255,255,255,0.02); border: none;
            color: #9ca3af; font-size: 0.75rem; font-weight: 600;
            transition: all 0.2s;
        }
        .oc-legend-toggle:hover { background: rgba(255,255,255,0.04); color: #e5e7eb; }
        .oc-legend-toggle i.rotate { transform: rotate(180deg); }
        .oc-legend-body {
            padding: 0 14px; max-height: 0; overflow: hidden;
            transition: max-height 0.35s ease, padding 0.35s ease;
        }
        .oc-legend-body.open { max-height: 500px; padding: 12px 14px; }
        .oc-legend-item {
            display: flex; align-items: flex-start; gap: 8px;
            padding: 6px 0; font-size: 0.7rem; color: #9ca3af;
        }
        .oc-legend-dot {
            width: 8px; height: 8px; border-radius: 50%; margin-top: 3px; flex-shrink: 0;
        }

        /* ── Toast ── */
        .toast {
            position: fixed; top: 20px; right: 20px; z-index: 9999;
            padding: 14px 22px; border-radius: 12px; color: #fff;
            font-size: 0.875rem; font-weight: 500;
            animation: toastIn 0.35s ease-out;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        }
        .toast-error   { background: linear-gradient(135deg, #dc2626, #ef4444); }
        .toast-success { background: linear-gradient(135deg, #059669, #10b981); }
        .toast-info    { background: linear-gradient(135deg, #2563eb, #3b82f6); }
        @keyframes toastIn { from { transform: translateX(120%); opacity:0; } to { transform: translateX(0); opacity:1; } }

        /* ── Timeframe pills ── */
        .tf-pill {
            display: inline-flex; align-items: center; justify-content: center;
            padding: 7px 16px; border-radius: 8px;
            font-family: 'Inter', sans-serif; font-size: 0.75rem; font-weight: 600;
            color: var(--text-secondary); background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            cursor: pointer; transition: all 0.2s ease; white-space: nowrap;
        }
        .tf-pill:hover {
            background: rgba(255,255,255,0.07);
            border-color: rgba(255,255,255,0.12);
            color: var(--text-primary);
        }
        .tf-pill.tf-active {
            background: linear-gradient(135deg, #059669, #10b981);
            border-color: transparent;
            color: #fff;
            box-shadow: 0 2px 12px rgba(16, 185, 129, 0.35);
        }

        /* ── Footer ── */
        .footer {
            border-top: 1px solid var(--border-subtle);
            background: rgba(4,8,7,0.5);
            backdrop-filter: blur(12px);
            padding: 28px 0;
            margin-top: 48px;
        }

        /* ── Price counter animation ── */
        .price-value { transition: color 0.3s ease; }

        /* Modebar */
        .modebar { display: none !important; }
        .js-plotly-plot .plotly .modebar { display: none !important; }
        
        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }
        
        /* ── Tabs & Stocks Custom Premium Styles ── */
        .tab-btn { position: relative; }
        .tab-btn::after {
            content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%) scaleX(0);
            width: 80%; height: 2px; background: linear-gradient(90deg, #10b981, #2dd4bf);
            transition: transform 0.3s ease;
        }
        .tab-btn.active::after { transform: translateX(-50%) scaleX(1); }
        
        .stock-card {
            transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
            position: relative;
            overflow: hidden;
            border-radius: 20px;
        }
        .stock-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, transparent, transparent);
            transition: background 0.4s ease;
        }
        .stock-card.signal-up::before { background: linear-gradient(90deg, #059669, #10b981, #34d399); }
        .stock-card.signal-down::before { background: linear-gradient(90deg, #dc2626, #ef4444, #f87171); }
        .stock-card.signal-hold::before { background: linear-gradient(90deg, #d97706, #f59e0b, #fbbf24); }
        
        .stock-card:hover {
            border-color: rgba(16, 185, 129, 0.3);
            box-shadow: 
                0 15px 35px -10px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(16, 185, 129, 0.08);
            transform: translateY(-3px);
        }

        /* ── Sparkline mini-chart ── */
        .sparkline-container { height: 32px; display: flex; align-items: flex-end; gap: 1px; opacity: 0.6; }
        .sparkline-bar {
            flex: 1; min-width: 3px; border-radius: 1px 1px 0 0;
            transition: height 0.3s ease, background 0.3s ease;
        }

        /* ── Confidence progress bar ── */
        .confidence-bar { height: 3px; border-radius: 2px; background: rgba(255,255,255,0.06); overflow: hidden; }
        .confidence-fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }
        .confidence-fill.high { background: linear-gradient(90deg, #10b981, #34d399); }
        .confidence-fill.medium { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
        .confidence-fill.low { background: linear-gradient(90deg, #ef4444, #f87171); }

        /* ── Loading Overlay ── */
        .app-loader {
            position: fixed; inset: 0; z-index: 9999;
            background: var(--bg-primary);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            transition: opacity 0.5s ease, visibility 0.5s ease;
        }
        .app-loader.hidden { opacity: 0; visibility: hidden; pointer-events: none; }
        .app-loader .loader-icon {
            width: 64px; height: 64px; border-radius: 16px;
            background: linear-gradient(135deg, #059669, #14b8a6);
            display: flex; align-items: center; justify-content: center;
            animation: loaderPulse 1.5s ease-in-out infinite;
            margin-bottom: 20px;
        }
        @keyframes loaderPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 0 30px 10px rgba(16, 185, 129, 0.15); }
        }
        .loader-bar { width: 180px; height: 3px; border-radius: 2px; background: rgba(255,255,255,0.06); overflow: hidden; margin-top: 16px; }
        .loader-bar-fill { height: 100%; width: 30%; border-radius: 2px; background: linear-gradient(90deg, #10b981, #2dd4bf); animation: loaderSlide 1.2s ease-in-out infinite; }
        @keyframes loaderSlide { 0% { transform: translateX(-100%); } 100% { transform: translateX(500%); } }

        /* ── Skeleton cards for initial load ── */
        .skeleton-price { width: 120px; height: 28px; }
        .skeleton-change { width: 90px; height: 16px; margin-top: 6px; }
        .skeleton-stat { width: 50px; height: 14px; }

        /* ── Smooth number animation ── */
        @keyframes countUp { from { opacity: 0.5; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
        .price-update { animation: countUp 0.3s ease-out; }

        /* ── Keyboard hint ── */
        .kbd-hint { font-size: 0.65rem; color: rgba(255,255,255,0.25); margin-top: 8px; text-align: center; }
        kbd { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; padding: 1px 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; }

        /* Selection style */
        ::selection {
            background: rgba(16, 185, 129, 0.3);
            color: #fff;
        }

        /* Fade-in animation */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up {
            animation: fadeInUp 0.5s ease-out both;
        }

        /* Stagger delay utilities */
        .delay-100 { animation-delay: 0.1s; }
        .delay-200 { animation-delay: 0.2s; }
        .delay-300 { animation-delay: 0.3s; }
        .delay-400 { animation-delay: 0.4s; }
    </style>
</head>
<body>
    <!-- Loading Overlay -->
    <div id="app-loader" class="app-loader">
        <div class="loader-icon"><i class="fas fa-bolt text-white text-2xl"></i></div>
        <div style="font-size:1.1rem;font-weight:800;letter-spacing:-0.03em;">Stock Market <span style="background:linear-gradient(135deg,#10b981,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Prediction</span></div>
        <div style="font-size:0.7rem;color:var(--text-secondary);margin-top:6px;letter-spacing:0.03em;">Loading market intelligence…</div>
        <div class="loader-bar"><div class="loader-bar-fill"></div></div>
    </div>
    <!-- Failsafe: always dismiss loader even if external scripts fail to load -->
    <script>
        // JWT Auth Wrapper
        async function apiFetch(url, options = {}) {
            const token = localStorage.getItem('token');
            if (token) {
                options.headers = options.headers || {};
                options.headers['Authorization'] = 'Bearer ' + token;
            }
            return fetch(url, options);
        }

        (function() {
            var maxWait = 5000;
            var t = setTimeout(function() {
                var loader = document.getElementById('app-loader');
                if (loader && !loader.classList.contains('hidden')) {
                    loader.classList.add('hidden');
                    console.warn('Failsafe: dismissed loader after ' + maxWait + 'ms');
                }
            }, maxWait);
            window.__loaderFailsafeTimer = t;
        })();
    </script>

    <script>
        window.__INITIAL_MARKET_DATA__ = {{ initial_market_data | tojson }};
        window.__INDIAN_STOCKS_CONFIG__ = {{ indian_stocks_config | tojson }};
        window.__IS_LOGGED_IN__ = {{ is_logged_in | tojson }};
        window.__CURRENT_USER__ = { id: {{ user_id | tojson }}, username: {{ username | tojson }} };
        
        // Ensure all fetch requests include credentials and CSRF token so sessions work properly
        const originalFetch = window.fetch;
        window.fetch = function() {
            let args = Array.prototype.slice.call(arguments);
            if (typeof args[0] === 'string' && args[0].startsWith('/api/')) {
                if (!args[1]) args[1] = {};
                args[1].credentials = 'same-origin';
                args[1].headers = args[1].headers || {};
                args[1].headers['X-CSRF-Token'] = '{{ csrf_token }}';
            }
            return originalFetch.apply(this, args);
        };
    </script>

    <div id="dashboard-wrapper" class="">
    <!-- ═══════════════════ HEADER ═══════════════════ -->
    <header class="header-glass sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div class="flex justify-between items-center">
                <!-- Logo -->
                <a href="/" class="flex items-center gap-3 group" style="text-decoration:none;color:inherit;">
                    <div class="w-9 h-9 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg,#059669,#14b8a6);box-shadow:0 4px 12px rgba(16,185,129,0.25);">
                        <i class="fas fa-bolt text-white text-sm"></i>
                    </div>
                    <div>
                        <h1 class="text-base font-bold tracking-tight leading-tight">Stock Market <span style="background:linear-gradient(135deg,#10b981,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Prediction</span></h1>
                        <p class="text-[0.65rem] text-gray-500 font-medium tracking-wide uppercase">Indian Market Intelligence</p>
                    </div>
                </a>
                <!-- Nav -->
                <div class="hidden md:flex items-center gap-6">
                    <a href="/" class="text-sm font-medium text-gray-300 hover:text-white transition-colors" style="text-decoration:none;">Home</a>
                    <div id="market-status" class="pill-hold px-3 py-1 rounded-full text-xs font-bold">
                        <span class="live-dot mr-1.5" style="vertical-align:middle;"></span>
                        <span id="market-status-text">{{ initial_status }}</span>
                    </div>
                </div>
                <div class="flex items-center gap-3">
                    <!-- Mobile status -->
                    <div class="md:hidden">
                        <div id="market-status-mobile" class="pill-hold px-3 py-1 rounded-full text-xs font-bold">
                            <span class="live-dot mr-1.5" style="vertical-align:middle;"></span>
                        </div>
                    </div>
                    <div class="hidden sm:flex items-center text-xs text-gray-500 mono">
                        <i class="far fa-clock mr-1"></i>
                        <span id="current-time">{{ initial_time }}</span>
                    </div>
                    <button onclick="refreshData()" id="refresh-btn" class="btn btn-ghost text-xs">
                        <i class="fas fa-arrows-rotate"></i><span class="hidden sm:inline">Refresh</span>
                    </button>
                    <button onclick="openAIModal()" id="ai-btn" class="btn btn-purple text-xs">
                        <i class="fas fa-brain"></i><span class="hidden sm:inline">AI Analysis</span>
                    </button>
                    <!-- Auth Button -->
                    <div id="auth-area">
                        {% if is_logged_in %}
                        <div class="flex items-center gap-2">
                            <div class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.04] border border-white/[0.06]">
                                <div class="w-6 h-6 rounded-full flex items-center justify-center text-[0.6rem] font-bold" style="background:linear-gradient(135deg,#059669,#14b8a6);">
                                    {{ username[0] | upper }}
                                </div>
                                <span class="text-xs font-medium text-gray-300 hidden sm:inline">{{ username }}</span>
                            </div>
                            <button onclick="doLogout()" class="btn btn-ghost text-xs" title="Sign Out">
                                <i class="fas fa-right-from-bracket"></i>
                            </button>
                        </div>
                        {% else %}
                        <button onclick="openAuthModal()" id="auth-btn" class="btn text-xs" style="background:linear-gradient(135deg,#059669,#14b8a6);">
                            <i class="fas fa-user"></i><span class="hidden sm:inline">Sign In</span>
                        </button>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- ═══════════════════ MAIN ═══════════════════ -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 relative z-1">
        <!-- Navigation Tab Bar (Glassmorphic) -->
        <!-- Navigation Tab Bar (Glassmorphic) -->
        <div class="flex gap-2 mb-8 bg-white/[0.02] border border-white/[0.05] p-1.5 rounded-2xl max-w-lg mx-auto sm:mx-0 overflow-x-auto whitespace-nowrap">
            <button id="tab-indices" onclick="switchSection('indices')" class="flex-1 flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-300 bg-gradient-to-r from-emerald-600/80 to-teal-600/80 text-white shadow-lg shadow-emerald-500/10 active min-w-[100px]">
                <i class="fas fa-chart-line"></i><span>Indices</span>
            </button>
            <button id="tab-stocks" onclick="switchSection('stocks')" class="flex-1 flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-300 text-gray-400 hover:text-white hover:bg-white/[0.04] min-w-[100px]">
                <i class="fas fa-building"></i><span>Stocks</span>
            </button>
        </div>

        <!-- Market Cards -->
        <section class="market-grid mb-8" id="market-cards-section">
            <!-- NIFTY 50 -->
            <div id="nifty-card" class="glass-card card-emerald p-5 animate-fade-in-up">
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <h2 class="text-[1.05rem] font-bold tracking-tight">NIFTY 50</h2>
                        <p class="text-[0.7rem] text-gray-500">NSE · National Stock Exchange</p>
                    </div>
                    <span class="tag tag-emerald">NSE</span>
                </div>
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <div id="nifty-price" class="text-[1.7rem] font-extrabold tracking-tight price-value">--</div>
                        <div id="nifty-change" class="text-sm font-semibold mt-0.5">--</div>
                    </div>
                    <div id="nifty-prediction" class="pill-hold px-3 py-1 rounded-full text-xs font-bold">HOLD</div>
                </div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
                    <div class="flex justify-between"><span class="text-gray-500">High</span><span id="nifty-high" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Low</span><span id="nifty-low" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Volume</span><span id="nifty-volume" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Updated</span><span id="nifty-time" class="font-medium mono" style="font-size:0.7rem">--:--</span></div>
                </div>
            </div>

            <!-- BANK NIFTY -->
            <div id="banknifty-card" class="glass-card card-purple p-5 animate-fade-in-up delay-100">
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <h2 class="text-[1.05rem] font-bold tracking-tight">BANK NIFTY</h2>
                        <p class="text-[0.7rem] text-gray-500">NSE · Banking Index</p>
                    </div>
                    <span class="tag tag-purple">NSE</span>
                </div>
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <div id="banknifty-price" class="text-[1.7rem] font-extrabold tracking-tight price-value">--</div>
                        <div id="banknifty-change" class="text-sm font-semibold mt-0.5">--</div>
                    </div>
                    <div id="banknifty-prediction" class="pill-hold px-3 py-1 rounded-full text-xs font-bold">HOLD</div>
                </div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
                    <div class="flex justify-between"><span class="text-gray-500">High</span><span id="banknifty-high" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Low</span><span id="banknifty-low" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Volume</span><span id="banknifty-volume" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Updated</span><span id="banknifty-time" class="font-medium mono" style="font-size:0.7rem">--:--</span></div>
                </div>
            </div>

            <!-- SENSEX -->
            <div id="sensex-card" class="glass-card card-blue p-5 animate-fade-in-up delay-200">
                <div class="flex justify-between items-start mb-3">
                    <div>
                        <h2 class="text-[1.05rem] font-bold tracking-tight">SENSEX</h2>
                        <p class="text-[0.7rem] text-gray-500">BSE · Bombay Stock Exchange</p>
                    </div>
                    <span class="tag tag-blue">BSE</span>
                </div>
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <div id="sensex-price" class="text-[1.7rem] font-extrabold tracking-tight price-value">--</div>
                        <div id="sensex-change" class="text-sm font-semibold mt-0.5">--</div>
                    </div>
                    <div id="sensex-prediction" class="pill-hold px-3 py-1 rounded-full text-xs font-bold">HOLD</div>
                </div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
                    <div class="flex justify-between"><span class="text-gray-500">High</span><span id="sensex-high" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Low</span><span id="sensex-low" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Volume</span><span id="sensex-volume" class="font-medium">--</span></div>
                    <div class="flex justify-between"><span class="text-gray-500">Updated</span><span id="sensex-time" class="font-medium mono" style="font-size:0.7rem">--:--</span></div>
                </div>
            </div>
        </section>

        <!-- Stocks Section -->
        <section id="stocks-section" class="hidden mb-8 animate-fade-in">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-6">
                <div>
                    <h2 class="text-base font-bold tracking-tight"><i class="fas fa-building mr-2 text-emerald-400"></i>Top 20 Indian Blue-chips</h2>
                    <p class="text-xs text-gray-500 mt-0.5">Live prices & AI-powered trend predictions based on technical indicators</p>
                </div>
                <div class="flex items-center gap-3">
                    <!-- Watchlist Toggle Buttons -->
                    <div class="flex rounded-xl bg-white/[0.02] border border-white/[0.05] p-1 text-xs">
                        <button onclick="setStockFilter('all')" id="btn-filter-all" class="px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 tf-active">All Stocks</button>
                        <button onclick="setStockFilter('watchlist')" id="btn-filter-watchlist" class="px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 text-gray-400 hover:text-white">Watchlist</button>
                    </div>
                    <div class="text-[0.7rem] px-3 py-1 rounded-full bg-white/[0.04] text-gray-400 font-medium border border-white/[0.05]">
                        <i class="far fa-clock mr-1.5 text-emerald-400"></i><span id="stocks-last-updated">Last updated: Just now</span>
                    </div>
                </div>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 animate-fade-in" id="stocks-grid">
                <div class="col-span-full py-16 text-center text-gray-600 glass-card">
                    <div class="animate-spin rounded-full h-8 w-8 border-2 border-transparent border-t-emerald-500 mx-auto mb-3"></div>
                    <p class="text-sm">Fetching stock market live predictions...</p>
                </div>
            </div>
        </section>

        <!-- Historical Values -->
        <section class="glass-card p-5 mb-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-5">
                <div>
                    <h3 class="text-base font-bold">Day-by-Day Closing Values</h3>
                    <p class="text-xs text-gray-500 mt-0.5">Historical market closing prices</p>
                </div>
                <select id="historical-symbol-select" onchange="loadHistoricalData()" class="styled-select">
                    <optgroup label="Indices" style="background:#0d1117;color:var(--text-primary);">
                        <option value="NIFTY_50" selected>NIFTY 50</option>
                        <option value="BANK_NIFTY">BANK NIFTY</option>
                        <option value="SENSEX">SENSEX</option>
                    </optgroup>
                </select>
            </div>
            <div id="historical-data-container">
                <div class="text-center py-12 text-gray-600">
                    <i class="fas fa-clock-rotate-left text-3xl mb-3 opacity-40"></i>
                    <p class="text-sm">Select an index to view historical closing values</p>
                </div>
            </div>
        </section>

        <!-- Candlestick Chart -->
        <section class="glass-card p-5 mb-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                <div>
                    <h3 class="text-base font-bold"><i class="fas fa-chart-candlestick mr-1.5 text-amber-400" style="font-size:0.9rem"></i>Candlestick Chart</h3>
                    <p class="text-xs text-gray-500 mt-0.5">OHLC price action</p>
                </div>
                <select id="chart-symbol-select" onchange="switchChartSymbol()" class="styled-select">
                    <optgroup label="Indices" style="background:#0d1117;color:var(--text-primary);">
                        <option value="NIFTY_50" selected>NIFTY 50</option>
                        <option value="BANK_NIFTY">BANK NIFTY</option>
                        <option value="SENSEX">SENSEX</option>
                    </optgroup>
                </select>
            </div>
            <!-- Timeframe pills -->
            <div id="tf-pills" class="flex flex-wrap gap-2 mb-4">
                <button onclick="setTimeframe('5min')"  class="tf-pill" data-tf="5min">5 Min</button>
                <button onclick="setTimeframe('1hr')"   class="tf-pill" data-tf="1hr">1 Hour</button>
                <button onclick="setTimeframe('1day')"  class="tf-pill tf-active" data-tf="1day">1 Day</button>
                <button onclick="setTimeframe('1yr')"   class="tf-pill" data-tf="1yr">1 Year</button>
                <button onclick="setTimeframe('3yr')"   class="tf-pill" data-tf="3yr">3 Years</button>
                <button onclick="setTimeframe('5yr')"   class="tf-pill" data-tf="5yr">5 Years</button>
                <button onclick="setTimeframe('lifetime')" class="tf-pill" data-tf="lifetime">Lifetime</button>
            </div>
            
            <!-- Chart Type Controls -->
            <div id="chart-type-controls" class="flex flex-wrap gap-2 mb-4 text-xs">
                <span class="text-gray-400 font-medium self-center mr-2">Chart Type:</span>
                <button onclick="setChartType('candle')" class="tf-pill tf-active" id="btn-chart-candle">Candles</button>
                <button onclick="setChartType('graph')" class="tf-pill" id="btn-chart-graph">Graph</button>
            </div>
            <div id="chart-container" style="min-height:420px;display:flex;align-items:center;justify-content:center;">
                <div class="text-center text-gray-600">
                    <i class="fas fa-chart-bar text-3xl mb-3 opacity-40"></i>
                    <p class="text-sm">Loading candlestick chart…</p>
                </div>
            </div>
            <div id="live-chart" style="height:440px;width:100%;display:none;"></div>
            <div class="mt-2 text-[0.7rem] text-gray-600 text-center">
                <span id="chart-info">Select a symbol and timeframe</span>
            </div>
        </section>

    </main>

    <!-- ═══════════════════ FOOTER ═══════════════════ -->
    <footer class="footer" style="border-top: 1px solid transparent; border-image: linear-gradient(90deg, transparent, rgba(59,130,246,0.3), rgba(139,92,246,0.3), transparent) 1;">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-gray-600">
                <div class="flex items-center gap-2">
                    <div class="w-5 h-5 rounded-md flex items-center justify-center" style="background:linear-gradient(135deg,#059669,#14b8a6);">
                        <i class="fas fa-bolt text-white" style="font-size:0.5rem;"></i>
                    </div>
                    <span class="font-semibold text-gray-400">Stock Market Prediction</span>
                    <span>· Indian Market Intelligence</span>
                </div>
                <div class="text-center sm:text-right text-gray-600" style="font-size:0.65rem;">
                    <p>⚠️ For informational purposes only. Not financial advice. Trade at your own risk.</p>
                </div>
            </div>
        </div>
    </footer>
    </div> <!-- Close dashboard-wrapper -->

    <!-- ═══════════════════ AI MODAL ═══════════════════ -->
    <div id="aiModal" class="modal-overlay">
        <div class="modal-panel">
            <div class="px-6 py-4 border-b" style="border-color:var(--border-subtle);background:rgba(255,255,255,0.02);border-radius:20px 20px 0 0;">
                <div class="flex justify-between items-center">
                    <h2 class="text-lg font-bold"><i class="fas fa-brain mr-2 text-teal-400"></i>AI Market Analysis</h2>
                    <button onclick="closeAIModal()" class="text-gray-500 hover:text-white transition-colors p-1"><i class="fas fa-xmark text-lg"></i></button>
                </div>
            </div>
            <div class="p-6" style="max-height:75vh;overflow-y:auto;">
                <div id="ai-analysis-content">
                    <div class="text-center py-10">
                        <div class="animate-spin rounded-full h-10 w-10 border-2 border-transparent border-t-teal-500 mx-auto mb-4"></div>
                        <p class="text-sm text-gray-500">Analyzing market data…</p>
                    </div>
                </div>
            </div>
            <div class="kbd-hint px-6 pb-4">Press <kbd>Esc</kbd> to close</div>
        </div>
    </div>

    <!-- ═══════════════════ AUTH MODAL ═══════════════════ -->
    <div id="authModal" class="modal-overlay">
        <div class="modal-panel" style="max-width:420px;">
            <!-- Header with tabs -->
            <div class="px-6 py-4 border-b" style="border-color:var(--border-subtle);background:rgba(255,255,255,0.02);border-radius:20px 20px 0 0;">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-bold"><i class="fas fa-shield-halved mr-2 text-emerald-400"></i>Account</h2>
                    <button onclick="closeAuthModal()" class="text-gray-500 hover:text-white transition-colors p-1"><i class="fas fa-xmark text-lg"></i></button>
                </div>
                <!-- Tab switcher -->
                <div class="flex rounded-xl bg-white/[0.03] border border-white/[0.06] p-1">
                    <button onclick="switchAuthTab('login')" id="tab-auth-login" class="flex-1 py-2 rounded-lg text-sm font-semibold transition-all duration-200 bg-gradient-to-r from-emerald-600/80 to-teal-600/80 text-white">Sign In</button>
                    <button onclick="switchAuthTab('register')" id="tab-auth-register" class="flex-1 py-2 rounded-lg text-sm font-semibold transition-all duration-200 text-gray-400 hover:text-white">Create Account</button>
                </div>
            </div>
            <!-- Login Form -->
            <div id="auth-login-form" class="p-6">
                <form onsubmit="submitLogin(event)" autocomplete="on">
                    <div class="mb-4">
                        <label class="block text-xs font-semibold text-gray-400 mb-1.5">Username or Email</label>
                        <input type="text" id="login-username" name="username" autocomplete="username" required
                            class="w-full px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 outline-none"
                            style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);"
                            onfocus="this.style.borderColor='rgba(16,185,129,0.5)';this.style.boxShadow='0 0 0 3px rgba(16,185,129,0.1)';"
                            onblur="this.style.borderColor='rgba(255,255,255,0.08)';this.style.boxShadow='none';"
                            placeholder="Enter your username or email">
                    </div>
                    <div class="mb-5">
                        <label class="block text-xs font-semibold text-gray-400 mb-1.5">Password</label>
                        <div style="position:relative;">
                            <input type="password" id="login-password" name="password" autocomplete="current-password" required minlength="8"
                                class="w-full px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 outline-none"
                                style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);padding-right:44px;"
                                onfocus="this.style.borderColor='rgba(16,185,129,0.5)';this.style.boxShadow='0 0 0 3px rgba(16,185,129,0.1)';"
                                onblur="this.style.borderColor='rgba(255,255,255,0.08)';this.style.boxShadow='none';"
                                placeholder="Enter your password">
                            <button type="button" onclick="togglePasswordVisibility('login-password', this)" class="text-gray-500 hover:text-gray-300" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;"><i class="fas fa-eye"></i></button>
                        </div>
                    </div>
                    <div id="login-error" class="mb-3 text-xs font-medium text-red-400" style="display:none;"></div>
                    <button type="submit" id="login-submit-btn" class="w-full py-3 rounded-xl text-sm font-bold transition-all duration-200" style="background:linear-gradient(135deg,#059669,#14b8a6);color:#fff;border:none;cursor:pointer;">
                        <i class="fas fa-right-to-bracket mr-2"></i>Sign In
                    </button>
                </form>
            </div>
            <!-- Register Form -->
            <div id="auth-register-form" class="p-6" style="display:none;">
                <form onsubmit="submitRegister(event)" autocomplete="on">
                    <div class="mb-4">
                        <label class="block text-xs font-semibold text-gray-400 mb-1.5">Username</label>
                        <input type="text" id="reg-username" name="username" autocomplete="username" required minlength="3" maxlength="20" pattern="^[a-zA-Z0-9_]{3,20}$"
                            class="w-full px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 outline-none"
                            style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);"
                            onfocus="this.style.borderColor='rgba(16,185,129,0.5)';this.style.boxShadow='0 0 0 3px rgba(16,185,129,0.1)';"
                            onblur="this.style.borderColor='rgba(255,255,255,0.08)';this.style.boxShadow='none';"
                            placeholder="3-20 chars, letters, numbers, underscore">
                        <p class="text-[0.65rem] text-gray-600 mt-1">3–20 characters · Letters, numbers, underscore only</p>
                    </div>
                    <div class="mb-4">
                        <label class="block text-xs font-semibold text-gray-400 mb-1.5">Email</label>
                        <input type="email" id="reg-email" name="email" autocomplete="email" required
                            class="w-full px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 outline-none"
                            style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);"
                            onfocus="this.style.borderColor='rgba(16,185,129,0.5)';this.style.boxShadow='0 0 0 3px rgba(16,185,129,0.1)';"
                            onblur="this.style.borderColor='rgba(255,255,255,0.08)';this.style.boxShadow='none';"
                            placeholder="you@example.com">
                    </div>
                    <div class="mb-4">
                        <label class="block text-xs font-semibold text-gray-400 mb-1.5">Password</label>
                        <div style="position:relative;">
                            <input type="password" id="reg-password" name="new-password" autocomplete="new-password" required minlength="8"
                                class="w-full px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 outline-none"
                                style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);padding-right:44px;"
                                onfocus="this.style.borderColor='rgba(16,185,129,0.5)';this.style.boxShadow='0 0 0 3px rgba(16,185,129,0.1)';"
                                onblur="this.style.borderColor='rgba(255,255,255,0.08)';this.style.boxShadow='none';"
                                placeholder="Minimum 8 characters">
                            <button type="button" onclick="togglePasswordVisibility('reg-password', this)" class="text-gray-500 hover:text-gray-300" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;"><i class="fas fa-eye"></i></button>
                        </div>
                        <div id="password-strength" class="mt-2" style="display:none;">
                            <div class="confidence-bar"><div id="pw-strength-fill" class="confidence-fill" style="width:0%;"></div></div>
                            <span id="pw-strength-text" class="text-[0.65rem] text-gray-600 mt-0.5 block"></span>
                        </div>
                    </div>
                    <div class="mb-5">
                        <label class="block text-xs font-semibold text-gray-400 mb-1.5">Confirm Password</label>
                        <input type="password" id="reg-confirm-password" autocomplete="new-password" required minlength="8"
                            class="w-full px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 outline-none"
                            style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);"
                            onfocus="this.style.borderColor='rgba(16,185,129,0.5)';this.style.boxShadow='0 0 0 3px rgba(16,185,129,0.1)';"
                            onblur="this.style.borderColor='rgba(255,255,255,0.08)';this.style.boxShadow='none';"
                            placeholder="Re-enter your password">
                    </div>
                    <div id="register-error" class="mb-3 text-xs font-medium text-red-400" style="display:none;"></div>
                    <button type="submit" id="register-submit-btn" class="w-full py-3 rounded-xl text-sm font-bold transition-all duration-200" style="background:linear-gradient(135deg,#059669,#14b8a6);color:#fff;border:none;cursor:pointer;">
                        <i class="fas fa-user-plus mr-2"></i>Create Account
                    </button>
                </form>
            </div>
            <div class="kbd-hint px-6 pb-4">Press <kbd>Esc</kbd> to close</div>
        </div>
    </div>
    <script>
        /* ═══════════════════ GLOBALS ═══════════════════ */
        let currentChartSymbol = null;
let lastChartData = null; // Store last chart details
let userWatchlist = []; // Global user watchlist
let currentStockFilter = 'all'; // Filter state: 'all' or 'watchlist'
let currentChartType = 'candle';
        let currentTimeframe = '1day';
        let marketData = {};
        let canRefresh = true;
        let isSearchFocused = false;
        let socket = null;
        let reconnectAttempts = 0;
        const MAX_RECONNECT = 5;
        const RECONNECT_DELAY = 2000;

        /* ═══════════════════ INIT ═══════════════════ */
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeApp);
        } else {
            initializeApp();
        }

        function initializeApp() {
            console.log('🚀 Initializing Agentic AI Trader…');
            updateDropdownOptions('indices'); // Set initial selects for indices
            updateTime();
            updateMarketStatus();

            // Use server-rendered initial data
            if (window.__INITIAL_MARKET_DATA__) {
                console.log('📦 Server-rendered data found');
                updateMarketCards(window.__INITIAL_MARKET_DATA__);
                delete window.__INITIAL_MARKET_DATA__;
            }

            // Fetch live data from API
            loadInitialData();

            // Connect websocket for real-time pushes
            connectWebSocket();

            // Auto-refresh every 10 seconds for near-real-time data
            setInterval(async () => {
                try {
                    const r = await apiFetch('/api/market/latest');
                    if (r.ok) { const d = await r.json(); updateMarketCards(d); }
                } catch(e) { console.warn('Auto-refresh failed:', e); }
            }, 10000);

            // Clock tick every second
            setInterval(updateTime, 1000);
            // Market status check every 10 seconds
            setInterval(updateMarketStatus, 10000);

            // Auto-load chart and historical data for NIFTY_50 (default)
            switchChartSymbol();
            loadHistoricalData();

            // Load stocks data initially
            loadStocksData();
            
            // Auto-refresh stocks data every 15 seconds
            setInterval(loadStocksData, 15000);

            // Dismiss loading overlay after initial data arrives
            setTimeout(() => {
                const loader = document.getElementById('app-loader');
                if (loader) loader.classList.add('hidden');
            }, 1800);

            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') closeAIModal();
            });

            console.log('✅ Initialization complete');
        }

        /* ═══════════════════ UI ANIMATION HELPERS ═══════════════════ */
        function animatePrice(el, newValue) {
            if (!el) return;
            el.classList.add('price-update');
            el.textContent = newValue;
            setTimeout(() => el.classList.remove('price-update'), 300);
        }

        function generateSparklineSVG(prices, isUp) {
            if (!prices || prices.length < 2) return '';
            const min = Math.min(...prices);
            const max = Math.max(...prices);
            const range = max - min || 1;
            const w = 80, h = 28;
            const points = prices.map((p, i) => {
                const x = (i / (prices.length - 1)) * w;
                const y = h - ((p - min) / range) * h;
                return x + ',' + y;
            }).join(' ');
            const color = isUp ? '#10b981' : '#ef4444';
            return '<svg width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" style="opacity:0.7;"><polyline points="' + points + '" fill="none" stroke="' + color + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
        }

        /* ═══════════════════ STOCKS LOGIC ═══════════════════ */
        let stocksData = [];

        function updateDropdownOptions(section) {
            const histSelect = document.getElementById('historical-symbol-select');
            const chartSelect = document.getElementById('chart-symbol-select');
            
            const INDICES_OPTIONS = `
                <optgroup label="Indices" style="background:#0d1117;color:var(--text-primary);">
                    <option value="NIFTY_50" selected>NIFTY 50</option>
                    <option value="BANK_NIFTY">BANK NIFTY</option>
                    <option value="SENSEX">SENSEX</option>
                </optgroup>
            `;
            
            const STOCKS_OPTIONS = `
                <optgroup label="Top Blue-chip Stocks" style="background:#0d1117;color:var(--text-primary);">
                    <option value="RELIANCE" selected>Reliance</option>
                    <option value="TCS">TCS</option>
                    <option value="HDFCBANK">HDFC Bank</option>
                    <option value="INFY">Infosys</option>
                    <option value="ICICIBANK">ICICI Bank</option>
                    <option value="HINDUNILVR">HUL</option>
                    <option value="SBIN">SBI</option>
                    <option value="BHARTIARTL">Bharti Airtel</option>
                    <option value="ITC">ITC</option>
                    <option value="KOTAKBANK">Kotak Bank</option>
                    <option value="LT">L&T</option>
                    <option value="AXISBANK">Axis Bank</option>
                    <option value="BAJFINANCE">Bajaj Finance</option>
                    <option value="MARUTI">Maruti Suzuki</option>
                    <option value="TATAMOTORS">Tata Motors</option>
                    <option value="TATASTEEL">Tata Steel</option>
                    <option value="SUNPHARMA">Sun Pharma</option>
                    <option value="ADANIENT">Adani Ent</option>
                    <option value="WIPRO">Wipro</option>
                    <option value="POWERGRID">Power Grid</option>
                </optgroup>
            `;
            
            if (section === 'indices') {
                if (histSelect) histSelect.innerHTML = INDICES_OPTIONS;
                if (chartSelect) chartSelect.innerHTML = INDICES_OPTIONS;
            } else if (section === 'stocks') {
                if (histSelect) histSelect.innerHTML = STOCKS_OPTIONS;
                if (chartSelect) chartSelect.innerHTML = STOCKS_OPTIONS;
            }
        }

        function switchSection(section) {
            console.log('🔄 Switching section to:', section);
            if (!['indices', 'stocks'].includes(section)) return;
            
            const tabs = {
                indices: document.getElementById('tab-indices'),
                stocks: document.getElementById('tab-stocks'),
            };
            
            const sections = {
                indices: document.getElementById('market-cards-section'),
                stocks: document.getElementById('stocks-section'),
            };
            
            // Reset classes
            for (const [key, tab] of Object.entries(tabs)) {
                if (tab) {
                    if (key === section) {
                        tab.className = "flex-1 flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-300 bg-gradient-to-r from-emerald-600/80 to-teal-600/80 text-white shadow-lg shadow-emerald-500/10 active min-w-[100px]";
                    } else {
                        tab.className = "flex-1 flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-300 text-gray-400 hover:text-white hover:bg-white/[0.04] min-w-[100px]";
                    }
                }
            }
            
            // Show/hide sections
            for (const [key, sec] of Object.entries(sections)) {
                if (sec) {
                    if (key === section) {
                        sec.style.display = (key === 'indices') ? 'grid' : 'block';
                        sec.classList.remove('hidden');
                        
                        // Load data when tab is opened
                        
                    } else {
                        sec.style.display = 'none';
                        sec.classList.add('hidden');
                    }
                }
            }
            
            // Dynamically update selects to restrict choices
            updateDropdownOptions(section);
            
            // Load section-specific data & refresh charts with active selection
            if (section === 'indices') {
                const activeSymbol = 'NIFTY_50';
                currentChartSymbol = activeSymbol;
                loadHistoricalData();
                loadCandleData(activeSymbol, currentTimeframe);
            } else if (section === 'stocks') {
                loadStocksData();
                const activeSymbol = 'RELIANCE';
                currentChartSymbol = activeSymbol;
                loadHistoricalData();
                loadCandleData(activeSymbol, currentTimeframe);
            }
        }

        function showAuthErrorMessage(msg) {
            const errEl = document.getElementById('auth-error-msg');
            if (errEl) {
                errEl.innerText = msg;
                errEl.classList.remove('hidden');
            }
        }

        async function loadWatchlist() {
            if (!currentUser) {
                userWatchlist = [];
                return;
            }
            try {
                const response = await apiFetch('/api/watchlist');
                if (response.ok) {
                    const data = await response.json();
                    userWatchlist = data.symbols || [];
                }
            } catch(e) {
                console.warn('Failed to load watchlist:', e);
            }
        }

        function isWatched(symbol) {
            return userWatchlist.includes(symbol);
        }

        async function toggleWatchlistEvent(e, symbol) {
            e.stopPropagation();
            if (!currentUser) {
                openAuthModal('login');
                showAuthErrorMessage("Please login to manage your watchlist.");
                return;
            }
            const wasWatched = isWatched(symbol);
            const url = wasWatched ? '/api/watchlist/remove' : '/api/watchlist/add';
            try {
                const response = await apiFetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ symbol: symbol })
                });
                if (response.ok) {
                    if (wasWatched) {
                        userWatchlist = userWatchlist.filter(s => s !== symbol);
                    } else {
                        userWatchlist.push(symbol);
                    }
                    renderStocksGrid();
                } else {
                    console.error('Watchlist API failed');
                }
            } catch(err) {
                console.error('Watchlist request error:', err);
            }
        }

        function setStockFilter(filter) {
            if (filter === 'watchlist' && !currentUser) {
                openAuthModal('login');
                showAuthErrorMessage("Please login to access your watchlist.");
                return;
            }
            currentStockFilter = filter;
            const btnAll = document.getElementById('btn-filter-all');
            const btnWatchlist = document.getElementById('btn-filter-watchlist');
            if (filter === 'all') {
                if (btnAll) btnAll.className = "px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 tf-active";
                if (btnWatchlist) btnWatchlist.className = "px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 text-gray-400 hover:text-white";
            } else {
                if (btnAll) btnAll.className = "px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 text-gray-400 hover:text-white";
                if (btnWatchlist) btnWatchlist.className = "px-3 py-1.5 rounded-lg font-semibold transition-all duration-200 tf-active";
            }
            renderStocksGrid();
        }

        function renderStocksGrid() {
            const grid = document.getElementById('stocks-grid');
            if (!grid) return;
            let filteredStocks = stocksData;
            if (currentStockFilter === 'watchlist') {
                filteredStocks = stocksData.filter(stock => isWatched(stock.symbol));
            }
            if (!filteredStocks || filteredStocks.length === 0) {
                if (currentStockFilter === 'watchlist') {
                    grid.innerHTML = '<div class="col-span-full py-16 text-center text-gray-500 glass-card"><i class="far fa-star text-2xl mb-2 opacity-40"></i><p class="text-sm">Your watchlist is empty. Add stocks by clicking the star icons!</p></div>';
                } else {
                    grid.innerHTML = '<div class="col-span-full py-16 text-center text-gray-500 glass-card"><i class="fas fa-triangle-exclamation text-2xl mb-2 text-amber-500"></i><p class="text-sm">No stocks data available.</p></div>';
                }
                return;
            }
            let html = '';
            filteredStocks.forEach(stock => {
                html += createStockCardHTML(stock);
            });
            grid.innerHTML = html;
        }

        async function loadStocksData() {
            const grid = document.getElementById('stocks-grid');
            const timeEl = document.getElementById('stocks-last-updated');
            if (!grid) return;
            
            try {
                const response = await apiFetch('/api/stocks/list');
                if (!response.ok) throw new Error('API request failed');
                
                stocksData = await response.json();
                
                if (!stocksData || stocksData.length === 0) {
                    grid.innerHTML = '<div class="col-span-full py-16 text-center text-gray-500 glass-card"><i class="fas fa-triangle-exclamation text-2xl mb-2 text-amber-500"></i><p class="text-sm">No stocks data available. Retrying...</p></div>';
                    return;
                }
                
                await loadWatchlist();
                renderStocksGrid();
                
                // Subscribe to real-time tick stream for all fetched stocks
                if (typeof socket !== 'undefined' && socket && socket.connected) {
                    stocksData.forEach(s => socket.emit('subscribe_tick_stream', {symbol: s.symbol}));
                }
                
                if (timeEl) {
                    timeEl.textContent = 'Last updated: ' + new Date().toLocaleTimeString('en-IN', {hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:true});
                }
            } catch (e) {
                console.error('❌ Failed to load stocks data:', e);
                if (grid.innerHTML.includes('animate-spin') || grid.innerHTML.includes('Fetching')) {
                    grid.innerHTML = '<div class="col-span-full py-16 text-center text-gray-500 glass-card"><i class="fas fa-triangle-exclamation text-2xl mb-2 text-red-500"></i><p class="text-sm">Failed to connect to stock service. Retrying...</p></div>';
                }
            }
        }

        function createStockCardHTML(stock) {
            const isUp = stock.change >= 0;
            const changeSign = isUp ? '▲' : '▼';
            const changeClass = isUp ? 'profit' : 'loss';
            
            // AI Signal colors + card border class
            let signalClass = 'pill-hold';
            let signalText = stock.prediction;
            let cardSignalClass = 'signal-hold';
            if (stock.prediction === 'UP') {
                signalClass = 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
                signalText = 'BUY';
                cardSignalClass = 'signal-up';
            } else if (stock.prediction === 'DOWN') {
                signalClass = 'bg-red-500/20 text-red-400 border border-red-500/30';
                signalText = 'SELL';
                cardSignalClass = 'signal-down';
            } else {
                signalClass = 'bg-amber-500/20 text-amber-400 border border-amber-500/30';
                signalText = 'HOLD';
                cardSignalClass = 'signal-hold';
            }
            
            const rsiVal = Number(stock.rsi) || 50;
            const confVal = Number(stock.confidence) || 50;
            const confLevel = confVal >= 70 ? 'high' : confVal >= 45 ? 'medium' : 'low';

            // Generate fake sparkline from price (deterministic variation)
            const sparkPrices = [];
            const base = stock.price || 1000;
            for (let i = 0; i < 7; i++) {
                const seed = (stock.symbol.charCodeAt(i % stock.symbol.length) * (i + 1)) % 100;
                sparkPrices.push(base * (1 + (seed - 50) * 0.003));
            }
            sparkPrices.push(base); // current price is last point
            const sparkSVG = generateSparklineSVG(sparkPrices, isUp);

            return `
                <div class="glass-card p-4 flex flex-col justify-between cursor-pointer hover:border-white/20 transition-all duration-300 stock-card ${cardSignalClass}" onclick="focusOnStock('${stock.symbol}')">
                    <div>
                        <div class="flex justify-between items-start mb-2">
                            <div class="truncate pr-2" style="max-width: 65%;">
                                <h3 class="text-xs sm:text-sm font-bold truncate leading-tight">${stock.display_name}</h3>
                                <p class="text-[0.65rem] text-gray-500 truncate mt-0.5">${stock.name} · ${stock.sector}</p>
                            </div>
                            <div class="flex flex-col items-end gap-1">
                                <div class="flex items-center gap-1.5">
                                    <span class="text-[0.6rem] uppercase tracking-wider px-1.5 py-0.5 rounded bg-white/[0.04] text-gray-400 border border-white/[0.05] font-mono leading-none">${stock.symbol}</span>
                                    <button onclick="toggleWatchlistEvent(event, '${stock.symbol}')" class="text-gray-500 hover:text-amber-400 focus:outline-none transition-colors text-xs z-10" id="star-${stock.symbol}" title="Add to Watchlist">
                                        <i class="${isWatched(stock.symbol) ? 'fas fa-star text-amber-400' : 'far fa-star'}"></i>
                                    </button>
                                </div>
                                <div class="text-[0.65rem] font-bold px-2.5 py-0.5 rounded-full ${signalClass}">${signalText}</div>
                            </div>
                        </div>
                        
                        <div class="flex justify-between items-end my-3">
                            <div>
                                <div class="text-base sm:text-lg font-extrabold tracking-tight font-mono">₹${stock.price.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                                <div class="text-[0.7rem] font-semibold ${changeClass} mt-0.5">${changeSign} ${Math.abs(stock.change).toFixed(2)} (${stock.change_percent.toFixed(2)}%)</div>
                            </div>
                            <div class="flex-shrink-0">${sparkSVG}</div>
                        </div>
                    </div>
                    
                    <div class="border-t border-white/[0.05] pt-2 mt-2 text-[0.65rem]">
                        <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-gray-500 mb-2">
                            <div class="flex justify-between"><span>RSI:</span><span class="font-medium text-gray-300 font-mono">${rsiVal.toFixed(1)}</span></div>
                            <div class="flex justify-between"><span>Confidence:</span><span class="font-medium text-gray-300 font-mono">${confVal.toFixed(0)}%</span></div>
                        </div>
                        <div class="confidence-bar mb-2"><div class="confidence-fill ${confLevel}" style="width:${Math.min(100, confVal)}%"></div></div>
                        <div class="bg-white/[0.02] border border-white/[0.04] rounded p-1.5 text-[0.6rem] text-gray-400 hover:text-white transition-colors leading-relaxed" style="white-space: normal; word-break: break-word;" title="${stock.analysis_text}">
                            ${stock.analysis_text}
                        </div>
                    </div>
                </div>
            `;
        }

        function focusOnStock(symbol) {
            console.log('🎯 Focusing on stock:', symbol);
            
            // Update selects
            const chartSelect = document.getElementById('chart-symbol-select');
            const histSelect = document.getElementById('historical-symbol-select');
            
            if (chartSelect) {
                chartSelect.value = symbol;
                switchChartSymbol();
            }
            
            if (histSelect) {
                histSelect.value = symbol;
                loadHistoricalData();
            }
            
            // Scroll to chart smoothly
            const chartContainer = document.getElementById('chart-container');
            if (chartContainer) {
                const chartSection = chartContainer.closest('section');
                if (chartSection) {
                    chartSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    // Brief visual glow indicator
                    chartSection.style.borderColor = 'rgba(59, 130, 246, 0.4)';
                    setTimeout(() => {
                        chartSection.style.borderColor = 'var(--border-subtle)';
                    }, 1500);
                }
            }
        }

        /* ═══════════════════ DATA LOADING ═══════════════════ */
        async function loadInitialData() {
            try {
                const routes = ['/api/market/latest', '/api/market-data'];
                let data = null;
                for (const route of routes) {
                    try {
                        const r = await apiFetch(route);
                        if (r.ok) { data = await r.json(); break; }
                    } catch(e) { /* try next */ }
                }
                if (data) {
                    const md = data.market_data || data;
                    if (md.NIFTY_50 || md.BANK_NIFTY || md.SENSEX) updateMarketCards(md);
                }
            } catch(e) {
                console.error('❌ Initial data load failed:', e);
                setTimeout(loadInitialData, 8000);
            }
        }

        /* ═══════════════════ WEBSOCKET ═══════════════════ */
        function connectWebSocket() {
            try {
                if (typeof io === 'undefined') {
                    console.warn('Socket.IO not loaded yet, retrying in 2s...');
                    setTimeout(connectWebSocket, 2000);
                    return;
                }
                socket = io();
                socket.on('connect', () => {
                    console.log('✅ WebSocket connected');
                    reconnectAttempts = 0;
                    ['NIFTY_50','BANK_NIFTY','SENSEX'].forEach(s => {
                        socket.emit('subscribe_market', {symbol: s});
                        socket.emit('subscribe_tick_stream', {symbol: s});
                    });
                });
                socket.on('market_update', d => { if (d && d.symbol) updateMarketCard(d); });
                socket.on('tick_update', d => { if (d && d.symbol) updateMarketCard(d); });
                socket.on('disconnect', () => attemptReconnect());
                socket.on('connect_error', () => attemptReconnect());
            } catch(e) { console.error('WebSocket init failed:', e); }
        }
        function attemptReconnect() {
            if (reconnectAttempts < MAX_RECONNECT) {
                reconnectAttempts++;
                setTimeout(connectWebSocket, RECONNECT_DELAY * reconnectAttempts);
            }
        }
        function updateMarketCard(d) {
            if (!['NIFTY_50', 'BANK_NIFTY', 'SENSEX'].includes(d.symbol)) {
                updateStockCard(d);
                return;
            }
            const prefix = d.symbol === 'NIFTY_50' ? 'nifty' : d.symbol === 'BANK_NIFTY' ? 'banknifty' : 'sensex';
            updateCard(prefix, d);
            // Flash effect
            const card = document.getElementById(prefix + '-card');
            if (card) { card.classList.add('data-flash'); setTimeout(() => card.classList.remove('data-flash'), 600); }
        }

        function updateStockCard(d) {
            if (!stocksData || stocksData.length === 0) return;
            const stockIndex = stocksData.findIndex(s => s.symbol === d.symbol);
            if (stockIndex !== -1) {
                stocksData[stockIndex].price = d.price;
                stocksData[stockIndex].change = d.change;
                stocksData[stockIndex].change_percent = d.change_percent;
                if (d.volume !== undefined) stocksData[stockIndex].volume = d.volume;
                
                // Debounce rendering slightly to avoid thrashing if many ticks arrive at once
                if (!window._stockRenderTimer) {
                    window._stockRenderTimer = setTimeout(() => {
                        renderStocksGrid();
                        window._stockRenderTimer = null;
                    }, 500);
                }
            }
        }

        /* ═══════════════════ CARD UPDATES ═══════════════════ */
        function updateMarketCards(data) {
            if (data.NIFTY_50)   updateCard('nifty', data.NIFTY_50);
            if (data.BANK_NIFTY) updateCard('banknifty', data.BANK_NIFTY);
            if (data.SENSEX)     updateCard('sensex', data.SENSEX);
        }

        function updateCard(prefix, data) {
            if (!data) return;
            const price = Number(data.price);
            if (isNaN(price)) return;

            const el = (id) => document.getElementById(id);
            const set = (id, val) => { const e = el(id); if (e) e.textContent = val; };

            // Price
            set(prefix + '-price', '₹' + price.toLocaleString('en-IN', {minimumFractionDigits:2, maximumFractionDigits:2}));

            // Change
            const ch = Number(data.change) || 0;
            const pct = Number(data.change_percent) || 0;
            const changeEl = el(prefix + '-change');
            if (changeEl) {
                changeEl.textContent = (ch >= 0 ? '▲' : '▼') + ' ' + Math.abs(ch).toFixed(2) + '  (' + Math.abs(pct).toFixed(2) + '%)';
                changeEl.className = 'text-sm font-semibold mt-0.5 ' + (ch >= 0 ? 'profit' : 'loss');
            }

            if (data.high !== undefined) {
                set(prefix + '-high', (Number(data.high) || 0).toLocaleString('en-IN', {minimumFractionDigits:2, maximumFractionDigits:2}));
            }
            if (data.low !== undefined) {
                set(prefix + '-low',  (Number(data.low)  || 0).toLocaleString('en-IN', {minimumFractionDigits:2, maximumFractionDigits:2}));
            }
            if (data.volume !== undefined) {
                set(prefix + '-volume', formatNumber(data.volume || 0));
            }

            // Prediction Pill
            const predEl = el(prefix + '-prediction');
            if (predEl && data.prediction) {
                predEl.textContent = data.prediction;
                predEl.className = 'text-[0.65rem] font-bold px-2 py-0.5 rounded-full mt-1 inline-block ' + 
                    (data.prediction === 'UP' ? 'pill-up' : data.prediction === 'DOWN' ? 'pill-down' : 'pill-hold');
            }

            // Time — handle both `updated` and `timestamp` keys
            const timeVal = data.updated || data.timestamp || '';
            const timeEl = el(prefix + '-time');
            if (timeEl && timeVal) timeEl.textContent = timeVal;
        }

        /* ═══════════════════ UTILITIES ═══════════════════ */
        function formatNumber(n) {
            n = Number(n) || 0;
            if (n >= 1e7)  return (n / 1e7).toFixed(1) + ' Cr';
            if (n >= 1e5)  return (n / 1e5).toFixed(1) + ' L';
            if (n >= 1e3)  return (n / 1e3).toFixed(1) + ' K';
            return n.toString();
        }

        function updateTime() {
            const el = document.getElementById('current-time');
            if (el) el.textContent = new Date().toLocaleTimeString('en-IN', {hour:'2-digit', minute:'2-digit', hour12:true});
        }

        function updateMarketStatus() {
            apiFetch('/api/market-status').then(r=>r.json()).then(d => {
                const statusEl = document.getElementById('market-status');
                const textEl = document.getElementById('market-status-text');
                if (textEl) textEl.textContent = d.status_display || 'Market Status';
                canRefresh = d.can_refresh !== false;
                canAnalyze = d.can_analyze !== false;
                const refreshBtn = document.getElementById('refresh-btn');
                const aiBtn = document.getElementById('ai-btn');
                if (refreshBtn) refreshBtn.disabled = !canRefresh;
                if (aiBtn) aiBtn.disabled = !canAnalyze;
                if (statusEl) {
                    statusEl.className = (d.status === 'open' ? 'pill-up' : 'pill-hold') + ' px-3 py-1 rounded-full text-xs font-bold';
                }
            }).catch(() => {});
        }

        function refreshData() {
            loadInitialData();
            showToast('Refreshing market data…', 'info');
        }

        function showToast(msg, type) {
            document.querySelectorAll('.toast').forEach(t => t.remove());
            const t = document.createElement('div');
            t.className = 'toast toast-' + (type || 'info');
            t.innerHTML = '<i class="fas ' + (type==='error'?'fa-circle-exclamation':type==='success'?'fa-circle-check':'fa-circle-info') + ' mr-2"></i>' + msg;
            document.body.appendChild(t);
            setTimeout(() => t.remove(), 3500);
        }

        /* ═══════════════════ HISTORICAL DATA ═══════════════════ */
        async function loadHistoricalData() {
            const sel = document.getElementById('historical-symbol-select');
            const sym = sel ? sel.value : '';
            const container = document.getElementById('historical-data-container');
            if (!sym) {
                container.innerHTML = '<div class="text-center py-12 text-gray-600"><i class="fas fa-clock-rotate-left text-3xl mb-3 opacity-40"></i><p class="text-sm">Select an index to view historical closing values</p></div>';
                return;
            }
            container.innerHTML = '<div class="text-center py-10"><div class="skeleton" style="width:100%;height:200px;"></div></div>';
            try {
                const r = await apiFetch('/api/historical-data/' + sym);
                const data = await r.json();
                displayHistoricalData(data, sym);
            } catch(e) {
                container.innerHTML = '<div class="text-center py-10 text-gray-600"><i class="fas fa-triangle-exclamation text-3xl mb-3 opacity-40"></i><p class="text-sm">Unable to load historical data. Please try again.</p></div>';
            }
        }

        function displayHistoricalData(data, symbol) {
            const container = document.getElementById('historical-data-container');
            if (!data || !data.length) {
                container.innerHTML = '<div class="text-center py-10 text-gray-600"><i class="fas fa-circle-info text-3xl mb-3 opacity-40"></i><p class="text-sm">No historical data available for ' + symbol.replace('_',' ') + '</p></div>';
                return;
            }
            let html = '<div class="overflow-x-auto"><table class="data-table"><thead><tr>';
            ['Date','Day','Close','Change','Change %','High','Low','Volume'].forEach(h => { html += '<th>' + h + '</th>'; });
            html += '</tr></thead><tbody>';
            data.forEach(item => {
                const cls = (item.change||0) >= 0 ? 'profit' : 'loss';
                const arrow = (item.change||0) >= 0 ? '▲' : '▼';
                const opac = item.is_weekend ? ' style="opacity:0.4"' : '';
                html += '<tr' + opac + '>'
                    + '<td class="font-medium">' + (item.date||'') + '</td>'
                    + '<td>' + (item.day||'') + '</td>'
                    + '<td class="font-bold">' + (item.close||0).toFixed(2) + '</td>'
                    + '<td class="' + cls + ' font-medium">' + arrow + ' ' + Math.abs(item.change||0).toFixed(2) + '</td>'
                    + '<td class="' + cls + ' font-medium">' + arrow + ' ' + Math.abs(item.change_percent||0).toFixed(2) + '%</td>'
                    + '<td>' + (item.high||0).toFixed(2) + '</td>'
                    + '<td>' + (item.low||0).toFixed(2) + '</td>'
                    + '<td>' + formatNumber(item.volume||0) + '</td>'
                    + '</tr>';
            });
            html += '</tbody></table></div>';
            container.innerHTML = html;
        }

        /* ═══════════════════ CANDLESTICK CHART ═══════════════════ */
        function switchChartSymbol() {
            const sel = document.getElementById('chart-symbol-select');
            const sym = sel ? sel.value : '';
            if (!sym) {
                document.getElementById('live-chart').style.display = 'none';
                document.getElementById('chart-container').style.display = 'flex';
                document.getElementById('chart-info').textContent = 'Select a symbol';
                return;
            }
            currentChartSymbol = sym;
            loadCandleData(sym, currentTimeframe);
        }

        function setTimeframe(tf) {
            currentTimeframe = tf;
            // Update pill active state
            document.querySelectorAll('.tf-pill').forEach(p => {
                p.classList.toggle('tf-active', p.dataset.tf === tf);
            });
            if (currentChartSymbol) loadCandleData(currentChartSymbol, tf);
        }

        async function loadCandleData(symbol, timeframe) {
            // Show loading skeleton
            const container = document.getElementById('chart-container');
            const chart = document.getElementById('live-chart');
            container.style.display = 'flex';
            container.innerHTML = '<div class="text-center"><div class="skeleton" style="width:100%;height:400px;"></div></div>';
            chart.style.display = 'none';

            try {
                const r = await apiFetch('/api/candle-data/' + symbol + '/' + timeframe);
                const data = await r.json();
                container.style.display = 'none';
                chart.style.display = 'block';
                lastChartData = data;
                if (typeof Plotly !== 'undefined') {
                    renderCandlestick(data);
                } else {
                    console.warn('Plotly not loaded yet, waiting...');
                    var plotlyWait = setInterval(function() {
                        if (typeof Plotly !== 'undefined') {
                            clearInterval(plotlyWait);
                            renderCandlestick(data);
                        }
                    }, 1000);
                }
                const info = document.getElementById('chart-info');
                if (info) info.textContent = (data.display_name||symbol) + ' · ' + (data.timeframe_label||timeframe) + ' · ' + (data.data_points||0) + ' candles';
            } catch(e) {
                console.error('Candle load failed:', e);
                container.innerHTML = '<div class="text-center text-gray-600"><i class="fas fa-triangle-exclamation text-2xl mb-2 opacity-40"></i><p class="text-sm">Chart data unavailable. Retrying…</p></div>';
                // Auto-retry once after 3s
                setTimeout(() => loadCandleData(symbol, timeframe), 3000);
            }
        }

        function setChartType(type) {
            currentChartType = type;
            const btnCandle = document.getElementById('btn-chart-candle');
            const btnGraph = document.getElementById('btn-chart-graph');
            if (btnCandle && btnGraph) {
                if (type === 'candle') {
                    btnCandle.classList.add('tf-active');
                    btnGraph.classList.remove('tf-active');
                } else {
                    btnCandle.classList.remove('tf-active');
                    btnGraph.classList.add('tf-active');
                }
            }
            if (lastChartData) {
                renderCandlestick(lastChartData);
            }
        }

        function renderCandlestick(cd) {
            /* ── Groww-style ultra-clean candlestick chart ── */
            const datesX = cd.hover_dates || cd.dates;
            
            // Compute ticks to prevent overlapping while showing more dates
            const N = cd.dates.length;
            const step = Math.max(1, Math.ceil(N / 12)); // Target ~12 tick labels
            const tickvals = [];
            const ticktext = [];
            for (let i = 0; i < N; i += step) {
                tickvals.push(datesX[i]);
                ticktext.push(cd.dates[i]);
            }
            if (N > 0 && tickvals[tickvals.length - 1] !== datesX[N - 1]) {
                tickvals.push(datesX[N - 1]);
                ticktext.push(cd.dates[N - 1]);
            }

            let mainTrace;
            if (currentChartType === 'graph') {
                mainTrace = {
                    x: datesX,
                    y: cd.close,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Price',
                    line: { color: '#00d09c', width: 2 },
                    hovertemplate: 'Price: ₹%{y:.2f}<extra></extra>'
                };
            } else {
                mainTrace = {
                    x: datesX,
                    open:  cd.open,
                    high:  cd.high,
                    low:   cd.low,
                    close: cd.close,
                    type: 'candlestick',
                    name: 'Price',
                    increasing: {
                        line: { color: '#00d09c', width: 1.5 },
                        fillcolor: '#00d09c',
                    },
                    decreasing: {
                        line: { color: '#eb5b3c', width: 1.5 },
                        fillcolor: '#eb5b3c',
                    },
                    whiskerwidth: 0, /* Removes the horizontal caps on wicks for a clean look */
                    hovertemplate: 
                        'Open:  ₹%{open:.2f}<br>' +
                        'High:  ₹%{high:.2f}<br>' +
                        'Low:   ₹%{low:.2f}<br>' +
                        'Close: ₹%{close:.2f}<extra></extra>',
                };
            }

            /* Volume bars — Solid muted colors sitting at the very bottom */
            const volColors = cd.close.map((c, i) =>
                c >= (cd.open[i] || c)
                    ? 'rgba(0, 208, 156, 0.25)'   /* muted green */
                    : 'rgba(235, 91, 60, 0.25)'    /* muted red */
            );
            const volumeTrace = {
                x: datesX,
                y: cd.volume,
                type: 'bar',
                name: 'Volume',
                marker: {
                    color: volColors,
                    line: { width: 0 },
                },
                yaxis: 'y2',
                hovertemplate: 'Volume: %{y:,}<extra></extra>',
            };

            const layout = {
                paper_bgcolor: 'transparent',
                plot_bgcolor:  'transparent',
                font: { color: '#9ca3af', family: 'Inter, sans-serif', size: 10 },
                xaxis: {
                    title: '',
                    showgrid: false, /* No vertical gridlines (Groww style) */
                    showline: false,
                    zeroline: false,
                    tickmode: 'array',
                    tickvals: tickvals,
                    ticktext: ticktext,
                    tickangle: 0, /* Straight labels, no rotation */
                    tickfont: { size: 10, color: '#6b7280' },
                    rangeslider: { visible: false },
                    type: 'category',
                    showspikes: true,
                    spikemode: 'across',
                    spikesnap: 'cursor',
                    spikethickness: 1,
                    spikedash: 'solid',
                    spikecolor: 'rgba(255,255,255,0.15)',
                },
                yaxis: {
                    title: '',
                    gridcolor: 'rgba(255,255,255,0.03)', /* Very faint horizontal lines */
                    showline: false,
                    zeroline: false,
                    tickfont: { size: 10, color: '#9ca3af' },
                    side: 'right',
                    tickformat: ',.2f',
                    showspikes: true,
                    spikemode: 'across',
                    spikesnap: 'cursor',
                    spikethickness: 1,
                    spikedash: 'solid',
                    spikecolor: 'rgba(255,255,255,0.15)',
                },
                yaxis2: {
                    overlaying: 'y',
                    side: 'left',
                    showgrid: false,
                    showticklabels: false,
                    showline: false,
                    zeroline: false,
                    range: [0, Math.max(...(cd.volume || [1])) * 6], /* Squeeze volume to the bottom 15% */
                },
                margin: { t: 15, r: 45, b: 25, l: 5 }, /* Extremely tight margins */
                showlegend: false,
                dragmode: 'pan',
                hovermode: 'x unified',
                hoverlabel: {
                    bgcolor: 'rgba(22, 27, 34, 0.95)',
                    bordercolor: 'rgba(255,255,255,0.05)',
                    font: { color: '#e5e7eb', family: 'Inter, sans-serif', size: 12 },
                },
            };

            const traces = [mainTrace, volumeTrace];

            Plotly.newPlot('live-chart', traces, layout, {
                displayModeBar: false,
                responsive: true,
                scrollZoom: true,
            });
        }


        /* ═══════════════════ AI ANALYSIS MODAL ═══════════════════ */
        function openAIModal() {
            showSymbolSelection();
        }
        function closeAIModal() {
            document.getElementById('aiModal').classList.remove('active');
        }
        // Close on overlay click
        document.addEventListener('click', e => {
            const modal = document.getElementById('aiModal');
            if (e.target === modal) closeAIModal();
        });

        function showSymbolSelection() {
            const modal = document.getElementById('aiModal');
            const content = document.getElementById('ai-analysis-content');
            content.innerHTML = `
                <div class="text-center mb-6">
                    <h3 class="text-lg font-bold mb-2">Select Index for Analysis</h3>
                    <p class="text-xs text-gray-500">AI-powered technical analysis with predictions</p>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
                    <button onclick="selectSymbol('NIFTY_50')" class="glass-card card-blue p-4 text-center cursor-pointer hover:scale-105 transition-transform" style="border:1px solid rgba(88,166,255,0.2)">
                        <div class="text-lg font-bold" style="color:var(--accent-blue)">NIFTY 50</div>
                        <div class="text-[0.7rem] text-gray-500 mt-1">NSE Index</div>
                    </button>
                    <button onclick="selectSymbol('BANK_NIFTY')" class="glass-card card-purple p-4 text-center cursor-pointer hover:scale-105 transition-transform" style="border:1px solid rgba(188,140,255,0.2)">
                        <div class="text-lg font-bold" style="color:var(--accent-purple)">BANK NIFTY</div>
                        <div class="text-[0.7rem] text-gray-500 mt-1">NSE Banking</div>
                    </button>
                    <button onclick="selectSymbol('SENSEX')" class="glass-card card-emerald p-4 text-center cursor-pointer hover:scale-105 transition-transform" style="border:1px solid rgba(63,185,80,0.2)">
                        <div class="text-lg font-bold" style="color:var(--accent-emerald)">SENSEX</div>
                        <div class="text-[0.7rem] text-gray-500 mt-1">BSE Index</div>
                    </button>
                </div>
                <div class="text-center">
                    <button onclick="closeAIModal()" class="btn btn-ghost text-xs">Cancel</button>
                </div>
            `;
            modal.classList.add('active');
        }

        function startAIAnalysisLoader(symbol) {
            const content = document.getElementById('ai-analysis-content');
            if (!content) return;
            content.innerHTML = `
                <div class="text-center py-10 px-4">
                    <div class="animate-spin rounded-full h-10 w-10 border-2 border-transparent border-t-purple-500 mx-auto mb-6"></div>
                    <h4 class="text-sm font-bold text-gray-200 mb-4">Agentic AI is Analyzing ${symbol}</h4>
                    <div class="max-w-xs mx-auto text-left flex flex-col gap-3.5 text-xs text-gray-400">
                        <div id="step-1" class="flex items-center gap-2.5"><i class="fas fa-spinner animate-spin text-purple-400"></i> <span>Initializing RAG Agent...</span></div>
                        <div id="step-2" class="flex items-center gap-2.5 text-gray-600"><i class="far fa-circle"></i> <span>Retrieving market indicators...</span></div>
                        <div id="step-3" class="flex items-center gap-2.5 text-gray-600"><i class="far fa-circle"></i> <span>Running deep learning prediction...</span></div>
                        <div id="step-4" class="flex items-center gap-2.5 text-gray-600"><i class="far fa-circle"></i> <span>Synthesizing recommendation...</span></div>
                    </div>
                </div>
            `;
            let currentStep = 1;
            const interval = setInterval(() => {
                const prevStep = document.getElementById(`step-${currentStep}`);
                if (prevStep) {
                    prevStep.innerHTML = '<i class="fas fa-circle-check text-emerald-400"></i> <span class="text-gray-300 font-semibold">' + prevStep.querySelector('span').innerText + '</span>';
                }
                currentStep++;
                if (currentStep <= 4) {
                    const nextStep = document.getElementById(`step-${currentStep}`);
                    if (nextStep) {
                        nextStep.className = "flex items-center gap-2.5 text-gray-200";
                        nextStep.innerHTML = `<i class="fas fa-spinner animate-spin text-purple-400"></i> <span>${nextStep.querySelector('span').innerText}</span>`;
                    }
                } else {
                    clearInterval(interval);
                }
            }, 1200);
            content.dataset.loaderInterval = interval;
        }

        function selectSymbol(symbol) {
            const modal = document.getElementById('aiModal');
            modal.dataset.currentSymbol = symbol;
            startAIAnalysisLoader(symbol);

            // Use a NEW AbortController for each request (fixes reuse bug)
            const fastController = new AbortController();
            const fastTimeout = setTimeout(() => fastController.abort(), 5000);

            apiFetch('/api/ai-analysis-fast/' + symbol, {signal: fastController.signal})
                .then(r => { clearTimeout(fastTimeout); if (!r.ok) throw new Error('Fast failed'); return r.json(); })
                .then(data => {
                    if (data.error) throw new Error(data.error);
                    displayDetailedAnalysis(data);
                    // Background enhancement with SEPARATE controller
                    const bgController = new AbortController();
                    const bgTimeout = setTimeout(() => bgController.abort(), 15000);
                    apiFetch('/api/ai-analysis/' + symbol, {signal: bgController.signal})
                        .then(r => { clearTimeout(bgTimeout); return r.ok ? r.json() : null; })
                        .then(full => { if (full && !full.error && full.predictions) displayDetailedAnalysis(full); })
                        .catch(() => {});
                })
                .catch(() => {
                    clearTimeout(fastTimeout);
                    // Fallback with NEW controller
                    const fallbackController = new AbortController();
                    const fallbackTimeout = setTimeout(() => fallbackController.abort(), 15000);
                    apiFetch('/api/ai-analysis/' + symbol, {signal: fallbackController.signal})
                        .then(r => { clearTimeout(fallbackTimeout); if (!r.ok) throw new Error('Full failed'); return r.json(); })
                        .then(data => { if (data.error) throw new Error(data.error); displayDetailedAnalysis(data); })
                        .catch(() => {
                            clearTimeout(fallbackTimeout);
                            const content = document.getElementById('ai-analysis-content');
                            if(content) content.innerHTML = `<div class="text-center py-10"><div class="text-3xl mb-3">⚠️</div><p class="text-sm text-gray-400">Analysis failed. Please try again.</p><button onclick="selectSymbol('${symbol}')" class="btn btn-blue text-xs mt-4">Retry</button></div>`;
                        });
                });
        }

        function displayDetailedAnalysis(data) {
            const content = document.getElementById('ai-analysis-content');
            if (content && content.dataset.loaderInterval) {
                clearInterval(Number(content.dataset.loaderInterval));
                delete content.dataset.loaderInterval;
            }
            const p  = data.predictions || {};
            const t  = data.technical_indicators || {};
            const ai = data.ai_trading_suggestion || {};
            const mi = data.market_intelligence || {};
            const isRAG = data.rag_enhanced || false;

            // Data quality badge
            const aq = p.analysis_quality || (p.is_fallback ? 'fallback' : 'full');
            const qualityBadge = aq === 'full' ? '<span class="tag" style="background:rgba(16,185,129,0.15);color:#10b981;font-size:0.6rem;">✅ Full Analysis</span>'
                : aq === 'partial' ? '<span class="tag" style="background:rgba(234,179,8,0.15);color:#eab308;font-size:0.6rem;">📊 Partial Analysis</span>'
                : aq === 'limited' ? '<span class="tag" style="background:rgba(249,115,22,0.15);color:#f97316;font-size:0.6rem;">⚠️ Limited Data</span>'
                : aq === 'fallback' || aq === 'error' ? '<span class="tag" style="background:rgba(239,68,68,0.15);color:#ef4444;font-size:0.6rem;">❌ No Data</span>'
                : '';
            const dataPoints = p.data_points_used ? `<span class="text-gray-600" style="font-size:0.55rem;">${p.data_points_used} days analyzed</span>` : '';

            const safe = (v,d) => (v !== undefined && v !== null) ? v : (d !== undefined ? d : 0);
            const safePct = (v) => { const n = Number(v); return isNaN(n) ? '0.0' : n.toFixed(1); };
            const safeFixed = (v,d) => { const n = Number(v); return isNaN(n) ? (d||'0.00') : n.toFixed(2); };

            const recClass = (p.recommendation||'') === 'BUY CALL' ? 'profit' : (p.recommendation||'') === 'BUY PUT' ? 'loss' : 'text-gray-400';
            const recIcon = (p.recommendation||'') === 'BUY CALL' ? '🟢' : (p.recommendation||'') === 'BUY PUT' ? '🔴' : '⚪';

            const currentSymbol = document.getElementById('aiModal').dataset.currentSymbol || '';
            const showOCTab = ['NIFTY_50', 'BANK_NIFTY'].includes(currentSymbol);

            content.innerHTML = `
                ${showOCTab ? `
                <div class="oc-tabs mb-4">
                    <button class="oc-tab active" onclick="switchOCTab('analysis')">📊 Analysis</button>
                    <button class="oc-tab" onclick="switchOCTab('optionchain')">⛓️ Options Chain</button>
                </div>` : ''}
                <div id="oc-analysis-tab">
                <div>
                    <div class="flex justify-between items-center mb-5">
                        <h3 class="text-lg font-bold">${data.display_name || ''}</h3>
                        <div class="flex items-center gap-2 flex-wrap justify-end">
                            ${qualityBadge}
                            ${dataPoints}
                            ${isRAG ? '<span class="tag tag-purple">RAG Enhanced</span>' : ''}
                            <span class="tag ${(ai.option_side||'') === 'CALL' ? 'tag-emerald' : (ai.option_side||'') === 'PUT' ? 'tag-red' : 'tag-amber'}">${ai.suggestion || p.option_side || 'HOLD'}</span>
                        </div>
                    </div>

                    <!-- Current Value -->
                    <div class="p-4 rounded-xl mb-4" style="background:rgba(255,255,255,0.02);border:1px solid var(--border-subtle);">
                        <div class="text-center">
                            <div class="text-xs text-gray-500 mb-1">CURRENT VALUE</div>
                            <div class="text-3xl font-extrabold">₹${safe(p.targets?.current_price, safe(data.market_data?.price, 0))}</div>
                            <div class="text-sm font-semibold mt-1 ${safe(p.targets?.current_change_percent, safe(data.market_data?.change_percent, 0)) >= 0 ? 'profit' : 'loss'}">
                                ${safe(p.targets?.current_change_percent, safe(data.market_data?.change_percent, 0)) >= 0 ? '+' : ''}${safePct(safe(p.targets?.current_change_percent, safe(data.market_data?.change_percent, 0)))}%
                            </div>
                        </div>
                    </div>

                    <!-- Recommendation -->
                    <div class="p-4 rounded-xl mb-4" style="background:rgba(255,255,255,0.02);border:1px solid var(--border-subtle);">
                        <div class="text-xs text-gray-500 mb-2">RECOMMENDATION</div>
                        <div class="text-center">
                            <div class="text-2xl font-extrabold ${recClass}">${recIcon} ${p.recommendation || 'HOLD'}</div>
                            <div class="text-xs text-gray-500 mt-1">Confidence: ${safePct(safe(p.confidence,0.5)*100)}%</div>
                        </div>
                        <div class="mt-3 w-full rounded-full h-2" style="background:rgba(255,255,255,0.06);">
                            <div class="h-2 rounded-full" style="width:${safe(p.confidence,0.5)*100}%;background:linear-gradient(90deg,#ef4444,#eab308,#22c55e);"></div>
                        </div>
                    </div>

                    <!-- Probabilities -->
                    <div class="grid grid-cols-3 gap-2 mb-4">
                        <div class="text-center p-3 rounded-lg" style="background:rgba(16,185,129,0.06);">
                            <div class="text-xs text-gray-500">UP</div>
                            <div class="text-lg font-bold profit">${safePct(safe(p.probabilities?.increase,0))}%</div>
                        </div>
                        <div class="text-center p-3 rounded-lg" style="background:rgba(248,81,73,0.06);">
                            <div class="text-xs text-gray-500">DOWN</div>
                            <div class="text-lg font-bold loss">${safePct(safe(p.probabilities?.decrease,0))}%</div>
                        </div>
                        <div class="text-center p-3 rounded-lg" style="background:rgba(255,255,255,0.03);">
                            <div class="text-xs text-gray-500">SIDEWAYS</div>
                            <div class="text-lg font-bold text-gray-400">${safePct(safe(p.probabilities?.sideways,0))}%</div>
                        </div>
                    </div>

                    <!-- End of Day Targets -->
                    <div class="grid grid-cols-2 gap-2 mb-4">
                        <div class="p-3 rounded-lg" style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.15);">
                            <div class="text-xs text-green-500 mb-1">UPSIDE TARGET</div>
                            <div class="text-xl font-bold" style="color:var(--accent-emerald)">₹${safeFixed(safe(p.targets?.end_of_day_up,0))}</div>
                        </div>
                        <div class="p-3 rounded-lg" style="background:rgba(248,81,73,0.06);border:1px solid rgba(248,81,73,0.15);">
                            <div class="text-xs text-red-500 mb-1">DOWNSIDE TARGET</div>
                            <div class="text-xl font-bold" style="color:var(--accent-red)">₹${safeFixed(safe(p.targets?.end_of_day_down,0))}</div>
                        </div>
                    </div>

                    <!-- Technical Indicators -->
                    <div class="p-4 rounded-xl mb-4" style="background:rgba(255,255,255,0.02);border:1px solid var(--border-subtle);">
                        <div class="text-xs text-gray-500 mb-3 font-semibold">TECHNICAL INDICATORS</div>
                        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-center text-xs">
                            <div>
                                <div class="text-gray-500">Trend</div>
                                <div class="font-bold text-sm">${safe(t.market_trend, 'N/A')}</div>
                            </div>
                            <div>
                                <div class="text-gray-500">RSI (14)</div>
                                <div class="font-bold text-sm ${safe(t.rsi,50)>70?'loss':safe(t.rsi,50)<30?'profit':'text-gray-300'}">${safeFixed(safe(t.rsi,50))}</div>
                            </div>
                            <div>
                                <div class="text-gray-500">Volatility</div>
                                <div class="font-bold text-sm text-yellow-400">${safeFixed(safe(t.volatility_percent,0))}%</div>
                            </div>
                            <div>
                                <div class="text-gray-500">Support</div>
                                <div class="font-bold text-sm profit">₹${safeFixed(safe(t.support_level,0))}</div>
                            </div>
                            <div>
                                <div class="text-gray-500">Resistance</div>
                                <div class="font-bold text-sm loss">₹${safeFixed(safe(t.resistance_level,0))}</div>
                            </div>
                            <div>
                                <div class="text-gray-500">Sentiment</div>
                                <div class="font-bold text-sm">${safe(t.sentiment_score,0) > 0.3 ? '🐂 Bullish' : safe(t.sentiment_score,0) < -0.3 ? '🐻 Bearish' : '😐 Neutral'}</div>
                            </div>
                        </div>
                    </div>

                    <!-- News Sentiment Section -->
                    ${(() => {
                        const news = data.news_analysis || {};
                        const articles = news.articles || [];
                        if (articles.length === 0) return '';
                        return `
                        <div class="p-4 rounded-xl mb-4" style="background:rgba(255,255,255,0.02);border:1px solid var(--border-subtle);">
                            <div class="flex justify-between items-center mb-3">
                                <div class="text-xs text-gray-500 font-semibold">MARKET NEWS & SENTIMENT</div>
                                <span class="tag ${news.news_sentiment_label === 'Bullish' ? 'tag-emerald' : news.news_sentiment_label === 'Bearish' ? 'tag-red' : 'tag-amber'}">
                                    ${news.news_sentiment_label === 'Bullish' ? '🐂 Bullish' : news.news_sentiment_label === 'Bearish' ? '🐻 Bearish' : '😐 Neutral'} (${news.news_sentiment_score > 0 ? '+' : ''}${safePct(news.news_sentiment_score)})
                                </span>
                            </div>
                            <div class="space-y-3">
                                ${articles.map(art => `
                                    <div class="p-2.5 rounded-lg text-xs" style="background:rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03);">
                                        <div class="flex justify-between items-start gap-2 mb-1.5">
                                            <a href="${art.url}" target="_blank" class="font-semibold text-blue-400 hover:text-blue-300 transition-colors leading-tight" style="word-break: break-word; text-align: left; display: block;">
                                                ${art.title}
                                            </a>
                                            <span class="px-1.5 py-0.5 rounded text-[0.6rem] font-bold shrink-0 ${art.label === 'Bullish' ? 'bg-emerald-500/10 text-emerald-400' : art.label === 'Bearish' ? 'bg-red-500/10 text-red-400' : 'bg-gray-500/10 text-gray-400'}">
                                                ${art.label}
                                            </span>
                                        </div>
                                        <div class="text-[0.65rem] text-gray-500 flex justify-between">
                                            <span>${art.source}</span>
                                            <span>${art.published_at}</span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        `;
                    })()}

                    ${ai.reasoning && ai.reasoning.length > 0 ? `
                    <div class="p-4 rounded-xl mb-4" style="background:rgba(139,92,246,0.04);border:1px solid rgba(139,92,246,0.12);">
                        <div class="text-xs text-purple-400 mb-2 font-semibold">AI REASONING</div>
                        <ul class="text-xs text-gray-400 space-y-1">${ai.reasoning.slice(0,4).map(r => '<li>• ' + r + '</li>').join('')}</ul>
                    </div>
                    ` : ''}

                    ${data.key_points && data.key_points.length > 0 ? `
                    <div class="p-4 rounded-xl mb-4" style="background:rgba(255,255,255,0.02);border:1px solid var(--border-subtle);">
                        <div class="text-xs text-gray-500 mb-2 font-semibold">KEY POINTS</div>
                        <ul class="text-xs text-gray-400 space-y-1">${data.key_points.slice(0,5).map(p => '<li>• ' + p + '</li>').join('')}</ul>
                    </div>
                    ` : ''}

                    ${data.risk_factors && data.risk_factors.length > 0 ? `
                    <div class="p-4 rounded-xl mb-4" style="background:rgba(248,81,73,0.04);border:1px solid rgba(248,81,73,0.12);">
                        <div class="text-xs text-red-400 mb-2 font-semibold">⚠️ RISK FACTORS</div>
                        <ul class="text-xs text-gray-400 space-y-1">${data.risk_factors.slice(0,3).map(r => '<li>• ' + r + '</li>').join('')}</ul>
                    </div>
                    ` : ''}
                    <div class="text-[0.65rem] text-gray-600 pt-2" style="border-top:1px solid var(--border-subtle);">
                        <i class="far fa-clock mr-1"></i>
                        ${data.timestamp ? new Date(data.timestamp).toLocaleString('en-IN') : ''}
                        ${isRAG ? ' · Powered by RAG' : ''}
                    </div>
                </div> <!-- Closes the inner div -->
                </div><!-- end oc-analysis-tab -->
                ${showOCTab ? `<div id="oc-chain-tab" style="display:none;"></div>` : ''}
            `;
        }

        /* ═══════════════════ OPTIONS CHAIN ═══════════════════ */
        function switchOCTab(tab) {
            const tabs = document.querySelectorAll('.oc-tab');
            tabs.forEach((t, i) => {
                t.classList.toggle('active', (tab === 'analysis' && i === 0) || (tab === 'optionchain' && i === 1));
            });
            const analysisTab = document.getElementById('oc-analysis-tab');
            const chainTab = document.getElementById('oc-chain-tab');
            if (analysisTab) analysisTab.style.display = tab === 'analysis' ? '' : 'none';
            if (chainTab) {
                chainTab.style.display = tab === 'optionchain' ? '' : 'none';
                if (tab === 'optionchain' && !chainTab.dataset.loaded) {
                    const symbol = document.getElementById('aiModal').dataset.currentSymbol;
                    loadOptionsChain(symbol);
                }
            }
        }

        function loadOptionsChain(symbol, expiry) {
            const chainTab = document.getElementById('oc-chain-tab');
            if (!chainTab) return;
            chainTab.innerHTML = `
                <div class="text-center py-8">
                    <div class="animate-spin rounded-full h-8 w-8 border-2 border-transparent border-t-emerald-500 mx-auto mb-3"></div>
                    <p class="text-xs text-gray-500">Loading options chain...</p>
                </div>`;
            const url = expiry ? `/api/options-chain/${symbol}/${expiry}` : `/api/options-chain/${symbol}`;
            apiFetch(url)
                .then(r => r.json())
                .then(data => {
                    if (data.error) throw new Error(data.error);
                    chainTab.dataset.loaded = '1';
                    renderOptionsChain(chainTab, data);
                })
                .catch(err => {
                    chainTab.innerHTML = `<div class="text-center py-8"><div class="text-2xl mb-2">⚠️</div><p class="text-xs text-gray-400">${err.message || 'Failed to load options chain'}</p><button onclick="loadOptionsChain('${symbol}')" class="btn btn-blue text-xs mt-3">Retry</button></div>`;
                });
        }

        function renderOptionsChain(container, data) {
            const chain = data.chain || [];
            const expiryDates = data.expiry_dates || [];
            const selectedExpiry = data.selected_expiry || '';
            const currentPrice = data.current_price || 0;
            const atmStrike = data.atm_strike || 0;
            const maxOI = Math.max(...chain.map(c => Math.max(c.call_oi || 0, c.put_oi || 0)), 1);
            const symbol = data.symbol || '';

            // Format expiry date for display
            const fmtExpiry = (d) => {
                const dt = new Date(d + 'T00:00:00');
                return dt.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' });
            };
            const fmtExpiryFull = (d) => {
                const dt = new Date(d + 'T00:00:00');
                return dt.toLocaleDateString('en-IN', { day: '2-digit', month: 'long' });
            };

            container.innerHTML = `
                <div style="position:relative;">
                    <!-- Header -->
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h3 class="text-sm font-bold">${(symbol || '').replace('_', ' ')} Options</h3>
                            <div class="text-[0.65rem] text-gray-500 mt-0.5">Current: ₹${Number(currentPrice).toLocaleString('en-IN', {minimumFractionDigits:2})}</div>
                        </div>
                        <div style="position:relative;" id="oc-expiry-wrapper">
                            <button class="oc-expiry-btn" onclick="toggleExpirySheet()">
                                <i class="far fa-calendar"></i>
                                <span id="oc-selected-expiry">${fmtExpiry(selectedExpiry)}</span>
                                <i class="fas fa-chevron-down" style="font-size:0.6rem;"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Expiry Bottom Sheet (hidden by default) -->
                    <div id="oc-expiry-sheet" class="oc-expiry-sheet" style="display:none;position:fixed;bottom:0;left:0;right:0;top:auto;border-radius:20px 20px 0 0;max-height:50vh;overflow-y:auto;z-index:100;">
                        <div style="width:40px;height:4px;background:rgba(255,255,255,0.15);border-radius:4px;margin:0 auto 16px;"></div>
                        <h4 class="text-sm font-bold mb-3">Select expiry date</h4>
                        ${expiryDates.map(d => `
                            <div class="oc-expiry-option ${d === selectedExpiry ? 'selected' : ''}" onclick="selectExpiry('${symbol}', '${d}')">
                                <div class="oc-expiry-radio"></div>
                                <span>${fmtExpiryFull(d)}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Options Chain Table -->
                <div style="max-height:400px;overflow-y:auto;border-radius:12px;border:1px solid rgba(255,255,255,0.06);" id="oc-table-scroll">
                    <table class="oc-table">
                        <thead>
                            <tr>
                                <th class="call-col" style="width:35%;color:#10b981;">Calls (Buy if UP 🟢)</th>
                                <th style="width:30%;text-align:center;">Strike</th>
                                <th class="put-col" style="width:35%;color:#ef4444;">Puts (Buy if DOWN 🔴)</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${chain.map(row => {
                                const isATM = row.strike === atmStrike;
                                const isITMCall = row.strike < currentPrice;
                                const isITMPut = row.strike > currentPrice;
                                const callOIWidth = Math.round((row.call_oi / maxOI) * 100);
                                const putOIWidth = Math.round((row.put_oi / maxOI) * 100);
                                return `
                                <tr class="${isATM ? 'atm-row' : ''} ${isITMCall ? 'itm-call' : ''}" ${isATM ? 'id="oc-atm-row"' : ''}>
                                    <td class="call-col">
                                        <div class="font-semibold" style="color:${row.call_change >= 0 ? '#10b981' : '#ef4444'}">₹${Number(row.call_price).toFixed(2)}</div>
                                        <div style="font-size:0.6rem;color:${row.call_change >= 0 ? '#10b981' : '#ef4444'};opacity:0.8;">${row.call_change >= 0 ? '+' : ''}${Number(row.call_change).toFixed(2)}%</div>
                                        <div class="oc-oi-bar" style="width:${callOIWidth}%;background:${isITMCall ? 'rgba(16,185,129,0.4)' : 'rgba(239,68,68,0.3)'};"></div>
                                    </td>
                                    <td class="strike-col">
                                        <div>${Number(row.strike).toLocaleString('en-IN')}</div>
                                        ${isATM ? '<div style="font-size:0.55rem;color:#eab308;margin-top:2px;">◀ ATM ▶</div>' : ''}
                                    </td>
                                    <td class="put-col">
                                        <div class="font-semibold" style="color:${row.put_change >= 0 ? '#10b981' : '#ef4444'}">₹${Number(row.put_price).toFixed(2)}</div>
                                        <div style="font-size:0.6rem;color:${row.put_change >= 0 ? '#10b981' : '#ef4444'};opacity:0.8;">${row.put_change >= 0 ? '+' : ''}${Number(row.put_change).toFixed(2)}%</div>
                                        <div class="oc-oi-bar" style="width:${putOIWidth}%;background:${isITMPut ? 'rgba(16,185,129,0.4)' : 'rgba(239,68,68,0.3)'};margin-left:auto;"></div>
                                    </td>
                                </tr>`;
                            }).join('')}
                        </tbody>
                    </table>
                </div>

                <!-- ATM Price Indicator -->
                <div class="flex justify-center mt-3 mb-4">
                    <div class="text-[0.65rem] text-gray-500 px-3 py-1.5 rounded-full" style="background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.15);">
                        ${Number(currentPrice).toLocaleString('en-IN', {minimumFractionDigits:2})} | ATM Strike: ${Number(atmStrike).toLocaleString('en-IN')}
                    </div>
                </div>

                <!-- Color Legend -->
                <div class="oc-legend">
                    <button class="oc-legend-toggle" onclick="toggleOCLegend(this)">
                        <i class="fas fa-circle-info" style="color:#10b981;"></i>
                        <span>💡 What do these colors mean?</span>
                        <i class="fas fa-chevron-down" style="margin-left:auto;font-size:0.6rem;transition:transform 0.3s;"></i>
                    </button>
                    <div class="oc-legend-body">
                        <div class="text-[0.7rem] font-semibold text-gray-300 mb-2">Color Guide</div>
                        <div class="oc-legend-item">
                            <div class="oc-legend-dot" style="background:#10b981;"></div>
                            <div><span class="text-gray-200 font-semibold">Green Price/% </span>— Price went UP today. Buyers are making profit.</div>
                        </div>
                        <div class="oc-legend-item">
                            <div class="oc-legend-dot" style="background:#ef4444;"></div>
                            <div><span class="text-gray-200 font-semibold">Red Price/% </span>— Price went DOWN today. Value decreased.</div>
                        </div>
                        <div class="oc-legend-item">
                            <div class="oc-legend-dot" style="background:#eab308;"></div>
                            <div><span class="text-gray-200 font-semibold">Yellow Row </span>— ATM (At The Money) — Strike closest to current market price.</div>
                        </div>
                        <div class="oc-legend-item">
                            <div class="oc-legend-dot" style="background:rgba(16,185,129,0.3);"></div>
                            <div><span class="text-gray-200 font-semibold">Green Tint Rows </span>— ITM (In The Money) — These options already have real value.</div>
                        </div>

                        <div style="border-top:1px solid rgba(255,255,255,0.06);margin:10px 0;"></div>
                        <div class="text-[0.7rem] font-semibold text-gray-300 mb-2">Quick Glossary</div>
                        <div class="oc-legend-item">
                            <span>📗</span>
                            <div><span class="text-gray-200 font-semibold">Call Option (Green)</span> — Buy this if you expect the price to **GO UP**. You profit if the market rises above your strike price.</div>
                        </div>
                        <div class="oc-legend-item">
                            <span>📕</span>
                            <div><span class="text-gray-200 font-semibold">Put Option (Red)</span> — Buy this if you expect the price to **GO DOWN**. You profit if the market falls below your strike price.</div>
                        </div>
                        <div class="oc-legend-item">
                            <span>🎯</span>
                            <div><span class="text-gray-200 font-semibold">Strike Price</span> — The target price level you're betting on.</div>
                        </div>
                        <div class="oc-legend-item">
                            <span>📅</span>
                            <div><span class="text-gray-200 font-semibold">Expiry Date</span> — Deadline for your option. After this, it expires worthless if not profitable.</div>
                        </div>
                        <div class="oc-legend-item">
                            <span>📊</span>
                            <div><span class="text-gray-200 font-semibold">OI (Open Interest)</span> — Number of active contracts. Higher = more popular & liquid.</div>
                        </div>
                        <div class="oc-legend-item">
                            <span>💰</span>
                            <div><span class="text-gray-200 font-semibold">Premium (Price)</span> — Cost to buy the option. This is your maximum risk.</div>
                        </div>
                    </div>
                </div>
            `;

            // Scroll to ATM row
            setTimeout(() => {
                const atmRow = document.getElementById('oc-atm-row');
                const scrollContainer = document.getElementById('oc-table-scroll');
                if (atmRow && scrollContainer) {
                    const offset = atmRow.offsetTop - scrollContainer.offsetTop - (scrollContainer.clientHeight / 2) + (atmRow.clientHeight / 2);
                    scrollContainer.scrollTop = offset;
                }
            }, 100);
        }

        function toggleExpirySheet() {
            const sheet = document.getElementById('oc-expiry-sheet');
            if (sheet) sheet.style.display = sheet.style.display === 'none' ? '' : 'none';
        }

        function selectExpiry(symbol, expiry) {
            const sheet = document.getElementById('oc-expiry-sheet');
            if (sheet) sheet.style.display = 'none';
            const chainTab = document.getElementById('oc-chain-tab');
            if (chainTab) chainTab.dataset.loaded = '';
            loadOptionsChain(symbol, expiry);
        }

        function toggleOCLegend(btn) {
            const body = btn.nextElementSibling;
            const icon = btn.querySelector('.fa-chevron-down');
            body.classList.toggle('open');
            if (icon) icon.classList.toggle('rotate');
        }

        // Close expiry sheet on outside click
        document.addEventListener('click', (e) => {
            const sheet = document.getElementById('oc-expiry-sheet');
            const wrapper = document.getElementById('oc-expiry-wrapper');
            if (sheet && sheet.style.display !== 'none' && wrapper && !wrapper.contains(e.target) && !sheet.contains(e.target)) {
                sheet.style.display = 'none';
            }
        });

        // Cleanup
        window.addEventListener('beforeunload', () => {
            // Cleanup WebSocket before leaving
            if (socket) socket.disconnect();
        });

        /* ═══════════════════ AUTH MODAL & SESSION JS ═══════════════════ */
        const currentUser = window.__IS_LOGGED_IN__
            ? { id: window.__CURRENT_USER__.id, username: window.__CURRENT_USER__.username, cash: 1000000.0 }
            : { id: 'guest', username: 'Guest', cash: 0 };

        function openAuthModal() {
            document.getElementById('authModal').classList.add('active');
            switchAuthTab('login');
        }
        function closeAuthModal() {
            document.getElementById('authModal').classList.remove('active');
            // Clear forms
            ['login-error', 'register-error'].forEach(id => { const el = document.getElementById(id); if(el) { el.style.display='none'; el.textContent=''; } });
        }
        function switchAuthTab(tab) {
            const loginTab = document.getElementById('tab-auth-login');
            const registerTab = document.getElementById('tab-auth-register');
            const loginForm = document.getElementById('auth-login-form');
            const registerForm = document.getElementById('auth-register-form');
            if (tab === 'login') {
                loginTab.className = 'flex-1 py-2 rounded-lg text-sm font-semibold transition-all duration-200 bg-gradient-to-r from-emerald-600/80 to-teal-600/80 text-white';
                registerTab.className = 'flex-1 py-2 rounded-lg text-sm font-semibold transition-all duration-200 text-gray-400 hover:text-white';
                loginForm.style.display = 'block';
                registerForm.style.display = 'none';
            } else {
                registerTab.className = 'flex-1 py-2 rounded-lg text-sm font-semibold transition-all duration-200 bg-gradient-to-r from-emerald-600/80 to-teal-600/80 text-white';
                loginTab.className = 'flex-1 py-2 rounded-lg text-sm font-semibold transition-all duration-200 text-gray-400 hover:text-white';
                loginForm.style.display = 'none';
                registerForm.style.display = 'block';
            }
        }
        function togglePasswordVisibility(inputId, btn) {
            const inp = document.getElementById(inputId);
            const icon = btn.querySelector('i');
            if (inp.type === 'password') {
                inp.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                inp.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        }
        // Password strength meter
        (function() {
            const pw = document.getElementById('reg-password');
            if (!pw) return;
            pw.addEventListener('input', function() {
                const val = this.value;
                const meter = document.getElementById('password-strength');
                const fill = document.getElementById('pw-strength-fill');
                const text = document.getElementById('pw-strength-text');
                if (!val) { meter.style.display = 'none'; return; }
                meter.style.display = 'block';
                let score = 0;
                if (val.length >= 8) score++;
                if (val.length >= 12) score++;
                if (/[A-Z]/.test(val)) score++;
                if (/[0-9]/.test(val)) score++;
                if (/[^A-Za-z0-9]/.test(val)) score++;
                const pct = Math.min(100, score * 20);
                fill.style.width = pct + '%';
                fill.className = 'confidence-fill ' + (pct >= 80 ? 'high' : pct >= 50 ? 'medium' : 'low');
                text.textContent = pct >= 80 ? 'Strong password' : pct >= 50 ? 'Moderate password' : 'Weak password';
            });
        })();
        async function submitLogin(e) {
            e.preventDefault();
            const errEl = document.getElementById('login-error');
            const btn = document.getElementById('login-submit-btn');
            errEl.style.display = 'none';
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Signing in…';
            try {
                const resp = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        username: document.getElementById('login-username').value.trim(),
                        password: document.getElementById('login-password').value
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    showToast(data.message || 'Welcome back!', 'success');
                    closeAuthModal();
                    setTimeout(() => location.reload(), 600);
                } else {
                    errEl.textContent = data.message || 'Login failed';
                    errEl.style.display = 'block';
                }
            } catch (err) {
                errEl.textContent = 'Network error. Please try again.';
                errEl.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-right-to-bracket mr-2"></i>Sign In';
            }
        }
        async function submitRegister(e) {
            e.preventDefault();
            const errEl = document.getElementById('register-error');
            const btn = document.getElementById('register-submit-btn');
            const pw = document.getElementById('reg-password').value;
            const cpw = document.getElementById('reg-confirm-password').value;
            errEl.style.display = 'none';
            if (pw !== cpw) {
                errEl.textContent = 'Passwords do not match';
                errEl.style.display = 'block';
                return;
            }
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Creating account…';
            try {
                const resp = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        username: document.getElementById('reg-username').value.trim(),
                        email: document.getElementById('reg-email').value.trim(),
                        password: pw
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    showToast(data.message || 'Account created!', 'success');
                    closeAuthModal();
                    setTimeout(() => location.reload(), 600);
                } else {
                    errEl.textContent = data.message || 'Registration failed';
                    errEl.style.display = 'block';
                }
            } catch (err) {
                errEl.textContent = 'Network error. Please try again.';
                errEl.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-user-plus mr-2"></i>Create Account';
            }
        }
        async function doLogout() {
            try {
                await fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' });
                showToast('Signed out successfully', 'info');
                setTimeout(() => location.reload(), 600);
            } catch (err) {
                showToast('Logout failed', 'error');
            }
        }
        // Close auth modal on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const authModal = document.getElementById('authModal');
                if (authModal && authModal.classList.contains('active')) closeAuthModal();
            }
        });

        // Stub for optional trade symbol dropdown (may not exist in all pages)
        function updateTradeSymbolDropdown() {
            try {
                const sel = document.getElementById('trade-symbol-select');
                if (!sel) return;
                const symbols = window.__INDIAN_STOCKS_CONFIG__ ? Object.keys(window.__INDIAN_STOCKS_CONFIG__) : [];
                if (symbols.length > 0) {
                    sel.innerHTML = symbols.map(s => `<option value="${s}">${s}</option>`).join('');
                }
            } catch(e) { /* optional UI element */ }
        }
        

    </script>
</body>
</html>
"""

LOGIN_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In — Stock Market Prediction</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">

    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0f0d;
            color: #1a1a2e;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }

        /* ── Ambient floating blobs behind everything ── */
        body::before, body::after {
            content: ''; position: absolute; border-radius: 50%;
            pointer-events: none; z-index: 0; filter: blur(160px); opacity: 0.12;
        }
        body::before { width: 500px; height: 500px; background: #059669; top: -5%; left: -5%; animation: ambientFloat 14s ease-in-out infinite; }
        body::after  { width: 420px; height: 420px; background: #0d9488; bottom: -5%; right: -5%; animation: ambientFloat 16s ease-in-out infinite alternate; }

        @keyframes ambientFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50%      { transform: translateY(-30px) scale(1.08); }
        }

        /* ── Main container: two panels ── */
        .login-wrapper {
            display: flex;
            width: 900px;
            max-width: 95vw;
            min-height: 600px;
            border-radius: 32px;
            overflow: hidden;
            box-shadow:
                0 30px 80px rgba(0,0,0,0.6),
                0 0 0 1px rgba(255,255,255,0.04);
            z-index: 10;
            position: relative;
        }

        /* ── LEFT PANEL — Green gradient splash ── */
        .splash-panel {
            flex: 1;
            background: linear-gradient(135deg, #059669 0%, #10b981 35%, #34d399 65%, #2dd4bf 100%);
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 48px 40px;
            overflow: hidden;
        }

        /* Diagonal decorative lines */
        .splash-panel::before {
            content: '';
            position: absolute;
            top: -60%;
            left: -20%;
            width: 160%;
            height: 200%;
            background: repeating-linear-gradient(
                -35deg,
                transparent,
                transparent 80px,
                rgba(255,255,255,0.06) 80px,
                rgba(255,255,255,0.06) 82px
            );
            pointer-events: none;
            animation: slideLines 20s linear infinite;
        }
        @keyframes slideLines {
            0%   { transform: translateX(0) translateY(0); }
            100% { transform: translateX(80px) translateY(80px); }
        }

        /* Additional accent line */
        .splash-panel::after {
            content: '';
            position: absolute;
            top: 15%;
            left: -10%;
            width: 120%;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
            transform: rotate(-35deg);
            pointer-events: none;
        }

        .splash-logo {
            width: 100px;
            height: 100px;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(12px);
            border-radius: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 28px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
            position: relative;
            z-index: 2;
        }
        .splash-logo i {
            font-size: 44px;
            color: #fff;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.15));
        }

        .splash-title {
            font-size: 2rem;
            font-weight: 900;
            color: #fff;
            text-align: center;
            line-height: 1.2;
            letter-spacing: -0.02em;
            position: relative;
            z-index: 2;
            text-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        .splash-subtitle {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.75);
            margin-top: 8px;
            font-weight: 500;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            position: relative;
            z-index: 2;
        }

        .splash-cta {
            margin-top: 48px;
            position: relative;
            z-index: 2;
        }
        .splash-cta button {
            background: #fff;
            color: #059669;
            border: none;
            padding: 16px 52px;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            letter-spacing: 0.01em;
        }
        .splash-cta button:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 14px 40px rgba(0,0,0,0.2);
        }
        .splash-cta button:active { transform: translateY(0) scale(0.98); }

        .splash-link {
            margin-top: 18px;
            color: rgba(255,255,255,0.7);
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: color 0.2s;
            position: relative;
            z-index: 2;
        }
        .splash-link:hover { color: #fff; }

        /* Floating decorative circles on splash */
        .deco-circle {
            position: absolute;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.12);
            pointer-events: none;
            z-index: 1;
        }
        .deco-circle-1 { width: 200px; height: 200px; top: -40px; right: -60px; animation: decoFloat 8s ease-in-out infinite; }
        .deco-circle-2 { width: 140px; height: 140px; bottom: -30px; left: -40px; animation: decoFloat 10s ease-in-out infinite alternate; }
        .deco-circle-3 { width: 80px; height: 80px; top: 30%; right: 10%; background: rgba(255,255,255,0.05); animation: decoFloat 6s ease-in-out infinite; }

        /* Floating micro-particles */
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255,255,255,0.25);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
        }
        .particle-1 { top: 20%; left: 15%; animation: particleDrift 12s ease-in-out infinite; }
        .particle-2 { top: 60%; left: 70%; width: 6px; height: 6px; animation: particleDrift 15s ease-in-out infinite alternate; }
        .particle-3 { top: 75%; left: 25%; width: 3px; height: 3px; animation: particleDrift 10s ease-in-out infinite; animation-delay: -3s; }
        .particle-4 { top: 35%; left: 80%; width: 5px; height: 5px; background: rgba(255,255,255,0.15); animation: particleDrift 18s ease-in-out infinite alternate; }
        .particle-5 { top: 85%; left: 55%; animation: particleDrift 14s ease-in-out infinite; animation-delay: -5s; }
        .particle-6 { top: 10%; left: 50%; width: 3px; height: 3px; animation: particleDrift 16s ease-in-out infinite alternate; animation-delay: -2s; }
        .particle-7 { top: 45%; left: 40%; width: 5px; height: 5px; background: rgba(255,255,255,0.18); animation: particleDrift 11s ease-in-out infinite; animation-delay: -7s; }
        .particle-8 { top: 90%; left: 85%; width: 3px; height: 3px; animation: particleDrift 13s ease-in-out infinite alternate; animation-delay: -4s; }

        @keyframes particleDrift {
            0%   { transform: translate(0, 0) scale(1); opacity: 0.3; }
            25%  { transform: translate(15px, -20px) scale(1.5); opacity: 0.7; }
            50%  { transform: translate(-10px, -35px) scale(1); opacity: 0.4; }
            75%  { transform: translate(20px, -15px) scale(1.3); opacity: 0.8; }
            100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
        }

        @keyframes decoFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50%      { transform: translateY(-15px) rotate(5deg); }
        }


        /* ── RIGHT PANEL — Form area ── */
        .form-panel {
            flex: 1;
            background: #fff;
            padding: 48px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow-y: auto;
        }

        /* Small decorative logo in form panel */
        .form-panel-logo {
            width: 52px;
            height: 52px;
            background: linear-gradient(135deg, #059669, #10b981);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 6px;
            box-shadow: 0 6px 20px rgba(16,185,129,0.3);
        }
        .form-panel-logo i { font-size: 22px; color: #fff; }

        .form-greeting {
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #047857, #059669, #10b981, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 28px;
            letter-spacing: -0.02em;
        }

        .form-label {
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            color: #6b7280;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .form-input-wrap {
            position: relative;
            margin-bottom: 18px;
        }
        .form-input-wrap .input-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #9ca3af;
            font-size: 0.9rem;
            pointer-events: none;
            transition: color 0.2s;
        }
        .form-input-wrap input {
            width: 100%;
            padding: 14px 14px 14px 42px;
            border: 1.5px solid rgba(229,231,235,0.8);
            border-radius: 14px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #1f2937;
            background: rgba(249,250,251,0.7);
            backdrop-filter: blur(8px);
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Inter', sans-serif;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.04);
        }
        .form-input-wrap input::placeholder { color: #9ca3af; font-weight: 400; }
        .form-input-wrap input:focus {
            border-color: #10b981;
            box-shadow: 0 0 0 4px rgba(16,185,129,0.12), inset 0 1px 3px rgba(16,185,129,0.06);
            background: rgba(255,255,255,0.95);
        }
        .form-input-wrap input:focus + .input-icon,
        .form-input-wrap input:focus ~ .input-icon {
            color: #10b981;
        }

        .toggle-pw-btn {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            color: #9ca3af;
            font-size: 0.9rem;
            transition: color 0.2s;
        }
        .toggle-pw-btn:hover { color: #6b7280; }

        .terms-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 22px;
            font-size: 0.78rem;
            color: #6b7280;
        }
        .terms-row input[type="checkbox"] {
            width: 16px; height: 16px;
            accent-color: #10b981;
            cursor: pointer;
        }
        .terms-row a {
            color: #10b981;
            font-weight: 700;
            text-decoration: none;
        }
        .terms-row a:hover { text-decoration: underline; }

        /* Remember me & Forgot password row */
        .remember-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            font-size: 0.78rem;
        }
        .remember-label {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #6b7280;
            cursor: pointer;
            font-weight: 500;
        }
        .remember-label input[type="checkbox"] {
            width: 16px; height: 16px;
            accent-color: #10b981;
            cursor: pointer;
        }
        .forgot-link {
            color: #10b981;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s;
            position: relative;
        }
        .forgot-link::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 1.5px;
            background: #10b981;
            transition: width 0.3s ease;
        }
        .forgot-link:hover::after { width: 100%; }
        .forgot-link:hover { color: #059669; }

        .btn-submit {
            width: 100%;
            padding: 15px 24px;
            border: none;
            border-radius: 14px;
            font-size: 0.95rem;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            letter-spacing: 0.02em;
            background: linear-gradient(135deg, #047857, #059669, #10b981);
            background-size: 200% 200%;
            color: #fff;
            box-shadow: 0 6px 25px rgba(16,185,129,0.35);
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
        }
        .btn-submit::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -60%;
            width: 40%;
            height: 200%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
            transform: skewX(-25deg);
            transition: left 0.6s ease;
        }
        .btn-submit:hover::after {
            left: 120%;
        }
        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(16,185,129,0.5);
            background-position: 100% 0;
        }
        .btn-submit:active { transform: translateY(0); }
        .btn-submit:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
            box-shadow: none !important;
        }
        .btn-submit:disabled::after { display: none; }

        /* Loading spinner */
        .btn-submit .spinner {
            display: none;
            width: 18px;
            height: 18px;
            border: 2.5px solid rgba(255,255,255,0.3);
            border-top-color: #fff;
            border-radius: 50%;
            animation: btnSpin 0.7s linear infinite;
        }
        .btn-submit.loading .spinner { display: inline-block; }
        .btn-submit.loading .btn-text { opacity: 0.7; }
        @keyframes btnSpin { to { transform: rotate(360deg); } }





        /* Confidence bar (for password strength) */
        .confidence-bar { height: 4px; border-radius: 2px; background: #e5e7eb; overflow: hidden; margin-top: 8px; }
        .confidence-fill { height: 100%; border-radius: 2px; transition: width 0.4s ease; }
        .confidence-fill.high   { background: linear-gradient(90deg, #10b981, #34d399); }
        .confidence-fill.medium { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
        .confidence-fill.low    { background: linear-gradient(90deg, #ef4444, #f87171); }

        .pw-hint {
            font-size: 0.68rem;
            color: #9ca3af;
            margin-top: 4px;
        }

        .form-error {
            font-size: 0.8rem;
            color: #ef4444;
            font-weight: 600;
            margin-bottom: 12px;
            padding: 8px 12px;
            background: #fef2f2;
            border-radius: 10px;
            border: 1px solid #fee2e2;
        }

        .tab-switch-link {
            text-align: center;
            margin-top: 24px;
            font-size: 0.82rem;
            color: #6b7280;
            padding: 14px 20px;
            background: rgba(249,250,251,0.6);
            border-radius: 12px;
            border: 1px solid rgba(229,231,235,0.5);
            transition: all 0.3s ease;
        }
        .tab-switch-link:hover {
            background: rgba(236,253,245,0.5);
            border-color: rgba(16,185,129,0.2);
        }
        .tab-switch-link a {
            color: #10b981;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            position: relative;
            transition: color 0.2s;
        }
        .tab-switch-link a::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 1.5px;
            background: #10b981;
            transition: width 0.3s ease;
        }
        .tab-switch-link a:hover { color: #059669; }
        .tab-switch-link a:hover::after { width: 100%; }

        /* ── Toast ── */
        .toast {
            position: fixed; top: 20px; right: 20px; z-index: 9999;
            padding: 14px 22px; border-radius: 12px; color: #fff;
            font-size: 0.875rem; font-weight: 500;
            animation: toastIn 0.35s ease-out;
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }
        .toast-error   { background: linear-gradient(135deg, #dc2626, #ef4444); }
        .toast-success { background: linear-gradient(135deg, #059669, #10b981); }
        @keyframes toastIn { from { transform: translateX(120%); opacity:0; } to { transform: translateX(0); opacity:1; } }

        /* ═══════════════════════════════════════════
           FLOATING BUBBLE ANIMATION
           Elements appear one-by-one, rising up
           with a scale-bounce + fade
           ═══════════════════════════════════════════ */
        .bubble-in {
            opacity: 0;
            transform: translateY(40px) scale(0.85);
            animation: bubbleRise 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }

        @keyframes bubbleRise {
            0% {
                opacity: 0;
                transform: translateY(40px) scale(0.85);
            }
            60% {
                opacity: 1;
                transform: translateY(-6px) scale(1.03);
            }
            80% {
                transform: translateY(3px) scale(0.98);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        /* Staggered delays for sequential bubble effect */
        .bubble-delay-1  { animation-delay: 0.05s; }
        .bubble-delay-2  { animation-delay: 0.12s; }
        .bubble-delay-3  { animation-delay: 0.20s; }
        .bubble-delay-4  { animation-delay: 0.28s; }
        .bubble-delay-5  { animation-delay: 0.36s; }
        .bubble-delay-6  { animation-delay: 0.44s; }
        .bubble-delay-7  { animation-delay: 0.52s; }
        .bubble-delay-8  { animation-delay: 0.60s; }
        .bubble-delay-9  { animation-delay: 0.68s; }
        .bubble-delay-10 { animation-delay: 0.76s; }
        .bubble-delay-11 { animation-delay: 0.84s; }
        .bubble-delay-12 { animation-delay: 0.92s; }

        /* Splash panel bubbles (slightly different timing) */
        .splash-bubble {
            opacity: 0;
            transform: translateY(50px) scale(0.8);
            animation: splashBubble 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }
        @keyframes splashBubble {
            0%   { opacity: 0; transform: translateY(50px) scale(0.8); }
            50%  { opacity: 1; transform: translateY(-8px) scale(1.05); }
            75%  { transform: translateY(4px) scale(0.97); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .splash-delay-1 { animation-delay: 0.1s; }
        .splash-delay-2 { animation-delay: 0.25s; }
        .splash-delay-3 { animation-delay: 0.4s; }
        .splash-delay-4 { animation-delay: 0.55s; }
        .splash-delay-5 { animation-delay: 0.7s; }

        /* ── Responsive: stack on mobile ── */
        @media (max-width: 768px) {
            .login-wrapper {
                flex-direction: column;
                max-width: 100vw;
                width: 100vw;
                min-height: 100vh;
                border-radius: 0;
            }
            .splash-panel {
                min-height: 260px;
                padding: 36px 24px;
                border-radius: 0;
            }
            .splash-logo { width: 72px; height: 72px; }
            .splash-logo i { font-size: 32px; }
            .splash-title { font-size: 1.5rem; }
            .splash-cta { margin-top: 28px; }
            .splash-cta button { padding: 13px 40px; font-size: 0.9rem; }
            .form-panel { padding: 32px 24px; }
            .form-greeting { font-size: 1.4rem; }
        }

        /* Tiny glow pulse on the splash logo */
        @keyframes logoPulse {
            0%, 100% { box-shadow: 0 12px 40px rgba(0,0,0,0.15), 0 0 0 0 rgba(255,255,255,0.15); }
            50%      { box-shadow: 0 12px 40px rgba(0,0,0,0.15), 0 0 0 12px rgba(255,255,255,0); }
        }
        .splash-logo { animation: logoPulse 3s ease-in-out infinite, splashBubble 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
    </style>
</head>
<body>

    <div class="login-wrapper">
        <!-- ═══ LEFT: Green Gradient Splash Panel ═══ -->
        <div class="splash-panel">
            <!-- Decorative circles -->
            <div class="deco-circle deco-circle-1"></div>
            <div class="deco-circle deco-circle-2"></div>
            <div class="deco-circle deco-circle-3"></div>

            <!-- Floating micro-particles -->
            <div class="particle particle-1"></div>
            <div class="particle particle-2"></div>
            <div class="particle particle-3"></div>
            <div class="particle particle-4"></div>
            <div class="particle particle-5"></div>
            <div class="particle particle-6"></div>
            <div class="particle particle-7"></div>
            <div class="particle particle-8"></div>

            <div class="splash-logo splash-bubble splash-delay-1">
                <i class="fas fa-chart-line"></i>
            </div>
            <div class="splash-title splash-bubble splash-delay-2">Stock Market<br>Prediction</div>
            <div class="splash-subtitle splash-bubble splash-delay-3">AI-Powered Indian Market Intelligence</div>

            <div class="splash-cta splash-bubble splash-delay-4">
                <button onclick="document.querySelector('.form-panel').scrollIntoView({behavior:'smooth'})">Get Started</button>
            </div>
            <div class="splash-link splash-bubble splash-delay-5" onclick="switchTab('login')">I already have an account</div>
        </div>

        <!-- ═══ RIGHT: Form Panel ═══ -->
        <div class="form-panel">

            <!-- ── Sign In Form ── -->
            <div id="login-form-container">
                <div class="form-panel-logo bubble-in bubble-delay-1">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="form-greeting bubble-in bubble-delay-2">Welcome Back!</div>

                <form onsubmit="handleLoginSubmit(event)">
                    <div class="form-input-wrap bubble-in bubble-delay-3">
                        <input type="text" id="login-username" required placeholder="Username or Email">
                        <i class="fas fa-user input-icon"></i>
                    </div>
                    <div class="form-input-wrap bubble-in bubble-delay-4">
                        <input type="password" id="login-password" required placeholder="Password" style="padding-right: 44px;">
                        <i class="fas fa-lock input-icon"></i>
                        <button type="button" onclick="togglePassword('login-password', this)" class="toggle-pw-btn"><i class="fas fa-eye"></i></button>
                    </div>

                    <div class="remember-row bubble-in bubble-delay-5">
                        <label class="remember-label">
                            <input type="checkbox" id="remember-me" checked>
                            <span>Remember me</span>
                        </label>
                        <a href="#" class="forgot-link" onclick="event.preventDefault()">Forgot password?</a>
                    </div>

                    <div id="login-error" class="form-error" style="display:none;"></div>

                    <div class="bubble-in bubble-delay-6">
                        <button type="submit" id="login-btn" class="btn-submit">
                            <span class="spinner"></span>
                            <span class="btn-text"><i class="fas fa-right-to-bracket"></i> Sign In</span>
                        </button>
                    </div>
                </form>



                <div class="tab-switch-link bubble-in bubble-delay-9">
                    Don't have an account? <a onclick="switchTab('register')">Create one</a>
                </div>
            </div>

            <!-- ── Register Form ── -->
            <div id="register-form-container" style="display:none;">
                <div class="form-panel-logo bubble-in bubble-delay-1">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="form-greeting bubble-in bubble-delay-2">Hello!</div>

                <form onsubmit="handleRegisterSubmit(event)">
                    <div class="form-input-wrap bubble-in bubble-delay-3">
                        <input type="text" id="reg-username" required minlength="3" maxlength="20" pattern="^[a-zA-Z0-9_]{3,20}$" placeholder="Username">
                        <i class="fas fa-user input-icon"></i>
                    </div>
                    <div class="form-input-wrap bubble-in bubble-delay-4">
                        <input type="email" id="reg-email" required placeholder="Email">
                        <i class="fas fa-envelope input-icon"></i>
                    </div>
                    <div class="form-input-wrap bubble-in bubble-delay-5">
                        <input type="password" id="reg-password" required minlength="8" placeholder="Password" style="padding-right: 44px;">
                        <i class="fas fa-lock input-icon"></i>
                        <button type="button" onclick="togglePassword('reg-password', this)" class="toggle-pw-btn"><i class="fas fa-eye"></i></button>
                    </div>
                    <!-- Strength meter -->
                    <div id="pw-strength-container" style="display:none; margin-bottom: 12px;">
                        <div class="confidence-bar"><div id="pw-strength-fill" class="confidence-fill" style="width:0%;"></div></div>
                        <span id="pw-strength-text" class="pw-hint"></span>
                    </div>
                    <div class="form-input-wrap bubble-in bubble-delay-6">
                        <input type="password" id="reg-confirm-password" required minlength="8" placeholder="Confirm Password">
                        <i class="fas fa-shield-halved input-icon"></i>
                    </div>

                    <div class="terms-row bubble-in bubble-delay-7">
                        <input type="checkbox" id="terms-check">
                        <label for="terms-check">I agree to the <a href="#">terms and conditions</a></label>
                    </div>

                    <div id="reg-error" class="form-error" style="display:none;"></div>

                    <div class="bubble-in bubble-delay-8">
                        <button type="submit" id="reg-btn" class="btn-submit">
                            <span class="spinner"></span>
                            <span class="btn-text"><i class="fas fa-user-plus"></i> Sign Up</span>
                        </button>
                    </div>
                </form>



                <div class="tab-switch-link bubble-in bubble-delay-12">
                    Already have an account? <a onclick="switchTab('login')">Sign In</a>
                </div>
            </div>

        </div>
    </div>

    <script>
        /* ── Tab Switching with re-triggering bubble animation ── */
        function switchTab(tab) {
            const loginContainer = document.getElementById('login-form-container');
            const regContainer = document.getElementById('register-form-container');

            if (tab === 'login') {
                loginContainer.style.display = 'block';
                regContainer.style.display = 'none';
                replayBubbles(loginContainer);
            } else {
                loginContainer.style.display = 'none';
                regContainer.style.display = 'block';
                replayBubbles(regContainer);
            }
            // Clear errors
            ['login-error', 'reg-error'].forEach(id => {
                const el = document.getElementById(id);
                if (el) { el.style.display = 'none'; el.textContent = ''; }
            });
        }

        /* Re-trigger bubble animations by cloning classes */
        function replayBubbles(container) {
            const bubbles = container.querySelectorAll('.bubble-in');
            bubbles.forEach(el => {
                el.style.animation = 'none';
                el.offsetHeight; /* force reflow */
                el.style.animation = '';
            });
        }

        /* ── Toggle Password Visibility ── */
        function togglePassword(id, btn) {
            const el = document.getElementById(id);
            const icon = btn.querySelector('i');
            if (el.type === 'password') {
                el.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                el.type = 'password';
                icon.className = 'fas fa-eye';
            }
        }

        /* ── Live Password Strength ── */
        const pwInput = document.getElementById('reg-password');
        pwInput.addEventListener('input', function() {
            const val = this.value;
            const container = document.getElementById('pw-strength-container');
            const fill = document.getElementById('pw-strength-fill');
            const text = document.getElementById('pw-strength-text');

            if (!val) { container.style.display = 'none'; return; }
            container.style.display = 'block';

            let score = 0;
            if (val.length >= 8)  score++;
            if (val.length >= 12) score++;
            if (/[A-Z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            const pct = Math.min(100, score * 20);
            fill.style.width = pct + '%';
            fill.className = 'confidence-fill ' + (pct >= 80 ? 'high' : pct >= 50 ? 'medium' : 'low');
            text.textContent = pct >= 80 ? 'Strong password' : pct >= 50 ? 'Moderate password' : 'Weak password';
        });

        /* ── Toast Notifications ── */
        function showToast(msg, type) {
            const oldToast = document.querySelector('.toast');
            if (oldToast) oldToast.remove();
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation'}" style="margin-right:8px;"></i>${msg}`;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3500);
        }

        /* ── Login Submit ── */
        async function handleLoginSubmit(e) {
            e.preventDefault();
            const errEl = document.getElementById('login-error');
            const btn = document.getElementById('login-btn');
            errEl.style.display = 'none';
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right:8px;"></i>Signing in…';

            try {
                const resp = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': '{{ csrf_token }}'
                    },
                    body: JSON.stringify({
                        username: document.getElementById('login-username').value.trim(),
                        password: document.getElementById('login-password').value
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    showToast(data.message || 'Welcome back!', 'success');
                    setTimeout(() => window.location.href = '/', 800);
                } else {
                    errEl.textContent = data.message || 'Login failed';
                    errEl.style.display = 'block';
                }
            } catch (err) {
                errEl.textContent = 'Network error. Please try again.';
                errEl.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-right-to-bracket" style="margin-right:4px;"></i> Sign In';
            }
        }

        /* ── Register Submit ── */
        async function handleRegisterSubmit(e) {
            e.preventDefault();
            const errEl = document.getElementById('reg-error');
            const btn = document.getElementById('reg-btn');
            const pw = document.getElementById('reg-password').value;
            const cpw = document.getElementById('reg-confirm-password').value;

            errEl.style.display = 'none';
            if (pw !== cpw) {
                errEl.textContent = 'Passwords do not match';
                errEl.style.display = 'block';
                return;
            }

            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right:8px;"></i>Creating account…';

            try {
                const resp = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': '{{ csrf_token }}'
                    },
                    body: JSON.stringify({
                        username: document.getElementById('reg-username').value.trim(),
                        email: document.getElementById('reg-email').value.trim(),
                        password: pw
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    showToast(data.message || 'Account created successfully!', 'success');
                    setTimeout(() => window.location.href = '/', 800);
                } else {
                    errEl.textContent = data.message || 'Registration failed';
                    errEl.style.display = 'block';
                }
            } catch (err) {
                errEl.textContent = 'Network error. Please try again.';
                errEl.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-user-plus" style="margin-right:4px;"></i> Sign Up';
            }
        }
    </script>
</body>
</html>
"""

