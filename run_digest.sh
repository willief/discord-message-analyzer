#!/bin/bash
# Discord User Digest Automation Script
# Exports Discord channels and generates markdown digests for a specified user

set -e  # Exit on any error

# ============================================================================
# CONFIGURATION
# ============================================================================

# Base directories
BASE_DIR="$HOME/projects/discord-analyser"
OUTPUT_DIR="$BASE_DIR/digests"
EXPORTS_DIR="$OUTPUT_DIR/discord_exports"

# DiscordChatExporter path (adjust if installed elsewhere)
DCE_CLI="$BASE_DIR/tools/DiscordChatExporter.Cli" # Python digest generator
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
    
    log "✓ All prerequisites met"
}

setup_directories() {
    log "Setting up directories..."
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$EXPORTS_DIR"
    log "✓ Directories ready"
}

export_channel() {
    local channel_id=$1
    local channel_name=$2
    
    log "Exporting #$channel_name..."
    
    DISCORD_TOKEN=$(cat "$TOKEN_FILE")
    
    "$DCE_CLI" export \
        -t "$DISCORD_TOKEN" \
        -c "$channel_id" \
        -f Json \
	--after "2024-02-01" \
        -o "$EXPORTS_DIR/${channel_name}.json" 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
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
    log "Cleaning up old exports (keeping JSON for archive)..."
    
    # Optional: Remove exports older than 90 days
    # find "$EXPORTS_DIR" -name "*.json" -mtime +90 -delete
    
    log "✓ Cleanup complete"
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
    log "=========================================="
    
    check_prerequisites
    setup_directories
    
    # Export Discord channels
    export_channel "$CHANNEL_GENERAL_CHAT" "general-chat"
    export_channel "$CHANNEL_GENERAL_SUPPORT" "general-support"
    export_channel "$CHANNEL_BUG_REPORTS" "bug-reports"
    
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
