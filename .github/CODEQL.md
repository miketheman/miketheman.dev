# CodeQL Configuration

This repository uses **CodeQL Default Setup** for security scanning.

## What is Default Setup?

Default setup is GitHub's recommended way to configure CodeQL. It:

- ✅ **Automatically includes caching** to speed up analysis
- ✅ Scans code on push and pull requests
- ✅ Runs security and quality queries
- ✅ Updates automatically with the latest CodeQL features
- ✅ Requires no workflow file or manual configuration

## Configuration

Default setup is managed through the repository settings:
- Navigate to: Settings → Code security and analysis → CodeQL analysis
- Default setup is currently **enabled**

## Caching

CodeQL default setup includes built-in caching optimizations that:
- Cache databases between runs
- Reuse analysis results when possible
- Significantly reduce scan times on subsequent runs
- Automatically manage cache invalidation

No additional configuration is needed for caching - it's included by default.

## Custom Configuration

If you need advanced configuration options not available in default setup, you can:
1. Disable default setup in repository settings
2. Create a custom `.github/workflows/codeql.yml` workflow file
3. Configure advanced options as needed

For most use cases, default setup provides optimal performance with zero configuration.
