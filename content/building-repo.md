Title: Building a Pelican Site with GitHub Pages and Poetry
Date: 2026-01-10
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

### Installing Poetry

<!-- Explain Poetry and why you chose it over pip/pipenv -->
<!-- Installation steps -->

### Initializing the Pelican Project

<!-- Steps to create the project -->
<!-- Configuration choices you made -->

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
