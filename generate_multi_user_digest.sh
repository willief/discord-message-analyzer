#!/bin/bash
#
# Discord Digest Generator - Multi-User Script
# Generates complete archives and weekly summaries for multiple users
# Date range: Feb 2024 to current time minus 1 hour
# Weekly digests cover 14 days (2 weeks)
# With HTML output, emojis, replies, and reactions
#

set -e  # Exit on error

# Configuration
EXPORTS_DIR="./digests"
OUTPUT_DIR="./outputs"
DEFAULT_USERS=("dirvine." "forthebux" "JimCollinson")
USERS=()
START_DATE="2024-02-01T00:00:00Z"  # Feb 1, 2024 UTC start

# Calculate end date: current system time minus 1 hour
END_DATE=$(date -u --date='1 hour ago' '+%Y-%m-%dT%H:%M:%SZ')

# Function to get user input (yes/no)
confirm() {
    local prompt="$1"
    local response
    while true; do
        read -p "$prompt (yes/no): " response
        case "$response" in
            [yY][eE][sS]|[yY])
                return 0
                ;;
            [nN][oO]|[nN])
                return 1
                ;;
            *)
                echo "Please answer yes or no."
                ;;
        esac
    done
}

# Function to get list of users from user input
get_user_list() {
    local prompt="$1"
    local user_input
    read -p "$prompt (comma-separated): " user_input
    
    # Convert comma-separated input to array
    if [ -n "$user_input" ]; then
        # Split by comma and trim whitespace
        IFS=',' read -ra users_array <<< "$user_input"
        for user in "${users_array[@]}"; do
            # Trim leading/trailing whitespace
            user=$(echo "$user" | xargs)
            if [ -n "$user" ]; then
                echo "$user"
            fi
        done
    fi
}

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "📊 Discord Digest Generator - Multi-User (Interactive)"
echo "================================================================================"
echo ""
echo "📋 Available exports: $EXPORTS_DIR"
echo "📂 Output directory: $OUTPUT_DIR"
echo ""

# Prompt for user selection
echo "🔤 User Selection:"
echo "─────────────────────────────────────────────────────────────────────────────"
echo ""
echo "Default users: ${DEFAULT_USERS[*]}"
echo ""

# Ask if user wants to include default users
if confirm "Include default users (${DEFAULT_USERS[*]})?"; then
    USERS+=("${DEFAULT_USERS[@]}")
    echo "✓ Default users added to processing list"
else
    echo "✗ Default users will not be processed"
fi

echo ""

# Ask if user wants to add additional users
if confirm "Add additional users?"; then
    echo "Enter additional users (comma-separated, e.g., user1,user2,user3):"
    read -p "Additional users: " additional_users
    
    if [ -n "$additional_users" ]; then
        # Parse comma-separated input
        IFS=',' read -ra additional_array <<< "$additional_users"
        for user in "${additional_array[@]}"; do
            # Trim whitespace
            user=$(echo "$user" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            if [ -n "$user" ]; then
                USERS+=("$user")
                echo "✓ Added: $user"
            fi
        done
    else
        echo "No additional users provided"
    fi
fi

echo ""

# Verify we have users to process
if [ ${#USERS[@]} -eq 0 ]; then
    echo "❌ No users selected for processing. Exiting."
    exit 1
fi

echo "📋 Users to process: ${USERS[*]}"
echo "📅 Date range: $START_DATE to $END_DATE"
echo "⏱️  Weekly digest: 14 days (2 weeks)"
echo ""
echo "──────────────────────────────────────────────────────────────────────────────"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to generate complete archive for a user
generate_complete_archive() {
    local username="$1"
    local safe_username=$(echo "$username" | tr '.' '_' | tr ' ' '_')
    
    echo ""
    echo "${BLUE}──────────────────────────────────────────────────────────────────────────────${NC}"
    echo "${GREEN}📁 Generating Complete Archive for: $username${NC}"
    echo "${BLUE}──────────────────────────────────────────────────────────────────────────────${NC}"
    
    python3 discord_digest.py \
        --exports "$EXPORTS_DIR" \
        --username "$username" \
        --archive-output "$OUTPUT_DIR/${safe_username}_complete_archive.md" \
        --json-output "$OUTPUT_DIR/${safe_username}_complete.json" \
        --weekly-output "$OUTPUT_DIR/${safe_username}_weekly.md" \
        --days 14 \
        --date-from "$START_DATE" \
        --date-to "$END_DATE" \
        --no-json
    
    # The HTML file is automatically created as ${safe_username}_complete_archive.html
    
    if [ -f "$OUTPUT_DIR/${safe_username}_complete_archive.html" ]; then
        echo "${GREEN}✓${NC} Complete archive HTML: $OUTPUT_DIR/${safe_username}_complete_archive.html"
    fi
    
    if [ -f "$OUTPUT_DIR/${safe_username}_weekly.md" ]; then
        echo "${GREEN}✓${NC} Weekly digest (14 days): $OUTPUT_DIR/${safe_username}_weekly.md"
    fi
}

# Function to generate weekly summary for a user
generate_weekly_summary() {
    local username="$1"
    local safe_username=$(echo "$username" | tr '.' '_' | tr ' ' '_')
    
    echo ""
    echo "${BLUE}──────────────────────────────────────────────────────────────────────────────${NC}"
    echo "${GREEN}📅 Generating Weekly Summary for: $username${NC}"
    echo "${BLUE}──────────────────────────────────────────────────────────────────────────────${NC}"
    
    # Note: Weekly digest is already generated above with 14-day coverage
    
    echo "${GREEN}✓${NC} Weekly summary (14 days) already generated: $OUTPUT_DIR/${safe_username}_weekly.md"
}

# Function to convert markdown to HTML using pandoc
convert_weekly_to_html() {
    local username="$1"
    local safe_username=$(echo "$username" | tr '.' '_' | tr ' ' '_')
    
    if command -v pandoc &> /dev/null; then
        echo ""
        echo "${YELLOW}📝 Converting weekly digest to HTML...${NC}"
        
        pandoc "$OUTPUT_DIR/${safe_username}_weekly.md" \
            -o "$OUTPUT_DIR/${safe_username}_weekly.html" \
            --standalone \
            --metadata title="$username Weekly Digest (14 days)" \
            --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-dark.min.css \
            2>/dev/null || echo "${YELLOW}⚠${NC}  Pandoc conversion had issues, markdown file available"
        
        if [ -f "$OUTPUT_DIR/${safe_username}_weekly.html" ]; then
            echo "${GREEN}✓${NC} Weekly HTML: $OUTPUT_DIR/${safe_username}_weekly.html"
        fi
    else
        echo "${YELLOW}⚠${NC}  Pandoc not installed - weekly digest is markdown only"
        echo "   Install with: sudo apt install pandoc"
    fi
}

# Process each user
for username in "${USERS[@]}"; do
    generate_complete_archive "$username"
    convert_weekly_to_html "$username"
done

# Generate combined summary
echo ""
echo "${BLUE}──────────────────────────────────────────────────────────────────────────────${NC}"
echo "${GREEN}📊 Generating Combined Summary${NC}"
echo "${BLUE}──────────────────────────────────────────────────────────────────────────────${NC}"

SUMMARY_FILE="$OUTPUT_DIR/SUMMARY.md"

cat > "$SUMMARY_FILE" << EOF
# Discord Digest Summary

**Generated:** $(date '+%Y-%m-%d %H:%M:%S')  
**Period:** $START_DATE to $END_DATE  
**Users:** ${USERS[*]}  
**Weekly Digest Coverage:** 14 days (2 weeks)

---

## 📂 Generated Files

EOF

for username in "${USERS[@]}"; do
    safe_username=$(echo "$username" | tr '.' '_' | tr ' ' '_')
    
    cat >> "$SUMMARY_FILE" << EOF

### $username

#### Complete Archive (All Messages Feb 2024 - Present)
- **HTML:** [\`${safe_username}_complete_archive.html\`](./${safe_username}_complete_archive.html) ⭐ **OPEN THIS!**
- **Markdown:** [\`${safe_username}_complete_archive.md\`](./${safe_username}_complete_archive.md)

#### Weekly Summary (Last 14 Days)
- **Markdown:** [\`${safe_username}_weekly.md\`](./${safe_username}_weekly.md)
EOF
    
    if [ -f "$OUTPUT_DIR/${safe_username}_weekly.html" ]; then
        echo "- **HTML:** [\`${safe_username}_weekly.html\`](./${safe_username}_weekly.html)" >> "$SUMMARY_FILE"
    fi
done

cat >> "$SUMMARY_FILE" << EOF

---

## 🎨 HTML Features

The HTML archives include:

- 📊 **Emojis in titles and dates**
- 🎨 **Color-coded message borders**
  - Green = Posts by the user
  - Orange = Replies to the user
- 💬 **Quote boxes** showing conversation context
- 👍 **Reaction emojis with counts** (e.g., 👍 5, ❤️ 2)
- 🔗 **Clickable links** to original Discord messages
- 🌙 **Discord-style dark theme**
- 📱 **Responsive design** (works on mobile)

## 📖 How to View

### Complete Archives (HTML)
\`\`\`bash
# Open in browser
xdg-open $OUTPUT_DIR/dirvine__complete_archive.html
xdg-open $OUTPUT_DIR/Bux_complete_archive.html

# Or
firefox $OUTPUT_DIR/dirvine__complete_archive.html
firefox $OUTPUT_DIR/Bux_complete_archive.html
\`\`\`

### Weekly Summaries (Markdown)
\`\`\`bash
# Read in terminal
cat $OUTPUT_DIR/dirvine__weekly.md
cat $OUTPUT_DIR/Bux_weekly.md

# Or open in editor
code $OUTPUT_DIR/dirvine__weekly.md
\`\`\`

---

**All files are in:** \`$OUTPUT_DIR/\`

**Last generated:** $(date -u '+%Y-%m-%d %H:%M:%S UTC')
EOF

echo "${GREEN}✓${NC} Summary file created: $SUMMARY_FILE"

# Display final summary
echo ""
echo "================================================================================"
echo "🎉 Generation Complete!"
echo "================================================================================"
echo ""
echo "📂 Output Directory: $OUTPUT_DIR"
echo ""
echo "📄 Generated Files:"
echo ""

for username in "${USERS[@]}"; do
    safe_username=$(echo "$username" | tr '.' '_' | tr ' ' '_')
    echo "  $username:"
    
    if [ -f "$OUTPUT_DIR/${safe_username}_complete_archive.html" ]; then
        size=$(du -h "$OUTPUT_DIR/${safe_username}_complete_archive.html" | cut -f1)
        echo "    ✓ Complete Archive (HTML): ${size}"
    fi
    
    if [ -f "$OUTPUT_DIR/${safe_username}_complete_archive.md" ]; then
        size=$(du -h "$OUTPUT_DIR/${safe_username}_complete_archive.md" | cut -f1)
        echo "    ✓ Complete Archive (MD):   ${size}"
    fi
    
    if [ -f "$OUTPUT_DIR/${safe_username}_weekly.md" ]; then
        size=$(du -h "$OUTPUT_DIR/${safe_username}_weekly.md" | cut -f1)
        echo "    ✓ Weekly Summary (MD):     ${size}"
    fi
    
    if [ -f "$OUTPUT_DIR/${safe_username}_weekly.html" ]; then
        size=$(du -h "$OUTPUT_DIR/${safe_username}_weekly.html" | cut -f1)
        echo "    ✓ Weekly Summary (HTML):   ${size}"
    fi
    echo ""
done

echo "================================================================================"
echo "🌐 Open HTML Files:"
echo "================================================================================"
echo ""

for username in "${USERS[@]}"; do
    safe_username=$(echo "$username" | tr '.' '_' | tr ' ' '_')
    if [ -f "$OUTPUT_DIR/${safe_username}_complete_archive.html" ]; then
        echo "  $username Complete Archive:"
        echo "    xdg-open $OUTPUT_DIR/${safe_username}_complete_archive.html"
        echo ""
    fi
done

echo "================================================================================"
echo ""
echo "📖 Read the summary:"
echo "  cat $SUMMARY_FILE"
echo ""
echo "================================================================================"
