#!/usr/bin/env python3
"""
Discord User Digest Generator - Enhanced Version
Generates markdown, HTML, and JSON summaries of a specified user's Discord activity
"""

import json
import os
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
import html


class DiscordUserDigestGenerator:
    """Generate markdown, HTML, and JSON digests of a Discord user's activity"""
    
    def __init__(self, target_username, exports_directory):
        self.target_username = target_username.lower()
        self.exports_directory = exports_directory
        
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
        target_message_ids = set()
        for msg in messages:
            author = msg.get('author', {})
            # Handle both string and dict author formats
            if isinstance(author, str):
                author_name = author
            else:
                author_name = author.get('name', '')
            
            if author_name.lower() == self.target_username:
                target_message_ids.add(msg.get('id'))
        
        # Collect target user's posts and replies to them
        for msg in messages:
            author = msg.get('author', {})
            # Handle both string and dict author formats
            if isinstance(author, str):
                author_name = author
            else:
                author_name = author.get('name', '')
            
            timestamp = msg.get('timestamp')
            
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                continue
            
            # Check if this is target user's post
            is_target_user = author_name.lower() == self.target_username
            
            # Check if this is a reply to target user
            is_reply_to_target_user = False
            replied_to_msg = None
            if 'reference' in msg:
                ref_id = msg['reference'].get('messageId')
                if ref_id in target_message_ids:
                    is_reply_to_target_user = True
                    # Find the original message
                    replied_to_msg = next((m for m in messages if m.get('id') == ref_id), None)
            
            if is_target_user or is_reply_to_target_user:
                entry = {
                    'datetime': dt,
                    'date': dt.date(),
                    'time': dt.strftime('%H:%M:%S'),
                    'channel': channel_name,
                    'server': guild_name,
                    'author': author_name,
                    'content': msg.get('content', ''),
                    'is_target_user': is_target_user,
                    'is_reply_to_target_user': is_reply_to_target_user,
                    'replied_to_msg': replied_to_msg,
                    'message_url': f"https://discord.com/channels/{data.get('guild', {}).get('id')}/{data.get('channel', {}).get('id')}/{msg.get('id')}"
                }
                
                self.all_messages.append(entry)
                self.messages_by_date[dt.date()].append(entry)
    
    def generate_complete_archive(self, output_file='user_complete_archive.md'):
        """Generate complete archive of all target user activity"""
        if not self.all_messages:
            print(f"No messages found for {self.target_username}.")
            return
        
        # Sort all messages chronologically
        sorted_messages = sorted(self.all_messages, key=lambda x: x['datetime'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.target_username} Complete Archive\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
            f.write(f"**Total messages: {len(sorted_messages)}**\n\n")
            f.write(f"This archive contains all posts by {self.target_username} and replies to their messages.\n\n")
            f.write("---\n\n")
            
            current_date = None
            for msg in sorted_messages:
                # Date header
                if msg['date'] != current_date:
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f"\n## {day_name}, {current_date}\n\n")
                
                self._write_message_markdown(f, msg)
        
        print(f"✓ Complete archive generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")
    
    def generate_html_archive(self, output_file='user_complete_archive.html'):
        """Generate HTML archive of all target user activity"""
        if not self.all_messages:
            print(f"No messages found for {self.target_username}.")
            return
        
        # Sort all messages chronologically
        sorted_messages = sorted(self.all_messages, key=lambda x: x['datetime'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write HTML header
            f.write(self._get_html_header())
            
            # Write summary
            f.write(f'<div class="summary">\n')
            f.write(f'<h1>{html.escape(self.target_username)} Complete Archive</h1>\n')
            f.write(f'<p class="meta">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>\n')
            f.write(f'<p class="stats">Total messages: {len(sorted_messages)}</p>\n')
            f.write(f'<p>This archive contains all posts by {html.escape(self.target_username)} and replies to their messages.</p>\n')
            f.write('</div>\n\n')
            
            # Write messages grouped by date
            current_date = None
            for msg in sorted_messages:
                # Date header
                if msg['date'] != current_date:
                    if current_date is not None:
                        f.write('</div>\n')  # Close previous day's container
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f'<div class="day-section">\n')
                    f.write(f'<h2 class="date-header">{day_name}, {current_date}</h2>\n')
                
                self._write_message_html(f, msg)
            
            if current_date is not None:
                f.write('</div>\n')  # Close last day's container
            
            # Write HTML footer
            f.write(self._get_html_footer())
        
        print(f"✓ HTML archive generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")
    
    def generate_json_digest(self, output_file='user_digest.json'):
        """Generate JSON digest with full context for AI processing"""
        if not self.all_messages:
            print(f"No messages found for {self.target_username}.")
            return
        
        # Sort all messages chronologically
        sorted_messages = sorted(self.all_messages, key=lambda x: x['datetime'])
        
        # Build the JSON structure
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
            
            # Add context if user was replying to someone
            if msg['is_target_user'] and msg['replied_to_msg']:
                replied_to = msg['replied_to_msg']
                replied_author_field = replied_to.get('author', {})
                if isinstance(replied_author_field, str):
                    replied_author = replied_author_field
                else:
                    replied_author = replied_author_field.get('name', 'Unknown')
                message_entry['replied_to'] = {
                    "author": replied_author,
                    "content": replied_to.get('content', ''),
                    "timestamp": replied_to.get('timestamp', '')
                }
            
            # Add context if this is a reply to target user
            if msg['is_reply_to_target_user'] and msg['replied_to_msg']:
                target_msg = msg['replied_to_msg']
                message_entry['replying_to_user_message'] = {
                    "content": target_msg.get('content', ''),
                    "timestamp": target_msg.get('timestamp', '')
                }
            
            digest["messages"].append(message_entry)
        
        # Write JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(digest, f, indent=2, ensure_ascii=False)
        
        print(f"✓ JSON digest generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")
    
    def generate_weekly_digest(self, output_file='user_weekly_digest.md', days=7):
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
            f.write(f"# {self.target_username} Weekly Digest\n\n")
            f.write(f"*Week of {cutoff_date} to {datetime.now().date()}*\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n")
            f.write(f"**Messages this week: {len(recent_messages)}**\n\n")
            f.write(f"This digest contains {self.target_username}'s recent posts and replies to their messages.\n\n")
            f.write("---\n\n")
            
            current_date = None
            for msg in recent_messages:
                # Date header
                if msg['date'] != current_date:
                    current_date = msg['date']
                    day_name = msg['datetime'].strftime('%A')
                    f.write(f"\n## {day_name}, {current_date}\n\n")
                
                self._write_message_markdown(f, msg)
        
        print(f"✓ Weekly digest generated: {output_file}")
        print(f"  Messages this week: {len(recent_messages)}")
    
    def _write_message_markdown(self, f, msg):
        """Write a single message entry to markdown"""
        # Channel badge
        f.write(f"**[#{msg['channel']}]** ")
        f.write(f"`{msg['time']}` ")
        
        if msg['is_target_user']:
            f.write(f"**{msg['author']}** said:\n\n")
            
            # If target user was replying to someone, show context
            if msg['replied_to_msg']:
                replied_to = msg['replied_to_msg']
                replied_author_field = replied_to.get('author', {})
                if isinstance(replied_author_field, str):
                    replied_author = replied_author_field
                else:
                    replied_author = replied_author_field.get('name', 'Unknown')
                replied_content = replied_to.get('content', '')
                f.write(f"> *Replying to {replied_author}:*\n")
                f.write(f"> {replied_content}\n\n")
            
            f.write(f"{msg['content']}\n\n")
        
        elif msg['is_reply_to_target_user']:
            f.write(f"**{msg['author']}** replied to {self.target_username}:\n\n")
            
            # Show what target user said
            if msg['replied_to_msg']:
                target_content = msg['replied_to_msg'].get('content', '')
                f.write(f"> *{self.target_username} said:*\n")
                f.write(f"> {target_content}\n\n")
            
            f.write(f"{msg['content']}\n\n")
        
        # Link to original message
        f.write(f"[View in Discord]({msg['message_url']})\n\n")
        f.write("---\n\n")
    
    def _write_message_html(self, f, msg):
        """Write a single message entry to HTML"""
        f.write('<div class="message">\n')
        
        # Message header
        f.write('<div class="message-header">\n')
        f.write(f'<span class="channel">#{html.escape(msg["channel"])}</span>\n')
        f.write(f'<span class="time">{html.escape(msg["time"])}</span>\n')
        f.write(f'<span class="author">{html.escape(msg["author"])}</span>\n')
        f.write('</div>\n')
        
        # Message body
        f.write('<div class="message-body">\n')
        
        if msg['is_target_user']:
            # If target user was replying to someone, show context
            if msg['replied_to_msg']:
                replied_to = msg['replied_to_msg']
                replied_author_field = replied_to.get('author', {})
                if isinstance(replied_author_field, str):
                    replied_author = replied_author_field
                else:
                    replied_author = replied_author_field.get('name', 'Unknown')
                replied_content = replied_to.get('content', '')
                f.write('<div class="reply-context">\n')
                f.write(f'<strong>Replying to {html.escape(replied_author)}:</strong><br>\n')
                f.write(f'{html.escape(replied_content)}\n')
                f.write('</div>\n')
            
            f.write(f'<div class="content user-post">{html.escape(msg["content"])}</div>\n')
        
        elif msg['is_reply_to_target_user']:
            # Show what target user said
            if msg['replied_to_msg']:
                target_content = msg['replied_to_msg'].get('content', '')
                f.write('<div class="reply-context">\n')
                f.write(f'<strong>{html.escape(self.target_username)} said:</strong><br>\n')
                f.write(f'{html.escape(target_content)}\n')
                f.write('</div>\n')
            
            f.write(f'<div class="content reply-to-user">{html.escape(msg["content"])}</div>\n')
        
        f.write('</div>\n')
        
        # Link to original message
        f.write(f'<div class="message-link"><a href="{html.escape(msg["message_url"])}" target="_blank">View in Discord →</a></div>\n')
        
        f.write('</div>\n\n')
    
    def _get_html_header(self):
        """Generate HTML document header with CSS"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Message Archive</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            background: #36393f;
            color: #dcddde;
            padding: 20px;
        }
        
        .summary {
            max-width: 1200px;
            margin: 0 auto 40px;
            background: #2f3136;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: #ffffff;
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        
        .meta {
            color: #b9bbbe;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        
        .stats {
            color: #7289da;
            font-size: 1.2em;
            font-weight: bold;
            margin: 15px 0;
        }
        
        .day-section {
            max-width: 1200px;
            margin: 0 auto 40px;
        }
        
        .date-header {
            color: #ffffff;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4e5058;
        }
        
        .message {
            background: #2f3136;
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        
        .message:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .message-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #4e5058;
        }
        
        .channel {
            background: #5865f2;
            color: #ffffff;
            padding: 3px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .time {
            color: #b9bbbe;
            font-size: 0.85em;
            font-family: 'Courier New', monospace;
        }
        
        .author {
            color: #ffffff;
            font-weight: bold;
            font-size: 1.05em;
        }
        
        .message-body {
            margin: 10px 0;
        }
        
        .reply-context {
            background: #202225;
            border-left: 4px solid #4e5058;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #b9bbbe;
        }
        
        .reply-context strong {
            color: #ffffff;
        }
        
        .content {
            padding: 10px 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .user-post {
            color: #dcddde;
            font-size: 1em;
        }
        
        .reply-to-user {
            color: #dcddde;
            font-size: 1em;
            background: #292b2f;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #7289da;
        }
        
        .message-link {
            text-align: right;
            margin-top: 10px;
        }
        
        .message-link a {
            color: #00b0f4;
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.2s;
        }
        
        .message-link a:hover {
            color: #00d9ff;
            text-decoration: underline;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            .date-header {
                font-size: 1.4em;
            }
            
            .message {
                padding: 10px 15px;
            }
            
            .message-header {
                flex-wrap: wrap;
                gap: 8px;
            }
        }
    </style>
</head>
<body>
"""
    
    def _get_html_footer(self):
        """Generate HTML document footer"""
        return """</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description='Generate markdown, HTML, and JSON digests of a Discord user\'s activity',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all formats (markdown, HTML, JSON) for dirvine
  python3 discord_digest_enhanced.py --exports ./discord_exports --username "dirvine."
  
  # Generate only HTML archive
  python3 discord_digest_enhanced.py --exports ./discord_exports --username "dirvine." --html-only
  
  # Generate only JSON digest
  python3 discord_digest_enhanced.py --exports ./discord_exports --username "dirvine." --json-only
  
  # Custom output filenames
  python3 discord_digest_enhanced.py --exports ./discord_exports --username "dirvine." \\
      --archive-output dirvine_archive.md \\
      --html-output dirvine_archive.html \\
      --json-output dirvine_digest.json
        """
    )
    
    parser.add_argument('--username', '-u', default='dirvine.',
                       help='Discord username to analyze (default: dirvine.)')
    parser.add_argument('--exports', '-e', required=True,
                       help='Directory containing Discord JSON exports')
    parser.add_argument('--archive-output', default='user_complete_archive.md',
                       help='Output file for markdown archive (default: user_complete_archive.md)')
    parser.add_argument('--html-output', default='user_complete_archive.html',
                       help='Output file for HTML archive (default: user_complete_archive.html)')
    parser.add_argument('--json-output', default='user_digest.json',
                       help='Output file for JSON digest (default: user_digest.json)')
    parser.add_argument('--weekly-output', default='user_weekly_digest.md',
                       help='Output file for weekly digest (default: user_weekly_digest.md)')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days for weekly digest (default: 7)')
    parser.add_argument('--archive-only', action='store_true',
                       help='Generate only the markdown archive')
    parser.add_argument('--html-only', action='store_true',
                       help='Generate only the HTML archive')
    parser.add_argument('--json-only', action='store_true',
                       help='Generate only the JSON digest')
    parser.add_argument('--weekly-only', action='store_true',
                       help='Generate only the weekly digest')
    parser.add_argument('--no-weekly', action='store_true',
                       help='Skip weekly digest generation')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Discord User Digest Generator - Enhanced")
    print("=" * 80)
    print(f"Target user: {args.username}")
    print(f"Processing exports from: {args.exports}\n")
    
    generator = DiscordUserDigestGenerator(args.username, args.exports)
    generator.process_exports()
    
    # Determine what to generate
    generate_all = not (args.archive_only or args.html_only or args.json_only or args.weekly_only)
    
    if generate_all or args.archive_only:
        generator.generate_complete_archive(args.archive_output)
    
    if generate_all or args.html_only:
        generator.generate_html_archive(args.html_output)
    
    if generate_all or args.json_only:
        generator.generate_json_digest(args.json_output)
    
    if (generate_all or args.weekly_only) and not args.no_weekly:
        generator.generate_weekly_digest(args.weekly_output, args.days)
    
    print("\n" + "=" * 80)
    print("Generation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
