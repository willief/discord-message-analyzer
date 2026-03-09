#!/usr/bin/env python3
"""
Integration Test Suite
Tests the complete Discord digest pipeline from export to query
"""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime


class IntegrationTester:
    """Test the complete pipeline"""
    
    def __init__(self, exports_dir, username='dirvine.'):
        self.exports_dir = Path(exports_dir)
        self.username = username
        self.test_results = []
        self.warnings = []
        self.errors = []
        
    def run_all_tests(self):
        """Run complete integration test"""
        print("=" * 80)
        print("Discord Digest Pipeline - Integration Test")
        print("=" * 80)
        print(f"Exports: {self.exports_dir}")
        print(f"Username: {self.username}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Test sequence
        self.test_1_verify_exports()
        self.test_2_generate_digest()
        self.test_3_verify_outputs()
        self.test_4_query_builder()
        
        # Display results
        self.display_results()
        
        return 0 if not self.errors else 1
    
    def test_1_verify_exports(self):
        """Test 1: Verify exports are valid and fresh"""
        test_name = "Step 1: Verify Exports"
        print(f"\n{'='*80}")
        print(test_name)
        print("=" * 80)
        
        try:
            result = subprocess.run(
                ['python3', 'test_discord_digest.py', '--exports', str(self.exports_dir), '--username', self.username],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.test_results.append(f"✓ {test_name}: Exports validated successfully")
                print("✓ Exports validation PASSED")
            else:
                self.warnings.append(f"⚠ {test_name}: Exports validation had warnings")
                print("⚠ Exports validation had warnings")
                print(result.stdout)
                
        except FileNotFoundError:
            self.errors.append(f"✗ {test_name}: test_discord_digest.py not found")
            print("✗ test_discord_digest.py not found!")
        except subprocess.TimeoutExpired:
            self.errors.append(f"✗ {test_name}: Timeout")
            print("✗ Timeout!")
        except Exception as e:
            self.errors.append(f"✗ {test_name}: {e}")
            print(f"✗ Error: {e}")
    
    def test_2_generate_digest(self):
        """Test 2: Generate digest files"""
        test_name = "Step 2: Generate Digest"
        print(f"\n{'='*80}")
        print(test_name)
        print("=" * 80)
        
        try:
            result = subprocess.run(
                [
                    'python3', 'discord_digest.py',
                    '--exports', str(self.exports_dir),
                    '--username', self.username
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.test_results.append(f"✓ {test_name}: Digest generated successfully")
                print("✓ Digest generation PASSED")
                print(result.stdout)
            else:
                self.errors.append(f"✗ {test_name}: Generation failed")
                print("✗ Digest generation FAILED")
                print(result.stdout)
                print(result.stderr)
                
        except FileNotFoundError:
            self.errors.append(f"✗ {test_name}: discord_digest.py not found")
            print("✗ discord_digest.py not found!")
        except subprocess.TimeoutExpired:
            self.errors.append(f"✗ {test_name}: Timeout")
            print("✗ Timeout!")
        except Exception as e:
            self.errors.append(f"✗ {test_name}: {e}")
            print(f"✗ Error: {e}")
    
    def test_3_verify_outputs(self):
        """Test 3: Verify output files were created"""
        test_name = "Step 3: Verify Outputs"
        print(f"\n{'='*80}")
        print(test_name)
        print("=" * 80)
        
        expected_files = [
            'outputs/user_complete_archive.md',
            'outputs/user_complete_archive.html',
            'outputs/user_digest.json',
            'outputs/user_weekly_digest.md'
        ]
        
        missing_files = []
        present_files = []
        
        for filepath in expected_files:
            path = Path(filepath)
            if path.exists():
                size = path.stat().st_size
                present_files.append((filepath, size))
                print(f"✓ Found: {filepath} ({size:,} bytes)")
            else:
                missing_files.append(filepath)
                print(f"✗ Missing: {filepath}")
        
        if not missing_files:
            self.test_results.append(f"✓ {test_name}: All {len(present_files)} output files created")
        else:
            self.errors.append(f"✗ {test_name}: {len(missing_files)} files missing")
        
        # Verify HTML file is not empty and well-formed
        html_file = Path('outputs/user_complete_archive.html')
        if html_file.exists():
            try:
                content = html_file.read_text(encoding='utf-8')
                if '<html' in content.lower() and '</html>' in content.lower():
                    if '📊' in content or 'Complete Archive' in content:
                        self.test_results.append(f"✓ {test_name}: HTML file is well-formed")
                        print("✓ HTML file is well-formed with expected content")
                    else:
                        self.warnings.append(f"⚠ {test_name}: HTML may be incomplete")
                        print("⚠ HTML file missing expected content")
                else:
                    self.errors.append(f"✗ {test_name}: HTML file is malformed")
                    print("✗ HTML file is malformed")
            except Exception as e:
                self.warnings.append(f"⚠ {test_name}: Could not verify HTML - {e}")
    
    def test_4_query_builder(self):
        """Test 4: Test query builder (optional - only if running)"""
        test_name = "Step 4: Query Builder"
        print(f"\n{'='*80}")
        print(test_name)
        print("=" * 80)
        
        try:
            import requests
            
            # Try to connect to query builder
            response = requests.get('http://localhost:5000', timeout=2)
            
            if response.status_code == 200:
                # Query builder is running, test it
                try:
                    result = subprocess.run(
                        ['python3', 'test_query_builder.py', '--exports', str(self.exports_dir)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        self.test_results.append(f"✓ {test_name}: Query builder tests passed")
                        print("✓ Query builder tests PASSED")
                    else:
                        self.warnings.append(f"⚠ {test_name}: Query builder tests had warnings")
                        print("⚠ Query builder tests had warnings")
                        print(result.stdout)
                        
                except FileNotFoundError:
                    self.warnings.append(f"⚠ {test_name}: test_query_builder.py not found")
                    print("⚠ test_query_builder.py not found")
                except Exception as e:
                    self.warnings.append(f"⚠ {test_name}: {e}")
                    print(f"⚠ Error: {e}")
            else:
                print("⚠ Query builder not running (optional)")
                print("  To test: python3 discord_query_builder.py ./digests 5000")
                
        except requests.ConnectionError:
            print("⚠ Query builder not running (optional)")
            print("  To test: python3 discord_query_builder.py ./digests 5000")
        except ImportError:
            print("⚠ 'requests' module not installed (optional)")
            print("  To install: pip install requests")
        except Exception as e:
            print(f"⚠ Could not test query builder: {e}")
    
    def display_results(self):
        """Display final test summary"""
        print("\n" + "=" * 80)
        print("INTEGRATION TEST RESULTS")
        print("=" * 80)
        
        # Passed tests
        if self.test_results:
            print("\n✓ PASSED:")
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
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.errors:
            print("\n❌ INTEGRATION TESTS FAILED")
            print("Fix the errors above and try again.")
        elif self.warnings:
            print("\n⚠️  INTEGRATION TESTS PASSED WITH WARNINGS")
            print("Review the warnings but the pipeline is functional.")
        else:
            print("\n✅ ALL INTEGRATION TESTS PASSED")
            print("Your Discord digest pipeline is fully functional!")
        
        print("=" * 80)
        
        # Next steps
        if not self.errors:
            print("\n📂 Generated Files:")
            print("  - outputs/user_complete_archive.html (Open in browser!)")
            print("  - outputs/user_complete_archive.md")
            print("  - outputs/user_digest.json")
            print("  - outputs/user_weekly_digest.md")
            print("\n🎯 Next Steps:")
            print("  1. Open outputs/user_complete_archive.html in your browser")
            print("  2. Start query builder: python3 discord_query_builder.py ./digests 5000")
            print("  3. Visit http://localhost:5000 for advanced search")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Run integration tests for the complete Discord digest pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This test runs the complete pipeline:
  1. Validates Discord exports
  2. Generates digest files
  3. Verifies outputs were created
  4. Tests query builder (if running)

Example:
  python3 test_integration.py --exports ./digests --username "dirvine."
        """
    )
    
    parser.add_argument('--exports', '-e', required=True,
                       help='Directory containing Discord JSON exports')
    parser.add_argument('--username', '-u', default='dirvine.',
                       help='Username to analyze (default: dirvine.)')
    
    args = parser.parse_args()
    
    tester = IntegrationTester(args.exports, args.username)
    exit_code = tester.run_all_tests()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
