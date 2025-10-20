#!/usr/bin/env python3
"""
Dirvine Digest Generator
Generates markdown summaries of dirvine's Discord activity for the Autonomi community
"""

import json
import os
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path


class DirvineDigestGenerator:
    """Generate markdown digests of dirvine's Discord activity"""
    
    def __init__(self, exports_directory):
        self.exports_directory = exports_directory
        self.target_username = "dirvine."
        
        # Store messages organized by date
        self.messages_by_date = defaultdict(list)
        self.all_messages = []
        
    def process_exports(self):
        """Process all JSON export files"""
        json_files = list(Path(self.exports_directory).rglob('*.json'))
        
        if not json_files:
            print(f"No JSON files found in {self.exports_directory}")
            return
        
        print(f"Processing {len(json_files)} export files...")
        
        for json_file in json_files:
            self._process_file(json_file)
    
    def _process_file(self, json_file_path):
        """Process a single JSON export file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {json_file_path}: {e}")
            return
        
        channel_name = data.get('channel', {}).get('name', 'Unknown')
        guild_name = data.get('guild', {}).get('name', 'Unknown')
        messages = data.get('messages', [])
        
        # Build lookup of all message IDs from dirvine
        dirvine_message_ids = set()
        for msg in messages:
            author = msg.get('author', {})
            if author.get('name', '').lower() == self.target_username:
                dirvine_message_ids.add(msg.get('id'))
        
        # Collect dirvine's posts and replies to him
        for msg in messages:
            author = msg.get('author', {})
            timestamp = msg.get('timestamp')
            
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                continue
            
            # Check if this is dirvine's post
            is_dirvine = author.get('name', '').lower() == self.target_username
            
            # Check if this is a reply to dirvine
            is_reply_to_dirvine = False
            replied_to_msg = None
            if 'reference' in msg:
                ref_id = msg['reference'].get('messageId')
                if ref_id in dirvine_message_ids:
                    is_reply_to_dirvine = True
                    # Find the original message
                    replied_to_msg = next((m for m in messages if m.get('id') == ref_id), None)
            
            if is_dirvine or is_reply_to_dirvine:
                entry = {
                    'datetime': dt,
                    'date': dt.date(),
                    'time': dt.strftime('%H:%M:%S'),
                    'channel': channel_name,
                    'server': guild_name,
                    'author': f"{author.get('name')}",
                    'content': msg.get('content', ''),
                    'is_dirvine': is_dirvine,
                    'is_reply_to_dirvine': is_reply_to_dirvine,
                    'replied_to_msg': replied_to_msg,
                    'message_url': f"https://discord.com/channels/{data.get('guild', {}).get('id')}/{data.get('channel', {}).get('id')}/{msg.get('id')}"
                }
                
                self.all_messages.append(entry)
                self.messages_by_date[dt.date()].append(entry)
    
    def generate_complete_archive(self, output_file='dirvine_complete_archive.md'):
        """Generate complete archive of all dirvine activity"""
        if not self.all_messages:
            print("No messages found for dirvine.")
            return
        
        # Sort all messages chronologically
        sorted_messages = sorted(self.all_messages, key=lambda x: x['datetime'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Dirvine Complete Archive\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
            f.write(f"**Total messages: {len(sorted_messages)}**\n\n")
            f.write("This archive contains all posts by dirvine and replies to his messages in the Autonomi Discord community.\n\n")
            f.write("---\n\n")
            
            current_date = None
            for msg in sorted_messages:
                # Date header
                if msg['date'] != current_date:
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f"\n## {day_name}, {current_date}\n\n")
                
                self._write_message(f, msg)
        
        print(f"✓ Complete archive generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")
    
    def generate_weekly_digest(self, output_file='dirvine_weekly_digest.md', days=7):
        """Generate digest of messages from the last N days"""
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        # Filter messages from last week
        recent_messages = [
            msg for msg in self.all_messages 
            if msg['date'] >= cutoff_date
        ]
        
        if not recent_messages:
            print(f"No messages found in the last {days} days.")
            return
        
        recent_messages.sort(key=lambda x: x['datetime'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Dirvine Weekly Digest\n\n")
            f.write(f"*Week of {cutoff_date} to {datetime.now().date()}*\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
            f.write(f"**Messages this week: {len(recent_messages)}**\n\n")
            f.write("This digest contains dirvine's recent posts and replies to his messages in the Autonomi Discord community.\n\n")
            f.write("---\n\n")
            
            current_date = None
            for msg in recent_messages:
                # Date header
                if msg['date'] != current_date:
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f"\n## {day_name}, {current_date}\n\n")
                
                self._write_message(f, msg)
        
        print(f"✓ Weekly digest generated: {output_file}")
        print(f"  Messages this week: {len(recent_messages)}")
    
    def _write_message(self, f, msg):
        """Write a single message entry to markdown"""
        # Channel badge
        f.write(f"**[#{msg['channel']}]** ")
        f.write(f"`{msg['time']}` ")
        
        if msg['is_dirvine']:
            f.write(f"**{msg['author']}** said:\n\n")
            
            # If dirvine was replying to someone, show context
            if msg['replied_to_msg']:
                replied_to = msg['replied_to_msg']
                replied_author = replied_to.get('author', {}).get('name', 'Unknown')
                replied_content = replied_to.get('content', '')
                f.write(f"> *Replying to {replied_author}:*\n")
                f.write(f"> {replied_content}\n\n")
            
            f.write(f"{msg['content']}\n\n")
        
        elif msg['is_reply_to_dirvine']:
            f.write(f"**{msg['author']}** replied to dirvine:\n\n")
            
            # Show what dirvine said
            if msg['replied_to_msg']:
                dirvine_content = msg['replied_to_msg'].get('content', '')
                f.write(f"> *dirvine said:*\n")
                f.write(f"> {dirvine_content}\n\n")
            
            f.write(f"{msg['content']}\n\n")
        
        # Link to original message
        f.write(f"[View in Discord]({msg['message_url']})\n\n")
        f.write("---\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate markdown digests of dirvine\'s Discord activity',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate both archive and weekly digest
  python3 dirvine_digest.py --exports ./discord_exports
  
  # Generate only the complete archive
  python3 dirvine_digest.py --exports ./discord_exports --archive-only
  
  # Generate only weekly digest
  python3 dirvine_digest.py --exports ./discord_exports --weekly-only
  
  # Custom output filenames
  python3 dirvine_digest.py --exports ./discord_exports --archive-output archive.md --weekly-output weekly.md
        """
    )
    
    parser.add_argument('--exports', '-e', required=True,
                       help='Directory containing Discord JSON exports')
    parser.add_argument('--archive-output', default='dirvine_complete_archive.md',
                       help='Output file for complete archive (default: dirvine_complete_archive.md)')
    parser.add_argument('--weekly-output', default='dirvine_weekly_digest.md',
                       help='Output file for weekly digest (default: dirvine_weekly_digest.md)')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days for weekly digest (default: 7)')
    parser.add_argument('--archive-only', action='store_true',
                       help='Generate only the complete archive')
    parser.add_argument('--weekly-only', action='store_true',
                       help='Generate only the weekly digest')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Dirvine Digest Generator")
    print("=" * 80)
    print(f"Processing exports from: {args.exports}\n")
    
    generator = DirvineDigestGenerator(args.exports)
    generator.process_exports()
    
    if not args.weekly_only:
        generator.generate_complete_archive(args.archive_output)
    
    if not args.archive_only:
        generator.generate_weekly_digest(args.weekly_output, args.days)
    
    print("\n" + "=" * 80)
    print("Generation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
