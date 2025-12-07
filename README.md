# miketheman.dev

A modern, responsive personal website generator that creates a beautiful "link in bio" style page. Features a QR code avatar and clean design that adapts to light/dark themes.

## ✨ Features

- **QR Code Avatar**: Automatically generates a QR code with embedded profile photo
- **Responsive Design**: Looks great on desktop and mobile devices
- **Dark Mode Support**: Automatically adapts to user's system preference
- **Easy Configuration**: Simple TOML file for all content and links
- **Extras Section**: Optional section for presentations, talks, and additional resources
- **Fast Generation**: Uses Python with Jinja2 templating
- **GitHub Actions Deploy**: Automated deployment to GitHub Pages

## 🚀 Quick Start

### Prerequisites
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- [just](https://github.com/casey/just) - Command runner (optional but recommended)

### Build the Site

```bash
# Using Just (recommended)
just build          # Generate the website
just serve          # Build and start development server
just avatar         # Generate new QR code avatar
just clean          # Clean generated files

# Or run scripts directly
./generate.py       # Generate the website
./serve.py          # Start development server
./avatar.py         # Generate QR code avatar (requires personal photo)
```

The resulting website will be created in the `dist/` directory.

### Configuration

Edit `metadata.toml` to customize your profile:

```toml
name = "Your Name"
title = "Your Title"
avatar = "https://yoursite.com/avatar.png"

[[links]]
url = "https://github.com/yourusername"
label = "GitHub"
icon = "fa-brands fa-github"

# Optional: Add extras section for presentations, talks, resources, etc.
[[extras]]
label = "PyCon 2024 - My Talk"
url = "https://example.com/slides"
icon = "fa-solid fa-presentation"
date = "2024-05-15"  # Required: ISO 8601 date format (YYYY-MM-DD)
```

#### Extras Section

The optional `extras` section allows you to showcase additional content like:
- Conference presentations and talks
- Slide decks and resources
- Video recordings
- Appendix materials

Extras are automatically sorted by date (most recent first). If more than 5 items are present, the additional items will be hidden behind an expandable "Show more" button.

Each extra item supports:
- `label`: Display text for the item
- `url`: Link to the resource
- `icon`: FontAwesome icon class
- `date`: **Required** - Date in ISO 8601 format (YYYY-MM-DD) for sorting

## 📁 Project Structure

```
├── generate.py          # Main site generator
├── avatar.py           # QR code avatar generator
├── serve.py            # Development server
├── justfile            # Task runner commands
├── metadata.toml       # Site configuration
├── templates/          # Jinja2 templates
│   └── index.html.j2  # Main page template
└── dist/              # Generated website
    ├── index.html
    └── avatar.png
```

## 🚀 Deploy

Deployment is handled automatically via GitHub Actions when you push to the main branch. The workflow builds the site and deploys it to GitHub Pages.

### Pull Request Previews

When you create a pull request, a preview of your changes is automatically deployed to a unique URL and linked in the PR description. This allows you to review changes before merging. The preview is automatically cleaned up when the PR is closed.

## 🎨 Customization

- **Styling**: Modify the CSS in `templates/index.html.j2`
- **Layout**: Update the Jinja2 template structure
- **Links**: Add/remove social links in `metadata.toml`
- **Extras**: Add optional extras section for presentations and resources
- **Avatar**: Replace with your own QR code using `avatar.py`
