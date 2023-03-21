# Packaging

## Build with setuptools

This will build the wheel and source distribution into `dist/`

```terminal
pip install --upgrade build
python -m build
```

## Upload with twine

[twine](https://twine.readthedocs.io/en/latest/)

```terminal
pip install --upgrade twine
```

Test on Test PyPI

```terminal
twine upload -r testpypi dist/*
```

Finally upload to official
```terminal
twine upload dist/*
```

## Testing on PyPI

Allows installing dependencies from standard PyPI.

```terminal
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hyperx
```

