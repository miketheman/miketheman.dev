# Default recipe to display help
default:
    @just --list

# Generate the website
build:
    @echo "🔨 Building website..."
    uv run src/generate.py
    @echo "✅ Website built in dist/"

# Start development server
serve: build
    @echo "🚀 Starting development server..."
    uv run src/serve.py

# Generate new avatar (requires personal photo)
avatar:
    @echo "🎨 Generating QR code avatar..."
    uv run src/avatar.py
    @echo "✅ Avatar generated"

# Fetch Font Awesome SVGs for any icons referenced in metadata.toml
icons:
    @echo "📦 Fetching icon SVGs..."
    uv run src/icons.py

# Download and self-host Google Fonts (writes assets/fonts/*.woff2 and assets/fonts.css)
fonts:
    @echo "📦 Fetching fonts..."
    uv run src/fonts.py

# Lint the rendered HTML (runs biome against dist/index.html)
lint: build
    @echo "🔍 Linting rendered HTML..."
    biome check dist/

# Render a visual snapshot of the built site for PR diffs
snapshot: build
    @echo "📸 Capturing visual snapshot..."
    uv run src/snapshot.py

# Render the 1200x630 OpenGraph card to assets/og.png
og:
    @echo "🖼️  Rendering OpenGraph card..."
    uv run src/og.py

# Clean generated files
clean:
    @echo "🧹 Cleaning generated files..."
    rm -f dist/index.html dist/avatar*.png
    @echo "✅ Cleaned"

# Show available recipes
help:
    @just --list