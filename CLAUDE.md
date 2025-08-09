# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Hugo-powered static blog (codegoalie.com) using a custom theme, deployed on Netlify. The site follows Hugo's standard directory structure with content in Markdown format and TOML front matter.

## Development Commands

### Local Development
- **Start development server**: `./start.sh` or `hugo server -D` (includes drafts)
- **Build for production**: `hugo --gc --minify`
- **Create new post**: `hugo new posts/YYYY-MM-DD-post-title.md`

### Content Creation
- Posts are created in `/content/posts/` using the archetype template
- New posts are created with `draft = true` by default
- Post filenames should follow the pattern: `YYYY-MM-DD-title.md` for dated posts
- Use categories in front matter to organize posts: `categories = ["Category1", "Category2"]`

## Architecture

### Content Structure
- **Posts**: `/content/posts/` - All blog posts in Markdown with TOML front matter
- **Static Assets**: `/static/` - Images, CSS, JS, fonts (copied directly to output)
- **Templates**: `/themes/codegoalie/layouts/` - Custom theme templates
- **Configuration**: `config.yml` - Main Hugo site configuration

### Theme Structure
- Uses custom "codegoalie" theme located in `/themes/codegoalie/`
- Styling with Bulma CSS framework + custom overrides
- Syntax highlighting via Highlight.js with Atom One Dark theme
- Responsive design optimized for mobile and desktop

### Build Process
- Hugo v0.80.0 static site generator
- Output directory: `/public/` (ignored in git)
- Netlify handles automated deployments with different contexts (production, preview, branch)
- Build includes garbage collection (`--gc`) and minification (`--minify`)

### Content Format
Posts use TOML front matter format:
```toml
+++
date = "2025-01-01T12:00:00-05:00"
title = "Post Title"
categories = ["Category1", "Category2"]
draft = false
+++
```

### Deployment
- Deployed automatically via Netlify on push to main branch
- Deploy previews generated for pull requests  
- Production builds use `hugo --gc --minify --enableGitInfo`
- Site URL: https://codegoalie.com