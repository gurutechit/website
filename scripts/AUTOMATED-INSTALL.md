# Automated Pelican Installation

This script automates the setup of a Pelican static site project by reading configuration from a JSON file instead of answering interactive prompts.

## Usage

### Basic Usage

Specify an answers file with the `-a` or `--answers` option:

```bash
poetry run python scripts/pelican_automated_install.py --answers /path/to/answers.json
```

If no answers file is specified, the script looks for `answers.json` in the same directory as the script (i.e., `scripts/answers.json`). See [answers.json.example](answers.json.example) for an example configuration.

### Backup Option

By default, the script backs up existing files before overwriting them. Each file is copied to a `.bak` extension (e.g., `pelicanconf.py` → `pelicanconf.py.bak`).

```bash
# Default behavior (backup enabled)
poetry run python scripts/pelican_automated_install.py

# Explicitly enable backup
poetry run python scripts/pelican_automated_install.py --backup

# Disable backup (overwrite without saving)
poetry run python scripts/pelican_automated_install.py --no-backup
```

Files that are backed up: `pelicanconf.py`, `publishconf.py`, `tasks.py`, `Makefile`

Note: Existing `.bak` files will be overwritten. Only the most recent backup is kept.

### Running from a Different Directory

If the script and/or the answers file are located outside the Pelican repository, you **must** use Poetry's `-C` option to specify the Pelican repository directory. This ensures the script runs within the correct virtual environment with Pelican installed.

**Example:**

```bash
poetry -C /path/to/pelican-repo run python /path/to/pelican_automated_install.py --answers /path/to/answers.json
```

Where:
- `/path/to/pelican-repo` is the directory containing the `pyproject.toml` with Pelican as a dependency
- `/path/to/pelican_automated_install.py` is the location of the automation script
- `/path/to/answers.json` is the location of your answers configuration file

## Answers File Structure

The answers file is a JSON document that provides all configuration values for Pelican setup.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `basedir` | string | Output directory where Pelican files will be generated. Use `.` for current directory or an absolute path. |
| `sitename` | string | Title of the website |
| `author` | string | Author name |
| `lang` | string | Default language code (2 characters, e.g., `en`, `it`, `de`) |
| `timezone` | string | Time zone (e.g., `Europe/Rome`, `America/New_York`) |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `siteurl` | string | `""` | URL prefix for the site (e.g., `https://example.com`) |
| `with_pagination` | boolean | `false` | Enable article pagination |
| `automation` | boolean | `true` | Generate `tasks.py` and `Makefile` |

### Upload Methods

Enable one or more upload methods by setting their flag to `true` and providing the required configuration.

#### FTP Upload

| Field | Type | Description |
|-------|------|-------------|
| `ftp` | boolean | Enable FTP upload |
| `ftp_host` | string | FTP server hostname |
| `ftp_user` | string | FTP username |
| `ftp_target_dir` | string | Target directory on FTP server |

#### SSH/Rsync Upload

| Field | Type | Description |
|-------|------|-------------|
| `ssh` | boolean | Enable SSH upload |
| `ssh_host` | string | SSH server hostname |
| `ssh_port` | integer | SSH port (default: 22) |
| `ssh_user` | string | SSH username |
| `ssh_target_dir` | string | Target directory on SSH server |

#### Dropbox Upload

| Field | Type | Description |
|-------|------|-------------|
| `dropbox` | boolean | Enable Dropbox upload |
| `dropbox_dir` | string | Dropbox directory path |

#### Amazon S3 Upload

| Field | Type | Description |
|-------|------|-------------|
| `s3` | boolean | Enable S3 upload |
| `s3_bucket` | string | S3 bucket name |

#### Rackspace Cloud Files Upload

| Field | Type | Description |
|-------|------|-------------|
| `cloudfiles` | boolean | Enable Cloud Files upload |
| `cloudfiles_username` | string | Rackspace username |
| `cloudfiles_api_key` | string | Rackspace API key |
| `cloudfiles_container` | string | Container name |

#### GitHub Pages Upload

| Field | Type | Description |
|-------|------|-------------|
| `github` | boolean | Enable GitHub Pages upload |
| `github_pages_branch` | string | Branch name (`gh-pages` for project sites, `main` for personal sites) |

## Examples

### Minimal Configuration

```json
{
    "basedir": ".",
    "sitename": "My Blog",
    "author": "John Doe",
    "lang": "en",
    "timezone": "Europe/London"
}
```

### GitHub Pages Configuration

```json
{
    "basedir": "/home/user/my-blog",
    "sitename": "My Tech Blog",
    "author": "Jane Smith",
    "lang": "en",
    "timezone": "America/New_York",
    "siteurl": "https://janesmith.github.io/my-blog",
    "with_pagination": true,
    "automation": true,
    "github": true,
    "github_pages_branch": "gh-pages"
}
```

### SSH Deployment Configuration

```json
{
    "basedir": ".",
    "sitename": "Company Blog",
    "author": "Dev Team",
    "lang": "en",
    "timezone": "UTC",
    "siteurl": "https://blog.example.com",
    "with_pagination": true,
    "automation": true,
    "ssh": true,
    "ssh_host": "blog.example.com",
    "ssh_port": 22,
    "ssh_user": "deploy",
    "ssh_target_dir": "/var/www/blog"
}
```

## Generated Files

The script generates the following files in the `basedir` directory:

| File | Description |
|------|-------------|
| `pelicanconf.py` | Main Pelican configuration |
| `publishconf.py` | Production publishing configuration |
| `tasks.py` | Invoke tasks for building and serving (if `automation: true`) |
| `Makefile` | Make targets for building and serving (if `automation: true`) |
| `content/` | Directory for your content (articles, pages) |
| `output/` | Directory where generated HTML will be placed |

## Error Handling

The script will exit with an error if:

- The answers file does not exist
- The answers file contains invalid JSON
- Required fields are missing from the answers file

Example error messages:

```
Error: Answers file not found: /path/to/answers.json
Error: Invalid JSON in /path/to/answers.json: Expecting value: line 1 column 1 (char 0)
Error: Missing required fields in answers file: basedir, author, lang, timezone
```
