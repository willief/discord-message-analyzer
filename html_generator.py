#!/usr/bin/env python3
"""
HTML Generator for Discord Digests
Separate module for HTML output generation with color-coded threads
"""

from datetime import datetime


class HTMLDigestGenerator:
    """Generate HTML archives with color-coded threads"""

    def __init__(self, target_username):
        self.target_username = target_username

    def generate_html_archive(self, messages, output_file):
        """Generate HTML archive from processed messages"""
        if not messages:
            print(f"No messages to generate HTML for.")
            return

        sorted_messages = sorted(messages, key=lambda x: x['datetime'])

        html_content = self._generate_header(len(sorted_messages))

        current_date = None
        for msg in sorted_messages:
            # Date header
            if msg['date'] != current_date:
                current_date = msg['date']
                day_name = msg['datetime'].strftime('%A')
                html_content += f'    <div class="date-header">📅 {day_name}, {current_date}</div>\n'

            html_content += self._generate_message_html(msg)

        html_content += self._generate_footer()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ HTML archive generated: {output_file}")
        print(f"  Total messages: {len(sorted_messages)}")

    def _generate_header(self, message_count):
        """Generate HTML header with styles"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.target_username} Complete Archive</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #1e1e1e;
            color: #e0e0e0;
            line-height: 1.6;
        }}
        .header {{
            background: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #5865f2;
        }}
        h1 {{
            margin: 0 0 10px 0;
            color: #ffffff;
        }}
        .date-header {{
            background: #3d3d3d;
            padding: 10px 15px;
            margin: 20px 0 10px 0;
            border-left: 4px solid #5865f2;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .message {{
            background: #2d2d2d;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #43b581;
        }}
        .message.reply {{
            border-left-color: #faa61a;
            background: #2a2a2d;
        }}
        .message-header {{
            display: flex;
            gap: 10px;
            align-items: baseline;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}
        .channel {{
            background: #5865f2;
            color: white;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .timestamp {{
            color: #72767d;
            font-size: 0.85em;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        .author {{
            font-weight: 600;
            color: #43b581;
            font-size: 1.05em;
        }}
        .author.reply {{
            color: #faa61a;
        }}
        .replied-to {{
            color: #72767d;
            font-size: 0.9em;
        }}
        .quote {{
            border-left: 3px solid #4e5058;
            padding: 8px 0 8px 12px;
            margin: 8px 0 12px 0;
            color: #b9bbbe;
            background: #1e1e1e;
            border-radius: 4px;
            font-size: 0.95em;
        }}
        .quote-author {{
            font-weight: 600;
            color: #b9bbbe;
            margin-bottom: 4px;
        }}
        .quote-author a:hover {{
            text-decoration: underline !important;
        }}    

        .content {{
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .reactions {{
            margin-top: 10px;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .reaction {{
            background: #1a1a1d;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.9em;
            border: 1px solid #4e5058;
        }}
        .discord-link {{
            display: inline-block;
            margin-top: 10px;
            color: #00b0f4;
            text-decoration: none;
            font-size: 0.85em;
            padding: 4px 8px;
            border-radius: 4px;
            background: #1a1a1d;
        }}
        .discord-link:hover {{
            background: #2a2a2d;
            text-decoration: underline;
        }}
        .stats {{
            color: #72767d;
            font-size: 0.95em;
            margin: 5px 0 0 0;
        }}
        .truncated {{
            color: #72767d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {self.target_username} Complete Archive</h1>
        <p class="stats">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}<br>
            Total messages: {message_count}
        </p>
    </div>
"""

    def _generate_message_html(self, msg):
        """Generate HTML for a single message"""
        msg_class = "message reply" if msg['is_reply_to_target_user'] else "message"
        author_class = "author reply" if msg['is_reply_to_target_user'] else "author"

        html = f'    <div class="{msg_class}">\n'
        html += f'        <div class="message-header">\n'
        html += f'            <span class="channel">#{msg["channel"]}</span>\n'
        html += f'            <span class="timestamp">{msg["time"]}</span>\n'
        html += f'            <span class="{author_class}">{self._html_escape(msg["author"])}</span>\n'

        if msg['is_reply_to_target_user']:
            html += f'            <span class="replied-to">→ replied to {self._html_escape(self.target_username)}</span>\n'

        html += f'        </div>\n'

        # Quoted context
        if msg.get('replied_to_msg'):
            html += self._generate_quote_html(msg['replied_to_msg'])

        # Message content
        content_html = self._html_escape(msg['content'])
        html += f'        <div class="content">{content_html}</div>\n'

        # Reactions (emojis)
        if msg.get('reactions'):
            html += self._generate_reactions_html(msg['reactions'])

        html += f'        <a href="{msg["message_url"]}" class="discord-link" target="_blank">View in Discord →</a>\n'
        html += f'    </div>\n'

        return html

    def _generate_quote_html(self, replied_to_msg):
        """Generate HTML for quoted message with link to original"""
        replied_author_field = replied_to_msg.get('author', {})
        if isinstance(replied_author_field, str):
            replied_author = replied_author_field
        else:
            replied_author = replied_author_field.get('name', 'Unknown')
        replied_content = replied_to_msg.get('content', '')

        # Build link to the original message if we have the ID
        original_msg_link = None
        if 'id' in replied_to_msg:
            # Extract guild and channel IDs from the message structure
            # These should be available in the replied_to_msg data
            guild_id = replied_to_msg.get('guild_id')
            channel_id = replied_to_msg.get('channel_id')
            msg_id = replied_to_msg.get('id')

            if guild_id and channel_id and msg_id:
                original_msg_link = f"https://discord.com/channels/{guild_id}/{channel_id}/{msg_id}"

        truncated = False
        if len(replied_content) > 100:
            replied_content = replied_content[:100]
            truncated = True

        replied_content_html = self._html_escape(replied_content)
        html = f'        <div class="quote">\n'
        html += f'            <div class="quote-author">'

        if original_msg_link:
            html += f'<a href="{original_msg_link}" target="_blank" style="color: #b9bbbe; text-decoration: none;">{self._html_escape(replied_author)}</a> said:'
        else:
            html += f'{self._html_escape(replied_author)} said:'

        html += f'</div>\n'
        html += f'            {replied_content_html}'
        if truncated:
            html += f'<span class="truncated"> ... [truncated]</span>'
        html += f'\n        </div>\n'

        return html

    def _generate_reactions_html(self, reactions):
        """Generate HTML for message reactions (emojis)"""
        if not reactions:
            return ""

        html = '        <div class="reactions">\n'
        for reaction in reactions:
            emoji = reaction.get('emoji', {})
            count = reaction.get('count', 0)

            # Get emoji representation
            if emoji.get('name'):
                emoji_display = emoji['name']
                # If it's a custom emoji with ID, show the name
                if emoji.get('id'):
                    emoji_display = f":{emoji_display}:"
            else:
                emoji_display = "❓"

            html += f'            <span class="reaction">{emoji_display} {count}</span>\n'

        html += '        </div>\n'
        return html

    def _generate_footer(self):
        """Generate HTML footer"""
        return """
</body>
</html>"""

    def _html_escape(self, text):
        """Escape HTML special characters"""
        if not text:
            return ""
        return (str(text)
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
