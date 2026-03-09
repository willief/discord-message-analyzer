#!/usr/bin/env python3
"""
Discord User Digest Generator
Generates markdown summaries of a specified user's Discord activity
"""

import json
import os
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from html_generator import HTMLDigestGenerator


class DiscordUserDigestGenerator:
    """Generate markdown digests of a Discord user's activity"""

    def __init__(self, target_username, exports_directory, date_from=None, date_to=None):
        self.target_username = target_username.lower()
        self.exports_directory = exports_directory
        self.date_from = date_from
        self.date_to = date_to

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

        # Build lookup of all message IDs from target user
        target_user_message_ids = set()
        for msg in messages:
            author = msg.get('author', {})
            # Handle both string and dict author formats
            if isinstance(author, str):
                author_name = author.lower()
            else:
                author_name = author.get('name', '').lower()
            
            if author_name == self.target_username:
                target_user_message_ids.add(msg.get('id'))

        # Collect target user's posts and replies to them
        for msg in messages:
            author = msg.get('author', {})
            timestamp = msg.get('timestamp')

            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                continue

            # Apply date range filtering if specified
            if self.date_from:
                date_from_obj = datetime.fromisoformat(self.date_from.replace('Z', '+00:00'))
                if dt < date_from_obj:
                    continue
            
            if self.date_to:
                date_to_obj = datetime.fromisoformat(self.date_to.replace('Z', '+00:00'))
                if dt > date_to_obj:
                    continue

            # Check if this is target user's post
            if isinstance(author, str):
                is_target_user = author.lower() == self.target_username
            else:
                is_target_user = author.get('name', '').lower() == self.target_username

            # Check if this is a reply to target user
            is_reply_to_target_user = False
            replied_to_msg = None
            if 'reference' in msg:
                ref_id = msg['reference'].get('messageId')
                if ref_id in target_user_message_ids:
                    is_reply_to_target_user = True
                    replied_to_msg = next(
                        (m for m in messages if m.get('id') == ref_id), None)
                # Add guild and channel IDs for URL construction
                if replied_to_msg:
                    replied_to_msg = replied_to_msg.copy()
                    replied_to_msg['guild_id'] = data.get(
                        'guild', {}).get('id')
                    replied_to_msg['channel_id'] = data.get(
                        'channel', {}).get('id')
                    print(
                        f"DEBUG: Guild ID: {replied_to_msg.get('guild_id')}, Channel ID: {replied_to_msg.get('channel_id')}, Msg ID: {replied_to_msg.get('id')}")

            if is_target_user or is_reply_to_target_user:
                # Check if message is within date range
                if self.date_from or self.date_to:
                    if self.date_from:
                        try:
                            date_from_obj = datetime.fromisoformat(self.date_from.replace('Z', '+00:00'))
                            if dt < date_from_obj:
                                continue  # Skip messages before start date
                        except ValueError:
                            pass  # Invalid date format, process anyway
                    
                    if self.date_to:
                        try:
                            date_to_obj = datetime.fromisoformat(self.date_to.replace('Z', '+00:00'))
                            if dt > date_to_obj:
                                continue  # Skip messages after end date
                        except ValueError:
                            pass  # Invalid date format, process anyway
                
                entry = {
                    'datetime': dt,
                    'date': dt.date(),
                    'time': dt.strftime('%H:%M:%S'),
                    'channel': channel_name,
                    'server': guild_name,
                    'author': author if isinstance(author, str) else author.get('name', 'Unknown'),
                    'content': msg.get('content', ''),
                    'is_target_user': is_target_user,
                    'is_reply_to_target_user': is_reply_to_target_user,
                    'replied_to_msg': replied_to_msg,
                    'reactions': msg.get('reactions', []),
                    'message_url': f"https://discord.com/channels/{data.get('guild', {}).get('id')}/{data.get('channel', {}).get('id')}/{msg.get('id')}"
                }

                self.all_messages.append(entry)
                self.messages_by_date[dt.date()].append(entry)

    def generate_complete_archive(self, output_file='user_complete_archive.md'):
        """Generate complete archive of all target user activity"""
        if not self.all_messages:
            print(f"No messages found for {self.target_username}.")
            return

        sorted_messages = sorted(
            self.all_messages, key=lambda x: x['datetime'])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.target_username} Complete Archive\n\n")
            f.write(
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
            f.write(f"**Total messages: {len(sorted_messages)}**\n\n")
            f.write(
                f"This archive contains all posts by {self.target_username} and replies to their messages.\n\n")
            f.write("---\n\n")

            current_date = None
            for msg in sorted_messages:
                if msg['date'] != current_date:
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f"\n## {day_name}, {current_date}\n\n")

                self._write_message(f, msg)

        print(f"âœ“ Complete archive generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")

    def generate_json_digest(self, output_file='user_digest.json'):
        """Generate JSON digest with full context for AI processing"""
        if not self.all_messages:
            print(f"No messages found for {self.target_username}.")
            return

        sorted_messages = sorted(
            self.all_messages, key=lambda x: x['datetime'])

        digest = {
            "metadata": {
                "username": self.target_username,
                "generated": datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
                "total_messages": len(sorted_messages),
                "date_range": {
                    "start": sorted_messages[0]['date'].isoformat() if sorted_messages else None,
                    "end": sorted_messages[-1]['date'].isoformat() if sorted_messages else None
                }
            },
            "messages": []
        }

        for msg in sorted_messages:
            message_entry = {
                "datetime": msg['datetime'].isoformat(),
                "date": msg['date'].isoformat(),
                "time": msg['time'],
                "channel": msg['channel'],
                "server": msg['server'],
                "author": msg['author'],
                "content": msg['content'],
                "message_url": msg['message_url'],
                "type": "posted_by_user" if msg['is_target_user'] else "reply_to_user"
            }

            if msg['is_target_user'] and msg['replied_to_msg']:
                replied_to = msg['replied_to_msg']
                message_entry['replied_to'] = {
                    "author": replied_to.get('author', {}).get('name', 'Unknown'),
                    "content": replied_to.get('content', ''),
                    "timestamp": replied_to.get('timestamp', '')
                }

            if msg['is_reply_to_target_user'] and msg['replied_to_msg']:
                target_msg = msg['replied_to_msg']
                message_entry['replying_to_user_message'] = {
                    "content": target_msg.get('content', ''),
                    "timestamp": target_msg.get('timestamp', '')
                }

            digest["messages"].append(message_entry)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(digest, f, indent=2, ensure_ascii=False)

        print(f"âœ“ JSON digest generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")

    def generate_weekly_digest(self, output_file='user_weekly_digest.md', days=7):
        """Generate digest of messages from the last N days"""
        cutoff_date = datetime.now().date() - timedelta(days=days)

        recent_messages = [
            msg for msg in self.all_messages
            if msg['date'] >= cutoff_date
        ]

        if not recent_messages:
            print(f"No messages found in the last {days} days.")
            return

        recent_messages.sort(key=lambda x: x['datetime'])

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.target_username} Weekly Digest\n\n")
            f.write(f"*Week of {cutoff_date} to {datetime.now().date()}*\n\n")
            f.write(
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
            f.write(f"**Messages this week: {len(recent_messages)}**\n\n")
            f.write(
                f"This digest contains {self.target_username}'s recent posts and replies to their messages.\n\n")
            f.write("---\n\n")

            current_date = None
            for msg in recent_messages:
                if msg['date'] != current_date:
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f"\n## {day_name}, {current_date}\n\n")

                self._write_message(f, msg)

        print(f"âœ“ Weekly digest generated: {output_file}")
        print(f"  Messages this week: {len(recent_messages)}")

    def _write_message(self, f, msg):
        """Write a single message entry to markdown with truncated quotes"""
        f.write(f"**[#{msg['channel']}]** ")
        f.write(f"`{msg['time']}` ")

        if msg['is_target_user']:
            f.write(f"**{msg['author']}** said:\n\n")

            if msg['replied_to_msg']:
                replied_to = msg['replied_to_msg']
                replied_author = replied_to.get(
                    'author', {}).get('name', 'Unknown')
                replied_content = replied_to.get('content', '')

                # Truncate long quotes to 100 characters
                if len(replied_content) > 100:
                    replied_content = replied_content[:100] + "... [truncated]"

                f.write(f"> *Replying to {replied_author}:*\n")
                f.write(f"> {replied_content}\n\n")

            f.write(f"{msg['content']}\n\n")

        elif msg['is_reply_to_target_user']:
            f.write(
                f"**{msg['author']}** replied to {self.target_username}:\n\n")

            if msg['replied_to_msg']:
                target_content = msg['replied_to_msg'].get('content', '')

                # Truncate long quotes to 100 characters
                if len(target_content) > 100:
                    target_content = target_content[:100] + "... [truncated]"

                f.write(f"> *{self.target_username} said:*\n")
                f.write(f"> {target_content}\n\n")

            f.write(f"{msg['content']}\n\n")

        f.write(f"[View in Discord]({msg['message_url']})\n\n")
        f.write("---\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate markdown digests of a Discord user\'s activity',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--username', '-u', default='dirvine.',
                        help='Discord username to analyze (default: dirvine.)')
    parser.add_argument('--exports', '-e', required=True,
                        help='Directory containing Discord JSON exports')
    parser.add_argument('--archive-output', default='user_complete_archive.md',
                        help='Output file for complete archive')
    parser.add_argument('--weekly-output', default='user_weekly_digest.md',
                        help='Output file for weekly digest')
    parser.add_argument('--json-output', default='user_digest.json',
                        help='Output file for JSON digest')
    parser.add_argument('--days', type=int, default=14,
                        help='Number of days for weekly digest (default: 14 - fortnightly)')
    parser.add_argument('--date-from', type=str, default=None,
                        help='Start date for filtering (ISO format: YYYY-MM-DDTHH:MM:SSZ)')
    parser.add_argument('--date-to', type=str, default=None,
                        help='End date for filtering (ISO format: YYYY-MM-DDTHH:MM:SSZ)')
    parser.add_argument('--archive-only', action='store_true',
                        help='Generate only the complete archive')
    parser.add_argument('--weekly-only', action='store_true',
                        help='Generate only the weekly digest')
    parser.add_argument('--no-json', action='store_true',
                        help='Skip JSON output generation')

    args = parser.parse_args()

    print("=" * 80)
    print("Discord User Digest Generator")
    print("=" * 80)
    print(f"Target user: {args.username}")
    print(f"Processing exports from: {args.exports}")
    if args.date_from or args.date_to:
        print(f"Date range: {args.date_from or 'start'} to {args.date_to or 'end'}\n")
    else:
        print()

    generator = DiscordUserDigestGenerator(
        args.username, 
        args.exports,
        date_from=args.date_from,
        date_to=args.date_to
    )
    generator.process_exports()

    if not args.weekly_only:
        generator.generate_complete_archive(args.archive_output)
        # Generate HTML version using separate module
        html_output = args.archive_output.replace('.md', '.html')
        html_gen = HTMLDigestGenerator(args.username)
        html_gen.generate_html_archive(generator.all_messages, html_output)

    generator.generate_weekly_digest(args.weekly_output, args.days)

    if not args.no_json:
        generator.generate_json_digest(args.json_output)

    print("\n" + "=" * 80)
    print("Generation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
