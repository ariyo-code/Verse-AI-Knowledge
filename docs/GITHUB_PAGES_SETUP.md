# GitHub Pages setup

The normal `Docs` workflow only validates that the MkDocs site builds successfully. It does **not** require GitHub Pages to be enabled.

To publish the site:

1. Open repository **Settings → Pages**.
2. Set **Build and deployment → Source** to **GitHub Actions**.
3. Open **Actions → Deploy Docs to GitHub Pages**.
4. Run the workflow manually.

Until Pages is enabled, do not run the deployment workflow. Documentation build validation remains independent from Pages deployment.
