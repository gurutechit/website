Title: Building a Pelican Site with GitHub Pages and Poetry
Date: 2026-02-13
Tags: pelican, python, github-pages, github-actions, poetry, devops
Slug: building-repo
Lang: en
Category: Tutorial
Status: draft

## Introduction

I decided to renew my old good website with the beginning of this New Year 2026. After all my own domain name gurutech.it is turning 25 and deserves it.
There are thousands of solutions to host a website, free or paid, but as a developer I wanted to explore something more DevOps oriented. Since I already have my code hosted on GitHub, I decided to go with GitHub Pages which is [free for public repositories](https://docs.github.com/en/get-started/learning-about-github/githubs-plans#github-free-for-personal-accounts) and can host [static content](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#about-github-pages).
So the final choice can be to write static content by myself in 90s style or go with a [static site generator](https://jamstack.org/generators/). There are easy and popular choices like Jekyll or Hugo but as Python oriented developer I picked up [Pelican](https://getpelican.com) because it seems to be supported enough and actively maintained with a background community.

## Prerequisites

### Mandatory Requirements

- GitHub Account to host website
- Linux terminal skills to run commands
- Python to run Pelican generator
- Git is already configured on your computer

### Optional Requirements

- Poetry[^1] to manage Python dependencies
- GitHub Actions[^2] to automate publishing of content
- Domain[^3] name to have your custom domain

## Desired Skills

Generally speaking a good knowledge of Linux and Python is recommended especially to be able to solve issues when something goes wrong (_"Anything that can go wrong will go wrong." (Murphy's Law)_).  
A basic knowledge of [GitHub Actions](https://docs.github.com/en/actions/get-started/quickstart) and the mechanism of CI/CD will be useful as well to understand automation processes.
Finally if you want to configure your [own domain name](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) you must know how to configure DNS records with your provider/registrar.

## Setting Up the Project

### Python Poetry

Package dependency and virtual environments management is crucial in Python (as in many modern languages). You can for sure use the old good `pip` tool with `requirements.txt`. Personally I prefer Poetry because it manages not only dependencies (separating dev and runtime deps) but also offers extra tooling from initializing a repository to publishing packages. Last but not least, Python official documentation does not endorse a specific tool but Poetry is named (among others) in their [packaging guidelines](https://packaging.python.org/en/latest/tutorials/managing-dependencies/).


Installation of Python Poetry is straightforward and well documented in the [official documentation](https://python-poetry.org/docs/#installing-with-the-official-installer) so please refer to it to get a working installation.

### Initializing the Pelican Project

#### GitHub repository

Let's start by creating a new GitHub repository by visiting [https://github.com/new](https://github.com/new). Pick a repo name e.g. `pelican-site` and remember to leave it as "Public" visibility (this is required to use GitHub Pages). It should be the default, but make sure to select: "No template", "No license", "No .gitignore", and do not add a README—you will do all of this later. You will also receive instructions to upload content to the newly created repository and this will be done at the end of this tutorial.

    :::bash
    mkdir pelican-site # usually the repo name you choose on GitHub above
    cd pelican-site
    git init
    git branch -M main
    git status

You will see an output like this if everything is successful:

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

#### Poetry project initialization

Use `poetry init` to initialize a project with Pelican dependencies and tooling. Use the `markdown` extension if you want to write content in Markdown. The toml-cli dependency is not strictly required but it will be used during this initial configuration to manage `pyproject.toml` settings.

    :::bash
    poetry init -n \
        --name "pelican-site" \
        --description "Pelican website with GitHub pages" \
        --python=">=3.10,<4.0" \
        --dev-dependency="pelican[markdown]" \
        --dev-dependency=tzdata \
        --dev-dependency=toml-cli

Poetry normally manages virtualenvs in your home directory. For better compatibility with GitHub it is better to install the `.venv` inside the repository root itself (adding it to .gitignore).

    :::bash
    poetry config --local virtualenvs.in-project true

Now create a default README (you can edit later).

    :::bash
    echo -e "# Pelican Site\n\nWelcome" > README.md

It's now time to install the specified dependencies with poetry install. Because we are not creating any Python package but we just want to manage dependencies the `--no-root` is required or poetry will issue an error.

    :::bash
    poetry install --no-root

To disable package mode completely in poetry (and avoid specifying --no-root) we need to add the following section to `pyproject.toml`

    :::toml
    [tool.poetry]
    package-mode = false

You can do it with your favorite editor or just use the toml-cli installed inside our virtualenv like this:

    :::bash
    poetry run toml add_section --toml-path pyproject.toml tool.poetry
    poetry run toml set --toml-path pyproject.toml --to-bool tool.poetry.package-mode false

Finally you will need a .gitignore for Python projects to be installed inside the repository. My suggestion is to use the one created by GitHub that you can download from [github/gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore). Just download the raw file and save it as .gitignore inside your current pelican-site directory. Since this repository is using Pelican the `output` directory (where the content is generated) must be ignored as well.

    :::bash
    curl -o .gitignore -sSL https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore
    echo -e "\n# Pelican site generator\noutput" >> .gitignore

If everything was successful you should be able to get virtualenv information with

    :::bash
    poetry env info

and get an output like this:

    :::text
    Virtualenv
    Python:         3.12.12
    Implementation: CPython
    Path:           /home/develop/gurutech-website/.venv
    Executable:     /home/develop/gurutech-website/.venv/bin/python
    Valid:          True

    Base
    Platform:   linux
    OS:         posix
    Python:     3.12.12
    Path:       /usr
    Executable: /usr/bin/python3.12

Your repository will contain the following files:

    :::bash
    ls --file-type -1A

```text
.git/
.gitignore
.venv/
README.md
poetry.lock
poetry.toml
pyproject.toml
```

Let's commit it:

    :::bash
    git add .gitignore README.md poetry.lock poetry.toml pyproject.toml
    git commit -m "poetry setup"

#### Pelican project initialization

You are now ready to [kickstart](https://docs.getpelican.com/en/latest/install.html#kickstart-your-site) your site. Since we are using poetry you must run the `pelican-quickstart` with:

    :::bash
    poetry run pelican-quickstart

You will be asked the following questions. Besides the defaults what is really **IMPORTANT** to specify is:

- the URL prefix in the format `https://your-github-username.github.io` (or use a [custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site))
- Generate `tasks.py` and `Makefile` for automation (answer yes)
- You can answer no to all other questions about uploading the website, including the GitHub pages that will be managed later with a workflow

```text
Welcome to pelican-quickstart v4.11.0.post0.
This script will help you create a new Pelican-based website.
Please answer the following questions so this script can generate the files
needed by Pelican.
Where do you want to create your new web site? [.]
What will be the title of this web site? pelican-site
Who will be the author of this web site? gurutech
What will be the default language of this web site? [C] en
Do you want to specify a URL prefix? e.g., https://example.com   (Y/n) y
What is your URL prefix? (see above example; no trailing slash) https://github-username.github.io
Do you want to enable article pagination? (Y/n) y
How many articles per page do you want? [10]
What is your time zone? [Europe/Rome]
Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n) y
Do you want to upload your website using FTP? (y/N) n
Do you want to upload your website using SSH? (y/N) n
Do you want to upload your website using Dropbox? (y/N) n
Do you want to upload your website using S3? (y/N) n
Do you want to upload your website using Rackspace Cloud Files? (y/N) n
Do you want to upload your website using GitHub Pages? (y/N) n
Done. Your new project is available at /home/develop/gurutech-website
```

You will now have the following files in your repository (notice `pelicanconf.py`, `publishconf.py`, `tasks.py` and `Makefile`)

    :::bash
    ls --file-type -1A

```text
.git/
.gitignore
.venv/
Makefile
README.md
content/
output/
pelicanconf.py
poetry.lock
poetry.toml
publishconf.py
pyproject.toml
tasks.py
```

You can now generate and serve the example configuration site with:

    :::bash
    poetry run make publish

```text
poetry run "pelican" "/home/develop/gurutech-website/content" -o "/home/develop/gurutech-website/output" -s "/home/develop/gurutech-website/publishconf.py"
[15:48:16] WARNING  Feeds generated without SITEURL set properly may not be valid   settings.py:679
Done: Processed 0 articles, 0 drafts, 0 hidden articles, 0 pages, 0 hidden pages and 0 draft pages in 0.03 seconds.
```

Check now the content of the output/ directory to confirm the above command worked:

    :::bash
    ls --file-type -1A output/

```text
archives.html
authors.html
categories.html
feeds/
index.html
tags.html
theme/
```

Last but not least you can serve the website locally and check it with your browser with:

    :::bash
    poetry run make serve

```text
poetry run "pelican" -l "/home/develop/gurutech-website/content" -o "/home/develop/gurutech-website/output" -s "/home/develop/gurutech-website/pelicanconf.py"
Serving site at: http://127.0.0.1:8000 - Tap CTRL-C to stop
[15:48:59] INFO     "GET / HTTP/1.1" 200 -          server.py:126
INFO     "GET /theme/css/main.css HTTP/1.1" 200 -   server.py:126
INFO     "GET /theme/css/reset.css HTTP/1.1" 200 -  server.py:126
```

Point your browser to [http://localhost:8000](http://127.0.0.1:8000) and you will see the site up and running.

Finally you can avoid prepending `poetry run` to make commands by modifying the `Makefile` targets. Check the current pelican targets:

    :::bash
    grep --no-group-separator -B1 -F '$(PELICAN)' Makefile

```text
html:
    "$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
regenerate:
    "$(PELICAN)" -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
serve:
    "$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
serve-global:
    "$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b $(SERVER)
devserver:
    "$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
devserver-global:
    "$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b 0.0.0.0
publish:
    "$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)
```

It will be enough to add `poetry run` in front of every `$(PELICAN)` command. You can do it with your editor or with sed search and replace:

    :::bash
    sed -ri 's;("\$\(PELICAN\)");poetry run \1;g' Makefile

It's time to commit the pelican setup:

    :::bash
    git add Makefile pelicanconf.py publishconf.py tasks.py
    git commit -m "pelican setup"

and you can finally push to remote repository before going to the next step:

    :::bash
    git remote add origin git@github.com:your-username/pelican-site.git
    git push -u origin main

## GitHub Pages Setup

### Repository Configuration

You need to enable your repository `pelican-site` to be hosted on GitHub Pages:

- Go to `https://github.com/your-username/pelican-site`
- Open Settings
- Navigate to Pages (under "Code and automation")
- In the "Build and deployment" section, select source: "GitHub Actions"
- Now in the left sidebar, click "Environments"
- Verify that an environment named `github-pages` has been created
- The environment `github-pages` contains just one protection rule:
  * Deployment branches and tags is restricted to "Selected branches and tags"
  * Only branch `main` is allowed

## Automating Deployment with GitHub Actions

### The Workflow File

Now you need a GitHub workflow to deploy your website. You can download the one I use for this website from [here](https://github.com/gurutechit/website/blob/main/.github/workflows/pelican-deploy.yml). Let's analyze the main points of it in the snippet below.

    #!yaml
    name: Deploy Pelican to GitHub Pages

    on:
      push:
        branches: ["main"]
        paths:
          - 'content/**'
          - 'pelicanconf.py'
          - 'publishconf.py'
          - 'theme/**'
          - 'pyproject.toml'
          - 'poetry.lock'
      workflow_dispatch:

    permissions:
      contents: read
      pages: write
      id-token: write

    concurrency:
      group: "pages"
      cancel-in-progress: false

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v6

          - name: Set up Python
            uses: actions/setup-python@v6
            with:
              python-version: '3.11'

          - name: Set up Poetry
            uses: abatilo/actions-poetry@v4

          - name: Install dependencies
            run: poetry install

          - name: Build
            run: make publish

          - name: Upload artifact
            uses: actions/upload-pages-artifact@v4
            with:
              path: ./output

      deploy:
        environment:
          name: github-pages
          url: ${{ steps.deployment.outputs.page_url }}
        runs-on: ubuntu-latest
        needs: build
        steps:
          - name: Deploy to GitHub Pages
            id: deployment
            uses: actions/deploy-pages@v4

What it will do:

**Triggers (lines 5-12):**

- On line 5 this workflow will be triggered only on commits to `main` branch
- On lines 6-12 this workflow will be triggered only on commits of the matching paths:
  * When the `content` or `theme` changes
  * When the Pelican configuration changes (`pelicanconf.py`, `publishconf.py`)
  * When `pyproject.toml` or `poetry.lock` changes e.g. because of an update to Pelican version

**Permissions (lines 15-18):**

- `contents: read` - allows the workflow to checkout the repository
- `pages: write` - allows publishing to GitHub Pages
- `id-token: write` - required for OIDC authentication with GitHub Pages

**Concurrency (lines 20-22):**

- `group: "pages"` - ensures only one Pages deployment runs at a time
- `cancel-in-progress: false` - prevents canceling a running deployment if a new one is queued

**Job `build` (lines 25-47):**

- There is a standard setup of Python/Poetry
- On line 42 run `make publish` like you would do locally to generate the `output` directory
- On lines 44-47 upload the `output` directory to a GitHub Pages artifact

**Job `deploy` (lines 49-58):**

- On line 50-51 the `environment: name: github-pages` links this job to the protected environment configured in repository settings
- On line 54 the `needs: build` ensures this job waits for the build job to complete
- On lines 56-58 the action `deploy-pages` deploys the artifact uploaded by the previous job to GitHub Pages

## Development Workflow

### Local Development

For local development use `make devserver` which auto-regenerates the site on file changes and serves it at http://localhost:8000.

    :::bash
    make devserver

See the [Pelican documentation](https://docs.getpelican.com/en/latest/publish.html) for more options, including live reload with `invoke livereload`.

### Publishing Changes

Just push your changes to the `main` branch and the GitHub Actions workflow handles the rest:

    :::bash
    git add content/my-new-article.md
    git commit -m "Add new article"
    git push

The workflow will automatically build and deploy your site to GitHub Pages. You can monitor the deployment progress in the Actions tab of your repository.

## Lessons Learned

I had never used a static website generator before, so exploring one of them, reading documentation, and learning the workflow allowed me to acquire more knowledge about them in general. I imagine that using Jekyll or Hugo would not be so different.

Using Poetry was my personal preference and probably a bit overkill for this project, but I was able to integrate it successfully.

For the development of the GitHub workflow, I started by asking GitHub to create a Jekyll workflow for me and then modified it. If you have an option to start from an official example that works, why not use it?

Using path filters in the workflow ensures it only runs when relevant files change (content, theme, configuration), saving CI minutes and avoiding unnecessary deployments.

## Conclusion

I finally renewed [www.gurutech.it](https://www.gurutech.it). Now I only have to write content and have it published automatically. Please have a look at the GitHub repository [here](https://github.com/gurutechit/website).

For next steps, I'm looking forward to automating the Pelican quickstart phase. I wrote some example code for it under [scripts/](https://github.com/gurutechit/website/tree/main/scripts) and opened an [issue](https://github.com/getpelican/pelican/issues/3565) on the main Pelican project to suggest an improvement.

## Resources

- [Pelican Documentation](https://docs.getpelican.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)


## Notes

[^1]: You can always manage Python dependencies manually using pip but it is better to [use a dedicated tool](https://packaging.python.org/en/latest/tutorials/managing-dependencies/).
[^2]: Alternatively you can quickstart running Pelican locally and publish content of `output/` directory with [a branch deployment](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#troubleshooting-publishing-from-a-branch)
[^3]: If you don't have a domain name you can use GH Pages with the included <username\>.github.io subdomain.
