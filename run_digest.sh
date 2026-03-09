#!/bin/bash
# Discord User Digest Automation Script
# Exports Discord channels and generates markdown digests for a specified user
# Now with incremental export support - only downloads new messages!

set -e  # Exit on any error

# ============================================================================
# CONFIGURATION
# ============================================================================

# Base directories
BASE_DIR="$HOME/projects/discord_analyser"
OUTPUT_DIR="$BASE_DIR/digests"
EXPORTS_DIR="$OUTPUT_DIR/discord_exports"

# DiscordChatExporter path (adjust if installed elsewhere)
DCE_CLI="$BASE_DIR/tools/DiscordChatExporter.Cli"

# Python digest generator
DIGEST_SCRIPT="$BASE_DIR/discord_digest.py"

# Target Discord username (can be overridden via command line)
TARGET_USERNAME="${1:-dirvine.}"

# Discord channel IDs
CHANNEL_GENERAL_CHAT="1209059622586163272"
CHANNEL_GENERAL_SUPPORT="1247881515107483759"
CHANNEL_BUG_REPORTS="1290643554267566130"

# Token location - CRITICAL: Keep this file secure (chmod 600)
TOKEN_FILE="$HOME/.discord/token"

# Log file
LOG_FILE="$OUTPUT_DIR/digest_generation.log"

# Minimum date for exports (fallback if no existing export found)
FALLBACK_DATE="2024-02-01"

# ============================================================================
# FUNCTIONS
# ============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $1"
    exit 1
}

check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if DiscordChatExporter exists
    if [ ! -f "$DCE_CLI" ]; then
        error_exit "DiscordChatExporter not found at $DCE_CLI"
    fi
    
    # Check if digest script exists
    if [ ! -f "$DIGEST_SCRIPT" ]; then
        error_exit "Digest script not found at $DIGEST_SCRIPT"
    fi
    
    # Check if token file exists
    if [ ! -f "$TOKEN_FILE" ]; then
        error_exit "Token file not found at $TOKEN_FILE. Create it with: echo 'YOUR_TOKEN' > $TOKEN_FILE && chmod 600 $TOKEN_FILE"
    fi
    
    # Verify token file permissions
    TOKEN_PERMS=$(stat -c "%a" "$TOKEN_FILE" 2>/dev/null || stat -f "%A" "$TOKEN_FILE" 2>/dev/null)
    if [ "$TOKEN_PERMS" != "600" ]; then
        log "WARNING: Token file has insecure permissions ($TOKEN_PERMS). Fixing..."
        chmod 600 "$TOKEN_FILE"
    fi
    
    # Check if jq is available for JSON parsing
    if ! command -v jq &> /dev/null; then
        log "WARNING: 'jq' not found. Install it for better performance: sudo apt install jq"
        log "Falling back to python for JSON parsing..."
    fi
    
    log "✓ All prerequisites met"
}

setup_directories() {
    log "Setting up directories..."
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$EXPORTS_DIR"
    log "✓ Directories ready"
}

get_last_message_timestamp() {
    local export_file=$1
    
    # Check if export file exists
    if [ ! -f "$export_file" ]; then
        echo ""
        return
    fi
    
    # Try to get the last message timestamp using jq (faster)
    if command -v jq &> /dev/null; then
        local timestamp=$(jq -r '.messages[-1].timestamp // empty' "$export_file" 2>/dev/null)
        if [ -n "$timestamp" ]; then
            echo "$timestamp"
            return
        fi
    fi
    
    # Fallback to python if jq fails or is not available
    local timestamp=$(python3 -c "
import json
import sys

try:
    with open('$export_file', 'r', encoding='utf-8') as f:
        data = json.load(f)
        messages = data.get('messages', [])
        if messages:
            print(messages[-1].get('timestamp', ''))
except Exception as e:
    pass
" 2>/dev/null)
    
    echo "$timestamp"
}

merge_json_exports() {
    local old_file=$1
    local new_file=$2
    local merged_file=$3
    
    log "  Merging old and new exports..."
    
    python3 -c "
import json
import sys
from datetime import datetime

try:
    # Read old export
    with open('$old_file', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    # Read new export
    with open('$new_file', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    # Combine messages, removing duplicates by message ID
    old_messages = old_data.get('messages', [])
    new_messages = new_data.get('messages', [])
    
    # Create a set of existing message IDs
    existing_ids = {msg['id'] for msg in old_messages}
    
    # Add only new messages that don't already exist
    added_count = 0
    for msg in new_messages:
        if msg['id'] not in existing_ids:
            old_messages.append(msg)
            added_count += 1
    
    # Sort messages by timestamp
    old_messages.sort(key=lambda x: x.get('timestamp', ''))
    
    # Update the data
    old_data['messages'] = old_messages
    
    # Write merged export
    with open('$merged_file', 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=2, ensure_ascii=False)
    
    print(f'Added {added_count} new messages')
    sys.exit(0)
    
except Exception as e:
    print(f'Error merging: {e}', file=sys.stderr)
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        # Replace old file with merged file
        mv "$merged_file" "$old_file"
        rm -f "$new_file"
    else
        error_exit "Failed to merge exports"
    fi
}

export_channel() {
    local channel_id=$1
    local channel_name=$2
    
    local export_file="$EXPORTS_DIR/${channel_name}.json"
    local temp_export_file="$EXPORTS_DIR/${channel_name}_temp.json"
    
    # Check for existing export and get last message timestamp
    local last_timestamp=$(get_last_message_timestamp "$export_file")
    
    if [ -n "$last_timestamp" ]; then
        log "Exporting #$channel_name (incremental from $last_timestamp)..."
        local after_date="$last_timestamp"
    else
        log "Exporting #$channel_name (full export from $FALLBACK_DATE)..."
        local after_date="$FALLBACK_DATE"
    fi
    
    DISCORD_TOKEN=$(cat "$TOKEN_FILE")
    
    # Export to temp file if we're doing incremental update
    local output_file="$export_file"
    if [ -f "$export_file" ]; then
        output_file="$temp_export_file"
    fi
    
    "$DCE_CLI" export \
        -t "$DISCORD_TOKEN" \
        -c "$channel_id" \
        -f Json \
        --after "$after_date" \
        -o "$output_file" 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        # If this was an incremental update, merge the files
        if [ -f "$temp_export_file" ]; then
            merge_json_exports "$export_file" "$temp_export_file" "${export_file}.merged"
        fi
        log "✓ Successfully exported #$channel_name"
    else
        error_exit "Failed to export #$channel_name"
    fi
}

generate_digests() {
    log "Generating markdown digests for user: $TARGET_USERNAME"
    
    cd "$OUTPUT_DIR"
    
    python3 "$DIGEST_SCRIPT" \
        --username "$TARGET_USERNAME" \
        --exports "$EXPORTS_DIR" \
        --archive-output "${TARGET_USERNAME}_complete_archive.md" \
        --weekly-output "${TARGET_USERNAME}_weekly_digest.md" \
        2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        log "✓ Digests generated successfully"
    else
        error_exit "Failed to generate digests"
    fi
}

create_timestamp_copy() {
    log "Creating timestamped copies..."
    
    TIMESTAMP=$(date '+%Y-%m-%d')
    
    if [ -f "$OUTPUT_DIR/${TARGET_USERNAME}_weekly_digest.md" ]; then
        cp "$OUTPUT_DIR/${TARGET_USERNAME}_weekly_digest.md" "$OUTPUT_DIR/${TARGET_USERNAME}_weekly_${TIMESTAMP}.md"
        log "✓ Created ${TARGET_USERNAME}_weekly_${TIMESTAMP}.md"
    fi
    
    if [ -f "$OUTPUT_DIR/${TARGET_USERNAME}_complete_archive.md" ]; then
        cp "$OUTPUT_DIR/${TARGET_USERNAME}_complete_archive.md" "$OUTPUT_DIR/${TARGET_USERNAME}_archive_${TIMESTAMP}.md"
        log "✓ Created ${TARGET_USERNAME}_archive_${TIMESTAMP}.md"
    fi
}

upload_to_autonomi() {
    log "Uploading to Autonomi network..."
    
    # TODO: Implement once Autonomi CLI is ready
    # Example: ant file upload -p "$OUTPUT_DIR/dirvine_complete_archive.md" "$OUTPUT_DIR/dirvine_weekly_digest.md"
    
    log "⚠ Autonomi upload not yet implemented - files available locally"
}

cleanup_old_exports() {
    log "Cleaning up temporary files..."
    
    # Remove any leftover temp files
    find "$EXPORTS_DIR" -name "*_temp.json" -delete 2>/dev/null || true
    find "$EXPORTS_DIR" -name "*.merged" -delete 2>/dev/null || true
    
    # Optional: Remove old timestamped digests (keeping last 30 days)
    # find "$OUTPUT_DIR" -name "${TARGET_USERNAME}_weekly_*.md" -mtime +30 -delete
    # find "$OUTPUT_DIR" -name "${TARGET_USERNAME}_archive_*.md" -mtime +90 -delete
    
    log "✓ Cleanup complete"
}

show_export_stats() {
    log "=========================================="
    log "Export Statistics:"
    
    for channel_file in "$EXPORTS_DIR"/*.json; do
        if [ -f "$channel_file" ]; then
            local channel_name=$(basename "$channel_file" .json)
            local message_count=$(python3 -c "
import json
try:
    with open('$channel_file', 'r') as f:
        data = json.load(f)
        print(len(data.get('messages', [])))
except:
    print(0)
")
            local file_size=$(du -h "$channel_file" | cut -f1)
            log "  #$channel_name: $message_count messages ($file_size)"
        fi
    done
    
    log "=========================================="
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    # Create directories FIRST before any logging
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$EXPORTS_DIR"

    log "=========================================="
    log "Discord User Digest Generation Started"
    log "Target user: $TARGET_USERNAME"
    log "Mode: Incremental (only new messages)"
    log "=========================================="
    
    check_prerequisites
    setup_directories
    
    # Export Discord channels (incremental)
    export_channel "$CHANNEL_GENERAL_CHAT" "general-chat"
    export_channel "$CHANNEL_GENERAL_SUPPORT" "general-support"
    export_channel "$CHANNEL_BUG_REPORTS" "bug-reports"
    
    # Show statistics
    show_export_stats
    
    # Generate digests
    generate_digests
    
    # Create timestamped copies
    create_timestamp_copy
    
    # Upload to Autonomi (placeholder)
    upload_to_autonomi
    
    # Cleanup
    cleanup_old_exports
    
    log "=========================================="
    log "Digest Generation Complete!"
    log "=========================================="
    log "Files available at: $OUTPUT_DIR"
    log "  - ${TARGET_USERNAME}_complete_archive.md"
    log "  - ${TARGET_USERNAME}_weekly_digest.md"
    log "  - JSON exports in: $EXPORTS_DIR"
}

# Run main function
main
