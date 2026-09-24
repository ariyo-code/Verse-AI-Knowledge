# Package / PyPI readiness

The project can be built as a normal Python wheel/sdist and installed locally as `verse-ai-knowledge`. V25 does **not** publish to PyPI.

Publishing a proprietary/source-available package is a separate maintainer decision. Review `LICENSE.md`, project metadata and the desired distribution policy before any upload.

Local validation command:

```bash
python -m build
```

In an offline environment where `build` is unavailable, `pip wheel . --no-deps --no-build-isolation` can still validate setuptools packaging if build requirements are already installed.
