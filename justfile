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

# Clean generated files
clean:
    @echo "🧹 Cleaning generated files..."
    rm -f dist/index.html dist/avatar.png
    @echo "✅ Cleaned"

# Show available recipes
help:
    @just --list