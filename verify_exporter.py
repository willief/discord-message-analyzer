#!/usr/bin/env python3
"""
Pre-Export Verification Script
Checks that DiscordChatExporter is properly installed and configured before running exports
"""

import subprocess
import sys
import os
from pathlib import Path


class ExporterVerifier:
    """Verify DiscordChatExporter setup"""
    
    def __init__(self):
        self.checks_passed = []
        self.checks_failed = []
        self.warnings = []
        
    def run_all_checks(self):
        """Run all verification checks"""
        print("=" * 80)
        print("DiscordChatExporter Pre-Export Verification")
        print("=" * 80)
        print()
        
        self.check_exporter_installed()
        self.check_exporter_executable()
        self.check_token_configured()
        self.check_output_directory()
        
        self.display_results()
        
        return len(self.checks_failed) == 0
    
    def check_exporter_installed(self):
        """Check if DiscordChatExporter exists"""
        test_name = "DiscordChatExporter Installation"
        
        possible_paths = [
            './discord-exporter/DiscordChatExporter.Cli',
            './DiscordChatExporter.Cli',
            'discord-exporter/DiscordChatExporter.Cli',
        ]
        
        found_path = None
        for path in possible_paths:
            if Path(path).exists():
                found_path = path
                break
        
        if found_path:
            self.checks_passed.append(f"✓ {test_name}: Found at {found_path}")
            self.exporter_path = found_path
        else:
            self.checks_failed.append(f"✗ {test_name}: Not found")
            self.exporter_path = None
            print(f"\n❌ DiscordChatExporter not found!\n")
            print("To install:")
            print("  wget https://github.com/Tyrrrz/DiscordChatExporter/releases/latest/download/DiscordChatExporter.Cli.linux-x64.zip")
            print("  unzip DiscordChatExporter.Cli.linux-x64.zip -d discord-exporter")
            print("  chmod +x discord-exporter/DiscordChatExporter.Cli")
            print()
    
    def check_exporter_executable(self):
        """Check if DiscordChatExporter is executable"""
        test_name = "Executable Permissions"
        
        if not self.exporter_path:
            return
        
        path = Path(self.exporter_path)
        
        if os.access(path, os.X_OK):
            # Try to get version
            try:
                result = subprocess.run(
                    [self.exporter_path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                version_info = result.stdout.strip() or result.stderr.strip()
                if version_info:
                    self.checks_passed.append(f"✓ {test_name}: Executable ({version_info})")
                else:
                    self.checks_passed.append(f"✓ {test_name}: Executable")
                    
            except subprocess.TimeoutExpired:
                self.warnings.append(f"⚠ {test_name}: File is executable but --version timed out")
            except Exception as e:
                self.warnings.append(f"⚠ {test_name}: File is executable but error running: {e}")
        else:
            self.checks_failed.append(f"✗ {test_name}: Not executable")
            print(f"\n❌ File not executable!\n")
            print(f"Fix with: chmod +x {self.exporter_path}")
            print()
    
    def check_token_configured(self):
        """Check if Discord token is configured"""
        test_name = "Discord Token"
        
        token_env = os.environ.get('DISCORD_TOKEN') or os.environ.get('DISCORD_BOT_TOKEN')
        
        if token_env:
            # Don't print the actual token, just confirm it exists
            token_preview = token_env[:10] + "..." if len(token_env) > 10 else "***"
            self.checks_passed.append(f"✓ {test_name}: Configured ({token_preview})")
        else:
            self.warnings.append(f"⚠ {test_name}: Not found in environment variables")
            print(f"\n⚠️  Discord token not configured in environment!\n")
            print("You'll need to provide the token when running exports.")
            print("To set it permanently:")
            print("  export DISCORD_TOKEN='your-token-here'")
            print("  # Add to ~/.bashrc or ~/.zshrc to make permanent")
            print()
    
    def check_output_directory(self):
        """Check if output directory exists or can be created"""
        test_name = "Output Directory"
        
        output_dirs = ['./digests', './discord_exports', './exports']
        
        existing = [d for d in output_dirs if Path(d).exists()]
        
        if existing:
            self.checks_passed.append(f"✓ {test_name}: Found {', '.join(existing)}")
        else:
            self.warnings.append(f"⚠ {test_name}: No standard output directory found")
            print(f"\n⚠️  No output directory found!\n")
            print("Create one with:")
            print("  mkdir -p digests")
            print()
    
    def display_results(self):
        """Display all check results"""
        print("\n" + "=" * 80)
        print("VERIFICATION RESULTS")
        print("=" * 80)
        
        if self.checks_passed:
            print("\n✓ PASSED:")
            for check in self.checks_passed:
                print(f"  {check}")
        
        if self.warnings:
            print("\n⚠ WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.checks_failed:
            print("\n✗ FAILED:")
            for check in self.checks_failed:
                print(f"  {check}")
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Passed: {len(self.checks_passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Failed: {len(self.checks_failed)}")
        
        if self.checks_failed:
            print("\n❌ VERIFICATION FAILED - Fix errors above before exporting")
        elif self.warnings:
            print("\n⚠️  VERIFICATION PASSED WITH WARNINGS")
        else:
            print("\n✅ ALL CHECKS PASSED - Ready to export!")
        
        print("=" * 80)


def show_export_command_examples():
    """Show example export commands"""
    print("\n" + "=" * 80)
    print("EXPORT COMMAND EXAMPLES")
    print("=" * 80)
    print("""
# Export a single channel:
./discord-exporter/DiscordChatExporter.Cli export \\
  -t "YOUR_DISCORD_TOKEN" \\
  -c "CHANNEL_ID" \\
  -f Json \\
  -o "digests/channel-name.json"

# Export with date range (last 7 days):
./discord-exporter/DiscordChatExporter.Cli export \\
  -t "YOUR_DISCORD_TOKEN" \\
  -c "CHANNEL_ID" \\
  -f Json \\
  --after "$(date -d '7 days ago' -Idate)" \\
  -o "digests/channel-name.json"

# Export multiple channels (using channel IDs from your Discord server):
# general-chat: CHANNEL_ID_1
# general-support: CHANNEL_ID_2
# bug-reports: CHANNEL_ID_3

for channel_id in CHANNEL_ID_1 CHANNEL_ID_2 CHANNEL_ID_3; do
  ./discord-exporter/DiscordChatExporter.Cli export \\
    -t "YOUR_DISCORD_TOKEN" \\
    -c "$channel_id" \\
    -f Json \\
    -o "digests/channel-$channel_id.json"
done
""")
    print("=" * 80)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verify DiscordChatExporter setup before running exports'
    )
    
    parser.add_argument('--show-examples', action='store_true',
                       help='Show example export commands')
    
    args = parser.parse_args()
    
    verifier = ExporterVerifier()
    success = verifier.run_all_checks()
    
    if args.show_examples:
        show_export_command_examples()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
