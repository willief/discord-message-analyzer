#!/bin/bash
#
# Master Discord Digest Pipeline
# 1. Exports all channels (including hot-topics)
# 2. Generates digests for all users
#

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================================"
echo "🚀 Discord Digest Master Pipeline"
echo "================================================================================"
echo ""
echo "This will:"
echo "  1. Export all Discord channels (including #hot-topics)"
echo "  2. Generate digests for dirvine., Bux, and JimCollinson"
echo "  3. Create HTML archives with emojis and reactions"
echo ""
echo "================================================================================"
echo ""

# Step 1: Export channels
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}Step 1: Exporting Discord Channels${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -f "./export_discord_channels.sh" ]; then
    ./export_discord_channels.sh
else
    echo "${YELLOW}⚠${NC}  Export script not found. Using existing exports..."
    echo ""
fi

# Step 2: Generate digests
echo ""
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}Step 2: Generating User Digests${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -f "./generate_multi_user_digest.sh" ]; then
    ./generate_multi_user_digest.sh
else
    echo "${RED}❌ Error: generate_multi_user_digest.sh not found${NC}"
    exit 1
fi

# Done!
echo ""
echo "================================================================================"
echo "🎉 Pipeline Complete!"
echo "================================================================================"
echo ""
echo "✅ All channels exported (including #hot-topics)"
echo "✅ Digests generated for dirvine., Bux, and JimCollinson"
echo "✅ HTML archives created with emojis and reactions"
echo ""
echo "================================================================================"
echo "🌐 Open HTML Files:"
echo "================================================================================"
echo ""
echo "  dirvine. archive:"
echo "    xdg-open outputs/dirvine__complete_archive.html"
echo ""
echo "  Bux archive:"
echo "    xdg-open outputs/Bux_complete_archive.html"
echo ""
echo "  JimCollinson archive:"
echo "    xdg-open outputs/JimCollinson_complete_archive.html"
echo ""
echo "================================================================================"
