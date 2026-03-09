#!/usr/bin/env python3
"""
Test Suite for Discord Digest Generator
Verifies that exports are fresh and processing is working correctly
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class DiscordDigestTester:
    """Test suite for Discord digest generation"""
    
    def __init__(self, exports_directory):
        self.exports_directory = Path(exports_directory)
        self.test_results = []
        self.warnings = []
        self.errors = []
        
    def run_all_tests(self):
        """Run all tests and display results"""
        print("=" * 80)
        print("Discord Digest Generator - Test Suite")
        print("=" * 80)
        print(f"Testing directory: {self.exports_directory}\n")
        
        # Run tests
        self.test_exports_exist()
        self.test_exports_fresh()
        self.test_json_validity()
        self.test_channels_present()
        self.test_recent_activity()
        self.test_user_presence()
        self.test_file_sizes()
        
        # Display results
        self.display_results()
        
        # Return exit code
        return 0 if not self.errors else 1
    
    def test_exports_exist(self):
        """Test 1: Check if export files exist"""
        test_name = "Export Files Exist"
        
        if not self.exports_directory.exists():
            self.errors.append(f"{test_name}: Directory '{self.exports_directory}' does not exist")
            return
        
        json_files = list(self.exports_directory.rglob('*.json'))
        
        if not json_files:
            self.errors.append(f"{test_name}: No JSON files found in {self.exports_directory}")
        else:
            self.test_results.append(f"✓ {test_name}: Found {len(json_files)} export files")
    
    def test_exports_fresh(self):
        """Test 2: Check if exports are recent (within last 7 days)"""
        test_name = "Exports Are Fresh"
        
        json_files = list(self.exports_directory.rglob('*.json'))
        if not json_files:
            return
        
        cutoff_date = datetime.now() - timedelta(days=7)
        stale_files = []
        
        for json_file in json_files:
            mod_time = datetime.fromtimestamp(json_file.stat().st_mtime)
            if mod_time < cutoff_date:
                stale_files.append((json_file.name, mod_time))
        
        if stale_files:
            self.warnings.append(f"{test_name}: {len(stale_files)} files older than 7 days")
            for filename, mod_time in stale_files:
                self.warnings.append(f"  - {filename}: Last modified {mod_time.strftime('%Y-%m-%d %H:%M')}")
        else:
            self.test_results.append(f"✓ {test_name}: All exports modified within last 7 days")
    
    def test_json_validity(self):
        """Test 3: Verify JSON files are valid and have expected structure"""
        test_name = "JSON Files Valid"
        
        json_files = list(self.exports_directory.rglob('*.json'))
        if not json_files:
            return
        
        # Skip known output files (not Discord exports)
        skip_files = {
            'user_digest.json', 'colored.json', 'with_emojis.json', 
            'with_links.json', 'truncated.json', 'test_run.json'
        }
        
        invalid_files = []
        skipped_count = 0
        
        for json_file in json_files:
            # Skip output files
            if json_file.name in skip_files:
                skipped_count += 1
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check for expected structure
                if 'channel' not in data or 'messages' not in data:
                    invalid_files.append((json_file.name, "Missing 'channel' or 'messages' key"))
                elif not isinstance(data['messages'], list):
                    invalid_files.append((json_file.name, "'messages' is not a list"))
                    
            except json.JSONDecodeError as e:
                invalid_files.append((json_file.name, f"Invalid JSON: {e}"))
            except Exception as e:
                invalid_files.append((json_file.name, f"Error: {e}"))
        
        if invalid_files:
            for filename, error in invalid_files:
                self.errors.append(f"{test_name}: {filename} - {error}")
        else:
            result_msg = f"✓ {test_name}: All JSON files are valid"
            if skipped_count > 0:
                result_msg += f" ({skipped_count} output files skipped)"
            self.test_results.append(result_msg)
    
    def test_channels_present(self):
        """Test 4: Verify expected channels are present"""
        test_name = "Expected Channels Present"
        
        expected_channels = ['general-chat', 'general-support', 'bug-reports']
        json_files = list(self.exports_directory.rglob('*.json'))
        
        if not json_files:
            return
        
        found_channels = set()
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                channel_name = data.get('channel', {}).get('name', 'Unknown')
                found_channels.add(channel_name)
            except:
                continue
        
        # Check for exact matches or partial matches (to handle emoji prefixes)
        found_base_channels = set()
        for channel in found_channels:
            # Extract base channel name (remove emoji prefixes like 🌐︱)
            base_name = channel.split('︱')[-1] if '︱' in channel else channel
            found_base_channels.add(base_name)
        
        missing_channels = set(expected_channels) - found_base_channels
        
        if missing_channels:
            self.warnings.append(f"{test_name}: Missing channels: {', '.join(missing_channels)}")
        
        if found_channels:
            self.test_results.append(f"✓ {test_name}: Found channels: {', '.join(sorted(found_channels))}")
    
    def test_recent_activity(self):
        """Test 5: Check for recent messages (within last 24 hours)"""
        test_name = "Recent Activity Detected"
        
        json_files = list(self.exports_directory.rglob('*.json'))
        if not json_files:
            return
        
        cutoff_date = datetime.now() - timedelta(hours=24)
        channels_with_activity = {}
        
        # Skip known output files
        skip_files = {
            'user_digest.json', 'colored.json', 'with_emojis.json', 
            'with_links.json', 'truncated.json', 'test_run.json'
        }
        
        for json_file in json_files:
            if json_file.name in skip_files:
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                channel_name = data.get('channel', {}).get('name', 'Unknown')
                messages = data.get('messages', [])
                
                recent_count = 0
                latest_message_time = None
                
                for msg in messages:
                    try:
                        timestamp = msg.get('timestamp', '')
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        
                        if latest_message_time is None or dt > latest_message_time:
                            latest_message_time = dt
                        
                        # Make cutoff timezone-aware
                        cutoff_aware = cutoff_date.replace(tzinfo=dt.tzinfo)
                        if dt > cutoff_aware:
                            recent_count += 1
                    except:
                        continue
                
                channels_with_activity[channel_name] = {
                    'recent_count': recent_count,
                    'latest': latest_message_time
                }
                
            except Exception as e:
                continue
        
        if not channels_with_activity:
            self.errors.append(f"{test_name}: Could not analyze activity")
            return
        
        # Report on each channel
        for channel, stats in channels_with_activity.items():
            if stats['latest']:
                age = datetime.now(stats['latest'].tzinfo) - stats['latest']
                age_hours = int(age.total_seconds() / 3600)
                
                if age_hours < 1:
                    age_str = f"{int(age.total_seconds() / 60)} minutes ago"
                else:
                    age_str = f"{age_hours} hours ago"
                
                if stats['recent_count'] > 0:
                    self.test_results.append(
                        f"✓ {channel}: {stats['recent_count']} messages in last 24h, "
                        f"latest {age_str}"
                    )
                else:
                    # Only warn if it's been more than 24 hours
                    if age_hours >= 24:
                        self.warnings.append(
                            f"{channel}: No messages in last 24h, latest was {age_str}"
                        )
                    else:
                        self.test_results.append(
                            f"✓ {channel}: Latest message {age_str} (within 24h)"
                        )
    
    def test_user_presence(self, target_username='dirvine.'):
        """Test 6: Verify target user has recent posts"""
        test_name = "Target User Activity"
        
        json_files = list(self.exports_directory.rglob('*.json'))
        if not json_files:
            return
        
        cutoff_date = datetime.now() - timedelta(days=7)
        user_messages = []
        
        # Skip known output files
        skip_files = {
            'user_digest.json', 'colored.json', 'with_emojis.json', 
            'with_links.json', 'truncated.json', 'test_run.json'
        }
        
        for json_file in json_files:
            if json_file.name in skip_files:
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                messages = data.get('messages', [])
                channel_name = data.get('channel', {}).get('name', 'Unknown')
                
                for msg in messages:
                    author = msg.get('author', {})
                    # Handle both string and dict formats
                    if isinstance(author, str):
                        author_name = author
                    else:
                        author_name = author.get('name', '')
                    
                    if author_name.lower() == target_username.lower():
                        try:
                            timestamp = msg.get('timestamp', '')
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            
                            if dt > cutoff_date:
                                user_messages.append({
                                    'channel': channel_name,
                                    'time': dt
                                })
                        except:
                            continue
            except:
                continue
        
        if not user_messages:
            self.warnings.append(
                f"{test_name}: No messages from '{target_username}' in last 7 days"
            )
        else:
            # Group by channel
            by_channel = defaultdict(int)
            for msg in user_messages:
                by_channel[msg['channel']] += 1
            
            total = len(user_messages)
            channel_summary = ', '.join([f"{ch}: {count}" for ch, count in by_channel.items()])
            
            self.test_results.append(
                f"✓ {test_name}: {total} messages from '{target_username}' in last 7 days"
            )
            self.test_results.append(f"  By channel: {channel_summary}")
    
    def test_file_sizes(self):
        """Test 7: Check that export files aren't empty or suspiciously small"""
        test_name = "File Sizes OK"
        
        json_files = list(self.exports_directory.rglob('*.json'))
        if not json_files:
            return
        
        small_files = []
        empty_files = []
        
        for json_file in json_files:
            size = json_file.stat().st_size
            
            if size == 0:
                empty_files.append(json_file.name)
            elif size < 1024:  # Less than 1KB is suspicious
                small_files.append((json_file.name, size))
        
        if empty_files:
            self.errors.append(f"{test_name}: Empty files: {', '.join(empty_files)}")
        
        if small_files:
            for filename, size in small_files:
                self.warnings.append(f"{test_name}: Small file {filename} ({size} bytes)")
        
        if not empty_files and not small_files:
            total_size = sum(f.stat().st_size for f in json_files)
            size_mb = total_size / (1024 * 1024)
            self.test_results.append(f"✓ {test_name}: Total {size_mb:.2f} MB across all files")
    
    def display_results(self):
        """Display test results in a formatted way"""
        print("\n" + "=" * 80)
        print("TEST RESULTS")
        print("=" * 80)
        
        # Passed tests
        if self.test_results:
            print("\n✓ PASSED TESTS:")
            for result in self.test_results:
                print(f"  {result}")
        
        # Warnings
        if self.warnings:
            print("\n⚠ WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        # Errors
        if self.errors:
            print("\n✗ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Passed: {len(self.test_results)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n❌ TESTS FAILED - Please address errors above")
        elif self.warnings:
            print("\n⚠️  TESTS PASSED WITH WARNINGS - Review warnings above")
        else:
            print("\n✅ ALL TESTS PASSED")
        
        print("=" * 80)


def test_discordchatexporter_installed():
    """Test if DiscordChatExporter is available"""
    import subprocess
    
    print("\n" + "=" * 80)
    print("Testing DiscordChatExporter Installation")
    print("=" * 80)
    
    # Common locations
    possible_paths = [
        './discord-exporter/DiscordChatExporter.Cli',
        './DiscordChatExporter.Cli',
        'DiscordChatExporter.Cli',
    ]
    
    found = False
    for path in possible_paths:
        try:
            result = subprocess.run(
                [path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 or 'DiscordChatExporter' in result.stdout + result.stderr:
                print(f"✓ DiscordChatExporter found at: {path}")
                print(f"  Output: {result.stdout.strip() or result.stderr.strip()}")
                found = True
                break
        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
            continue
    
    if not found:
        print("⚠️  DiscordChatExporter not found in common locations")
        print("   Checked paths:")
        for path in possible_paths:
            print(f"   - {path}")
        print("\n   To install:")
        print("   wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip")
        print("   unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter")
        print("   chmod +x discord-exporter/DiscordChatExporter.Cli")
    
    print("=" * 80)
    return found


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test Discord exports and processing pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--exports', '-e', required=True,
                       help='Directory containing Discord JSON exports')
    parser.add_argument('--username', '-u', default='dirvine.',
                       help='Username to check for activity (default: dirvine.)')
    parser.add_argument('--check-exporter', action='store_true',
                       help='Also check if DiscordChatExporter is installed')
    
    args = parser.parse_args()
    
    # Test exports
    tester = DiscordDigestTester(args.exports)
    exit_code = tester.run_all_tests()
    
    # Test DiscordChatExporter if requested
    if args.check_exporter:
        test_discordchatexporter_installed()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
