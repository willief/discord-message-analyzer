# Discord Digest Generator - Quick Reference

## One-Liners
```bash
# Export all channels
for cid in 1209059622586163272 1247881515107483759 1290643554267566130; do
  ./discord-exporter/DiscordChatExporter.Cli export -t "$TOKEN" -c $cid -f Json -o "discord_exports/channel_$cid.json"
done

# Generate all digests for all users
./generate_all_digests.sh discord_exports outputs

# View all HTML files
xdg-open outputs/*.html

# Count messages per user
grep -l "dirvine" discord_exports/*.json | xargs -I {} jq '.messages | length' {}

# Check latest message timestamp
jq '.messages[-1].timestamp' discord_exports/general-chat.json
```

## Command Examples

### Single User, All Formats, Complete Archive
```bash
python3 discord_digest.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --output ./outputs \
  --complete \
  --formats md,html,json
```

### Batch All Users
```bash
./generate_all_digests.sh discord_exports outputs
```

### Weekly Only (Markdown)
```bash
python3 discord_digest.py \
  --exports ./discord_exports \
  --username "dirvine." \
  --weekly \
  --formats md
```

### Fortnightly (HTML)
```bash
python3 discord_digest.py \
  --exports ./discord_exports \
  --username "forthebux" \
  --fortnightly \
  --formats html
```

### JSON for AI/LLM Processing
```bash
python3 discord_digest.py \
  --exports ./discord_exports \
  --username "JimCollinson" \
  --all \
  --formats json
```

### Show Help
```bash
python3 discord_digest.py --help
```

## Output File Naming
```
{safe_username}_{type}_{period}.{format}

Examples:
- dirvine__complete_archive.md
- dirvine__complete_archive.html
- dirvine__complete_archive.json
- dirvine__weekly_digest.md
- dirvine__weekly_digest.html
- dirvine__weekly_digest.json
- dirvine__fortnightly_digest.md
- forthebux__complete_archive.json
- JimCollinson__weekly_digest.html
```

## File Format Comparison

| Format | Best For | Size | View |
|--------|----------|------|------|
| **MD** | GitHub, Docs | Small | Text editor |
| **HTML** | Reading, Sharing | Medium | Browser |
| **JSON** | AI, Analysis | Large | jq, Python |

## Export Without DiscordChatExporter

If you have JSON exports already, just organize them:
```bash
mkdir -p discord_exports
cp your_exports/*.json discord_exports/
./generate_all_digests.sh discord_exports outputs
```

## Filter Messages (Post-Generation)
```bash
# Count messages in JSON
jq '.messages | length' outputs/dirvine__complete_archive.json

# Get specific date
jq '.messages[] | select(.date == "2024-11-15")' outputs/dirvine__complete_archive.json

# Search for keywords
jq '.messages[] | select(.content | contains("autonomi"))' outputs/dirvine__complete_archive.json

# Get message count by channel
jq '.messages | group_by(.channel) | map({channel: .[0].channel, count: length})' outputs/dirvine__complete_archive.json
```

## GitHub Actions Manual Run
```bash
# In GitHub Actions UI:
1. Click "Actions" tab
2. Select "Generate Discord Digests" workflow
3. Click "Run workflow" button
4. Select branch (main)
5. Click "Run workflow"

# Wait ~2 minutes, then download artifacts
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "command not found: python3" | Install Python 3, or use `python` |
| "Permission denied" | `chmod +x generate_all_digests.sh` |
| "No JSON files found" | Check `ls discord_exports/` |
| "No messages found" | Verify username spelling |
| "Token invalid" | Check Discord token in env var |
| "Channel not found" | Verify channel ID and token permissions |

## Linux/macOS Commands
```bash
# Make script executable
chmod +x generate_all_digests.sh

# Run with bash explicitly
bash generate_all_digests.sh

# View file sizes
du -sh outputs/*

# Count total files
ls outputs/ | wc -l

# View recently modified
ls -lt outputs/ | head -10

# Delete all outputs
rm outputs/*
```

## Windows (PowerShell) Commands
```powershell
# Make Python executable (usually automatic)
python discord_digest.py --help

# Run batch for all users (use Python directly)
python discord_digest.py --exports .\discord_exports --username "dirvine." --all

# For loop equivalent
@("dirvine.", "forthebux", "JimCollinson") | ForEach-Object {
    python discord_digest.py --exports .\discord_exports --username $_ --all
}

# View outputs
Get-ChildItem outputs/ | Select-Object Name, Length

# Delete outputs
Remove-Item outputs/*
```

## Environment Variables
```bash
# Set default exports directory
export DISCORD_EXPORTS=./discord_exports

# Then use in script (modify script to support this)
python3 discord_digest.py --exports $DISCORD_EXPORTS --username "dirvine." --all
```

## Cron Job (Auto-Run Weekly)
```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday 22:00)
0 22 * * 0 cd /path/to/project && ./generate_all_digests.sh discord_exports outputs

# View cron jobs
crontab -l
```

## Time Zones

All timestamps are in UTC. Adjust display or timezone as needed:
```bash
# Convert UTC to your timezone (example: EST)
TZ=America/New_York ls outputs/
```

## Debugging
```bash
# Enable verbose output (add to discord_digest.py)
import logging
logging.basicConfig(level=logging.DEBUG)

# Check Python version
python3 --version

# Verify JSON is valid
jq '.' discord_exports/general-chat.json > /dev/null && echo "Valid JSON"

# Count total messages
jq '.messages | length' discord_exports/*.json | awk '{s+=$1} END {print s}'
```

## Advanced: Analyze All Messages
```bash
# Get statistics
jq '{
  total: .messages | length,
  unique_authors: .messages | map(.author) | unique | length,
  date_range: {start: .messages[0].date, end: .messages[-1].date},
  by_channel: (.messages | group_by(.channel) | map({(.[0].channel): length}) | add)
}' outputs/dirvine__complete_archive.json | jq .
```

## Performance Tuning

For large message sets (100k+):
```bash
# Process each user sequentially (slower but safer)
for user in "dirvine." "forthebux" "JimCollinson"; do
  python3 discord_digest.py --exports ./discord_exports --username "$user" --all
  sleep 5  # Wait between runs
done

# Or in parallel (faster, needs more RAM)
parallel --jobs 3 'python3 discord_digest.py --exports ./discord_exports --username {} --all' ::: "dirvine." "forthebux" "JimCollinson"
```

---

**See README.md for full documentation**