# miketheman.dev

A static website to display links.

Driven by a `metadata.toml` file and a `generate.py` script to create the HTML.

## Build

With `uv` installed, run:

```bash
./generate.py
```

The resulting `index.html` file will be created in the root directory.

## Deploy

Handled via GitHub Actions. See the `.github/workflows/deploy.yml` file for details.
