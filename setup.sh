#!/bin/bash
#
# Discord Digest Generator - Setup Script
# Prepares environment and verifies dependencies
#

set -e

echo "================================================================================"
echo "📦 Discord Digest Generator - Setup"
echo "================================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    echo "  Install from: https://www.python.org/downloads/"
    exit 1
fi

# Check required directories
echo ""
echo "Checking directories..."
mkdir -p discord_exports outputs
echo -e "${GREEN}✓${NC} Created directories: discord_exports, outputs"

# Make scripts executable
echo ""
echo "Setting up scripts..."
chmod +x generate_all_digests.sh test_diagnostics.py 2>/dev/null || true
echo -e "${GREEN}✓${NC} Scripts made executable"

# Test Python imports
echo ""
echo "Testing Python standard library..."
python3 -c "import json, pathlib, datetime, collections, argparse, html" && \
    echo -e "${GREEN}✓${NC} All required modules available" || \
    echo -e "${RED}✗${NC} Some modules missing"

# Show next steps
echo ""
echo "================================================================================"
echo "✅ Setup Complete!"
echo "================================================================================"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Export Discord channels using DiscordChatExporter:"
echo "   wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip"
echo "   unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter"
echo "   chmod +x discord-exporter/DiscordChatExporter.Cli"
echo ""
echo "2. Run the exporter:"
echo "   ./discord-exporter/DiscordChatExporter.Cli export -t YOUR_TOKEN -c CHANNEL_ID -f Json -o discord_exports/channel.json"
echo ""
echo "3. Generate digests:"
echo "   ./generate_all_digests.sh discord_exports outputs"
echo ""
echo "4. View results:"
echo "   xdg-open outputs/dirvine__complete_archive.html"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Full documentation"
echo "   - QUICK_REFERENCE.md - Common commands"
echo ""
echo "🧪 Test your setup:"
echo "   python3 test_diagnostics.py --exports ./discord_exports"
echo ""
echo "================================================================================"
echo ""

# Optional: Download DiscordChatExporter
read -p "Download DiscordChatExporter now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading DiscordChatExporter..."
    mkdir -p discord-exporter
    cd discord-exporter
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -q https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip
        unzip -q DiscordChatExporter.Cli.linux-x64.zip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl -L -o DiscordChatExporter.Cli.osx-x64.zip https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.osx-x64.zip
        unzip -q DiscordChatExporter.Cli.osx-x64.zip
    else
        echo "⚠️  Unsupported OS for auto-download. Download manually:"
        echo "   https://github.com/Tyrrrz/DiscordChatExporter/releases"
    fi
    
    chmod +x DiscordChatExporter.Cli
    cd ..
    echo -e "${GREEN}✓${NC} DiscordChatExporter installed"
fi

echo ""
echo "📝 Add your Discord token to environment:"
echo "   export DISCORD_BOT_TOKEN='your_token_here'"
echo ""
echo "✨ Ready to go!"
echo ""