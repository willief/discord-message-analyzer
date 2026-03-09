# Discord Digest Generator - Quick Start Guide

## 📥 Files You Need

Your working version has **2 files**:
1. **discord_digest.py** - Main script
2. **html_generator.py** - HTML generation module (imported by discord_digest.py)

Both files must be in the same directory!

## 🚀 Usage

### Generate All Formats (Markdown, HTML, JSON)

```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine."
```

This creates:
- ✅ `outputs/user_complete_archive.md` - Markdown archive
- ✅ `outputs/user_complete_archive.html` - Beautiful HTML with emojis & colors
- ✅ `outputs/user_digest.json` - JSON for AI analysis
- ✅ `outputs/user_weekly_digest.md` - Last 7 days

All files are automatically placed in the `outputs/` directory!

### Custom Output Names

```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --archive-output dirvine_complete.md \
  --json-output dirvine_digest.json
```

### Only Generate Archive (skip weekly)

```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --archive-only
```

### Last 30 Days

```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --days 30
```

### Skip JSON Output

```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --no-json
```

## 🎨 What You Get in HTML

Your HTML output includes:

### Visual Features
- 📊 Emoji in title
- 📅 Calendar emoji on date headers  
- 🎨 Color-coded message borders:
  - **Green border** - Posts by target user
  - **Orange border** - Replies to target user
- 💬 Quote boxes with truncated long quotes
- 👍 Reaction emojis with counts (e.g., 👍 2, ❤️ 1)
- 🔗 Clickable links to original Discord messages

### Smart Features
- **Truncated quotes** - Long replies shown as first 100 chars + "... [truncated]"
- **Thread context** - Shows who replied to whom
- **Clickable quoted messages** - Click on quotes to jump to original message in Discord
- **Dark theme** - Easy on the eyes

## 📂 File Organization

```
your_project/
├── discord_digest.py           # Main script
├── html_generator.py           # HTML generator
├── digests/                    # INPUT: Your JSON exports
│   └── discord_exports/
│       ├── channel1.json
│       └── channel2.json
└── outputs/                    # OUTPUT: Generated files (auto-created)
    ├── user_complete_archive.md
    ├── user_complete_archive.html
    ├── user_digest.json
    └── user_weekly_digest.md
```

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'html_generator'"

Both `discord_digest.py` and `html_generator.py` must be in the **same directory**!

```bash
# Check they're together
ls -l discord_digest.py html_generator.py
```

### "No JSON files found"

Make sure you're pointing to the right directory:

```bash
# Check what's in your digests folder
ls -la digests/discord_exports/

# Try with full path
python3 discord_digest.py --exports ~/projects/discord_analyser/digests --username "dirvine."
```

### Emojis not showing

The HTML file should work in any modern browser. Make sure you're opening the `.html` file (not the `.md` file).

## 🎯 Next: Query Builder

Want to search and filter messages? Use the query builder:

```bash
python3 discord_query_builder.py ./digests 5000
```

Then open: http://localhost:5000

## 📊 Key Differences from Enhanced Version

Your working version has:
- ✅ Split into 2 files (better organization)
- ✅ Truncated quotes (first 100 chars)
- ✅ Clickable quote links to original messages
- ✅ Color-coded borders (green for posts, orange for replies)
- ✅ Better reaction emoji display
- ✅ Quote boxes with proper styling

The enhanced version I created has:
- ✅ All-in-one file (easier to distribute)
- ✅ Query builder web interface
- ✅ More command-line options

**Use your working version!** It has all the visual features you want.

---

**Pro Tip**: Open the HTML file in your browser and bookmark it for easy access to the archive!
