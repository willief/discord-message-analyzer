# Discord Message Analyzer

A comprehensive Python tool for analyzing Discord chat history exports. Track user activity, interactions, and conversations across Discord servers with automated weekly digests and AI-ready JSON output.

## Features

- 📊 **Complete Activity Tracking**
  - Posts by target user
  - Replies to the user
  - Reactions by the user
  - Messages the user replied to

- 📝 **Multiple Output Formats**
  - Human-readable Markdown reports
  - AI-processable JSON with full context
  - Weekly digests and complete archives

- 🌐 **Autonomi Network Integration**
  - Automatic upload to decentralized storage
  - Public access via anttp.antsnest.site URLs
  - Permanent, censorship-resistant hosting

- 🤖 **Automation Ready**
  - Cron job support for scheduled runs
  - Multi-user tracking via simple config
  - Batch processing capabilities

- 🧪 **Well Tested**
  - Comprehensive test suite
  - Validated with real Discord data
  - CI/CD ready

## Prerequisites

- Python 3.7 or later
- [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) (included in `tools/`)
- Discord account with access to channels you want to analyze
- (Optional) Autonomi CLI for decentralized storage

## Quick Start

### 1. Installation
```bash
git clone https://github.com/YOUR_USERNAME/discord_analyser.git
cd discord_analyser

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Get Your Discord Token

1. Open Discord in a web browser
2. Press F12 to open Developer Tools
3. Go to Application → Local Storage → discord.com
4. Find the "token" entry and copy its value

⚠️ **Security**: Treat this token like a password. Never share it or commit it to git.

### 3. Store Token Securely
```bash
mkdir -p ~/.discord
chmod 700 ~/.discord
echo "YOUR_TOKEN_HERE" > ~/.discord/token
chmod 600 ~/.discord/token
```

### 4. Get Channel IDs

1. Enable Developer Mode in Discord (Settings → Advanced)
2. Right-click on channels and select "Copy ID"

### 5. Export Discord Messages
```bash
# Export a single channel (last 6 months)
./tools/DiscordChatExporter.Cli export \
  -t "$(cat ~/.discord/token)" \
  -c CHANNEL_ID \
  -f Json \
  --after "2024-05-01" \
  -o "digests/discord_exports/channel-name.json"
```

### 6. Generate Digests
```bash
# Analyze a specific user
python3 discord_digest.py \
  --username "dirvine." \
  --exports digests/discord_exports \
  --archive-output digests/archive.md \
  --weekly-output digests/weekly.md \
  --json-output digests/digest.json
```

## Usage Examples

### Single User Analysis
```bash
python3 discord_digest.py \
  --username "someuser" \
  --exports ./discord_exports \
  --output ./output/report.md
```

### Multi-User Tracking

Create a `users.txt` file:
```
dirvine.
joshuef
bochaco
# Add more users, one per line
```

Run the multi-user script:
```bash
./run_multi_user_digests.sh
```

### Automated Weekly Digests

Set up a cron job:
```bash
crontab -e
```

Add this line for weekly Sunday 22:00 runs:
```cron
0 22 * * 0 /home/YOUR_USER/projects/discord_analyser/run_multi_user_digests.sh >> /home/YOUR_USER/projects/discord_analyser/digests/cron.log 2>&1
```

### Full Automation Script

Use `run_digest.sh` for complete automation (export + analyze + upload):
```bash
./run_digest.sh "username"
```

This will:
1. Export specified Discord channels
2. Generate markdown and JSON digests
3. Upload to Autonomi network (if configured)
4. Save public URLs for sharing

## Output Formats

### Markdown Reports

Human-readable format with:
- Chronological organization by date
- Visual thread formatting with emojis
- Channel tags and timestamps
- Discord links to original messages

### JSON Digests

AI-ready structured data with:
- Complete metadata (username, date range, counts)
- Full conversation context
- Interaction types (posts, replies, reactions)
- Timestamps and channel information

Perfect for:
- AI analysis and summarization
- Data mining and research
- Integration with other tools

## Autonomi Network Integration

The tool can automatically upload digests to the Autonomi decentralized network:
```bash
# Upload is automatic in run_digest.sh if Autonomi CLI is installed
# Get shareable URLs like:
# https://anttp.antsnest.site/{address}/username_weekly_2025-10-31.txt
```

Benefits:
- Permanent storage
- Censorship resistant
- Public access without hosting costs
- Community-owned data

## Project Structure
```
discord_analyser/
├── discord_digest.py           # Main analysis script
├── run_digest.sh              # Automation script (export + analyze + upload)
├── run_multi_user_digests.sh  # Multi-user wrapper
├── users.txt                  # List of users to track
├── config.example.yaml        # Configuration template
├── tools/
│   └── DiscordChatExporter.Cli
├── digests/
│   ├── discord_exports/       # JSON exports from Discord
│   └── *.md, *.json          # Generated reports
├── tests/
│   ├── run_tests.sh          # Test suite
│   └── fixtures/             # Test data
├── requirements.txt
├── LICENSE
└── README.md
```

## Configuration

### Environment Variables

- `DISCORD_TOKEN`: Your Discord authentication token (store in `~/.discord/token`)

### Config File (Optional)

Copy `config.example.yaml` to `config.yaml` and customize:
```yaml
target_username: "your_user"
exports_directory: "./digests/discord_exports"
archive_output: "archive.md"
weekly_output: "weekly.md"
json_output: "digest.json"
```

## Testing

Run the test suite to verify everything works:
```bash
./tests/run_tests.sh
```

Tests cover:
- Digest generation
- Output file creation
- JSON structure validation
- Message capture accuracy
- Interaction type detection
- Markdown formatting

## Security Best Practices

🔒 **Never commit sensitive data:**
- Discord tokens
- Actual message exports
- Real server/channel IDs in examples
- Generated reports with private conversations

✅ **Always:**
- Use `.gitignore` (included in repo)
- Store tokens in secure files with `600` permissions
- Use read-only bot tokens when possible
- Regularly rotate tokens

## Contributing

We welcome contributions from the Autonomi community! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report bugs
- Feature requests
- Code contribution guidelines
- Development setup
- Testing requirements

## Use Cases

- **Community Management**: Track key contributor activity
- **Content Curation**: Compile thought leadership from community experts
- **AI Training**: Generate structured datasets for AI analysis
- **Historical Archives**: Preserve important community discussions
- **Research**: Analyze communication patterns and engagement

## Troubleshooting

### "No messages found"

- Verify username is exact (including periods, case-sensitive)
- Check date range in export command
- Ensure exports directory has JSON files

### "Token invalid"

- Token may have expired - get a fresh one
- Verify token file permissions are `600`
- Check token was copied correctly (no extra spaces)

### Export very slow

- Use `--after` date filter to limit timeframe
- Export fewer channels at once
- Consider running overnight for large servers

## Roadmap

- [ ] HTML output format
- [ ] Date range filtering in analyzer
- [ ] CSV export for spreadsheet analysis
- [ ] Sentiment analysis
- [ ] Activity visualization (charts)
- [ ] Web UI for non-technical users
- [ ] Real-time Discord bot integration

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the [Autonomi Community](https://autonomi.com)
- Uses [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) by Tyrrrz
- Integrates with [Autonomi Network](https://autonomi.com) for decentralized storage

## Support

- 🐛 [Report bugs](https://github.com/YOUR_USERNAME/discord_analyser/issues)
- 💡 [Request features](https://github.com/YOUR_USERNAME/discord_analyser/issues)
- 💬 [Join discussion](https://discord.gg/autonomi) in Autonomi Discord

---

**Made with ❤️ for the Autonomi Community**