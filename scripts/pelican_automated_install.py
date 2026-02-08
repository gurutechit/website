#!/usr/bin/env python
"""Automated Pelican installation script using answers from JSON file."""

import argparse
import json
import os
import shutil
import sys

import pelican.tools.pelican_quickstart as pqs


def backup_file(filepath):
    """Backup a file by copying it to .bak extension if it exists."""
    if os.path.isfile(filepath):
        backup_path = filepath + ".bak"
        shutil.copy2(filepath, backup_path)
        print(f"Backed up: {filepath} -> {backup_path}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_answers = os.path.join(script_dir, "answers.json")

    parser = argparse.ArgumentParser(
        description="Automated Pelican project setup from JSON answers file."
    )
    parser.add_argument(
        "-a", "--answers",
        default=default_answers,
        help=f"Path to answers JSON file (default: {default_answers})"
    )
    parser.add_argument(
        "--backup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Backup existing files before overwriting (default: True)"
    )
    args = parser.parse_args()

    # Load and validate answers file
    answers_file = os.path.abspath(args.answers)
    if not os.path.isfile(answers_file):
        sys.exit(f"Error: Answers file not found: {answers_file}")

    try:
        with open(answers_file, "r", encoding="utf-8") as f:
            answers = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON in {answers_file}: {e}")

    # Validate required fields
    required_fields = ["basedir", "sitename", "author", "lang", "timezone"]
    missing = [f for f in required_fields if f not in answers]
    if missing:
        sys.exit(f"Error: Missing required fields in answers file: {', '.join(missing)}")

    # Update pqs.CONF with answers
    basedir = os.path.abspath(answers["basedir"])
    pqs.CONF["basedir"] = basedir
    pqs.CONF["sitename"] = answers["sitename"]
    pqs.CONF["author"] = answers["author"]
    pqs.CONF["lang"] = answers["lang"]
    pqs.CONF["timezone"] = answers["timezone"]
    pqs.CONF["siteurl"] = answers.get("siteurl", "")
    pqs.CONF["with_pagination"] = answers.get("with_pagination", False)
    pqs.CONF["default_pagination"] = False if not answers.get("with_pagination") else 10

    # Add upload options and their settings if enabled
    if answers.get("ftp"):
        pqs.CONF["ftp"] = (True,)
        for key in ["ftp_host", "ftp_user", "ftp_target_dir"]:
            if key in answers:
                pqs.CONF[key] = answers[key]
    if answers.get("ssh"):
        pqs.CONF["ssh"] = (True,)
        for key in ["ssh_host", "ssh_port", "ssh_user", "ssh_target_dir"]:
            if key in answers:
                pqs.CONF[key] = answers[key]
    if answers.get("dropbox"):
        pqs.CONF["dropbox"] = (True,)
        if "dropbox_dir" in answers:
            pqs.CONF["dropbox_dir"] = answers["dropbox_dir"]
    if answers.get("s3"):
        pqs.CONF["s3"] = (True,)
        if "s3_bucket" in answers:
            pqs.CONF["s3_bucket"] = answers["s3_bucket"]
    if answers.get("cloudfiles"):
        pqs.CONF["cloudfiles"] = (True,)
        for key in ["cloudfiles_username", "cloudfiles_api_key", "cloudfiles_container"]:
            if key in answers:
                pqs.CONF[key] = answers[key]
    if answers.get("github"):
        pqs.CONF["github"] = (True,)
        if "github_pages_branch" in answers:
            pqs.CONF["github_pages_branch"] = answers["github_pages_branch"]

    # Create content and output directories
    for dirname in ["content", "output"]:
        dirpath = os.path.join(basedir, dirname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            print(f"Created directory: {dirpath}")

    # Backup existing files if requested
    if args.backup:
        for filename in ["pelicanconf.py", "publishconf.py", "tasks.py", "Makefile"]:
            backup_file(os.path.join(basedir, filename))

    # Generate pelicanconf.py (uses repr() for values)
    conf_python = {key: repr(value) for key, value in pqs.CONF.items()}
    pqs.render_jinja_template("pelicanconf.py.jinja2", conf_python, "pelicanconf.py")

    # Generate publishconf.py
    pqs.render_jinja_template("publishconf.py.jinja2", pqs.CONF, "publishconf.py")

    # Generate automation files if requested
    if answers.get("automation", True):
        pqs.render_jinja_template("tasks.py.jinja2", pqs.CONF, "tasks.py")
        pqs.render_jinja_template("Makefile.jinja2", pqs.CONF, "Makefile")

    print(f"Done. Your new project is available at {basedir}")


if __name__ == "__main__":
    main()
