{% if cookiecutter.use_pytest == "y" %}
import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent))

def main():
    """Run pytest with specified arguments"""
    # Set test environment
    os.environ["ENVIRONMENT"] = "test"
    
    # Run pytest with verbose output and show coverage
    sys.exit(pytest.main(["-v", "--cov=app", "tests/"]))

if __name__ == "__main__":
    main()
{% endif %}
