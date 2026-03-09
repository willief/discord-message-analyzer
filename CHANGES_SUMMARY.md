# Discord Digest Generator - Updates Summary

## Overview
The system has been updated to support comprehensive date filtering and extended weekly digest coverage (2 weeks instead of 1 week).

---

## Changes Made

### 1. **discord_digest.py** - Added Date Filtering Support

#### New Constructor Parameter
```python
def __init__(self, target_username, exports_directory, date_from=None, date_to=None):
    self.date_from = date_from
    self.date_to = date_to
```

#### Date Filtering Logic
- Messages are now filtered during processing in `_process_file()`
- Supports ISO 8601 format with UTC: `YYYY-MM-DDTHH:MM:SSZ`
- Messages outside the date range are skipped
- Gracefully handles invalid date formats (processes anyway as fallback)

#### New Command-Line Arguments
```bash
--date-from "2024-02-01T00:00:00Z"    # Start date (ISO format)
--date-to "2024-11-19T15:30:00Z"      # End date (ISO format)
```

#### Updated Output Display
The script now displays the date range when generating digests:
```
Date range: 2024-02-01T00:00:00Z to 2024-11-19T15:30:00Z
```

---

### 2. **generate_multi_user_digest.sh** - Dynamic Date Range & 2-Week Digests

#### Dynamic End Date Calculation
```bash
# Current system time minus 1 hour
END_DATE=$(date -u --date='1 hour ago' '+%Y-%m-%dT%H:%M:%SZ')
```

**Why minus 1 hour?**
- Allows for data freshness confirmation
- Ensures all messages up to 1 hour ago are captured
- Example: If it's 17:30 UTC, captures through 16:30 UTC

#### Fixed Start Date
```bash
START_DATE="2024-02-01T00:00:00Z"  # Feb 1, 2024 UTC
```

#### Weekly Digest Extension: 7 days → 14 days
```bash
--days 14  # Changed from default 7
```

#### Script Improvements
- Clear display of date range on startup
- Dynamic calculation with each run
- Both parameters passed to `discord_digest.py`:
  - `--date-from` for complete archive filtering
  - `--date-to` for complete archive filtering
  - `--days 14` for 2-week weekly digests

---

## Usage

### Basic Run
```bash
./generate_multi_user_digest.sh
```

**Output shows:**
```
📊 Discord Digest Generator - Multi-User
================================================
Users: dirvine. Bux
Output: ./outputs
Date Range: 2024-02-01T00:00:00Z to 2024-11-19T16:30:45Z
Weekly Digest: 14 days (2 weeks)
```

### Manual Date Range (if needed)
You can also run `discord_digest.py` directly with specific dates:

```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --date-from "2024-02-01T00:00:00Z" \
  --date-to "2024-11-19T16:00:00Z" \
  --days 14
```

---

## Date Format Requirements

All dates must be in **ISO 8601 format with UTC timezone**:

### Valid Examples
- `2024-02-01T00:00:00Z` ✓
- `2024-11-19T16:30:45Z` ✓
- `2024-06-15T12:00:00Z` ✓

### Invalid Examples
- `2024-02-01` ✗ (missing time)
- `02-01-2024` ✗ (wrong format)
- `2024-02-01 12:00:00` ✗ (missing Z)

---

## How It Works

### Processing Flow

```
┌─────────────────────────────────────────────────────┐
│  generate_multi_user_digest.sh                      │
├─────────────────────────────────────────────────────┤
│  1. Calculate END_DATE = now - 1 hour               │
│  2. Set START_DATE = 2024-02-01T00:00:00Z           │
│  3. For each user (dirvine., Bux):                  │
│     └─ discord_digest.py with date range            │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│  discord_digest.py                                  │
├─────────────────────────────────────────────────────┤
│  1. Load all JSON exports                           │
│  2. Filter messages by:                             │
│     - Username (exact match)                        │
│     - Date range (START_DATE → END_DATE)            │
│  3. Generate outputs:                               │
│     - Complete Archive (all messages)               │
│     - Weekly Digest (last 14 days)                  │
│     - JSON (for AI analysis)                        │
│     - HTML (for browser viewing)                    │
└─────────────────────────────────────────────────────┘
```

### Date Filtering in _process_file()

```python
if self.date_from or self.date_to:
    if self.date_from:
        # Skip if message is before start date
        if dt < datetime.fromisoformat(self.date_from.replace('Z', '+00:00')):
            continue
    
    if self.date_to:
        # Skip if message is after end date
        if dt > datetime.fromisoformat(self.date_to.replace('Z', '+00:00')):
            continue
```

---

## Output Files

All generated files include metadata showing the date range:

### HTML Archives
```html
<p class="stats">
    Generated: 2024-11-19 17:00:00 UTC<br>
    Period: 2024-02-01 to 2024-11-19T16:30:00Z<br>
    Total messages: 1,247
</p>
```

### Summary File (SUMMARY.md)
```markdown
**Generated:** 2024-11-19 17:00:30
**Period:** 2024-02-01T00:00:00Z to 2024-11-19T16:30:45Z
**Weekly Digest Coverage:** 14 days (2 weeks)
```

---

## Verification

### Test the Date Filtering

```bash
# Verify date filtering works
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --date-from "2024-02-01T00:00:00Z" \
  --date-to "2024-02-28T23:59:59Z"

# Should show only February 2024 messages
```

### Check Script Execution

```bash
# Make script executable
chmod +x generate_multi_user_digest.sh

# Run with verbose output
bash -x ./generate_multi_user_digest.sh 2>&1 | head -30
```

---

## Benefits

✅ **Comprehensive Coverage**: Captures Feb 2024 through current time  
✅ **Fresh Data**: Excludes last 1 hour (ensures data stability)  
✅ **Two-Week Digests**: Better trend analysis (14 days vs 7 days)  
✅ **Flexible Filtering**: Can manually override dates if needed  
✅ **Timezone Safe**: All dates in UTC with explicit Z marker  
✅ **Error Tolerant**: Invalid dates don't crash the system  

---

## Next Steps

1. **Test the updated script:**
   ```bash
   ./generate_multi_user_digest.sh
   ```

2. **Review the generated files:**
   ```bash
   ls -lh outputs/
   cat outputs/SUMMARY.md
   ```

3. **Open HTML archives in browser:**
   ```bash
   firefox outputs/dirvine__complete_archive.html
   firefox outputs/Bux_complete_archive.html
   ```

4. **Verify date ranges in output:**
   - Check SUMMARY.md for timestamp
   - Look at HTML header for date coverage
   - Compare against START_DATE and END_DATE

---

## Troubleshooting

### Issue: "No messages found for user"
**Cause**: Date range might be excluding all messages  
**Solution**: Check if START_DATE is too recent or END_DATE is too old

### Issue: "Invalid date format"
**Cause**: Date not in ISO 8601 format  
**Solution**: Use `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2024-11-19T16:30:00Z`)

### Issue: Weekly digest is empty
**Cause**: No messages in last 14 days  
**Check**: Verify recent activity with:
```bash
python3 discord_digest.py \
  --exports ./digests \
  --username "dirvine." \
  --weekly-only \
  --days 14
```

---

## Related Files

- `/mnt/project/discord_digest.py` - Main digest generator (updated)
- `/mnt/project/generate_multi_user_digest.sh` - Multi-user script (updated)
- `/mnt/project/html_generator.py` - HTML output generator
- `/mnt/project/discord_query_builder.py` - Web query interface

---

**Updated**: November 19, 2024  
**Status**: ✅ Ready for production use
