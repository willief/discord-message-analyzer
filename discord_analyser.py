#!/usr/bin/env python3
"""
Discord Message Analyzer
A tool for extracting and analyzing Discord messages for specific users across any timeframe.

This script processes Discord chat exports (in JSON format from DiscordChatExporter)
and generates organized reports of a target user's activity and interactions.
"""

import json
import os
import argparse
import yaml
from datetime import datetime
from collections import defaultdict
from pathlib import Path


class DiscordMessageAnalyzer:
    """
    Analyzes Discord message exports to find posts by and replies to specific users.
    
    This class handles the core logic of parsing Discord's JSON export format,
    identifying relevant messages, and organizing them for reporting.
    """
    
    def __init__(self, target_username, target_discriminator=None):
        """
        Initialize the analyzer for a specific Discord user.
        
        Args:
            target_username: The username to search for (e.g., "dirvine.")
            target_discriminator: Optional discriminator (the #1234 part), or None
        """
        # Store the target username in lowercase for case-insensitive matching
        # This handles situations where capitalization might vary in exports
        self.target_username = target_username.lower()
        self.target_discriminator = target_discriminator
        
        # We'll organize results by channel name for easy browsing
        # defaultdict automatically creates empty lists for new keys
        self.results = defaultdict(list)
        
        # Keep track of statistics for the final summary
        self.stats = {
            'files_processed': 0,
            'total_messages': 0,
            'posts_by_user': 0,
            'replies_to_user': 0
        }
        
    def matches_target_user(self, author):
        """
        Check if a message author matches our target user.
        
        Discord's author data includes both the username and discriminator.
        We need to match both when a discriminator is specified, or just
        the username when we're not filtering by discriminator.
        
        Args:
            author: Dictionary containing author information from Discord JSON
            
        Returns:
            Boolean indicating whether this author matches our target
        """
        author_name = author.get('name', '').lower()
        author_discriminator = author.get('discriminator', '0000')
        
        # First check if the username matches
        if author_name != self.target_username:
            return False
            
        # If we specified a discriminator, verify it matches too
        # This is useful when multiple users have similar usernames
        if self.target_discriminator and author_discriminator != self.target_discriminator:
            return False
            
        return True
    
    def extract_from_file(self, json_file_path):
        """
        Process a single JSON export file from DiscordChatExporter.
        
        This method implements a two-pass algorithm:
        1. First pass: Identify all message IDs belonging to our target user
        2. Second pass: Collect both the target's messages and replies to them
        
        The two-pass approach is necessary because Discord's reply system uses
        message ID references, and we need to know which IDs belong to our target
        before we can identify replies to them.
        
        Args:
            json_file_path: Path to the JSON file to process
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {json_file_path}: {e}")
            return
        except Exception as e:
            print(f"Error reading {json_file_path}: {e}")
            return
        
        # Extract metadata about this channel from the JSON
        # This information appears at the top of each export file
        channel_name = data.get('channel', {}).get('name', 'Unknown Channel')
        channel_id = data.get('channel', {}).get('id', 'Unknown ID')
        guild_name = data.get('guild', {}).get('name', 'Unknown Server')
        
        # Create a friendly identifier combining server and channel names
        # This helps when you're analyzing exports from multiple servers
        channel_identifier = f"{guild_name} / {channel_name}"
        
        # First pass: Build a set of all message IDs from our target user
        # Sets are perfect here because they provide O(1) lookup time
        target_message_ids = set()
        messages = data.get('messages', [])
        
        for message in messages:
            author = message.get('author', {})
            if self.matches_target_user(author):
                target_message_ids.add(message.get('id'))
        
        # Second pass: Collect relevant messages
        # We're looking for both messages BY the target and messages TO the target
        for message in messages:
            author = message.get('author', {})
            message_id = message.get('id')
            timestamp = message.get('timestamp')
            content = message.get('content', '')
            
            # Parse the timestamp into a proper datetime object
            # Discord uses ISO 8601 format with a 'Z' suffix for UTC
            # We replace the Z with timezone info that Python can parse
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                # If timestamp parsing fails, use current time as fallback
                # This shouldn't happen with valid Discord exports, but we handle it gracefully
                dt = datetime.now()
            
            # Build a dictionary containing all relevant message data
            # This structure makes it easy to generate reports later
            entry = {
                'message_id': message_id,
                'timestamp': timestamp,
                'datetime': dt,
                'author': f"{author.get('name')}#{author.get('discriminator', '0000')}",
                'author_id': author.get('id'),
                'content': content,
                'attachments': message.get('attachments', []),
                'embeds': message.get('embeds', []),
                'reactions': message.get('reactions', []),
                'channel': channel_name,
                'channel_id': channel_id,
                'server': guild_name
            }
            
            # Determine what type of interaction this message represents
            is_by_target = self.matches_target_user(author)
            is_reply_to_target = False
            
            # Check if this message is a reply by looking at the reference field
            # Discord's reply system stores the ID of the message being replied to
            if 'reference' in message:
                ref_msg_id = message['reference'].get('messageId')
                if ref_msg_id in target_message_ids:
                    is_reply_to_target = True
            
            # Add this message to results if it's relevant
            if is_by_target:
                entry['type'] = 'posted_by_target'
                if 'reference' in message:
                    entry['replying_to'] = message['reference'].get('messageId')
                self.results[channel_identifier].append(entry)
                self.stats['posts_by_user'] += 1
                self.stats['total_messages'] += 1
                
            elif is_reply_to_target:
                entry['type'] = 'reply_to_target'
                entry['replying_to'] = message['reference'].get('messageId')
                self.results[channel_identifier].append(entry)
                self.stats['replies_to_user'] += 1
                self.stats['total_messages'] += 1
        
        self.stats['files_processed'] += 1
    
    def process_directory(self, directory_path):
        """
        Process all JSON files in a directory and its subdirectories.
        
        This method uses Python's pathlib to recursively find all JSON files,
        which is more robust than manually walking the directory tree.
        
        Args:
            directory_path: Root directory to search for JSON files
        """
        json_files = list(Path(directory_path).rglob('*.json'))
        
        if not json_files:
            print(f"Warning: No JSON files found in {directory_path}")
            return
        
        print(f"Found {len(json_files)} JSON file(s) to process...\n")
        
        for json_file in json_files:
            print(f"Processing: {json_file.name}")
            self.extract_from_file(json_file)
    
    def generate_report(self, output_file='discord_report.txt'):
        """
        Generate a comprehensive human-readable report.
        
        The report is organized by channel and sorted chronologically within
        each channel, making it easy to follow conversation threads.
        
        Args:
            output_file: Path where the report will be saved
        """
        if not self.results:
            print("\nNo messages found for the specified user.")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write report header with metadata
            f.write("=" * 80 + "\n")
            f.write(f"Discord Message Analysis Report\n")
            f.write(f"Target User: {self.target_username}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Write summary statistics
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total messages found: {self.stats['total_messages']}\n")
            f.write(f"Posts by target user: {self.stats['posts_by_user']}\n")
            f.write(f"Replies to target user: {self.stats['replies_to_user']}\n")
            f.write(f"Channels with activity: {len(self.results)}\n")
            f.write(f"Files processed: {self.stats['files_processed']}\n")
            f.write("\n")
            
            # Sort channels alphabetically for consistent output
            for channel_name in sorted(self.results.keys()):
                messages = self.results[channel_name]
                
                # Sort messages chronologically within each channel
                # This preserves the natural flow of conversations
                messages.sort(key=lambda x: x['datetime'])
                
                # Channel header with visual separator
                f.write("\n" + "#" * 80 + "\n")
                f.write(f"CHANNEL: {channel_name}\n")
                f.write(f"Total interactions: {len(messages)}\n")
                f.write("#" * 80 + "\n\n")
                
                # Write each message with full details
                for msg in messages:
                    f.write(f"[{msg['timestamp']}]\n")
                    f.write(f"Author: {msg['author']}\n")
                    f.write(f"Type: {msg['type'].replace('_', ' ').title()}\n")
                    
                    if msg['content']:
                        f.write(f"Message: {msg['content']}\n")
                    
                    # Include attachment information if present
                    # This helps identify when images or files were shared
                    if msg.get('attachments'):
                        f.write(f"Attachments: {len(msg['attachments'])} file(s)\n")
                        for att in msg['attachments']:
                            f.write(f"  - {att.get('fileName', 'unknown')} ({att.get('url', 'no URL')})\n")
                    
                    # Include reaction counts if present
                    # Reactions can indicate how the community responded to messages
                    if msg.get('reactions'):
                        f.write(f"Reactions: ")
                        reaction_summary = [f"{r.get('emoji', {}).get('name', '?')} ({r.get('count', 0)})" 
                                          for r in msg['reactions']]
                        f.write(", ".join(reaction_summary) + "\n")
                    
                    f.write("-" * 80 + "\n\n")
        
        print(f"\n✓ Report generated: {output_file}")
        print(f"✓ Total channels with activity: {len(self.results)}")
        print(f"✓ Total messages found: {self.stats['total_messages']}")


def load_config(config_file):
    """
    Load configuration from a YAML file.
    
    YAML is chosen because it's human-readable and supports comments,
    making it easy for users to understand and modify their configuration.
    
    Args:
        config_file: Path to the YAML configuration file
        
    Returns:
        Dictionary containing configuration values
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Run with --create-config to generate a template configuration file.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        return None


def create_template_config(config_file='config.yaml'):
    """
    Create a template configuration file with explanatory comments.
    
    This makes it easy for new users to get started without having to
    write the configuration from scratch.
    
    Args:
        config_file: Path where the template will be created
    """
    template = """# Discord Message Analyzer Configuration File
# 
# This file controls how the analyzer searches through your Discord exports.
# Edit the values below to match your specific analysis needs.

# Target User Configuration
# The username to search for in Discord exports
# Important: Include any periods or special characters exactly as they appear
# in the Discord username (not the display name or nickname)
target_username: "username"

# Optional: Specify the discriminator if using old-style Discord usernames
# Format: "1234" or leave as null for new-style usernames without discriminators
target_discriminator: null

# Export Directory Configuration
# Path to the directory containing your JSON export files from DiscordChatExporter
# Can be absolute (/home/user/exports) or relative (./discord_exports)
exports_directory: "./discord_exports"

# Output Configuration
# Where to save the generated report
output_report: "discord_analysis_report.txt"

# Optional: Date filtering
# If you want to only analyze messages within a specific timeframe,
# you can specify start and end dates here
# Format: "YYYY-MM-DD" or null for no filtering
date_filter:
  start_date: null  # Example: "2025-04-18"
  end_date: null    # Example: "2025-10-18"
"""
    
    with open(config_file, 'w') as f:
        f.write(template)
    
    print(f"✓ Template configuration file created: {config_file}")
    print(f"  Edit this file to customize your analysis settings.")


def main():
    """
    Main entry point for the Discord Message Analyzer.
    
    This function handles command-line arguments, loads configuration,
    and orchestrates the analysis process.
    """
    # Set up command-line argument parsing
    # argparse makes it easy to create a professional CLI interface
    parser = argparse.ArgumentParser(
        description='Analyze Discord message exports to find posts by and replies to specific users.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use a configuration file
  python discord_analyzer.py --config my_config.yaml
  
  # Override config settings via command line
  python discord_analyzer.py --config config.yaml --username dirvine. --output results.txt
  
  # Create a template configuration file
  python discord_analyzer.py --create-config
  
  # Run with command-line arguments only (no config file)
  python discord_analyzer.py --username dirvine. --exports ./exports --output report.txt
        """
    )
    
    parser.add_argument('--config', '-c', 
                       help='Path to YAML configuration file')
    parser.add_argument('--create-config', 
                       action='store_true',
                       help='Create a template configuration file and exit')
    parser.add_argument('--username', '-u', 
                       help='Target username to search for (overrides config)')
    parser.add_argument('--discriminator', '-d', 
                       help='Target discriminator (overrides config)')
    parser.add_argument('--exports', '-e', 
                       help='Directory containing JSON exports (overrides config)')
    parser.add_argument('--output', '-o', 
                       help='Output report file path (overrides config)')
    
    args = parser.parse_args()
    
    # Handle template creation request
    if args.create_config:
        create_template_config()
        return
    
    # Load configuration from file if specified
    config = {}
    if args.config:
        config = load_config(args.config)
        if config is None:
            return
    
    # Command-line arguments override config file settings
    # This allows for quick one-off changes without editing the config
    username = args.username or config.get('target_username')
    discriminator = args.discriminator or config.get('target_discriminator')
    exports_dir = args.exports or config.get('exports_directory')
    output_file = args.output or config.get('output_report', 'discord_report.txt')
    
    # Validate that we have the minimum required information
    if not username:
        print("Error: No target username specified.")
        print("Either provide --username or create a config file with --create-config")
        return
    
    if not exports_dir:
        print("Error: No exports directory specified.")
        print("Either provide --exports or specify exports_directory in config file")
        return
    
    # Display analysis configuration
    print("=" * 80)
    print("Discord Message Analyzer")
    print("=" * 80)
    print(f"Target user: {username}")
    if discriminator:
        print(f"Discriminator: {discriminator}")
    print(f"Searching in: {exports_dir}")
    print(f"Output will be saved to: {output_file}")
    print("=" * 80 + "\n")
    
    # Create analyzer instance and run the analysis
    analyzer = DiscordMessageAnalyzer(username, discriminator)
    analyzer.process_directory(exports_dir)
    analyzer.generate_report(output_file)
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()