# Discord Message Analyzer - Enhanced Version

A comprehensive toolkit for analyzing Discord message exports with support for markdown, HTML, JSON output, and an advanced web-based query builder.

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install flask PyYAML

# Or create a requirements.txt:
# Flask==3.0.0
# PyYAML==6.0.1
```

### Getting Discord Exports

Use [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) to export your Discord channels:

```bash
# Download DiscordChatExporter
wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip
unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter
chmod +x discord-exporter/DiscordChatExporter.Cli

# Export a channel (replace YOUR_TOKEN and CHANNEL_ID)
./discord-exporter/DiscordChatExporter.Cli export \
  -t "YOUR_DISCORD_TOKEN" \
  -c "CHANNEL_ID" \
  -f Json \
  -o "discord_exports/channel.json"
```

## 📊 Method 1: Generate Complete Archives (Command Line)

### Basic Usage for Dirvine

Generate all formats (Markdown, HTML, and JSON) for user "dirvine.":

```bash
python3 discord_digest_enhanced.py --exports ./discord_exports --username "dirvine."
```

This will create:
- `user_complete_archive.md` - Markdown format
- `user_complete_archive.html` - Beautiful HTML page (open in browser!)
- `user_digest.json` - Machine-readable JSON
- `user_weekly_digest.md` - Last 7 days in markdown

### Generate Only HTML

```bash
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --html-only \
  --html-output dirvine_complete.html
```

### Generate Only JSON

```bash
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --json-only \
  --json-output dirvine_messages.json
```

### Custom Date Range (Last 30 Days)

```bash
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --weekly-only \
  --days 30 \
  --weekly-output last_30_days.md
```

### All Available Options

```bash
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \                    # Required: directory with JSON exports
  --username "dirvine." \                          # Username to analyze
  --archive-output complete_archive.md \           # Markdown output filename
  --html-output complete_archive.html \            # HTML output filename
  --json-output message_digest.json \              # JSON output filename
  --weekly-output weekly_digest.md \               # Weekly digest filename
  --days 7 \                                       # Number of days for weekly digest
  --archive-only                                   # Generate only markdown archive
  --html-only                                      # Generate only HTML
  --json-only                                      # Generate only JSON
  --weekly-only                                    # Generate only weekly digest
  --no-weekly                                      # Skip weekly digest generation
```

## 🔍 Method 2: Web Query Builder (Advanced Filtering)

### Start the Web Interface

```bash
python3 discord_query_builder.py ./discord_exports 5000
```

Then open your browser to: **http://localhost:5000**

### Features

The web interface provides:

#### 🎯 Advanced Filters
- **Username**: Filter by specific user
- **Include Replies**: Show replies to that user's messages
- **Channels**: Select one or multiple channels
- **Servers**: Filter by Discord server
- **Keyword Search**: Find messages containing specific text
- **Date Range**: Filter between specific dates
- **Limit**: Control max number of results

#### 📈 Real-time Statistics
- Total message count
- Date range coverage
- Top authors (in results)
- Messages by channel
- Messages by date

#### 💾 Export Options
- **JSON Export**: Machine-readable format with full metadata
- **CSV Export**: Import into spreadsheets (Excel, Google Sheets)

### Example Queries

**Find all messages from dirvine about "node":**
- Username: `dirvine.`
- Keyword: `node`
- Click Search

**Get all conversations in #general-chat last month:**
- Channels: `general-chat`
- Date From: `2024-10-01`
- Date To: `2024-10-31`
- Click Search

**Find all questions asked to dirvine:**
- Username: `dirvine.`
- Include Replies: ✓ (checked)
- Keyword: `?`
- Click Search

## 📁 Output Formats Explained

### Markdown (.md)
- Human-readable text format
- Great for GitHub, documentation
- Easy to convert to other formats
- Shows message threads and context

### HTML (.html)
- **Beautiful, styled web page**
- Discord-themed dark mode design
- Responsive (works on mobile)
- Hover effects and smooth scrolling
- Click links to jump to Discord

#### HTML Features:
- Date headers for easy navigation
- Channel badges
- Author highlighting
- Reply context (shows what was replied to)
- Direct links to original Discord messages
- Mobile-friendly responsive design

### JSON (.json)
- Machine-readable structured data
- Perfect for:
  - AI/LLM analysis
  - Data science workflows
  - Custom processing scripts
  - Database imports
- Includes full metadata and timestamps

## 🤖 GitHub Actions Automation

### Automated Weekly Digests

Create `.github/workflows/digest.yml`:

```yaml
name: Generate Weekly Digests

on:
  schedule:
    - cron: '0 22 * * 0'  # Every Sunday at 22:00 UTC
  workflow_dispatch:       # Manual trigger

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Download DiscordChatExporter
        run: |
          wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip
          unzip DiscordChatExporter.Cli.linux-x64.zip -d exporter
          chmod +x exporter/DiscordChatExporter.Cli
      
      - name: Export channels
        env:
          DISCORD_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
        run: |
          mkdir -p exports
          ./exporter/DiscordChatExporter.Cli export \
            -t "$DISCORD_TOKEN" \
            -c "CHANNEL_ID_HERE" \
            -f Json \
            -o "exports/channel.json"
      
      - name: Generate digests
        run: |
          python3 discord_digest_enhanced.py \
            --exports exports \
            --username "dirvine." \
            --html-output dirvine_archive.html \
            --json-output dirvine_digest.json
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: digests-${{ github.run_number }}
          path: |
            *.html
            *.json
            *.md
          retention-days: 90
```

## 📊 Example Use Cases

### 1. Track Community Leader Activity

```bash
# Generate HTML archive for easy browsing
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --html-only \
  --html-output dirvine_complete.html

# Open in browser to see all messages with beautiful formatting
```

### 2. Export for AI Analysis

```bash
# Generate JSON for feeding into Claude/ChatGPT
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --json-only \
  --json-output dirvine_for_ai.json

# The JSON includes full context and can be uploaded to AI chat
```

### 3. Create Monthly Reports

```bash
# Get last 30 days
python3 discord_digest_enhanced.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --weekly-only \
  --days 30 \
  --weekly-output october_report.md
```

### 4. Research Specific Topics

```bash
# Start web interface
python3 discord_query_builder.py ./discord_exports

# Use keyword search for "autonomi" or "node" or "network"
# Export results as CSV for analysis in Excel
```

### 5. Monitor Support Channels

```bash
# Query builder: filter by #general-support channel
# Keyword: "error" or "problem" or "help"
# Date range: Last 7 days
# Export as CSV to track support trends
```

## 🎨 HTML Output Features

The HTML archive includes:

### Visual Design
- Discord-themed dark mode (matches Discord's UI)
- Purple/blue gradient header
- Smooth animations and hover effects
- Card-based message layout
- Responsive design (mobile-friendly)

### Organization
- Messages grouped by date
- Day-of-week headers (Monday, Tuesday, etc.)
- Channel badges with color coding
- Time stamps for each message

### Interactivity
- Hover to highlight messages
- Click links to jump to Discord
- Smooth scrolling
- Reply context shown inline

### Statistics Banner
- Total message count
- Date range coverage
- Generation timestamp

## 📝 File Structure

```
project/
├── discord_digest_enhanced.py      # Main generator script
├── discord_query_builder.py        # Web interface
├── discord_exports/                # Your exported JSON files
│   ├── general-chat.json
│   ├── general-support.json
│   └── bug-reports.json
├── templates/                      # Auto-generated
│   └── index.html                 # Web UI template
└── outputs/                       # Generated files
    ├── user_complete_archive.md
    ├── user_complete_archive.html
    ├── user_digest.json
    └── user_weekly_digest.md
```

## 🔒 Security Notes

**NEVER commit:**
- Discord tokens
- Actual message exports
- Real server/channel IDs in public repos
- Personal configuration files

**Always use:**
- GitHub Secrets for tokens
- `.gitignore` for exports directory
- Placeholder values in documentation

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting code
- Documentation improvements

## 📜 License

MIT License - See LICENSE file for details

## 🆘 Troubleshooting

### "No JSON files found"
- Check that exports directory contains `.json` files
- Verify exports were created with JSON format (not HTML/TXT)

### "No messages found for user"
- Check username spelling and capitalization
- Try searching with lowercase (script converts to lowercase)
- Verify the user has messages in the exported channels

### Web interface won't start
- Install Flask: `pip install flask`
- Check port is not in use: `lsof -i :5000`
- Try a different port: `python3 discord_query_builder.py ./discord_exports 8080`

### HTML file is blank or broken
- Open the HTML file in a modern browser (Chrome, Firefox, Safari)
- Check browser console for errors (F12)
- Verify the file isn't empty: `ls -lh user_complete_archive.html`

## 🎯 Next Steps

1. **Export your channels** using DiscordChatExporter
2. **Generate HTML archive** to browse messages beautifully
3. **Generate JSON** for AI analysis
4. **Start web interface** for advanced queries
5. **Set up GitHub Actions** for automated weekly digests

---

**Made with ❤️ for the Autonomi community**
