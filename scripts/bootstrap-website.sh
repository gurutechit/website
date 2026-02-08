#!/bin/bash
set -euo pipefail

TMPWWW=$(mktemp --tmpdir -d www-XXXXXX)

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
pushd "$SCRIPT_DIR"
REPO_PATH="$(git rev-parse --show-toplevel)"
popd

pushd "$TMPWWW"
# Initialize a git repo
git init

# Init poetry with Pelican dependencies and tooling
poetry init -n \
    --name "gh-pelican" \
    --description "Pelican website with GitHub pages" \
    --python=">=3.10,<4.0" \
    --dev-dependency="pelican[markdown]" \
    --dev-dependency=tzdata \
    --dev-dependency=toml-cli
poetry config --local virtualenvs.in-project true
echo -e "# Pelican Website\n\nWelcome" >README.md

# Install dependencies
poetry install --no-root
poetry run toml add_section --toml-path pyproject.toml tool.poetry
poetry run toml set --toml-path pyproject.toml --to-bool tool.poetry.package-mode false

# Setup Python gitignore
curl -o .gitignore -sSL https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore

# Add Pelican folders to gitignore
echo -e "\n# Pelican site generator\noutput" >>.gitignore

# Configure Pelican with Automation
poetry run python "$REPO_PATH/scripts/pelican_automated_install.py" --answers "$REPO_PATH/scripts/answers.json.example"

# Modify Makefile to work with poetry
sed -ri 's;("\$\(PELICAN\)");poetry run \1;g' Makefile
popd
echo "Repository template in $TMPWWW"
echo "cd $TMPWWW"
exit 0

# $ git status
#
#On branch main
#
#No commits yet
#
#Untracked files:
#  (use "git add <file>..." to include in what will be committed)
#	.gitignore
#	README.md
#	poetry.lock
#	poetry.toml
#	pyproject.toml
#
#nothing added to commit but untracked files present (use "git add" to track

# $ git status
# On branch main
#
# No commits yet
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#         .gitignore
#         Makefile
#         README.md
#         pelicanconf.py
#         poetry.lock
#         poetry.toml
#         publishconf.py
#         pyproject.toml
#         tasks.py
#
# nothing added to commit but untracked files present (use "git add" to track)
