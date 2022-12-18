# Prefect utilities package

This package is meant to store code that can be shared across various flows in your Prefect project.

The code shown here uses BigQuery and Postgres, but you can extend it with:
   - commonly used functions and classes
   - shared utilities
   - custom reusable business logic 

You can install the package from the root project directory:
```
pip install .
```

or in editable mode (makes local development easier):

```
pip install -e .
```

Ideally, replace the ``prefect_utils`` package name based on what your project is about. 

