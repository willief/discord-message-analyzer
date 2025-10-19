# Discord Message Analyzer

A comprehensive Python tool for analyzing Discord chat history exports. This tool helps you extract and organize messages posted by specific users and replies to those users across any number of Discord channels and servers.

## What This Tool Does

Discord Message Analyzer processes JSON export files from DiscordChatExporter and generates organized, chronological reports showing:

- All messages posted by a specific user
- All replies to that user's messages
- Messages organized by server and channel
- Complete message content, timestamps, attachments, and reactions
- Summary statistics about the user's activity

This is particularly useful for community managers, researchers, or anyone who needs to track specific user interactions across Discord communities over time.

## Prerequisites

Before using this tool, you need to have:

1. **Python 3.7 or later** installed on your system
2. **PyYAML library** for configuration file parsing
3. **DiscordChatExporter** for exporting Discord messages to JSON format
4. **Access to Discord channels** you want to analyze (you can only export channels you have permission to view)

### Installing Python Dependencies

Install the required Python library:

```bash
pip install pyyaml
```

Or if you're using a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
pip install pyyaml
```

### Getting DiscordChatExporter

Download DiscordChatExporter from the official GitHub repository:

https://github.com/Tyrrrz/DiscordChatExporter

For Linux, download the `DiscordChatExporter.Cli.linux-x64.zip` file from the latest release. Extract it and make it executable:

```bash
wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip
unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter
chmod +x discord-exporter/DiscordChatExporter.Cli
```

## Getting Started

### Step 1: Export Discord Messages

First, you need to export messages from Discord using DiscordChatExporter. This requires your Discord authorization token.

#### Getting Your Discord Token

1. Open Discord in a web browser (not the desktop app)
2. Press F12 to open Developer Tools
3. Go to the "Application" or "Storage" tab
4. Look for "Local Storage" and click on the Discord domain
5. Find the "token" entry and copy its value

**Security Warning**: Treat your Discord token like a password. Anyone with this token can access your Discord account until you change your password.

#### Exporting Channel Messages

To export messages from specific channels for the last 6 months:

```bash
./DiscordChatExporter.Cli export \
  -t YOUR_TOKEN \
  -c CHANNEL_ID_1 -c CHANNEL_ID_2 -c CHANNEL_ID_3 \
  -f Json \
  -o "discord_exports/%C.json" \
  --after "2025-04-18"
```

To export all channels from a server:

```bash
./DiscordChatExporter.Cli export \
  -t YOUR_TOKEN \
  -g SERVER_ID \
  -f Json \
  -o "discord_exports/%C.json" \
  --after "2025-04-18"
```

**Getting Channel and Server IDs**: Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode). Then right-click on any channel or server icon and select "Copy ID".

The `%C` in the output path tells DiscordChatExporter to use the channel name as the filename, giving you clean, descriptive filenames like `general-chat.json` instead of long auto-generated names.

### Step 2: Set Up the Analyzer

Save the `discord_analyzer.py` script to your project directory. Then create a configuration file:

```bash
python3 discord_analyzer.py --create-config
```

This creates a `config.yaml` file with explanatory comments. Edit this file to specify:

- The username you want to search for
- Where your exported JSON files are located
- Where you want the analysis report saved

Example configuration:

```yaml
target_username: "dirvine."
target_discriminator: null
exports_directory: "./discord_exports"
output_report: "dirvine_analysis.txt"
```

**Important**: Use the exact Discord username, including any periods or special characters. This is the account username, not the display name or nickname.

### Step 3: Run the Analysis

With your configuration file set up and JSON exports ready:

```bash
python3 discord_analyzer.py --config config.yaml
```

The tool will process all JSON files in your exports directory and generate a comprehensive report showing all interactions involving your target user.

## Usage Examples

### Using a Configuration File

Create and use a config file for repeated analyses:

```bash
# Create the template
python3 discord_analyzer.py --create-config

# Edit config.yaml with your settings

# Run the analysis
python3 discord_analyzer.py --config config.yaml
```

### Command-Line Only (No Config File)

For quick one-off analyses, you can provide everything via command-line arguments:

```bash
python3 discord_analyzer.py \
  --username "dirvine." \
  --exports "./discord_exports" \
  --output "analysis_report.txt"
```

### Overriding Config Settings

You can use a config file for most settings but override specific values:

```bash
python3 discord_analyzer.py \
  --config config.yaml \
  --username "different_user" \
  --output "different_report.txt"
```

This is useful when you want to analyze different users using the same export files.

### Analyzing Multiple Users

To analyze multiple users from the same exports, simply run the tool multiple times with different usernames:

```bash
python3 discord_analyzer.py --config config.yaml --username "user1." --output "user1_report.txt"
python3 discord_analyzer.py --config config.yaml --username "user2." --output "user2_report.txt"
python3 discord_analyzer.py --config config.yaml --username "user3." --output "user3_report.txt"
```

## Understanding the Output

The generated report includes:

**Summary Section**: Statistics about total messages found, posts by the user, replies to the user, and number of channels analyzed.

**Channel Sections**: Messages organized by server and channel, sorted chronologically. Each message shows:
- Exact timestamp
- Author name and discriminator
- Message type (posted by target or reply to target)
- Full message content
- Attachments (if any) with filenames and URLs
- Reactions (if any) with counts

This organization makes it easy to follow conversation threads and understand the context of interactions.

## Project Structure

A typical project directory looks like this:

```
your-project/
├── discord_analyzer.py          # Main analysis script
├── config.yaml                  # Configuration file
├── discord_exports/             # Directory with JSON exports
│   ├── general-chat.json
│   ├── general-support.json
│   └── bug-reports.json
└── discord_analysis_report.txt  # Generated report
```

## Troubleshooting

### "No JSON files found"

Make sure your `exports_directory` path in the config file points to the correct location. You can use either absolute paths (`/home/user/exports`) or relative paths (`./discord_exports`).

Check that your JSON files are actually in that directory:
```bash
ls -la discord_exports/
```

### "No messages found for the specified user"

This usually means the username doesn't match exactly. Common issues:

- Missing or extra periods in the username (e.g., `"dirvine"` vs `"dirvine."`)
- Wrong capitalization (though the script is case-insensitive)
- Using a display name or nickname instead of the actual account username

To find the exact username, open one of your JSON files and search for a message you know was written by that user. Look at the `"name"` field in the author section.

### Token Expired or Invalid

If DiscordChatExporter gives authentication errors, your token may have expired. Discord tokens expire when you change your password or log out. Get a fresh token using the method described in the "Getting Your Discord Token" section.

### Permission Errors

You can only export channels you have permission to view in Discord. If DiscordChatExporter reports permission errors for certain channels, you don't have access to those channels and cannot export them.

## Advanced Usage

### Filtering by Date Range

While the analyzer doesn't currently filter by date (it processes all messages in the exports), you can control the date range when exporting with DiscordChatExporter:

```bash
# Only messages after a specific date
--after "2025-04-18"

# Only messages before a specific date
--before "2025-10-18"

# Messages in a specific date range
--after "2025-04-18" --before "2025-10-18"
```

### Processing Large Exports

For very large Discord servers with millions of messages, the analysis might take several minutes. The script shows progress as it processes each file. Consider:

- Exporting only specific channels rather than entire servers
- Using date filters to limit the export size
- Running the analysis on smaller batches of channels

### Automated Batch Processing

You can create shell scripts to automate analyzing multiple users or multiple time periods:

```bash
#!/bin/bash
# analyze_users.sh

users=("dirvine." "user2" "user3")

for user in "${users[@]}"; do
    echo "Analyzing $user..."
    python3 discord_analyzer.py \
        --config config.yaml \
        --username "$user" \
        --output "${user}_report.txt"
done

echo "All analyses complete!"
```

## Privacy and Ethics

This tool is designed for legitimate use cases like:

- Community management and moderation
- Academic research with proper consent
- Personal archiving of your own Discord activity
- Analyzing open community discussions

Please respect privacy and Discord's Terms of Service:

- Only export and analyze channels you have legitimate access to
- Don't use this tool to harass or stalk users
- Respect confidential or private communications
- Follow your organization's data handling policies
- Be aware of GDPR and other privacy regulations if applicable

## Contributing

This is an open-source tool designed to be extended and customized. Some potential enhancements:

- Support for analyzing multiple users in a single run
- Date range filtering within the analyzer (not just at export time)
- HTML or CSV output formats in addition to text
- Sentiment analysis or other statistical processing
- Visualization of message patterns over time
- Integration with other Discord analysis tools

## License

This tool is provided as-is for educational and analytical purposes. DiscordChatExporter is created by Tyrrrz and licensed separately. Always respect Discord's Terms of Service and applicable privacy laws when using these tools.

## Support

For issues with:

- **DiscordChatExporter**: See the official repository at https://github.com/Tyrrrz/DiscordChatExporter
- **Discord API changes**: Check Discord's developer documentation at https://discord.com/developers/docs
- **This analyzer tool**: Check that your configuration is correct and your JSON exports are valid

## Changelog

### Version 1.0
- Initial release
- Support for analyzing posts by and replies to specific users
- YAML configuration file support
- Command-line argument override capability
- Comprehensive text report generation
- Summary statistics
- Multi-channel and multi-server support