When you make changes to your `setup.py`, make sure you run the following in the root of your local module:

```sh
pipenv install .
```

This ensures that any requirements from your `setup.py` are added to your Pipfile for installation when deploying with CDK
