#!/bin/bash
# Multi-User Discord Digest Wrapper
# Runs digest generation for multiple users from a config file

set -e

# Configuration
BASE_DIR="$HOME/projects/discord_analyser"
USERS_FILE="$BASE_DIR/users.txt"
DIGEST_SCRIPT="$BASE_DIR/run_digest.sh"
LOG_FILE="$BASE_DIR/digests/multi_user.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if users file exists
if [ ! -f "$USERS_FILE" ]; then
    log "ERROR: Users file not found at $USERS_FILE"
    log "Creating example users.txt file..."
    
    cat > "$USERS_FILE" << 'EOF'
# Discord Users to Track
# One username per line
# Lines starting with # are comments
# Empty lines are ignored

dirvine.

# Add more users below:
# someuser
# anotheruser
EOF
    
    log "✓ Created example users.txt at $USERS_FILE"
    log "  Edit this file to add the Discord usernames you want to track"
    exit 0
fi

# Check if digest script exists
if [ ! -f "$DIGEST_SCRIPT" ]; then
    log "ERROR: Digest script not found at $DIGEST_SCRIPT"
    exit 1
fi

log "=========================================="
log "Multi-User Discord Digest Generation"
log "=========================================="

# Count users (excluding comments and empty lines)
USER_COUNT=$(grep -v '^#' "$USERS_FILE" | grep -v '^$' | wc -l)
log "Found $USER_COUNT user(s) to process"
log ""

CURRENT_USER=0
SUCCESSFUL=0
FAILED=0

# Read users file and process each user
while IFS= read -r username || [ -n "$username" ]; do
    # Skip comments and empty lines
    [[ "$username" =~ ^#.*$ ]] && continue
    [[ -z "$username" ]] && continue
    
    CURRENT_USER=$((CURRENT_USER + 1))
    
    log "=========================================="
    log "Processing user $CURRENT_USER of $USER_COUNT: $username"
    log "=========================================="
    
    # Run digest for this user
    if "$DIGEST_SCRIPT" "$username"; then
        log "✓ Successfully completed digest for $username"
        SUCCESSFUL=$((SUCCESSFUL + 1))
    else
        log "✗ Failed to generate digest for $username"
        FAILED=$((FAILED + 1))
    fi
    
    log ""
    
    # Add a small delay between users to avoid overwhelming the system
    if [ $CURRENT_USER -lt $USER_COUNT ]; then
        log "Waiting 10 seconds before next user..."
        sleep 10
    fi
    
done < "$USERS_FILE"

log "=========================================="
log "Multi-User Digest Generation Complete"
log "=========================================="
log "Total users: $USER_COUNT"
log "Successful: $SUCCESSFUL"
log "Failed: $FAILED"
log "=========================================="

exit 0
