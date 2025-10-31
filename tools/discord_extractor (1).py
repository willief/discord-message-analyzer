import json
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path

class DiscordMessageExtractor:
    def __init__(self, target_username, target_discriminator=None):
        """
        Initialize the extractor for a specific Discord user.
        
        Args:
            target_username: The username to search for (e.g., "JohnDoe")
            target_discriminator: Optional discriminator (the #1234 part), or None for new usernames
        """
        self.target_username = target_username.lower()
        self.target_discriminator = target_discriminator
        self.results = defaultdict(list)  # Organized by channel name
        
    def matches_target_user(self, author):
        """Check if a message author matches our target user."""
        # Discord usernames can be in different formats depending on the export
        author_name = author.get('name', '').lower()
        author_discriminator = author.get('discriminator', '0000')
        
        # Check username match
        if author_name != self.target_username:
            return False
            
        # If we specified a discriminator, check that too
        if self.target_discriminator and author_discriminator != self.target_discriminator:
            return False
            
        return True
    
    def is_reply_to_target(self, message, target_user_id):
        """
        Check if this message is a reply to our target user.
        Discord's reference field indicates when a message is a reply.
        """
        if 'reference' not in message:
            return False
            
        # The reference contains the messageId being replied to
        # We need to track which messages belong to our target user
        return message.get('reference', {}).get('messageId') in target_user_id
    
    def extract_from_file(self, json_file_path):
        """
        Process a single JSON export file from DiscordChatExporter.
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {json_file_path}: {e}")
            return
        
        # Extract channel metadata
        channel_name = data.get('channel', {}).get('name', 'Unknown Channel')
        channel_id = data.get('channel', {}).get('id', 'Unknown ID')
        guild_name = data.get('guild', {}).get('name', 'Unknown Server')
        
        # Track message IDs from our target user for reply detection
        target_message_ids = set()
        
        # First pass: identify all messages by target user
        messages = data.get('messages', [])
        for message in messages:
            author = message.get('author', {})
            if self.matches_target_user(author):
                target_message_ids.add(message.get('id'))
        
        # Second pass: collect target user messages and replies to them
        for message in messages:
            author = message.get('author', {})
            message_id = message.get('id')
            timestamp = message.get('timestamp')
            content = message.get('content', '')
            
            # Parse timestamp into datetime object for sorting
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            entry = {
                'message_id': message_id,
                'timestamp': timestamp,
                'datetime': dt,
                'author': f"{author.get('name')}#{author.get('discriminator', '0000')}",
                'author_id': author.get('id'),
                'content': content,
                'attachments': message.get('attachments', []),
                'embeds': message.get('embeds', []),
                'channel': channel_name,
                'channel_id': channel_id,
                'server': guild_name
            }
            
            # Check if this is a message by our target user
            if self.matches_target_user(author):
                entry['type'] = 'posted_by_target'
                # Check if target user is replying to someone
                if 'reference' in message:
                    entry['replying_to'] = message['reference'].get('messageId')
                self.results[f"{guild_name} / {channel_name}"].append(entry)
                
            # Check if this is a reply to our target user
            elif 'reference' in message:
                ref_msg_id = message['reference'].get('messageId')
                if ref_msg_id in target_message_ids:
                    entry['type'] = 'reply_to_target'
                    entry['replying_to'] = ref_msg_id
                    self.results[f"{guild_name} / {channel_name}"].append(entry)
    
    def process_directory(self, directory_path):
        """
        Process all JSON files in a directory (and subdirectories).
        """
        json_files = list(Path(directory_path).rglob('*.json'))
        
        if not json_files:
            print(f"No JSON files found in {directory_path}")
            return
        
        print(f"Found {len(json_files)} JSON files to process...")
        
        for json_file in json_files:
            print(f"Processing: {json_file.name}")
            self.extract_from_file(json_file)
    
    def generate_report(self, output_file='discord_report.txt'):
        """
        Generate a human-readable report organized by channel and date.
        """
        if not self.results:
            print("No messages found for the specified user.")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Discord Message Report for: {self.target_username}\n")
            f.write("=" * 80 + "\n\n")
            
            # Sort channels alphabetically
            for channel_name in sorted(self.results.keys()):
                messages = self.results[channel_name]
                
                # Sort messages by datetime
                messages.sort(key=lambda x: x['datetime'])
                
                f.write(f"\n{'#' * 80}\n")
                f.write(f"CHANNEL: {channel_name}\n")
                f.write(f"Total interactions: {len(messages)}\n")
                f.write(f"{'#' * 80}\n\n")
                
                for msg in messages:
                    f.write(f"[{msg['timestamp']}]\n")
                    f.write(f"Author: {msg['author']}\n")
                    f.write(f"Type: {msg['type'].replace('_', ' ').title()}\n")
                    
                    if msg['content']:
                        f.write(f"Message: {msg['content']}\n")
                    
                    if msg.get('attachments'):
                        f.write(f"Attachments: {len(msg['attachments'])} file(s)\n")
                        for att in msg['attachments']:
                            f.write(f"  - {att.get('fileName', 'unknown')}\n")
                    
                    f.write("-" * 80 + "\n\n")
        
        print(f"\nReport generated: {output_file}")
        print(f"Total channels with activity: {len(self.results)}")
        print(f"Total messages found: {sum(len(msgs) for msgs in self.results.values())}")


# Example usage:
if __name__ == "__main__":
    # Configuration - UPDATE THESE VALUES
    TARGET_USERNAME = "YourUsername"  # Change this to the username you're looking for
    TARGET_DISCRIMINATOR = None  # Set to "1234" if using old-style Discord tags, or None
    EXPORTS_DIRECTORY = "./discord_exports"  # Directory containing your JSON exports
    OUTPUT_REPORT = "discord_user_report.txt"
    
    print("=" * 80)
    print("Discord Message Extractor")
    print("=" * 80)
    print(f"Target user: {TARGET_USERNAME}")
    print(f"Searching in: {EXPORTS_DIRECTORY}")
    print(f"Output will be saved to: {OUTPUT_REPORT}")
    print("=" * 80 + "\n")
    
    # Create extractor instance
    extractor = DiscordMessageExtractor(TARGET_USERNAME, TARGET_DISCRIMINATOR)
    
    # Process all JSON files in the exports directory
    extractor.process_directory(EXPORTS_DIRECTORY)
    
    # Generate the organized report
    extractor.generate_report(OUTPUT_REPORT)
    
    print("\n" + "=" * 80)
    print("Processing complete!")
    print("=" * 80)
