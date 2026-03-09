# Discord Digest Generator - Quick Reference

## 👥 Users Being Tracked

1. **dirvine.**
2. **Bux**
3. **JimCollinson** ✨ NEW!

## 📺 Channels Being Monitored

1. **#general-chat** (1209059622586163272)
2. **#general-support** (1247881515107483759)
3. **#bug-reports** (1290643554267566130)
4. **#hot-topics** (1315677640581054464) ✨ NEW!

---

## 🚀 Quick Start

### One Command - Complete Pipeline

```bash
# Set your Discord token
export DISCORD_TOKEN='your-discord-token-here'

# Run everything!
./run_complete_pipeline.sh
```

This will:
1. ✅ Export all 4 channels
2. ✅ Generate digests for all 3 users
3. ✅ Create HTML with emojis & reactions

---

## 📂 Output Files

```
outputs/
├── dirvine__complete_archive.html       ⭐ HTML with emojis
├── dirvine__complete_archive.md         📄 Markdown
├── dirvine__weekly.md                   📅 Last 7 days
│
├── Bux_complete_archive.html            ⭐ HTML with emojis
├── Bux_complete_archive.md              📄 Markdown
├── Bux_weekly.md                        📅 Last 7 days
│
├── JimCollinson_complete_archive.html   ⭐ HTML with emojis ✨ NEW!
├── JimCollinson_complete_archive.md     📄 Markdown ✨ NEW!
├── JimCollinson_weekly.md               📅 Last 7 days ✨ NEW!
│
└── SUMMARY.md                           📊 Overview
```

---

## 🌐 View HTML Archives

```bash
# Open all three archives
xdg-open outputs/dirvine__complete_archive.html
xdg-open outputs/Bux_complete_archive.html
xdg-open outputs/JimCollinson_complete_archive.html

# Or in Firefox
firefox outputs/dirvine__complete_archive.html &
firefox outputs/Bux_complete_archive.html &
firefox outputs/JimCollinson_complete_archive.html &
```

---

## 🎨 HTML Features

Each archive includes:
- 📊 Emojis in titles
- 📅 Calendar emoji on dates
- 🎨 Color-coded borders (green = posts, orange = replies)
- 💬 Quote boxes with context
- 👍 Reaction counts (👍 5, ❤️ 2)
- 🔗 Clickable Discord links
- 🌙 Dark theme
- 📱 Mobile responsive

---

## ⚙️ Customize

### Add More Users

Edit `generate_multi_user_digest.sh`:
```bash
USERS=("dirvine." "Bux" "JimCollinson" "NewUser")
```

### Add More Channels

Edit `export_discord_channels.sh`:
```bash
declare -A CHANNELS=(
    ["general-chat"]="1209059622586163272"
    ["general-support"]="1247881515107483759"
    ["bug-reports"]="1290643554267566130"
    ["hot-topics"]="1315677640581054464"
    ["new-channel"]="YOUR_CHANNEL_ID_HERE"
)
```

### Change Date Range

Edit `generate_multi_user_digest.sh`:
```bash
START_DATE="2024-01-01"  # Start from Jan 2024
```

### Change Weekly Period

```bash
# Last 14 days instead of 7
# Edit the script or run manually:
python3 discord_digest.py \
  --exports ./digests \
  --username "JimCollinson" \
  --weekly-only \
  --days 14
```

---

## 🔄 Run Individual Steps

### Export Only
```bash
export DISCORD_TOKEN='your-token'
./export_discord_channels.sh
```

### Generate Digests Only (Use Existing Exports)
```bash
./generate_multi_user_digest.sh
```

### Single User Digest
```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "JimCollinson"
```

---

## 📊 What Each User Gets

For **each** of the 3 users (dirvine., Bux, JimCollinson):

### Complete Archive (Since Feb 2024)
- All posts BY the user
- All replies TO the user
- From ALL 4 channels
- With emojis, reactions, quotes
- HTML + Markdown versions

### Weekly Summary
- Last 7 days of activity
- Same format as complete archive
- Markdown format

---

## 🎯 Example Workflow

```bash
# Morning: Export fresh data
export DISCORD_TOKEN='your-token'
./export_discord_channels.sh

# Then: Generate digests
./generate_multi_user_digest.sh

# View: Open in browser
firefox outputs/dirvine__complete_archive.html
firefox outputs/Bux_complete_archive.html
firefox outputs/JimCollinson_complete_archive.html
```

---

## 📅 Schedule It

Run automatically every Sunday:

```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 10 PM)
0 22 * * 0 cd /home/willie/projects/discord_analyser && DISCORD_TOKEN='your-token' ./run_complete_pipeline.sh
```

---

## 🔧 Troubleshooting

### "No messages found for JimCollinson"
- Check the username spelling is exact
- Usernames are case-sensitive
- Try: `JimCollinson`, `jimcollinson`, or check Discord for exact format

### "Channel not exported"
- Verify channel ID is correct
- Check Discord token has access to the channel
- Run export manually to see errors

### "HTML file is blank"
- Check the user has actually posted in the channels
- Verify exports completed successfully
- Look at the markdown file to see if data is there

---

## 💡 Pro Tips

1. **Test with one user first:**
   ```bash
   python3 discord_digest.py --exports ./digests --username "JimCollinson"
   ```

2. **Check exports before processing:**
   ```bash
   ls -lh digests/discord_exports/
   ```

3. **Read the summary:**
   ```bash
   cat outputs/SUMMARY.md
   ```

4. **Verify user posts:**
   ```bash
   grep -i "jimcollinson" digests/discord_exports/*.json
   ```

---

**All three users now tracked across all four channels! 🎉**
