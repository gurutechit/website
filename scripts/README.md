# Pelican Support Scripts

This directory contains support scripts for Pelican static site setup and management.

## Available Scripts

- `pelican_automated_install.py` - Automated Pelican project setup from JSON configuration

### Automated Install

The `pelican_automated_install.py` script automates Pelican project setup by reading configuration from a JSON file instead of answering interactive prompts.

#### Quick Start

```bash
# Using a custom answers file
poetry run python scripts/pelican_automated_install.py --answers /path/to/answers.json
```

See [answers.json.example](answers.json.example) for an example configuration file. For detailed usage and all options, see [AUTOMATED-INSTALL.md](AUTOMATED-INSTALL.md).

#### Testing

The [AUTOMATED-TESTS.md](AUTOMATED-TESTS.md) document contains test cases and a complete test script for verifying the automation script functionality. This documentation is designed to be used by Claude Code for automated testing of the script.
