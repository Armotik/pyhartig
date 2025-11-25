"""
PyTest Configuration for PyHartig Test Suite

This configuration module provides global fixtures and settings
for the comprehensive test suite, enabling detailed debug output
and trace generation.
"""

import pytest
import sys
from pathlib import Path


def pytest_configure(config):
    """
    Configure pytest with custom settings.
    
    Args:
        config: pytest configuration object
    """
    # Register custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test location.
    
    Args:
        config: pytest configuration object
        items: list of test items
    """
    for item in items:
        # Add markers based on test file name
        if "test_01" in str(item.fspath) or "test_02" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_03" in str(item.fspath) or "test_04" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "test_08" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


@pytest.fixture(scope="session")
def project_root():
    """
    Provide path to project root directory.
    
    Returns:
        Path: Project root directory
    """
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def data_directory(project_root):
    """
    Provide path to data directory.
    
    Returns:
        Path: Data directory
    """
    return project_root / "data"


@pytest.fixture(scope="session")
def test_output_dir(project_root):
    """
    Provide path to test output directory.
    
    Creates the directory if it doesn't exist.
    
    Returns:
        Path: Test output directory
    """
    output_dir = project_root / "tests" / "test_output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture
def capture_debug_output(capsys):
    """
    Fixture to capture and return debug output.
    
    Provides a context manager that captures stdout/stderr
    during test execution.
    
    Args:
        capsys: pytest's capsys fixture
        
    Returns:
        callable: Function to get captured output
    """
    def get_output():
        captured = capsys.readouterr()
        return captured.out + captured.err
    
    return get_output


@pytest.fixture(autouse=True)
def reset_environment():
    """
    Auto-use fixture to reset environment before each test.
    
    Ensures clean state between tests.
    """
    # Add any cleanup or reset logic here
    yield
    # Teardown logic if needed


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Add custom summary information to test report.
    
    Args:
        terminalreporter: pytest terminal reporter
        exitstatus: test exit status
        config: pytest configuration
    """
    if exitstatus == 0:
        terminalreporter.write_sep("=", "TEST SUITE SUMMARY", green=True, bold=True)
        terminalreporter.write_line("All tests passed successfully!")
        terminalreporter.write_line("Debug traces available in test output.")
    else:
        terminalreporter.write_sep("=", "TEST SUITE SUMMARY", red=True, bold=True)
        terminalreporter.write_line(f"Tests completed with status: {exitstatus}")


# Configure pytest options
def pytest_addoption(parser):
    """
    Add custom command-line options to pytest.
    
    Args:
        parser: pytest argument parser
    """
    parser.addoption(
        "--debug-trace",
        action="store_true",
        default=False,
        help="Enable detailed debug trace output"
    )
    parser.addoption(
        "--save-traces",
        action="store_true",
        default=False,
        help="Save debug traces to files"
    )

