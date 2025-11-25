#!/usr/bin/env python3
"""
Test Runner and Documentation Generator

This script executes the complete PyHartig test suite and generates
comprehensive documentation including debug traces for the README.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def print_section(title, char="="):
    """Print a formatted section header."""
    width = 80
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}\n")


def run_tests_with_output():
    """
    Execute test suite with verbose output and capture results.
    
    Returns:
        tuple: (return_code, output)
    """
    print_section("PyHartig Test Suite Execution", "=")
    
    test_suite_path = Path(__file__).parent
    
    # Run pytest with verbose output and capture
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_suite_path),
        "-v",  # Verbose
        "-s",  # No capture (show print statements)
        "--tb=short",  # Short traceback format
        "--color=yes",  # Colored output
        "-p", "no:warnings",  # Disable warnings
    ]
    
    print(f"Executing command: {' '.join(cmd)}\n")
    print(f"Test suite location: {test_suite_path}\n")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=test_suite_path.parent.parent,
            capture_output=False,
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def generate_test_summary():
    """Generate a summary of the test suite structure."""
    print_section("Test Suite Structure", "-")
    
    test_files = [
        ("test_01_source_operators.py", "Source Operator Tests", 
         "Validates JSON source operators with iteration and extraction"),
        ("test_02_extend_operators.py", "Extend Operator Tests",
         "Tests attribute augmentation with expressions"),
        ("test_03_operator_composition.py", "Operator Composition Tests",
         "Validates operator fusion and pipeline construction"),
        ("test_04_complete_pipelines.py", "Complete Pipeline Tests",
         "End-to-end transformation scenarios"),
        ("test_05_builtin_functions.py", "Built-in Function Tests",
         "Tests for RDF term construction functions"),
        ("test_06_expression_system.py", "Expression System Tests",
         "Validates expression evaluation and composition"),
        ("test_07_library_integration.py", "Library Integration Tests",
         "Tests for external library integration (jsonpath-ng, etc.)"),
        ("test_08_real_data_integration.py", "Real Data Integration Tests",
         "Tests using actual project data files"),
    ]
    
    for i, (filename, title, description) in enumerate(test_files, 1):
        print(f"{i}. {title}")
        print(f"   File: {filename}")
        print(f"   Description: {description}")
        print()


def main():
    """Main execution function."""
    print_section("PyHartig Comprehensive Test Suite", "=")
    print("This test suite validates all components of the PyHartig system")
    print("with detailed debug traces for documentation purposes.")
    print()
    
    # Show test structure
    generate_test_summary()
    
    # Run tests
    return_code = run_tests_with_output()
    
    # Final summary
    print_section("Test Execution Complete", "=")
    if return_code == 0:
        print("✓ All tests passed successfully!")
        print("✓ Debug traces have been generated")
        print("✓ Results can be used for README documentation")
    else:
        print(f"✗ Tests completed with errors (exit code: {return_code})")
        print("  Review the output above for details")
    
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())

