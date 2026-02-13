Title: Building a Pelican Site with GitHub Pages and Poetry
Date: 2026-02-13
Tags: pelican, python, github-pages, github-actions, poetry, devops
Slug: building-repo
Lang: en
Category: Tutorial
Status: draft

## Introduction

I decided to renew my old good website with the beginning of this New Year 2026. After all my own domain name gurutech.it is turning 25 and deserves it.
There are for sure thousands of solutions to host a website, free or paid, but after all I am a developer and I would like to explore something more DevOps oriented. Since I already have my code hosted on GitHub I decided to go with GitHub Pages that are [free for public repositories](https://docs.github.com/en/get-started/learning-about-github/githubs-plans#github-free-for-personal-accounts) and can host on it [static content](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#about-github-pages).
So the final choice can be to write static content by myself in 90s style or go with a [static site generator](https://jamstack.org/generators/). There are easy and popular choices like Jekyll or Hugo but as Python oriented developer I picked up [Pelican](https://getpelican.com) because it seems to be supported enough and actively maintained with a background community.

## Prerequisites

### Mandatory Requirements
- GitHub Account to host website
- Linux terminal skills to run commands
- Python to run Pelican generator

### Optional Requirements

- Poetry[^1] to manage Pyhton dependencies
- GitHub Actions[^2] to automate publishing of content
- Domain[^3] name to have your custom domain

## Desired skills

Generally speaking a good knowledge of Linux and Python is recommended especially to be able to solve issues when something goes wrong (_"Anything that can go wrong will go wrong." (Murphy's Law)_).  
A basic knowledge of [GitHub Actions](https://docs.github.com/en/actions/get-started/quickstart) and the mechanism of CI/CD will be useful as well to understand automation processes.
Finally If you want to configure your [own domain name](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) you must know how to configure DNS records with your provider/registar.

## Setting Up the Project

### Python Poetry

Package dependency and virtual environments management is crucial in Python (as in many modern languages). You can for sure use the old good `pip` tool with `requirements.txt`. Personally I do prefer Poetry because it allows me to manage not only the dependencies (dividing it in devs and program deps) but offers a series of extra tooling from init a repository to publishing packages that makes it my personal choice for every project. Last but not least Python official documentation do not endorse a speficic tool but Poetry is named (among with others) in their [packaging guidelines](https://packaging.python.org/en/latest/tutorials/managing-dependencies/).


Installation of Python Poetry is straightforward and well documented in the [official documentation](https://python-poetry.org/docs/#installing-with-the-official-installer) so please refer to it to get a working installation.

### Initializing the Pelican Project

#### GitHub repository

Let's start by creating a new GitHub repository by visiting [https://github.com/new](https://github.com/new). Pickup a repo name e.g. `pelican-site` and remeber to leave it as "Public" visibility (this is required to use GitHub pages). It should be the default but be sure to select on other options: "No template", "No license", "No .gitignore" and do not add a README, you will do all of this later. You will also receive instructions to upload content to the new created repository and this will be done at the end of this tutorial.

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

Use `poetry init` to initialize a project with Pelican dependencies and tooling. Use the `markdown` extension if you wants to write contents in Markdown. The toml-cli dependency is not strictly required but it will be used during this initial configuration to manage `pyproject.toml` settings.

    :::bash
    poetry init -n \
        --name "pelican-site" \
        --description "Pelican website with GitHub pages" \
        --python=">=3.10,<4.0" \
        --dev-dependency="pelican[markdown]" \
        --dev-dependency=tzdata \
        --dev-dependency=toml-cli

Poetry normally manage virtualenvs in your home directory. For better compatibility with GitHub is better to install the `.venv` inside the repository root itself (adding it to .gitignore).

    :::bash
    poetry config --local virtualenvs.in-project true

Now create a default README (You can edit later).

    :::bash
    echo -e "# Pelican Site\n\nWelcome" > README.md

It's now time to install the specified dependencies with poetry install. Becasue we are not creating any Python package but we just want to manage dependencies the `--no-root` is required or poetry will issue an error.

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

Finally you will need a .gitignore for Python projects to be installed inside the repository. My suggestion it to use the one created by GitHub that you can download from [github/gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore). Just download the raw file and save it as .gitignore inside you current pelican-site directory. Since this repository is using pelican the `output` directory (where the content is generated) must be ignored as well.

    :::bash
    curl -o .gitignore -sSL https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore
    echo -e "\n# Pelican site generator\noutput" >>.gitignore

#### Pelican project initialization

```bash
git remote add origin git@github.com:your-username/pelican-site.git
git push -u origin main
```

## Project Structure

<!-- Explain the directory layout -->
<!-- Key files: pelicanconf.py, publishconf.py, content/, theme/ -->

## Configuration

### Development vs Production Settings

<!-- Explain the dual configuration model -->
<!-- pelicanconf.py for local development -->
<!-- publishconf.py for production -->

### Customizing the Theme

<!-- Any theme modifications you made -->

## GitHub Pages Setup

### Repository Configuration

<!-- How to set up the repo for GitHub Pages -->
<!-- Branch settings, custom domain (CNAME) -->

## Automating Deployment with GitHub Actions

### The Workflow File

<!-- Explain the pelican-deploy.yml workflow -->
<!-- Triggers, steps, secrets needed -->

### Branch Protection and PR Workflow

<!-- Why you chose squash merges -->
<!-- Protected branch settings -->

## Development Workflow

### Local Development

<!-- make devserver, live reload -->
<!-- Testing changes locally -->

### Publishing Changes

<!-- The process from writing content to deployment -->

## Lessons Learned

<!-- What challenges did you face? -->
<!-- What would you do differently? -->
<!-- Tips for others -->

## Conclusion

<!-- Summary and next steps -->
<!-- Links to the repository, live site -->

## Resources

<!-- Useful links -->
<!-- - [Pelican Documentation](https://docs.getpelican.com/) -->
<!-- - [Poetry Documentation](https://python-poetry.org/docs/) -->
<!-- - [GitHub Pages Documentation](https://docs.github.com/en/pages) -->


If you are not comfortable with Github actions or you can run generation locally and fallback to basic GH page deployment of static content from a branch

[^1]: You can always manage Python dependencies manually using pip but it is better to [use a dedicaded tool](https://packaging.python.org/en/latest/tutorials/managing-dependencies/).
[^2]: Alternativaly you can quickstart running Pelican locally and publish content of `output/` directory with [a branch deployment](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#troubleshooting-publishing-from-a-branch)
[^3]: If you don't have a domain name you can use GH pages with the included _\<username\>_.github.io subdomain.
