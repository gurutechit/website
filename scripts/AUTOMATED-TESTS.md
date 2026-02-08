# Automated Tests for pelican_automated_install.py

This document describes how to test the `pelican_automated_install.py` script with various configurations.

## Prerequisites

- Poetry environment with Pelican installed
- Run all commands from the repository root directory

## Generating Random Markers

Each test uses random markers to verify values are correctly passed through to output files. Generate markers with:

```bash
# Generate one random marker (8 chars, starts/ends with letter)
dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -1

# Generate multiple markers (e.g., 3)
dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -3
```

## Safe Cleanup

Always use safe cleanup to remove test directories. This verifies the directory exists and matches the expected mktemp pattern before removal:

```bash
# Safe removal function
safe_rm_test_dir() {
    local dir="$1"
    if [[ -d "$dir" ]] && [[ "$dir" =~ pelican-test-[a-zA-Z0-9]{6}$ ]]; then
        rm -rf "$dir"
    else
        echo "Warning: Refusing to remove '$dir' - not a valid test directory" >&2
    fi
}
```

## Test Cases

### 1. Error Handling Tests

#### Missing answers file

```bash
poetry run python scripts/pelican_automated_install.py -a nonexistent.json
# Expected: Error: Answers file not found: .../nonexistent.json
# Exit code: 1
```

#### Invalid JSON

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
echo "not valid json" > "$TEST_DIR/invalid.json"
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/invalid.json"
# Expected: Error: Invalid JSON in .../invalid.json: Expecting value: line 1 column 1 (char 0)
# Exit code: 1
[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

#### Missing required fields

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
echo '{"sitename": "test"}' > "$TEST_DIR/incomplete.json"
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/incomplete.json"
# Expected: Error: Missing required fields in answers file: basedir, author, lang, timezone
# Exit code: 1
[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

### 2. FTP Upload Configuration Test

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -6))

cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "FTP Test Site ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "it",
    "timezone": "Europe/Rome",
    "siteurl": "https://ftp-site-${MARKERS[2]}.example.com",
    "with_pagination": true,
    "automation": true,
    "ftp": true,
    "ftp_host": "ftp-host-${MARKERS[3]}.example.com",
    "ftp_user": "ftpuser-${MARKERS[4]}",
    "ftp_target_dir": "/var/www/ftp-dir-${MARKERS[5]}"
}
EOF

poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json"

# Verify markers
grep "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[1]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[2]}" "$TEST_DIR/publishconf.py" && \
grep "${MARKERS[3]}" "$TEST_DIR/Makefile" && \
grep "${MARKERS[4]}" "$TEST_DIR/Makefile" && \
grep "${MARKERS[5]}" "$TEST_DIR/Makefile" && \
echo "FTP TEST: PASSED"

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

### 3. SSH Upload Configuration Test

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -7))

cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "SSH Test Site ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "de",
    "timezone": "Europe/Berlin",
    "siteurl": "https://ssh-site-${MARKERS[2]}.example.com",
    "with_pagination": false,
    "automation": true,
    "ssh": true,
    "ssh_host": "ssh-host-${MARKERS[3]}.example.com",
    "ssh_port": 2222,
    "ssh_user": "sshuser-${MARKERS[4]}",
    "ssh_target_dir": "/home/web/ssh-dir-${MARKERS[5]}"
}
EOF

poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json"

# Verify markers
grep "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[1]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[2]}" "$TEST_DIR/publishconf.py" && \
grep "${MARKERS[3]}" "$TEST_DIR/tasks.py" && \
grep "2222" "$TEST_DIR/tasks.py" && \
grep "${MARKERS[4]}" "$TEST_DIR/tasks.py" && \
grep "${MARKERS[5]}" "$TEST_DIR/tasks.py" && \
echo "SSH TEST: PASSED"

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

### 4. GitHub Pages Configuration Test

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -3))

cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "GitHub Test Site ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "fr",
    "timezone": "Europe/Paris",
    "siteurl": "https://github-site-${MARKERS[2]}.github.io",
    "with_pagination": true,
    "automation": true,
    "github": true,
    "github_pages_branch": "gh-pages"
}
EOF

poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json"

# Verify markers
grep "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[1]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[2]}" "$TEST_DIR/publishconf.py" && \
grep "gh-pages" "$TEST_DIR/tasks.py" && \
grep "gh-pages" "$TEST_DIR/Makefile" && \
echo "GITHUB TEST: PASSED"

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

### 5. Multiple Upload Methods Test (S3 + Dropbox)

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -5))

cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Multi Test Site ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "es",
    "timezone": "Europe/Madrid",
    "siteurl": "https://multi-site-${MARKERS[2]}.example.com",
    "with_pagination": true,
    "automation": true,
    "s3": true,
    "s3_bucket": "s3bucket-${MARKERS[3]}",
    "dropbox": true,
    "dropbox_dir": "~/Dropbox/dropbox-dir-${MARKERS[4]}/"
}
EOF

poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json"

# Verify markers
grep "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[1]}" "$TEST_DIR/pelicanconf.py" && \
grep "${MARKERS[2]}" "$TEST_DIR/publishconf.py" && \
grep "${MARKERS[3]}" "$TEST_DIR/Makefile" && \
grep "${MARKERS[4]}" "$TEST_DIR/Makefile" && \
echo "MULTI TEST: PASSED"

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

### 6. Backup Option Tests

#### Backup enabled by default

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -2))

cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Backup Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF

# First run - generate files
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null

# Verify no .bak files exist after first run
if ls "$TEST_DIR"/*.bak 2>/dev/null; then
    echo "BACKUP TEST 1 FAILED: .bak files should not exist after first run"
else
    echo "BACKUP TEST 1a: No .bak files after first run - PASSED"
fi

# Second run - should create backups
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null

# Verify .bak files exist
if [[ -f "$TEST_DIR/pelicanconf.py.bak" ]] && \
   [[ -f "$TEST_DIR/publishconf.py.bak" ]] && \
   [[ -f "$TEST_DIR/tasks.py.bak" ]] && \
   [[ -f "$TEST_DIR/Makefile.bak" ]]; then
    echo "BACKUP TEST 1b: .bak files created on second run - PASSED"
else
    echo "BACKUP TEST 1 FAILED: .bak files not created"
fi

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

#### --no-backup disables backup

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -2))

cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "No Backup Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF

# First run
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null

# Second run with --no-backup
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" --no-backup > /dev/null

# Verify no .bak files exist
if ls "$TEST_DIR"/*.bak 2>/dev/null; then
    echo "NO-BACKUP TEST FAILED: .bak files should not exist with --no-backup"
else
    echo "NO-BACKUP TEST: PASSED"
fi

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

#### Backup preserves original content

```bash
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -4))

# First run with first marker
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Original ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null

# Second run with different marker
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Updated ${MARKERS[2]}",
    "author": "author-${MARKERS[3]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null

# Verify .bak contains original marker, new file contains updated marker
if grep -q "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py.bak" && \
   grep -q "${MARKERS[2]}" "$TEST_DIR/pelicanconf.py"; then
    echo "BACKUP CONTENT TEST: PASSED"
else
    echo "BACKUP CONTENT TEST FAILED: backup should contain original, file should contain updated"
fi

[[ -d "$TEST_DIR" ]] && [[ "$TEST_DIR" =~ pelican-test-[a-zA-Z0-9]{6}$ ]] && rm -rf "$TEST_DIR"
```

## Run All Tests

```bash
#!/bin/bash
set -e

# Helper function to generate random markers
gen_markers() {
    dd if=/dev/urandom bs=16k count=1 status=none | tr -dc "[a-zA-Z0-9]" | grep -oE "[a-zA-Z][a-zA-Z0-9]{6}[a-zA-Z]" | head -"$1"
}

# Safe removal function - only removes directories matching mktemp pattern
safe_rm_test_dir() {
    local dir="$1"
    if [[ -d "$dir" ]] && [[ "$dir" =~ pelican-test-[a-zA-Z0-9]{6}$ ]]; then
        rm -rf "$dir"
    else
        echo "Warning: Refusing to remove '$dir' - not a valid test directory" >&2
        return 1
    fi
}

echo "=== Running all pelican_automated_install.py tests ==="

# Test 1: Missing file
echo -n "Test 1 - Missing file: "
if poetry run python scripts/pelican_automated_install.py -a nonexistent.json 2>&1 | grep -q "Answers file not found"; then
    echo "PASSED"
else
    echo "FAILED"
    exit 1
fi

# Test 2: Invalid JSON
echo -n "Test 2 - Invalid JSON: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
echo "not valid json" > "$TEST_DIR/invalid.json"
if poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/invalid.json" 2>&1 | grep -q "Invalid JSON"; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 3: Missing fields
echo -n "Test 3 - Missing fields: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
echo '{"sitename": "test"}' > "$TEST_DIR/incomplete.json"
if poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/incomplete.json" 2>&1 | grep -q "Missing required fields"; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 4: FTP configuration
echo -n "Test 4 - FTP configuration: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(gen_markers 4))
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "FTP Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true,
    "ftp": true,
    "ftp_host": "ftp-host-${MARKERS[2]}",
    "ftp_user": "ftpuser-${MARKERS[3]}",
    "ftp_target_dir": "/ftp-dir"
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
if grep -q "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
   grep -q "${MARKERS[2]}" "$TEST_DIR/Makefile" && \
   grep -q "${MARKERS[3]}" "$TEST_DIR/Makefile"; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 5: SSH configuration
echo -n "Test 5 - SSH configuration: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(gen_markers 4))
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "SSH Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Berlin",
    "automation": true,
    "ssh": true,
    "ssh_host": "ssh-host-${MARKERS[2]}",
    "ssh_port": 2222,
    "ssh_user": "sshuser-${MARKERS[3]}",
    "ssh_target_dir": "/ssh-dir"
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
if grep -q "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
   grep -q "${MARKERS[2]}" "$TEST_DIR/tasks.py" && \
   grep -q "2222" "$TEST_DIR/tasks.py"; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 6: GitHub Pages configuration
echo -n "Test 6 - GitHub Pages configuration: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(gen_markers 2))
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "GitHub Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Paris",
    "automation": true,
    "github": true,
    "github_pages_branch": "gh-pages"
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
if grep -q "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py" && \
   grep -q "gh-pages" "$TEST_DIR/tasks.py" && \
   grep -q "gh-pages" "$TEST_DIR/Makefile"; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 7: Backup enabled by default
echo -n "Test 7 - Backup enabled by default: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(gen_markers 2))
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Backup Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
if [[ -f "$TEST_DIR/pelicanconf.py.bak" ]] && \
   [[ -f "$TEST_DIR/publishconf.py.bak" ]] && \
   [[ -f "$TEST_DIR/tasks.py.bak" ]] && \
   [[ -f "$TEST_DIR/Makefile.bak" ]]; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 8: --no-backup disables backup
echo -n "Test 8 - --no-backup disables backup: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(gen_markers 2))
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "No Backup Test ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" --no-backup > /dev/null
if ! ls "$TEST_DIR"/*.bak >/dev/null 2>&1; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

# Test 9: Backup preserves original content
echo -n "Test 9 - Backup preserves original content: "
TEST_DIR=$(mktemp --tmpdir -d pelican-test-XXXXXX)
MARKERS=($(gen_markers 4))
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Original ${MARKERS[0]}",
    "author": "author-${MARKERS[1]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
cat > "$TEST_DIR/answers.json" << EOF
{
    "basedir": "$TEST_DIR",
    "sitename": "Updated ${MARKERS[2]}",
    "author": "author-${MARKERS[3]}",
    "lang": "en",
    "timezone": "Europe/Rome",
    "automation": true
}
EOF
poetry run python scripts/pelican_automated_install.py -a "$TEST_DIR/answers.json" > /dev/null
if grep -q "${MARKERS[0]}" "$TEST_DIR/pelicanconf.py.bak" && \
   grep -q "${MARKERS[2]}" "$TEST_DIR/pelicanconf.py"; then
    echo "PASSED"
else
    echo "FAILED"
    safe_rm_test_dir "$TEST_DIR"
    exit 1
fi
safe_rm_test_dir "$TEST_DIR"

echo "=== All tests passed ==="
```
