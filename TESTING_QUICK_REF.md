# Testing Quick Reference

## 🧪 All Test Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `verify_exporter.py` | Pre-export setup check | `python3 verify_exporter.py` |
| `test_discord_digest.py` | Export validation | `python3 test_discord_digest.py --exports ./digests` |
| `test_query_builder.py` | Query builder tests | `python3 test_query_builder.py --exports ./digests` |
| `test_integration.py` | Complete pipeline test | `python3 test_integration.py --exports ./digests` |

---

## ✅ Quick Test Commands

### Before First Run
```bash
python3 verify_exporter.py
```

### After Exporting Data
```bash
python3 test_discord_digest.py --exports ./digests --username "dirvine."
```

### Test Query Builder (optional)
```bash
# Start server first
python3 discord_query_builder.py ./digests 5000 &

# Run tests
python3 test_query_builder.py --exports ./digests --performance
```

### Test Everything
```bash
python3 test_integration.py --exports ./digests --username "dirvine."
```

---

## 🎯 What Each Test Checks

### verify_exporter.py
✅ DiscordChatExporter installed  
✅ File is executable  
✅ Discord token configured  
✅ Output directory exists  

### test_discord_digest.py
✅ Export files exist  
✅ Files are fresh (< 7 days)  
✅ Valid JSON structure  
✅ Expected channels present  
✅ Recent activity detected  
✅ Target user has posts  
✅ File sizes reasonable  

### test_query_builder.py
✅ Server running  
✅ API endpoints work  
✅ Filters functional  
✅ Exports (JSON/CSV) work  
✅ Statistics calculated  
⚡ Performance benchmarks  

### test_integration.py
✅ Validates exports  
✅ Generates digest  
✅ Verifies outputs created  
✅ Tests query builder  

---

## 🚦 Exit Codes

All tests return proper exit codes for automation:
- **0** = Success
- **1** = Failure

Example:
```bash
python3 test_integration.py --exports ./digests
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed!"
fi
```

---

## 📋 Troubleshooting

### "Server not running"
```bash
# Start the query builder
python3 discord_query_builder.py ./digests 5000
```

### "No JSON files found"
```bash
# Check the path
ls -la ./digests/

# Verify you're in the right directory
pwd
```

### "test_*.py not found"
```bash
# Make sure you're in the project directory
cd ~/projects/discord_analyser

# Check files exist
ls -la test_*.py
```

### "ModuleNotFoundError: No module named 'requests'"
```bash
# Install required dependencies
pip install requests flask
```

---

## 🎬 Complete Workflow Example

```bash
#!/bin/bash
# Complete test workflow

# Step 1: Verify setup
echo "Step 1: Verifying DiscordChatExporter..."
python3 verify_exporter.py || exit 1

# Step 2: Export channels (your process here)
echo "Step 2: Exporting channels..."
# Your export commands...

# Step 3: Validate exports
echo "Step 3: Validating exports..."
python3 test_discord_digest.py --exports ./digests --username "dirvine." || exit 1

# Step 4: Run integration test
echo "Step 4: Running integration test..."
python3 test_integration.py --exports ./digests --username "dirvine." || exit 1

echo "✅ All tests passed! Pipeline is healthy."
```

---

## 📊 Expected Test Times

| Test | Duration | Notes |
|------|----------|-------|
| verify_exporter | < 5s | Fast setup check |
| test_discord_digest | 5-15s | Depends on export size |
| test_query_builder | 10-30s | Includes API tests |
| test_integration | 30-60s | Runs full pipeline |

---

## 🔧 Common Fixes

**Stale Exports Warning**
```bash
# Re-export your channels
./discord-exporter/DiscordChatExporter.Cli export ...
```

**No Recent User Activity**
```bash
# Check username format
python3 test_discord_digest.py --exports ./digests --username "username"

# Try without trailing dot
python3 test_discord_digest.py --exports ./digests --username "dirvine"
```

**Query Builder Port Conflict**
```bash
# Use different port
python3 discord_query_builder.py ./digests 8080
python3 test_query_builder.py --exports ./digests --port 8080
```

---

**For full documentation, see TESTING.md**
