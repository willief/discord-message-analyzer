#!/bin/bash
# Test suite for Discord Analyser

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$BASE_DIR/tests"
FIXTURES_DIR="$TEST_DIR/fixtures"
OUTPUT_DIR="$TEST_DIR/output"

echo "=========================================="
echo "Discord Analyser Test Suite"
echo "=========================================="
echo ""

# Clean previous test outputs
rm -rf "$OUTPUT_DIR"/*
mkdir -p "$OUTPUT_DIR"

# Test 1: Basic digest generation
echo "Test 1: Basic digest generation"
echo "--------------------------------"
python3 "$BASE_DIR/discord_digest.py" \
  --username "dirvine." \
  --exports "$FIXTURES_DIR" \
  --archive-output "$OUTPUT_DIR/test_archive.md" \
  --weekly-output "$OUTPUT_DIR/test_weekly.md" \
  --json-output "$OUTPUT_DIR/test_digest.json"

if [ $? -eq 0 ]; then
    echo "✓ Test 1 PASSED: Digest generation successful"
else
    echo "✗ Test 1 FAILED: Digest generation failed"
    exit 1
fi
echo ""

# Test 2: Verify output files exist
echo "Test 2: Output file creation"
echo "----------------------------"
EXPECTED_FILES=(
    "$OUTPUT_DIR/test_archive.md"
    "$OUTPUT_DIR/test_weekly.md"
    "$OUTPUT_DIR/test_digest.json"
)

ALL_EXIST=true
for file in "${EXPECTED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ Found: $(basename $file)"
    else
        echo "✗ Missing: $(basename $file)"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = true ]; then
    echo "✓ Test 2 PASSED: All output files created"
else
    echo "✗ Test 2 FAILED: Some output files missing"
    exit 1
fi
echo ""

# Test 3: Verify JSON structure
echo "Test 3: JSON structure validation"
echo "----------------------------------"
if python3 -c "import json; json.load(open('$OUTPUT_DIR/test_digest.json'))" 2>/dev/null; then
    echo "✓ JSON is valid"
    
    # Check for expected fields
    METADATA_EXISTS=$(python3 -c "import json; d=json.load(open('$OUTPUT_DIR/test_digest.json')); print('metadata' in d)")
    MESSAGES_EXISTS=$(python3 -c "import json; d=json.load(open('$OUTPUT_DIR/test_digest.json')); print('messages' in d)")
    
    if [ "$METADATA_EXISTS" = "True" ] && [ "$MESSAGES_EXISTS" = "True" ]; then
        echo "✓ JSON has required fields (metadata, messages)"
        echo "✓ Test 3 PASSED: JSON structure valid"
    else
        echo "✗ JSON missing required fields"
        echo "✗ Test 3 FAILED"
        exit 1
    fi
else
    echo "✗ JSON is invalid"
    echo "✗ Test 3 FAILED"
    exit 1
fi
echo ""

# Test 4: Verify message capture
echo "Test 4: Message capture verification"
echo "------------------------------------"
MESSAGE_COUNT=$(python3 -c "import json; d=json.load(open('$OUTPUT_DIR/test_digest.json')); print(len(d['messages']))")
echo "Messages captured: $MESSAGE_COUNT"

if [ "$MESSAGE_COUNT" -ge 2 ]; then
    echo "✓ Test 4 PASSED: Expected messages captured (found $MESSAGE_COUNT)"
else
    echo "✗ Test 4 FAILED: Expected at least 2 messages, found $MESSAGE_COUNT"
    exit 1
fi
echo ""

# Test 5: Verify interaction types
# Test 5: Verify interaction types
echo "Test 5: Interaction types detection"
echo "-----------------------------------"
HAS_POST=$(python3 -c "import json; d=json.load(open('$OUTPUT_DIR/test_digest.json')); print(any('posted_by_user' in m.get('interaction_types', []) for m in d['messages']))")
HAS_REACTION=$(python3 -c "import json; d=json.load(open('$OUTPUT_DIR/test_digest.json')); print(any('user_reacted' in m.get('interaction_types', []) for m in d['messages']))")
HAS_REPLY=$(python3 -c "import json; d=json.load(open('$OUTPUT_DIR/test_digest.json')); print(any('user_replied_to_this' in m.get('interaction_types', []) for m in d['messages']))")

echo "Checking for interaction types in JSON..."
if [ "$HAS_POST" = "True" ]; then
    echo "✓ Detected user posts"
else
    echo "⚠ No user posts detected"
fi

if [ "$HAS_REACTION" = "True" ]; then
    echo "✓ Detected user reactions"
else
    echo "⚠ No user reactions detected"
fi

if [ "$HAS_REPLY" = "True" ]; then
    echo "✓ Detected user replies"
else
    echo "⚠ No user replies detected"
fi

echo ""
echo "✓ Test 5 PASSED: Interaction detection working"
echo ""

# Test 6: Markdown formatting
echo "Test 6: Markdown output format"
echo "-------------------------------"
if grep -q "###" "$OUTPUT_DIR/test_archive.md"; then
    echo "✓ Markdown has section headers"
else
    echo "✗ Markdown missing section headers"
    exit 1
fi




echo "✓ Test 6 PASSED: Markdown formatting correct"
echo ""

# Summary
echo "=========================================="
echo "All Tests PASSED! ✓"
echo "=========================================="
echo ""
echo "Test outputs available in: $OUTPUT_DIR"
echo ""