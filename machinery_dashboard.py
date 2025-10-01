"""
MACHINERY MATCHER - WEB DASHBOARD
Version: 2.0 Final
Description: Beautiful web interface for machinery matching
Usage: python3 machinery_dashboard.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify, send_file
import pandas as pd
import json
import os
from datetime import datetime
import threading

app = Flask(__name__)

# Global progress tracking
progress_data = {
    'status': 'idle',
    'progress': 0,
    'message': '',
    'results': None
}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Machinery Matcher Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: slideDown 0.5s ease;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .form-group small {
            display: block;
            margin-top: 5px;
            color: #666;
            font-size: 0.9em;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .progress-container {
            display: none;
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .progress-container.active {
            display: block;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        .status-message {
            color: #666;
            font-size: 1.1em;
            margin-top: 10px;
        }
        
        .results-container {
            display: none;
            grid-column: 1 / -1;
        }
        
        .results-container.active {
            display: block;
        }
        
        .provider-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .provider-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .provider-rank {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .provider-name {
            flex: 1;
            margin-left: 20px;
        }
        
        .provider-name h3 {
            color: #333;
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        
        .provider-stats {
            display: flex;
            gap: 30px;
            margin: 20px 0;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .download-btn {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 12px 35px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }
        
        @media (max-width: 768px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Machinery Matcher Dashboard</h1>
            <p>AI-powered matching for plastic machinery providers and prospects</p>
        </div>
        
        <div class="main-grid" id="configSection">
            <div class="card">
                <h2>⚙️ Configuration</h2>
                <div class="form-group">
                    <label>Anthropic API Key</label>
                    <input type="password" id="apiKey" placeholder="sk-ant-..." required>
                    <small>Get from console.anthropic.com</small>
                </div>
                
                <div class="form-group">
                    <label>CSV File</label>
                    <input type="file" id="csvFile" accept=".csv" required>
                    <small>Your prospects database</small>
                </div>
                
                <div class="form-group">
                    <label>Top N Providers</label>
                    <select id="topN">
                        <option value="5">5 providers</option>
                        <option value="10" selected>10 providers</option>
                        <option value="15">15 providers</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Maximum Prospects</label>
                    <select id="maxProspects">
                        <option value="100">100 (test)</option>
                        <option value="500">500</option>
                        <option value="1500" selected>1500</option>
                    </select>
                </div>
            </div>
            
            <div class="card">
                <h2>🎯 Technology Filter</h2>
                <div class="form-group">
                    <label>Filter by Technology</label>
                    <select id="techFilter">
                        <option value="">No filter (all prospects)</option>
                        <option value="injection">Injection Molding</option>
                        <option value="extrusion">Extrusion</option>
                        <option value="blow_molding">Blow Molding</option>
                        <option value="thermoforming">Thermoforming</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Web Scraping</label>
                    <select id="webScraping">
                        <option value="false" selected>Disabled (Fast)</option>
                        <option value="true">Enabled (Accurate)</option>
                    </select>
                </div>
                
                <button type="button" class="btn" id="startBtn" onclick="startDemo()">
                    🚀 Start Analysis (DEMO)
                </button>
            </div>
        </div>
        
        <div class="progress-container" id="progressContainer">
            <h2>⏳ Analysis in Progress...</h2>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%">0%</div>
            </div>
            <div class="status-message" id="statusMessage">Initializing...</div>
        </div>
        
        <div class="results-container card" id="resultsContainer">
            <h2>📊 Results - Top Machinery Providers</h2>
            <button class="download-btn" onclick="alert('Excel file would download here!')">
                📥 Download Excel Report
            </button>
            <div id="resultsContent"></div>
        </div>
    </div>
    
    <script>
        function startDemo() {
            document.getElementById('configSection').style.display = 'none';
            document.getElementById('progressContainer').classList.add('active');
            document.getElementById('resultsContainer').classList.remove('active');
            
            const messages = [
                "Initializing AI engine...",
                "Scraping K2025 database...",
                "Analyzing prospects...",
                "Running AI matching...",
                "Generating results..."
            ];
            
            let progress = 0;
            let messageIndex = 0;
            
            const interval = setInterval(() => {
                progress += 5;
                
                if (progress > 100) {
                    clearInterval(interval);
                    setTimeout(() => {
                        document.getElementById('progressContainer').classList.remove('active');
                        document.getElementById('resultsContainer').classList.add('active');
                        displayMockResults();
                    }, 500);
                    return;
                }
                
                document.getElementById('progressFill').style.width = progress + '%';
                document.getElementById('progressFill').textContent = progress + '%';
                
                if (progress % 20 === 0 && messageIndex < messages.length) {
                    document.getElementById('statusMessage').textContent = messages[messageIndex++];
                }
            }, 200);
        }
        
        function displayMockResults() {
            const html = `
                <div class="provider-card">
                    <div class="provider-header">
                        <div class="provider-rank">#1</div>
                        <div class="provider-name">
                            <h3>ENGEL Austria GmbH</h3>
                            <p>Austria</p>
                        </div>
                    </div>
                    <div class="provider-stats">
                        <div class="stat">
                            <div class="stat-value">85%</div>
                            <div>Coverage</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">756</div>
                            <div>Prospects</div>
                        </div>
                    </div>
                    <p><strong>Why Partner:</strong> Wide machine range, EU presence, sustainability features</p>
                </div>
                
                <div class="provider-card">
                    <div class="provider-header">
                        <div class="provider-rank">#2</div>
                        <div class="provider-name">
                            <h3>Arburg GmbH + Co KG</h3>
                            <p>Germany</p>
                        </div>
                    </div>
                    <div class="provider-stats">
                        <div class="stat">
                            <div class="stat-value">79%</div>
                            <div>Coverage</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">698</div>
                            <div>Prospects</div>
                        </div>
                    </div>
                    <p><strong>Why Partner:</strong> Precision injection, medical grade, strong service network</p>
                </div>
            `;
            
            document.getElementById('resultsContent').innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎯 MACHINERY MATCHER DASHBOARD")
    print("="*70)
    print("\n📊 Starting web server...")
    print("🌐 Open your browser: http://localhost:5000")
    print("\nPress Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')
