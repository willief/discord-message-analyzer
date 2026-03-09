# Discord Digest Generator - Quick Reference

## ✅ Updates Successfully Applied

### 1. Date Filtering Support Added to discord_digest.py

**New Arguments:**
```bash
--date-from "2024-02-01T00:00:00Z"    # Start date (ISO 8601)
--date-to "2024-11-19T16:30:00Z"      # End date (ISO 8601)
```

**Verification:**
```bash
python3 discord_digest.py --help | grep date-from
```

### 2. Dynamic Date Range in generate_multi_user_digest.sh

**Start Date:** `2024-02-01T00:00:00Z` (February 1, 2024)

**End Date:** Dynamic calculation (system time - 1 hour)
```bash
# Current time: 2024-11-19 17:30:00 UTC
# End Date becomes: 2024-11-19T16:30:00Z
```

**Verification:**
```bash
./generate_multi_user_digest.sh
# Shows: Date Range: 2024-02-01T00:00:00Z to 2024-11-19T16:30:00Z
```

### 3. Two-Week Weekly Digests

**Changed:** 7 days → 14 days

**In script:**
```bash
--days 14  # Changed from default 7
```

**Effect:** Weekly digest now covers last 2 weeks instead of 1 week

---

## 🚀 Quick Start

```bash
# Make sure script is executable
chmod +x generate_multi_user_digest.sh

# Run the generator
./generate_multi_user_digest.sh

# Check the output
ls -lh outputs/
cat outputs/SUMMARY.md
```

---

## 📋 File Modifications

### discord_digest.py
- ✅ Added `date_from` and `date_to` parameters to `__init__`
- ✅ Added date filtering logic in `_process_file()`
- ✅ Added `--date-from` and `--date-to` command-line arguments
- ✅ Updated output to show date range

### generate_multi_user_digest.sh
- ✅ Added dynamic END_DATE calculation (system time - 1 hour)
- ✅ Updated START_DATE to ISO 8601 format: `2024-02-01T00:00:00Z`
- ✅ Changed weekly digest to `--days 14`
- ✅ Pass both `--date-from` and `--date-to` to discord_digest.py
- ✅ Updated SUMMARY.md to show date range and 14-day coverage

---

## 🔍 Date Format

All dates must use **ISO 8601 with UTC**:

```
YYYY-MM-DDTHH:MM:SSZ

✓ Valid:    2024-02-01T00:00:00Z
✓ Valid:    2024-11-19T16:30:45Z
✗ Invalid:  2024-02-01 (no time)
✗ Invalid:  02/01/2024 (wrong format)
```

---

## 🧪 Verification

### Check Arguments Exist
```bash
python3 discord_digest.py --help | grep -E "date-from|date-to"
```

### Check Script Syntax
```bash
bash -n generate_multi_user_digest.sh
# (no output = success)
```

### Test End Date Calculation
```bash
date -u --date='1 hour ago' '+%Y-%m-%dT%H:%M:%SZ'
# Shows: 2024-11-19T16:30:00Z (example)
```

---

## 📊 How It Works

```
generate_multi_user_digest.sh
  ↓
  1. Calculate END_DATE = now - 1 hour
  2. Set START_DATE = 2024-02-01T00:00:00Z
  3. For each user:
     └─ discord_digest.py --date-from START_DATE --date-to END_DATE --days 14
       ↓
       Filters messages by:
       - Username match
       - Date within range
       - Generates 4 outputs:
         * Complete archive (all messages)
         * Weekly digest (14 days)
         * HTML (formatted)
         * JSON (machine-readable)
```

---

## 🎯 Expected Results

### Complete Archives
- Include all messages from **Feb 1, 2024** to **current time - 1 hour**
- Organized by date
- Includes reply context and emojis

### Weekly Digests
- Include messages from **last 14 days** (not just 7)
- Better for trend analysis
- Shows recent activity

### Summary File
```markdown
**Period:** 2024-02-01T00:00:00Z to 2024-11-19T16:30:45Z
**Weekly Digest Coverage:** 14 days (2 weeks)
```

---

## ⚙️ Processing Levels

### Level 1: Export-Time Filtering
*Not implemented yet (would need DiscordChatExporter API)*

### Level 2: Processing-Time Filtering ✅
- **Implemented in:** discord_digest.py
- **How:** Messages compared to date range during processing
- **Effect:** Only messages within range are included in output

---

## 📝 Example Commands

### Process a Specific Date Range
```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --date-from "2024-02-01T00:00:00Z" \
  --date-to "2024-11-19T16:30:00Z" \
  --days 14
```

### Get Last Month Only
```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --date-from "2024-10-19T00:00:00Z" \
  --date-to "2024-11-19T16:30:00Z" \
  --weekly-only
```

### Get Only This Week
```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --date-from "2024-11-12T00:00:00Z" \
  --date-to "2024-11-19T16:30:00Z"
```

---

## 🐛 Troubleshooting

### Issue: "No messages found"
**Check:** Is date range correct? Try wider range.
```bash
python3 discord_digest.py --exports ./digests --username "test" --date-from "2024-02-01T00:00:00Z" --date-to "2025-12-31T23:59:59Z"
```

### Issue: Script returns "command not found"
**Fix:** Make executable and use correct path
```bash
chmod +x generate_multi_user_digest.sh
./generate_multi_user_digest.sh  # not bash generate_multi_user_digest.sh
```

### Issue: Date format error
**Fix:** Use ISO 8601 with Z for UTC
```bash
# WRONG: 2024-02-01
# RIGHT: 2024-02-01T00:00:00Z
```

---

## ✨ Key Benefits

| Feature | Before | After |
|---------|--------|-------|
| Date Filtering | ❌ No | ✅ Yes (ISO 8601) |
| Dynamic End Date | ❌ No | ✅ Yes (now - 1 hour) |
| Weekly Digest Period | 7 days | **14 days** |
| Start Date | Manual | **Feb 1, 2024** |
| Date Range Display | ❌ No | ✅ Yes |

---

## 📚 Related Files

- `/mnt/project/discord_digest.py` - Main generator (updated)
- `/mnt/project/generate_multi_user_digest.sh` - Multi-user script (updated)
- `/mnt/project/html_generator.py` - HTML generation
- `/mnt/project/discord_query_builder.py` - Web interface

---

## ✅ Checklist

- [x] Date filtering added to discord_digest.py
- [x] Dynamic date calculation in shell script
- [x] Weekly digest changed to 14 days
- [x] Both date parameters passed to Python script
- [x] START_DATE set to Feb 1, 2024
- [x] END_DATE calculated as system time - 1 hour
- [x] Script updated and executable
- [x] Help text includes new arguments
- [x] Documentation created

---

**Last Updated:** November 19, 2024  
**Status:** ✅ Ready for production
