# miketheman.dev

A modern, responsive personal website generator that creates a beautiful "link in bio" style page. Features a QR code avatar and clean design that adapts to light/dark themes.

## ✨ Features

- **QR Code Avatar**: Automatically generates a QR code with embedded profile photo
- **Responsive Design**: Looks great on desktop and mobile devices
- **Dark Mode Support**: Automatically adapts to user's system preference
- **Easy Configuration**: Simple TOML file for all content and links
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
```

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

## 🎨 Customization

- **Styling**: Modify the CSS in `templates/index.html.j2`
- **Layout**: Update the Jinja2 template structure
- **Links**: Add/remove social links in `metadata.toml`
- **Avatar**: Replace with your own QR code using `avatar.py`
