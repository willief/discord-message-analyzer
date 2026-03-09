#!/bin/bash
# End-to-End Test Suite for Discord Analyser
# Tests the complete workflow from export to digest generation

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$BASE_DIR/tests"
E2E_DIR="$TEST_DIR/e2e_output"
DCE_CLI="$BASE_DIR/tools/DiscordChatExporter.Cli"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_test() {
    echo -e "${GREEN}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "=========================================="
echo "Discord Analyser E2E Test Suite"
echo "=========================================="
echo ""

# Clean previous test outputs
rm -rf "$E2E_DIR"
mkdir -p "$E2E_DIR"

# Test 1: Verify DiscordChatExporter exists and is executable
log_test "Test 1: DiscordChatExporter availability"
echo "--------------------------------------------"

if [ ! -f "$DCE_CLI" ]; then
    log_fail "DiscordChatExporter not found at $DCE_CLI"
    exit 1
fi

if [ ! -x "$DCE_CLI" ]; then
    log_fail "DiscordChatExporter is not executable"
    log_warn "Run: chmod +x $DCE_CLI"
    exit 1
fi

log_pass "DiscordChatExporter found and executable"

# Test version command
if "$DCE_CLI" --version > /dev/null 2>&1; then
    VERSION=$("$DCE_CLI" --version 2>&1 | head -1)
    log_pass "Version check successful: $VERSION"
else
    log_fail "Could not get DiscordChatExporter version"
    exit 1
fi

echo ""

# Test 2: Verify token file structure
log_test "Test 2: Token file structure"
echo "------------------------------"

TOKEN_FILE="$HOME/.discord/token"

if [ ! -f "$TOKEN_FILE" ]; then
    log_warn "Token file not found at $TOKEN_FILE"
    log_warn "E2E export tests will be skipped"
    log_warn "To enable export tests: echo 'YOUR_TOKEN' > $TOKEN_FILE && chmod 600 $TOKEN_FILE"
    SKIP_EXPORT_TESTS=true
else
    TOKEN_PERMS=$(stat -c "%a" "$TOKEN_FILE" 2>/dev/null || stat -f "%A" "$TOKEN_FILE" 2>/dev/null)
    if [ "$TOKEN_PERMS" != "600" ]; then
        log_warn "Token file has insecure permissions: $TOKEN_PERMS"
        log_warn "Recommended: chmod 600 $TOKEN_FILE"
    else
        log_pass "Token file exists with secure permissions"
    fi
    
    TOKEN=$(cat "$TOKEN_FILE")
    if [ -z "$TOKEN" ]; then
        log_warn "Token file is empty"
        SKIP_EXPORT_TESTS=true
    else
        log_pass "Token file contains data"
    fi
fi

echo ""

# Test 3: Test with fixture data (always runs)
log_test "Test 3: Processing with fixture data"
echo "---------------------------------------"

python3 "$BASE_DIR/discord_digest.py" \
    --username "dirvine." \
    --exports "$TEST_DIR/fixtures" \
    --archive-output "$E2E_DIR/fixture_archive.md" \
    --weekly-output "$E2E_DIR/fixture_weekly.md" \
    --json-output "$E2E_DIR/fixture_digest.json" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    log_pass "Successfully processed fixture data"
    
    # Verify outputs
    if [ -f "$E2E_DIR/fixture_archive.md" ] && [ -f "$E2E_DIR/fixture_digest.json" ]; then
        log_pass "All output files created"
    else
        log_fail "Some output files missing"
        exit 1
    fi
else
    log_fail "Failed to process fixture data"
    exit 1
fi

echo ""

# Test 4: Export with real Discord API (conditional)
if [ "$SKIP_EXPORT_TESTS" = true ]; then
    log_warn "Skipping export tests (no valid token)"
    echo ""
else
    log_test "Test 4: Real Discord export (dry run)"
    echo "---------------------------------------"
    log_warn "This test requires network access and a valid Discord token"
    log_warn "It will attempt to export just 1 day of messages from a test channel"
    
    # Use a well-known public server channel for testing
    # Autonomi General chat channel ID (from your setup)
    TEST_CHANNEL_ID="1209059622586163272"
    
    echo "Attempting export from Autonomi General #general-chat (last 1 day)..."
    
    "$DCE_CLI" export \
        -t "$TOKEN" \
        -c "$TEST_CHANNEL_ID" \
        -f Json \
        --after "$(date -d '1 day ago' +%Y-%m-%d)" \
        -o "$E2E_DIR/e2e_test_export.json" > "$E2E_DIR/export.log" 2>&1
    
    EXPORT_EXIT_CODE=$?
    
    if [ $EXPORT_EXIT_CODE -eq 0 ]; then
        log_pass "Export completed successfully"
        
        # Verify exported file
        if [ -f "$E2E_DIR/e2e_test_export.json" ]; then
            FILE_SIZE=$(stat -f%z "$E2E_DIR/e2e_test_export.json" 2>/dev/null || stat -c%s "$E2E_DIR/e2e_test_export.json")
            if [ "$FILE_SIZE" -gt 100 ]; then
                log_pass "Export file created (${FILE_SIZE} bytes)"
                
                # Test 5: Process real export
                log_test "Test 5: Processing real export"
                echo "-----------------------------------"
                
                mkdir -p "$E2E_DIR/real_exports"
                cp "$E2E_DIR/e2e_test_export.json" "$E2E_DIR/real_exports/"
                
                python3 "$BASE_DIR/discord_digest.py" \
                    --username "dirvine." \
                    --exports "$E2E_DIR/real_exports" \
                    --archive-output "$E2E_DIR/real_archive.md" \
                    --weekly-output "$E2E_DIR/real_weekly.md" \
                    --json-output "$E2E_DIR/real_digest.json"
                
                if [ $? -eq 0 ]; then
                    log_pass "Successfully processed real export"
                    
                    # Count messages in JSON
                    MSG_COUNT=$(python3 -c "import json; d=json.load(open('$E2E_DIR/real_digest.json')); print(len(d['messages']))" 2>/dev/null || echo "0")
                    log_pass "Found $MSG_COUNT messages in digest"
                else
                    log_fail "Failed to process real export"
                    exit 1
                fi
            else
                log_warn "Export file is very small (${FILE_SIZE} bytes) - might be empty"
            fi
        else
            log_fail "Export file not created"
            exit 1
        fi
    else
        log_fail "Export failed with exit code $EXPORT_EXIT_CODE"
        log_warn "Check $E2E_DIR/export.log for details"
        
        # Show last few lines of error log
        if [ -f "$E2E_DIR/export.log" ]; then
            echo "Last 10 lines of export log:"
            tail -10 "$E2E_DIR/export.log"
        fi
        
        # Don't fail the entire test suite if export fails
        # (might be rate limited, network issues, etc.)
        log_warn "Export test failed but continuing with other tests"
    fi
    
    echo ""
fi

# Test 6: Full automation script (dry run)
log_test "Test 6: Automation script validation"
echo "--------------------------------------"

if [ -f "$BASE_DIR/run_digest.sh" ]; then
    # Check script syntax
    bash -n "$BASE_DIR/run_digest.sh"
    if [ $? -eq 0 ]; then
        log_pass "run_digest.sh syntax valid"
    else
        log_fail "run_digest.sh has syntax errors"
        exit 1
    fi
    
    # Check if script is executable
    if [ -x "$BASE_DIR/run_digest.sh" ]; then
        log_pass "run_digest.sh is executable"
    else
        log_warn "run_digest.sh is not executable (chmod +x recommended)"
    fi
else
    log_fail "run_digest.sh not found"
    exit 1
fi

# Test multi-user script
if [ -f "$BASE_DIR/run_multi_user_digests.sh" ]; then
    bash -n "$BASE_DIR/run_multi_user_digests.sh"
    if [ $? -eq 0 ]; then
        log_pass "run_multi_user_digests.sh syntax valid"
    else
        log_fail "run_multi_user_digests.sh has syntax errors"
        exit 1
    fi
else
    log_fail "run_multi_user_digests.sh not found"
    exit 1
fi

echo ""

# Test 7: Autonomi CLI detection
log_test "Test 7: Autonomi CLI availability"
echo "-----------------------------------"

if command -v ant &> /dev/null; then
    ANT_VERSION=$(ant --version 2>&1 | head -1)
    log_pass "Autonomi CLI found: $ANT_VERSION"
else
    log_warn "Autonomi CLI not found"
    log_warn "Install with: cargo install autonomi-cli"
    log_warn "Upload tests will be skipped"
fi

echo ""

# Summary
echo "=========================================="
echo "E2E Test Summary"
echo "=========================================="
echo "Test outputs available in: $E2E_DIR"
echo ""

if [ "$SKIP_EXPORT_TESTS" = true ]; then
    echo "Note: Export tests were skipped (no Discord token)"
    echo "To enable: echo 'YOUR_TOKEN' > ~/.discord/token && chmod 600 ~/.discord/token"
fi

echo ""
log_pass "All E2E tests completed!"
echo "=========================================="