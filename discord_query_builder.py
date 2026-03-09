#!/usr/bin/env python3
"""
Discord Digest Query Builder - Web Interface
A web-based interface for querying and analyzing Discord message exports
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import tempfile
import os

app = Flask(__name__)

class DiscordQueryEngine:
    """Query engine for Discord message data"""
    
    def __init__(self, exports_directory):
        self.exports_directory = exports_directory
        self.all_messages = []
        self.users = set()
        self.channels = set()
        self.servers = set()
        self._load_all_exports()
    
    def _load_all_exports(self):
        """Load all JSON exports into memory"""
        json_files = list(Path(self.exports_directory).rglob('*.json'))
        
        # Skip known output files (not Discord exports)
        skip_files = {
            'user_digest.json', 'colored.json', 'with_emojis.json',
            'with_links.json', 'truncated.json', 'test_run.json'
        }
        
        loaded_count = 0
        skipped_count = 0
        
        for json_file in json_files:
            # Skip output files
            if json_file.name in skip_files:
                skipped_count += 1
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Verify it's a Discord export (has channel and messages)
                if 'channel' not in data or 'messages' not in data:
                    print(f"Skipping {json_file.name}: Not a Discord export format")
                    skipped_count += 1
                    continue
                
                channel_name = data.get('channel', {}).get('name', 'Unknown')
                guild_name = data.get('guild', {}).get('name', 'Unknown')
                guild_id = data.get('guild', {}).get('id', '')
                channel_id = data.get('channel', {}).get('id', '')
                messages = data.get('messages', [])
                
                self.channels.add(channel_name)
                self.servers.add(guild_name)
                
                for msg in messages:
                    author = msg.get('author', {})
                    author_name = author.get('name', 'Unknown')
                    self.users.add(author_name)
                    
                    try:
                        dt = datetime.fromisoformat(msg.get('timestamp', '').replace('Z', '+00:00'))
                    except:
                        continue
                    
                    self.all_messages.append({
                        'id': msg.get('id'),
                        'author': author_name,
                        'content': msg.get('content', ''),
                        'timestamp': dt,
                        'date': dt.date(),
                        'time': dt.strftime('%H:%M:%S'),
                        'channel': channel_name,
                        'server': guild_name,
                        'reference': msg.get('reference', {}),
                        'message_url': f"https://discord.com/channels/{guild_id}/{channel_id}/{msg.get('id')}"
                    })
                
                loaded_count += 1
                
            except Exception as e:
                print(f"Error loading {json_file.name}: {e}")
                skipped_count += 1
                continue
        
        # Sort by timestamp
        self.all_messages.sort(key=lambda x: x['timestamp'])
        print(f"Loaded {len(self.all_messages)} messages from {loaded_count} files ({skipped_count} files skipped)")
    
    def query(self, filters):
        """
        Query messages with various filters
        
        Filters:
        - username: filter by author
        - channel: filter by channel name
        - server: filter by server name
        - date_from: start date (YYYY-MM-DD)
        - date_to: end date (YYYY-MM-DD)
        - keyword: search in message content
        - include_replies_to: include replies to specified user
        - limit: max results
        """
        results = self.all_messages.copy()
        
        # Filter by username
        if filters.get('username'):
            username = filters['username'].lower()
            if filters.get('include_replies_to'):
                # Build lookup of user's message IDs
                user_msg_ids = {m['id'] for m in results if m['author'].lower() == username}
                # Include messages BY user OR replying TO user
                results = [
                    m for m in results 
                    if m['author'].lower() == username or 
                    m['reference'].get('messageId') in user_msg_ids
                ]
            else:
                results = [m for m in results if m['author'].lower() == username]
        
        # Filter by channel
        if filters.get('channel'):
            channels = filters['channel'] if isinstance(filters['channel'], list) else [filters['channel']]
            results = [m for m in results if m['channel'] in channels]
        
        # Filter by server
        if filters.get('server'):
            servers = filters['server'] if isinstance(filters['server'], list) else [filters['server']]
            results = [m for m in results if m['server'] in servers]
        
        # Filter by date range
        if filters.get('date_from'):
            date_from = datetime.strptime(filters['date_from'], '%Y-%m-%d').date()
            results = [m for m in results if m['date'] >= date_from]
        
        if filters.get('date_to'):
            date_to = datetime.strptime(filters['date_to'], '%Y-%m-%d').date()
            results = [m for m in results if m['date'] <= date_to]
        
        # Filter by keyword
        if filters.get('keyword'):
            keyword = filters['keyword'].lower()
            results = [m for m in results if keyword in m['content'].lower()]
        
        # Limit results
        if filters.get('limit'):
            results = results[-int(filters['limit']):]
        
        return results
    
    def get_statistics(self, messages):
        """Generate statistics for a set of messages"""
        if not messages:
            return {}
        
        authors = defaultdict(int)
        channels = defaultdict(int)
        dates = defaultdict(int)
        
        for msg in messages:
            authors[msg['author']] += 1
            channels[msg['channel']] += 1
            dates[msg['date'].isoformat()] += 1
        
        return {
            'total': len(messages),
            'date_range': {
                'start': messages[0]['date'].isoformat(),
                'end': messages[-1]['date'].isoformat()
            },
            'top_authors': sorted(authors.items(), key=lambda x: x[1], reverse=True)[:10],
            'by_channel': sorted(channels.items(), key=lambda x: x[1], reverse=True),
            'by_date': sorted(dates.items())
        }


# Global query engine (will be initialized in main)
query_engine = None


@app.route('/')
def index():
    """Main query builder page"""
    return render_template('index.html',
                         users=sorted(query_engine.users),
                         channels=sorted(query_engine.channels),
                         servers=sorted(query_engine.servers))


@app.route('/api/query', methods=['POST'])
def api_query():
    """API endpoint for querying messages"""
    filters = request.json
    results = query_engine.query(filters)
    stats = query_engine.get_statistics(results)
    
    # Convert to JSON-serializable format
    results_json = []
    for msg in results:
        results_json.append({
            'author': msg['author'],
            'content': msg['content'],
            'timestamp': msg['timestamp'].isoformat(),
            'date': msg['date'].isoformat(),
            'time': msg['time'],
            'channel': msg['channel'],
            'server': msg['server'],
            'message_url': msg['message_url']
        })
    
    return jsonify({
        'results': results_json,
        'statistics': stats
    })


@app.route('/api/export', methods=['POST'])
def api_export():
    """Export query results in various formats"""
    data = request.json
    filters = data.get('filters', {})
    format_type = data.get('format', 'json')
    
    results = query_engine.query(filters)
    
    if format_type == 'json':
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump({
                'metadata': {
                    'generated': datetime.now().isoformat(),
                    'total_messages': len(results),
                    'filters': filters
                },
                'messages': [{
                    'author': msg['author'],
                    'content': msg['content'],
                    'timestamp': msg['timestamp'].isoformat(),
                    'channel': msg['channel'],
                    'server': msg['server'],
                    'message_url': msg['message_url']
                } for msg in results]
            }, f, indent=2)
            temp_path = f.name
        
        return send_file(temp_path, as_attachment=True, download_name='discord_query_results.json')
    
    elif format_type == 'csv':
        import csv
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Time', 'Author', 'Channel', 'Server', 'Content', 'URL'])
            for msg in results:
                writer.writerow([
                    msg['date'].isoformat(),
                    msg['time'],
                    msg['author'],
                    msg['channel'],
                    msg['server'],
                    msg['content'],
                    msg['message_url']
                ])
            temp_path = f.name
        
        return send_file(temp_path, as_attachment=True, download_name='discord_query_results.csv')


def create_templates():
    """Create HTML template for the web interface"""
    template_dir = Path('templates')
    template_dir.mkdir(exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Query Builder</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 400px 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .query-builder, .results-panel {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .query-builder h2, .results-panel h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        
        input[type="text"],
        input[type="date"],
        input[type="number"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        select[multiple] {
            min-height: 120px;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: auto;
            cursor: pointer;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 25px;
        }
        
        button {
            flex: 1;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .stats {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .results {
            max-height: 600px;
            overflow-y: auto;
        }
        
        .message {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            transition: transform 0.2s;
        }
        
        .message:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .message-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .message-author {
            font-weight: bold;
            color: #667eea;
        }
        
        .message-meta {
            font-size: 0.85em;
            color: #666;
        }
        
        .message-content {
            color: #333;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .message-link {
            text-align: right;
            margin-top: 10px;
        }
        
        .message-link a {
            color: #667eea;
            text-decoration: none;
            font-size: 0.9em;
        }
        
        .message-link a:hover {
            text-decoration: underline;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .export-buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .export-buttons button {
            flex: 1;
            padding: 10px;
            font-size: 14px;
        }
        
        @media (max-width: 968px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Discord Query Builder</h1>
            <p class="subtitle">Advanced search and analysis for Discord message exports</p>
        </header>
        
        <div class="main-content">
            <!-- Query Builder Panel -->
            <div class="query-builder">
                <h2>Build Your Query</h2>
                
                <form id="queryForm">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <select id="username" name="username">
                            <option value="">All Users</option>
                            {% for user in users %}
                            <option value="{{ user }}">{{ user }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group checkbox-group">
                        <input type="checkbox" id="includeReplies" name="includeReplies">
                        <label for="includeReplies">Include replies to this user</label>
                    </div>
                    
                    <div class="form-group">
                        <label for="channel">Channels (hold Ctrl/Cmd for multiple)</label>
                        <select id="channel" name="channel" multiple>
                            {% for channel in channels %}
                            <option value="{{ channel }}">{{ channel }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="server">Servers</label>
                        <select id="server" name="server" multiple>
                            {% for server in servers %}
                            <option value="{{ server }}">{{ server }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="keyword">Keyword Search</label>
                        <input type="text" id="keyword" name="keyword" placeholder="Search message content...">
                    </div>
                    
                    <div class="form-group">
                        <label for="dateFrom">Date From</label>
                        <input type="date" id="dateFrom" name="dateFrom">
                    </div>
                    
                    <div class="form-group">
                        <label for="dateTo">Date To</label>
                        <input type="date" id="dateTo" name="dateTo">
                    </div>
                    
                    <div class="form-group">
                        <label for="limit">Max Results</label>
                        <input type="number" id="limit" name="limit" value="100" min="1" max="10000">
                    </div>
                    
                    <div class="button-group">
                        <button type="submit" class="btn-primary">Search</button>
                        <button type="button" class="btn-secondary" onclick="resetForm()">Reset</button>
                    </div>
                </form>
            </div>
            
            <!-- Results Panel -->
            <div class="results-panel">
                <h2>Results</h2>
                
                <div id="statistics" style="display: none;">
                    <div class="stats">
                        <h3 style="margin-bottom: 10px;">📊 Statistics</h3>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <span class="stat-value" id="statTotal">0</span>
                                <span class="stat-label">Total Messages</span>
                            </div>
                            <div class="stat-card">
                                <span class="stat-value" id="statDays">0</span>
                                <span class="stat-label">Days</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="export-buttons">
                        <button class="btn-primary" onclick="exportResults('json')">📥 Export JSON</button>
                        <button class="btn-primary" onclick="exportResults('csv')">📥 Export CSV</button>
                    </div>
                </div>
                
                <div id="results" class="results">
                    <div style="text-align: center; padding: 60px; color: #999;">
                        <p style="font-size: 4em; margin-bottom: 20px;">🔍</p>
                        <p>Build your query and click Search to see results</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentFilters = {};
        
        document.getElementById('queryForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            await performQuery();
        });
        
        async function performQuery() {
            const form = document.getElementById('queryForm');
            const formData = new FormData(form);
            
            // Build filters object
            const filters = {};
            
            if (formData.get('username')) {
                filters.username = formData.get('username');
            }
            
            if (document.getElementById('includeReplies').checked) {
                filters.include_replies_to = true;
            }
            
            const channels = Array.from(document.getElementById('channel').selectedOptions).map(o => o.value);
            if (channels.length > 0) {
                filters.channel = channels;
            }
            
            const servers = Array.from(document.getElementById('server').selectedOptions).map(o => o.value);
            if (servers.length > 0) {
                filters.server = servers;
            }
            
            if (formData.get('keyword')) {
                filters.keyword = formData.get('keyword');
            }
            
            if (formData.get('dateFrom')) {
                filters.date_from = formData.get('dateFrom');
            }
            
            if (formData.get('dateTo')) {
                filters.date_to = formData.get('dateTo');
            }
            
            if (formData.get('limit')) {
                filters.limit = parseInt(formData.get('limit'));
            }
            
            currentFilters = filters;
            
            // Show loading
            document.getElementById('results').innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Searching messages...</p>
                </div>
            `;
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(filters)
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                document.getElementById('results').innerHTML = `
                    <div class="loading">
                        <p style="color: red;">Error: ${error.message}</p>
                    </div>
                `;
            }
        }
        
        function displayResults(data) {
            const { results, statistics } = data;
            
            // Update statistics
            if (statistics.total > 0) {
                document.getElementById('statistics').style.display = 'block';
                document.getElementById('statTotal').textContent = statistics.total;
                
                if (statistics.date_range) {
                    const start = new Date(statistics.date_range.start);
                    const end = new Date(statistics.date_range.end);
                    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
                    document.getElementById('statDays').textContent = days;
                }
            } else {
                document.getElementById('statistics').style.display = 'none';
            }
            
            // Display results
            const resultsDiv = document.getElementById('results');
            
            if (results.length === 0) {
                resultsDiv.innerHTML = `
                    <div class="loading">
                        <p style="color: #999;">No messages found matching your query.</p>
                    </div>
                `;
                return;
            }
            
            let html = '';
            for (const msg of results) {
                html += `
                    <div class="message">
                        <div class="message-header">
                            <span class="message-author">${escapeHtml(msg.author)}</span>
                            <span class="message-meta">
                                #${escapeHtml(msg.channel)} • ${msg.date} ${msg.time}
                            </span>
                        </div>
                        <div class="message-content">${escapeHtml(msg.content)}</div>
                        <div class="message-link">
                            <a href="${msg.message_url}" target="_blank">View in Discord →</a>
                        </div>
                    </div>
                `;
            }
            
            resultsDiv.innerHTML = html;
        }
        
        async function exportResults(format) {
            try {
                const response = await fetch('/api/export', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        filters: currentFilters,
                        format: format
                    })
                });
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `discord_query_results.${format}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch (error) {
                alert('Export failed: ' + error.message);
            }
        }
        
        function resetForm() {
            document.getElementById('queryForm').reset();
            document.getElementById('results').innerHTML = `
                <div style="text-align: center; padding: 60px; color: #999;">
                    <p style="font-size: 4em; margin-bottom: 20px;">🔍</p>
                    <p>Build your query and click Search to see results</p>
                </div>
            `;
            document.getElementById('statistics').style.display = 'none';
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""
    
    with open(template_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 discord_query_builder.py <exports_directory> [port]")
        print("\nExample:")
        print("  python3 discord_query_builder.py ./discord_exports 5000")
        sys.exit(1)
    
    exports_dir = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    if not Path(exports_dir).exists():
        print(f"Error: Directory '{exports_dir}' does not exist")
        sys.exit(1)
    
    # Initialize query engine
    global query_engine
    print("Loading Discord exports...")
    query_engine = DiscordQueryEngine(exports_dir)
    
    # Create templates
    create_templates()
    
    print(f"\n{'='*80}")
    print("Discord Query Builder - Web Interface")
    print(f"{'='*80}")
    print(f"Loaded: {len(query_engine.all_messages)} messages")
    print(f"Users: {len(query_engine.users)}")
    print(f"Channels: {len(query_engine.channels)}")
    print(f"Servers: {len(query_engine.servers)}")
    print(f"\n🌐 Server starting at: http://localhost:{port}")
    print(f"{'='*80}\n")
    
    app.run(debug=True, port=port, host='0.0.0.0')


if __name__ == '__main__':
    main()
