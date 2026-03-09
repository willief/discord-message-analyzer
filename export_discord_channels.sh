#!/bin/bash
#
# Discord Channel Exporter
# Exports multiple channels including hot-topics
#

set -e  # Exit on error

# Configuration
DISCORD_TOKEN="${DISCORD_TOKEN:-}"  # Use environment variable or set below
OUTPUT_DIR="./digests/discord_exports"
EXPORTER_PATH="./discord-exporter/DiscordChatExporter.Cli"

# Channel IDs
declare -A CHANNELS=(
    ["general-chat"]="1209059622586163272"
    ["general-support"]="1247881515107483759"
    ["bug-reports"]="1290643554267566130"
    ["hot-topics"]="1315677640581054464"
)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================================"
echo "📥 Discord Channel Exporter"
echo "================================================================================"
echo ""

# Check if token is set
if [ -z "$DISCORD_TOKEN" ]; then
    echo "${RED}❌ Error: DISCORD_TOKEN not set${NC}"
    echo ""
    echo "Set it with:"
    echo "  export DISCORD_TOKEN='your-token-here'"
    echo "Or edit this script and add it to the DISCORD_TOKEN variable"
    exit 1
fi

# Check if DiscordChatExporter exists
if [ ! -f "$EXPORTER_PATH" ]; then
    echo "${RED}❌ Error: DiscordChatExporter not found at $EXPORTER_PATH${NC}"
    echo ""
    echo "Install with:"
    echo "  wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip"
    echo "  unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter"
    echo "  chmod +x discord-exporter/DiscordChatExporter.Cli"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Export each channel
for channel_name in "${!CHANNELS[@]}"; do
    channel_id="${CHANNELS[$channel_name]}"
    output_file="$OUTPUT_DIR/${channel_name}.json"
    
    echo ""
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${GREEN}📤 Exporting #${channel_name}${NC}"
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "Channel ID: $channel_id"
    echo "Output: $output_file"
    echo ""
    
    "$EXPORTER_PATH" export \
        -t "$DISCORD_TOKEN" \
        -c "$channel_id" \
        -f Json \
        -o "$output_file"
    
    if [ -f "$output_file" ]; then
        size=$(du -h "$output_file" | cut -f1)
        echo ""
        echo "${GREEN}✓${NC} Exported successfully: $size"
    else
        echo ""
        echo "${RED}✗${NC} Export failed"
    fi
done

# Summary
echo ""
echo "================================================================================"
echo "🎉 Export Complete!"
echo "================================================================================"
echo ""
echo "📂 Exported channels:"
ls -lh "$OUTPUT_DIR"/*.json 2>/dev/null || echo "No files found"
echo ""
echo "================================================================================"
echo ""
echo "🎯 Next step: Generate digests"
echo "  ./generate_multi_user_digest.sh"
echo ""
echo "================================================================================"
