#!/usr/bin/env python3
"""
Test Suite for Discord Query Builder
Verifies that the query engine and web interface are working correctly
"""

import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class QueryBuilderTester:
    """Test suite for Discord Query Builder"""
    
    def __init__(self, exports_directory, base_url='http://localhost:5000'):
        self.exports_directory = Path(exports_directory)
        self.base_url = base_url
        self.test_results = []
        self.warnings = []
        self.errors = []
        
    def run_all_tests(self):
        """Run all tests and display results"""
        print("=" * 80)
        print("Discord Query Builder - Test Suite")
        print("=" * 80)
        print(f"Testing exports: {self.exports_directory}")
        print(f"Testing server: {self.base_url}\n")
        
        # Run tests
        self.test_exports_valid()
        self.test_server_running()
        self.test_query_endpoint()
        self.test_filters()
        self.test_export_endpoint()
        self.test_statistics()
        
        # Display results
        self.display_results()
        
        # Return exit code
        return 0 if not self.errors else 1
    
    def test_exports_valid(self):
        """Test 1: Verify exports directory is valid"""
        test_name = "Exports Directory Valid"
        
        if not self.exports_directory.exists():
            self.errors.append(f"{test_name}: Directory '{self.exports_directory}' does not exist")
            return
        
        json_files = list(self.exports_directory.rglob('*.json'))
        
        # Skip output files
        skip_files = {
            'user_digest.json', 'colored.json', 'with_emojis.json',
            'with_links.json', 'truncated.json', 'test_run.json'
        }
        export_files = [f for f in json_files if f.name not in skip_files]
        
        if not export_files:
            self.errors.append(f"{test_name}: No valid export JSON files found")
        else:
            self.test_results.append(f"✓ {test_name}: Found {len(export_files)} export files")
    
    def test_server_running(self):
        """Test 2: Check if query builder server is running"""
        test_name = "Server Running"
        
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.test_results.append(f"✓ {test_name}: Server responding on {self.base_url}")
            else:
                self.errors.append(f"{test_name}: Server returned status {response.status_code}")
        except requests.ConnectionError:
            self.errors.append(f"{test_name}: Cannot connect to {self.base_url}")
            self.warnings.append("  Start server with: python3 discord_query_builder.py ./digests 5000")
        except requests.Timeout:
            self.errors.append(f"{test_name}: Server timeout")
        except Exception as e:
            self.errors.append(f"{test_name}: Error - {e}")
    
    def test_query_endpoint(self):
        """Test 3: Test basic query endpoint"""
        test_name = "Query Endpoint"
        
        try:
            # Test empty query (should return all messages)
            response = requests.post(
                f"{self.base_url}/api/query",
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'results' in data and 'statistics' in data:
                    total = len(data['results'])
                    self.test_results.append(f"✓ {test_name}: Endpoint working, {total} total messages")
                else:
                    self.errors.append(f"{test_name}: Invalid response structure")
            else:
                self.errors.append(f"{test_name}: HTTP {response.status_code}")
                
        except requests.ConnectionError:
            self.errors.append(f"{test_name}: Server not running")
        except Exception as e:
            self.errors.append(f"{test_name}: Error - {e}")
    
    def test_filters(self):
        """Test 4: Test various filter combinations"""
        test_name = "Filter Functionality"
        
        try:
            # Test 1: Username filter
            response = requests.post(
                f"{self.base_url}/api/query",
                json={"username": "dirvine."},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                user_count = len(data['results'])
                self.test_results.append(f"✓ {test_name} (Username): Found {user_count} messages from 'dirvine.'")
            else:
                self.warnings.append(f"{test_name} (Username): HTTP {response.status_code}")
            
            # Test 2: Date filter
            today = datetime.now().date()
            week_ago = today - timedelta(days=7)
            
            response = requests.post(
                f"{self.base_url}/api/query",
                json={
                    "date_from": week_ago.isoformat(),
                    "date_to": today.isoformat()
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                date_count = len(data['results'])
                self.test_results.append(f"✓ {test_name} (Date Range): Found {date_count} messages in last 7 days")
            else:
                self.warnings.append(f"{test_name} (Date Range): HTTP {response.status_code}")
            
            # Test 3: Keyword filter
            response = requests.post(
                f"{self.base_url}/api/query",
                json={"keyword": "test"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                keyword_count = len(data['results'])
                self.test_results.append(f"✓ {test_name} (Keyword): Found {keyword_count} messages with 'test'")
            else:
                self.warnings.append(f"{test_name} (Keyword): HTTP {response.status_code}")
            
            # Test 4: Limit filter
            response = requests.post(
                f"{self.base_url}/api/query",
                json={"limit": 10},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if len(data['results']) <= 10:
                    self.test_results.append(f"✓ {test_name} (Limit): Correctly limited to {len(data['results'])} results")
                else:
                    self.warnings.append(f"{test_name} (Limit): Returned {len(data['results'])} results (expected ≤10)")
            else:
                self.warnings.append(f"{test_name} (Limit): HTTP {response.status_code}")
                
        except requests.ConnectionError:
            self.errors.append(f"{test_name}: Server not running")
        except Exception as e:
            self.errors.append(f"{test_name}: Error - {e}")
    
    def test_export_endpoint(self):
        """Test 5: Test export endpoints (JSON and CSV)"""
        test_name = "Export Endpoints"
        
        try:
            # Test JSON export
            response = requests.post(
                f"{self.base_url}/api/export",
                json={
                    "filters": {"limit": 5},
                    "format": "json"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                if response.headers.get('Content-Type', '').startswith('application/json'):
                    self.test_results.append(f"✓ {test_name} (JSON): Export working")
                else:
                    # Might be file download
                    self.test_results.append(f"✓ {test_name} (JSON): File download working")
            else:
                self.warnings.append(f"{test_name} (JSON): HTTP {response.status_code}")
            
            # Test CSV export
            response = requests.post(
                f"{self.base_url}/api/export",
                json={
                    "filters": {"limit": 5},
                    "format": "csv"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                self.test_results.append(f"✓ {test_name} (CSV): Export working")
            else:
                self.warnings.append(f"{test_name} (CSV): HTTP {response.status_code}")
                
        except requests.ConnectionError:
            self.errors.append(f"{test_name}: Server not running")
        except Exception as e:
            self.errors.append(f"{test_name}: Error - {e}")
    
    def test_statistics(self):
        """Test 6: Verify statistics are calculated correctly"""
        test_name = "Statistics Calculation"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/query",
                json={"limit": 100},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('statistics', {})
                
                checks = []
                
                # Check total matches results
                if stats.get('total') == len(data['results']):
                    checks.append("total count")
                
                # Check date range exists
                if 'date_range' in stats and stats['date_range']:
                    checks.append("date range")
                
                # Check top authors exists
                if 'top_authors' in stats and isinstance(stats['top_authors'], list):
                    checks.append("top authors")
                
                # Check channel breakdown exists
                if 'by_channel' in stats and isinstance(stats['by_channel'], list):
                    checks.append("channel breakdown")
                
                if checks:
                    self.test_results.append(f"✓ {test_name}: Calculating {', '.join(checks)}")
                else:
                    self.warnings.append(f"{test_name}: Statistics incomplete")
            else:
                self.warnings.append(f"{test_name}: HTTP {response.status_code}")
                
        except requests.ConnectionError:
            self.errors.append(f"{test_name}: Server not running")
        except Exception as e:
            self.errors.append(f"{test_name}: Error - {e}")
    
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


class QueryBuilderPerformanceTester:
    """Performance tests for query builder"""
    
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        
    def run_performance_tests(self):
        """Run performance benchmarks"""
        print("\n" + "=" * 80)
        print("PERFORMANCE TESTS")
        print("=" * 80)
        
        tests = [
            ("Small query (10 results)", {"limit": 10}),
            ("Medium query (100 results)", {"limit": 100}),
            ("Large query (1000 results)", {"limit": 1000}),
            ("Keyword search", {"keyword": "test", "limit": 100}),
            ("Date range query", {
                "date_from": (datetime.now() - timedelta(days=30)).date().isoformat(),
                "limit": 100
            }),
        ]
        
        results = []
        
        for test_name, query in tests:
            try:
                start = datetime.now()
                response = requests.post(
                    f"{self.base_url}/api/query",
                    json=query,
                    timeout=30
                )
                duration = (datetime.now() - start).total_seconds()
                
                if response.status_code == 200:
                    data = response.json()
                    count = len(data['results'])
                    results.append((test_name, duration, count))
                    print(f"✓ {test_name}: {duration:.3f}s ({count} results)")
                else:
                    print(f"✗ {test_name}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"✗ {test_name}: Error - {e}")
        
        if results:
            print("\n" + "=" * 80)
            print("PERFORMANCE SUMMARY")
            print("=" * 80)
            avg_time = sum(r[1] for r in results) / len(results)
            print(f"Average query time: {avg_time:.3f}s")
            
            slowest = max(results, key=lambda x: x[1])
            print(f"Slowest query: {slowest[0]} ({slowest[1]:.3f}s)")
            
            fastest = min(results, key=lambda x: x[1])
            print(f"Fastest query: {fastest[0]} ({fastest[1]:.3f}s)")
        
        print("=" * 80)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test Discord Query Builder functionality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test query builder on default port
  python3 test_query_builder.py --exports ./digests
  
  # Test on custom port
  python3 test_query_builder.py --exports ./digests --port 8080
  
  # Include performance tests
  python3 test_query_builder.py --exports ./digests --performance
  
  # Test without server (offline tests only)
  python3 test_query_builder.py --exports ./digests --offline
        """
    )
    
    parser.add_argument('--exports', '-e', required=True,
                       help='Directory containing Discord JSON exports')
    parser.add_argument('--port', '-p', type=int, default=5000,
                       help='Port where query builder is running (default: 5000)')
    parser.add_argument('--performance', action='store_true',
                       help='Run performance benchmarks')
    parser.add_argument('--offline', action='store_true',
                       help='Skip server tests (only test exports)')
    
    args = parser.parse_args()
    
    base_url = f"http://localhost:{args.port}"
    
    # Run functional tests
    tester = QueryBuilderTester(args.exports, base_url)
    
    if args.offline:
        # Only run export validation test
        print("=" * 80)
        print("Running offline tests only")
        print("=" * 80)
        tester.test_exports_valid()
        tester.display_results()
    else:
        exit_code = tester.run_all_tests()
        
        # Run performance tests if requested
        if args.performance and exit_code == 0:
            perf_tester = QueryBuilderPerformanceTester(base_url)
            perf_tester.run_performance_tests()
        
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
