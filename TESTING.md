# Testing Suite Documentation

## Overview

Three test scripts to ensure your Discord export and digest pipeline is working correctly:

1. **verify_exporter.py** - Pre-export checks (run BEFORE exporting)
2. **test_discord_digest.py** - Post-export validation (run AFTER exporting)
3. **test_query_builder.py** - Query builder functionality tests
4. **test_integration.py** - Complete pipeline integration test

---

## 1️⃣ Pre-Export Verification

Run this BEFORE exporting to ensure DiscordChatExporter is set up correctly.

### Usage

```bash
python3 verify_exporter.py
```

### What It Checks

✅ **DiscordChatExporter Installation**
   - Checks if the binary exists in expected locations
   - Verifies it's the correct file

✅ **Executable Permissions**
   - Ensures the file can be executed
   - Gets version information

✅ **Discord Token Configuration**
   - Checks if DISCORD_TOKEN environment variable is set
   - Protects your token (only shows first 10 characters)

✅ **Output Directory**
   - Verifies export destination exists
   - Checks common locations: `./digests`, `./discord_exports`, `./exports`

### Example Output

```
================================================================================
DiscordChatExporter Pre-Export Verification
================================================================================

================================================================================
VERIFICATION RESULTS
================================================================================

✓ PASSED:
  ✓ DiscordChatExporter Installation: Found at ./discord-exporter/DiscordChatExporter.Cli
  ✓ Executable Permissions: Executable (DiscordChatExporter 2.43.1)
  ✓ Discord Token: Configured (MTIzNDU2...)
  ✓ Output Directory: Found ./digests

================================================================================
SUMMARY
================================================================================
Passed: 4
Warnings: 0
Failed: 0

✅ ALL CHECKS PASSED - Ready to export!
================================================================================
```

### Show Export Examples

```bash
python3 verify_exporter.py --show-examples
```

This displays example commands for exporting channels.

---

## 2️⃣ Post-Export Testing

Run this AFTER exporting to verify your exports are fresh and complete.

### Usage

```bash
# Basic test
python3 test_discord_digest.py --exports ./digests

# Check specific user
python3 test_discord_digest.py --exports ./digests --username "dirvine."

# Also verify DiscordChatExporter
python3 test_discord_digest.py --exports ./digests --check-exporter
```

### What It Tests

#### Test 1: Export Files Exist
- Verifies JSON files are present in the exports directory
- Counts total files found

#### Test 2: Exports Are Fresh
- Checks if files were modified within the last 7 days
- **WARNING** if any files are older (may indicate stale exports)
- Shows last modification time for stale files

#### Test 3: JSON Files Valid
- Verifies each file is valid JSON
- Checks for required structure (`channel`, `messages` keys)
- Reports any malformed files

#### Test 4: Expected Channels Present
- Verifies important channels are included:
  - `general-chat`
  - `general-support`
  - `bug-reports`
- **WARNING** if any expected channels are missing

#### Test 5: Recent Activity Detected
- Checks for messages within the last 24 hours
- Shows latest message timestamp per channel
- **WARNING** if a channel has no recent activity

#### Test 6: Target User Activity
- Verifies the target user has posted recently (last 7 days)
- Shows message count per channel
- **WARNING** if user has no recent messages

#### Test 7: File Sizes OK
- Checks that files aren't empty or suspiciously small
- **ERROR** if any file is 0 bytes
- **WARNING** if file is < 1KB
- Shows total size across all files

### Example Output

```
================================================================================
Discord Digest Generator - Test Suite
================================================================================
Testing directory: ./digests

================================================================================
TEST RESULTS
================================================================================

✓ PASSED TESTS:
  ✓ Export Files Exist: Found 9 export files
  ✓ Exports Are Fresh: All exports modified within last 7 days
  ✓ JSON Files Valid: All JSON files are valid
  ✓ Expected Channels Present: Found channels: bug-reports, general-chat, general-support
  ✓ general-chat: 45 messages in last 24h, latest 2 hours ago
  ✓ general-support: 12 messages in last 24h, latest 5 hours ago
  ✓ bug-reports: 3 messages in last 24h, latest 8 hours ago
  ✓ Target User Activity: 8 messages from 'dirvine.' in last 7 days
    By channel: general-chat: 5, general-support: 2, bug-reports: 1
  ✓ File Sizes OK: Total 12.45 MB across all files

================================================================================
SUMMARY
================================================================================
Passed: 9
Warnings: 0
Errors: 0

✅ ALL TESTS PASSED
================================================================================
```

### Exit Codes

- **0** - All tests passed
- **1** - One or more tests failed

Useful for automation scripts:

```bash
python3 test_discord_digest.py --exports ./digests
if [ $? -eq 0 ]; then
    echo "Tests passed, generating digest..."
    python3 discord_digest.py --exports ./digests --username "dirvine."
else
    echo "Tests failed, check exports!"
    exit 1
fi
```

---

## 🔄 Complete Workflow

### Step 1: Verify Setup (Before First Run)
```bash
python3 verify_exporter.py --show-examples
```

### Step 2: Export Channels
```bash
./discord-exporter/DiscordChatExporter.Cli export \
  -t "$DISCORD_TOKEN" \
  -c "CHANNEL_ID" \
  -f Json \
  -o "digests/channel.json"
```

### Step 3: Test Exports
```bash
python3 test_discord_digest.py --exports ./digests --username "dirvine."
```

### Step 4: Generate Digest (If Tests Pass)
```bash
python3 discord_digest.py --exports ./digests --username "dirvine."
```

---

## 🤖 Automated Testing Script

Create `run_digest_pipeline.sh`:

```bash
#!/bin/bash
set -e  # Exit on error

echo "📋 Starting digest pipeline..."

# Step 1: Verify exports are fresh
echo "🔍 Testing exports..."
python3 test_discord_digest.py --exports ./digests --username "dirvine."

if [ $? -ne 0 ]; then
    echo "❌ Export tests failed!"
    echo "💡 Tip: Re-run your export commands to get fresh data"
    exit 1
fi

# Step 2: Generate digest
echo "📊 Generating digest..."
python3 discord_digest.py --exports ./digests --username "dirvine."

# Step 3: Verify outputs
echo "✅ Checking outputs..."
if [ -f "outputs/user_complete_archive.html" ]; then
    echo "✓ HTML archive created"
    ls -lh outputs/user_complete_archive.html
else
    echo "❌ HTML archive missing!"
    exit 1
fi

echo "🎉 Pipeline complete!"
```

Make it executable:
```bash
chmod +x run_digest_pipeline.sh
./run_digest_pipeline.sh
```

---

## 🔧 Common Issues and Solutions

### Issue: "No JSON files found"
**Solution:** Check the `--exports` path is correct
```bash
ls -la ./digests/
```

### Issue: "Exports older than 7 days"
**Solution:** Re-run your DiscordChatExporter commands to get fresh data

### Issue: "No recent activity detected"
**Solution:** This might be normal if channels are quiet. Check Discord to verify.

### Issue: "Target user has no recent messages"
**Solution:** Verify the username is correct (case-insensitive, but must match)

### Issue: "DiscordChatExporter not found"
**Solution:** Install it:
```bash
wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip
unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter
chmod +x discord-exporter/DiscordChatExporter.Cli
```

---

## 📊 Integration with GitHub Actions

Add to your workflow:

```yaml
- name: Verify DiscordChatExporter
  run: python3 verify_exporter.py

- name: Export channels
  run: |
    # Your export commands here

- name: Test exports
  run: python3 test_discord_digest.py --exports ./digests --username "dirvine."

- name: Generate digest
  if: success()
  run: python3 discord_digest.py --exports ./digests --username "dirvine."
```

---

## 🎯 Next Steps

1. ✅ Run `verify_exporter.py` to check setup
2. ✅ Export your Discord channels
3. ✅ Run `test_discord_digest.py` to verify exports
4. ✅ Generate digest with `discord_digest.py`
5. ✅ Open `outputs/user_complete_archive.html` in browser

---

**Pro Tip:** Add these test scripts to your automation pipeline to catch issues early!

---

## 3️⃣ Query Builder Testing

Run this to test the web query builder interface.

### Usage

```bash
# Start the query builder first
python3 discord_query_builder.py ./digests 5000 &

# Then run tests
python3 test_query_builder.py --exports ./digests
```

### What It Tests

- **Server Running**: Checks if accessible
- **Query Endpoint**: Tests API responses
- **Filters**: Username, date range, keyword, limit
- **Export**: JSON and CSV downloads
- **Statistics**: Message counts, date ranges, breakdowns

### Performance Testing

```bash
python3 test_query_builder.py --exports ./digests --performance
```

Tests query speed with different result sizes.

---

## 4️⃣ Integration Testing

Tests the complete pipeline end-to-end.

### Usage

```bash
python3 test_integration.py --exports ./digests --username "dirvine."
```

### What It Does

1. Validates exports
2. Generates digest
3. Verifies outputs
4. Tests query builder (if running)

Provides a complete health check of your pipeline!

---

## 🔄 Complete Test Workflow

```bash
# 1. Verify setup (before first run)
python3 verify_exporter.py

# 2. Test exports (after exporting)
python3 test_discord_digest.py --exports ./digests --username "dirvine."

# 3. Run integration test (tests everything)
python3 test_integration.py --exports ./digests --username "dirvine."

# 4. Test query builder (if using web interface)
python3 discord_query_builder.py ./digests 5000 &
python3 test_query_builder.py --exports ./digests --performance
```

---

## 📊 Test Summary

| Test | When to Run | What It Checks | Required |
|------|-------------|----------------|----------|
| **verify_exporter** | Before exporting | DiscordChatExporter setup | Yes |
| **test_discord_digest** | After exporting | Export freshness & validity | Yes |
| **test_query_builder** | When using web UI | Query builder functionality | Optional |
| **test_integration** | Anytime | Complete pipeline | Recommended |

---

## 🎯 CI/CD Integration

Add to your automation:

```yaml
- name: Test exports
  run: python3 test_discord_digest.py --exports ./digests --username "dirvine."

- name: Run integration tests
  run: python3 test_integration.py --exports ./digests --username "dirvine."
```

---

**All tests are designed to be automation-friendly with proper exit codes!**
