# Copilot Instructions for miketheman.dev

## Repository Overview

This is a modern, responsive personal website generator that creates a beautiful "link in bio" style page. The project uses Python with Jinja2 templating to generate a static website from TOML configuration, with automated deployment to GitHub Pages.

## Technology Stack

- **Python**: 3.13+ (minimum version required)
- **Package Manager**: [uv](https://docs.astral.sh/uv/) - Fast Python package manager with inline script metadata
- **Templating**: Jinja2 for HTML generation
- **Task Runner**: [just](https://github.com/casey/just) (optional but recommended)
- **Deployment**: GitHub Actions to GitHub Pages
- **Key Libraries**: 
  - `jinja2` - Template rendering
  - `qrcode[pil]` - QR code generation with PIL support

## Project Structure

```
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment workflow
├── templates/
│   └── index.html.j2          # Jinja2 template for the main page
├── dist/                      # Generated website output (not committed)
├── generate.py                # Main site generator script
├── avatar.py                  # QR code avatar generator script
├── serve.py                   # Development server script
├── metadata.toml              # Site configuration and content
├── metadata.example.toml      # Example configuration
├── avatar.png                 # Generated QR code avatar
└── justfile                   # Task runner commands
```

## Development Workflow

### Building and Testing

All Python scripts use inline script metadata (PEP 723) and should be executed with `uv run`:

```bash
# Generate the website
./generate.py
# or
uv run generate.py

# Start development server (builds first if needed)
./serve.py
# or
uv run serve.py

# Generate new QR code avatar (requires personal photo)
./avatar.py
# or
uv run avatar.py
```

### Using just (Task Runner)

When `just` is available, use these convenient commands:

```bash
just build          # Generate the website
just serve          # Build and start development server
just avatar         # Generate new QR code avatar
just clean          # Clean generated files
```

### Build Process

1. The `generate.py` script reads `metadata.toml`
2. Renders the Jinja2 template (`templates/index.html.j2`)
3. Outputs to `dist/index.html`
4. Copies `avatar.png` to `dist/` if it exists

## Code Conventions

### Python Style

- **Python Version**: Always use features compatible with Python 3.13+
- **Script Metadata**: All executable Python scripts use inline script metadata (PEP 723) in the shebang format:
  ```python
  #!/usr/bin/env -S uv run --script
  # /// script
  # requires-python = ">=3.13"
  # dependencies = [
  #   "package-name",
  # ]
  # ///
  ```
- **Error Handling**: Use try-except blocks with user-friendly error messages (with emoji prefixes)
- **Console Output**: Use emoji prefixes for status messages:
  - ✅ for success
  - ❌ for errors
  - ⚠️ for warnings
  - 🚀 for server/deployment actions
  - 🔨 for build actions
  - 🎨 for avatar/design actions

### File Organization

- Keep scripts in the root directory
- Templates in `templates/`
- Generated output in `dist/`
- Configuration in `metadata.toml`

### Configuration

- **Primary Config**: `metadata.toml` contains all site content and links
- **Format**: TOML with clear sections for profile info and links array
- **Links Order**: The order of `[[links]]` sections determines display order

## Making Changes

### Modifying Site Content

Edit `metadata.toml` to update:
- Profile information (name, title, description, avatar URL)
- Social links (URL, label, icon class)

### Modifying Layout/Style

Edit `templates/index.html.j2`:
- HTML structure
- Inline CSS styles
- Template logic

### Modifying Build Logic

Edit `generate.py`:
- Template context data
- File generation logic
- Error handling

### Creating New Features

1. Update the relevant Python script(s)
2. Ensure inline script metadata includes all required dependencies
3. Test locally with `./script.py` or `uv run script.py`
4. Update documentation if needed
5. Ensure GitHub Actions workflow continues to work

## Dependencies

### Adding New Dependencies

When adding new Python dependencies:

1. Update the inline script metadata in the relevant `.py` file:
   ```python
   # /// script
   # requires-python = ">=3.13"
   # dependencies = [
   #   "existing-package",
   #   "new-package",
   # ]
   # ///
   ```

2. The `generate.py.lock` file is automatically managed by `uv` and doesn't need manual updates. It's used by GitHub Actions for reproducible builds.

### Current Dependencies

- **generate.py**: `jinja2`
- **avatar.py**: `qrcode[pil]` (includes PIL/Pillow)
- **serve.py**: No external dependencies (uses stdlib only)

## Deployment

### Automatic Deployment

- **Trigger**: Push to `main` branch
- **Process**: GitHub Actions workflow (`.github/workflows/deploy.yml`)
- **Steps**:
  1. Checkout code
  2. Install uv
  3. Build site with `uv run generate.py`
  4. Upload artifact
  5. Deploy to GitHub Pages

### Manual Deployment

Can be triggered via GitHub Actions `workflow_dispatch` event.

## Testing

Currently, this project doesn't have automated tests. When making changes:

1. Build the site locally: `./generate.py`
2. Test with development server: `./serve.py`
3. Verify the generated HTML in `dist/index.html`
4. Check that the site displays correctly in a browser
5. Verify all links work as expected

## Common Tasks

### Updating Profile Information

Edit `metadata.toml` and rebuild:
```bash
./generate.py
./serve.py  # Test locally
```

### Adding a New Social Link

Add a new `[[links]]` section in `metadata.toml`:
```toml
[[links]]
url = "https://example.com/profile"
label = "Service Name"
icon = "fa-brands fa-service"  # Font Awesome icon class
```

### Changing Site Design

1. Edit `templates/index.html.j2`
2. Rebuild and test: `./generate.py && ./serve.py`
3. Check responsive design on different screen sizes
4. Verify dark mode support

### Regenerating Avatar

1. Edit the hardcoded `AVATAR_FILE_PATH` variable in `avatar.py` (currently points to a specific Dropbox location) to point to your own profile photo file path
2. Run: `./avatar.py`
3. Rebuild site: `./generate.py`

Note: The avatar.py script requires a personal photo file at the path you specify.

## Important Notes

- **Generated Files**: The `dist/` directory contains generated files and should not be edited directly
- **Avatar File**: The `avatar.py` script has a hardcoded path to a personal photo file that needs to be updated before use. Edit the `AVATAR_FILE_PATH` variable to point to your own profile photo.
- **Python Version**: Always ensure scripts are compatible with Python 3.13+
- **uv Requirement**: All scripts are designed to run with `uv` for consistent dependency management
- **Executable Scripts**: All `.py` scripts in the root are executable with proper shebangs
- **Lock Files**: `generate.py.lock` is automatically managed by `uv` and tracks dependencies for the deployment workflow
