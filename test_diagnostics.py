#!/usr/bin/env python3
"""
Discord Digest Generator - Diagnostic Test Suite
Tests exports, JSON validity, message counts, and more
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class DigestDiagnostics:
    """Run diagnostic tests on Discord exports"""

    def __init__(self, exports_dir):
        self.exports_dir = Path(exports_dir)
        self.results = []
        self.warnings = []
        self.errors = []

    def run_all_tests(self):
        """Run complete diagnostic suite"""
        print("=" * 80)
        print("📋 Discord Digest Generator - Diagnostics")
        print("=" * 80)
        print(f"Testing: {self.exports_dir}\n")

        self.test_directory_exists()
        self.test_json_files_found()
        self.test_json_validity()
        self.test_message_counts()
        self.test_user_presence()
        self.test_channels()
        self.test_date_ranges()

        self.print_results()
        return 0 if not self.errors else 1

    def test_directory_exists(self):
        """Check if exports directory exists"""
        if self.exports_dir.exists():
            self.results.append(f"✓ Directory exists: {self.exports_dir}")
        else:
            self.errors.append(f"❌ Directory not found: {self.exports_dir}")

    def test_json_files_found(self):
        """Check for JSON export files"""
        json_files = list(self.exports_dir.glob('*.json'))

        if not json_files:
            self.errors.append("❌ No .json files found in exports directory")
            return

        self.results.append(f"✓ Found {len(json_files)} JSON export files:")
        for f in sorted(json_files):
            size_mb = f.stat().st_size / (1024 * 1024)
            self.results.append(f"  - {f.name} ({size_mb:.2f} MB)")

    def test_json_validity(self):
        """Validate JSON structure"""
        json_files = list(self.exports_dir.glob('*.json'))

        if not json_files:
            return

        invalid = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Check structure
                if 'messages' not in data:
                    invalid.append((json_file.name, "Missing 'messages' key"))
                elif not isinstance(data['messages'], list):
                    invalid.append(
                        (json_file.name, "'messages' is not a list"))
                elif not data['messages']:
                    self.warnings.append(f"⚠ {json_file.name}: No messages")

            except json.JSONDecodeError as e:
                invalid.append(
                    (json_file.name, f"Invalid JSON: {str(e)[:50]}"))
            except Exception as e:
                invalid.append((json_file.name, f"Error: {str(e)[:50]}"))

        if invalid:
            for name, error in invalid:
                self.errors.append(f"❌ {name}: {error}")
        else:
            self.results.append("✓ All JSON files valid")

    def test_message_counts(self):
        """Count total messages"""
        json_files = list(self.exports_dir.glob('*.json'))

        if not json_files:
            return

        total = 0
        by_channel = defaultdict(int)

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                messages = data.get('messages', [])
                channel = data.get('channel', {}).get('name', 'Unknown')
                by_channel[channel] = len(messages)
                total += len(messages)

            except:
                continue

        self.results.append(f"✓ Total messages: {total:,}")
        self.results.append("  By channel:")
        for channel, count in sorted(by_channel.items(), key=lambda x: x[1], reverse=True):
            self.results.append(f"    - {channel}: {count:,}")

    def test_user_presence(self):
        """Check for target users in exports"""
        json_files = list(self.exports_dir.glob('*.json'))
        users_to_find = ["dirvine.", "forthebux", "JimCollinson"]
        found_users = defaultdict(int)

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for msg in data.get('messages', []):
                    author = msg.get('author', {})
                    author_name = author.get('name', '') if isinstance(
                        author, dict) else str(author)
                    if author_name in users_to_find:
                        found_users[author_name] += 1

            except:
                continue

        if found_users:
            self.results.append("✓ Users found in exports:")
            for user, count in sorted(found_users.items()):
                self.results.append(f"  - {user}: {count} messages")
        else:
            self.warnings.append(
                "⚠ None of the default users found in exports")
            self.results.append("  To-find: " + ", ".join(users_to_find))

    def test_channels(self):
        """List all channels in exports"""
        json_files = list(self.exports_dir.glob('*.json'))
        channels = set()

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                channel = data.get('channel', {}).get('name', 'Unknown')
                channels.add(channel)
            except:
                continue

        if channels:
            self.results.append(f"✓ Channels exported: {len(channels)}")
            for channel in sorted(channels):
                self.results.append(f"  - {channel}")

    def test_date_ranges(self):
        """Check date coverage"""
        json_files = list(self.exports_dir.glob('*.json'))

        earliest = None
        latest = None

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for msg in data.get('messages', []):
                    try:
                        dt = datetime.fromisoformat(
                            msg.get('timestamp', '').replace('Z', '+00:00'))
                        if earliest is None or dt < earliest:
                            earliest = dt
                        if latest is None or dt > latest:
                            latest = dt
                    except:
                        continue
            except:
                continue

        if earliest and latest:
            days = (latest - earliest).days
            self.results.append(
                f"✓ Date range: {earliest.date()} to {latest.date()} ({days} days)")
        else:
            self.warnings.append("⚠ Could not determine date range")

    def print_results(self):
        """Print formatted results"""
        print("\n" + "=" * 80)
        print("📊 RESULTS")
        print("=" * 80)

        if self.results:
            print("\n✅ PASSED:")
            for r in self.results:
                print(f"  {r}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for w in self.warnings:
                print(f"  {w}")

        if self.errors:
            print("\n❌ ERRORS:")
            for e in self.errors:
                print(f"  {e}")

        print("\n" + "=" * 80)
        print("📈 SUMMARY")
        print("=" * 80)
        print(f"Passed:  {len(self.results)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors:   {len(self.errors)}")

        if self.errors:
            print("\n❌ Issues found - review errors above")
        elif self.warnings:
            print("\n⚠️  Warnings present - check above")
        else:
            print("\n✅ All checks passed!")

        print("=" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Diagnostic test suite for Discord exports')
    parser.add_argument('--exports', '-e', default='./discord_exports',
                        help='Exports directory (default: ./discord_exports)')

    args = parser.parse_args()

    tester = DigestDiagnostics(args.exports)
    exit_code = tester.run_all_tests()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
