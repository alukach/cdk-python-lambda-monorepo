# CDK Python Lambda Monorepo 🐍📦


## The low-down

This repositories purpose is to document and display a pattern we're developing at Development Seed to standardise/explore making CDK Python Lambda (and other serverless services) Monorepos

On taking upon this exploration, we came up with the following requirements for our solution:

* We want deterministically built Layers (Layers are common across some Lambdas)
* We want deterministically built Lambdas
* We want to test our Lambdas locally with the Layers that they depend upon
* We want to use [aws-lambda-python](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-lambda-python-readme.html) to deploy Layers and Lambdas - Allowing us to provide `Pipfile`'s for deterministic builds

Building on those requirements: by building Layers, we're referring to times where we write a module locally within our repo that many of our Lambda functions depend on.

We want to not only deploy and build those deterministically, we also want to be able to develop our Lambda functions that use them locally. The key point here is that we don't want to have to change how we import our layers locally to how they're used once deployed. I.E we want `import <module name>` to work both locally and when deployed.

---

## Contents
* [So what does this look like?](#so-what-does-this-look-like)
* [Layers](#layers)
* [Lambdas](#lambdas)
* [CDK](#cdk)
* [Development - Requirements](#requirements)
* [Development - Getting Started 🏃‍♀️](#getting-started-🏃‍♀️)
* [Development - Making a new module](#making-a-new-module)
* [Development - Making a new Lambda](#making-a-new-lambda)
* [Development - Deploying your module and Lambda](#deploying-your-module-and-lambda)

---

## So what does this look like?

**TL;DR:**
> We use `setup.py` files to allow us to install our Layers locally per-Lambda for development. We then use these to generate `Pipfile` and `Pipfile.lock` files for deterministic builds and deployments. Each Lambda is its own `pipenv` 'environment', whilst this is quite verbose, it works.

We'll explain the full process of creating a new Layer and Lambda that uses it further below, but to start, let's give you a high level idea of what this pattern looks like

---

### Layers

For modules that we write locally that our Lambdas depend on, they need to be structured as so:

```
layers # Our top-level Layers directory
└── <layer-name> # A container directory for our Layer
    ├── Pipfile # Pipfile for aws-lambda-python
    ├── Pipfile.lock # Lockfile to go along with our Pipfile
    ├── <layer-name> # The module this Layer is going to provide
    │   └── __init__.py # Our module code (other files can go here too!)
    └── setup.py # Setup file that lists which dependencies our module has
```

---

### Lambdas

For Lambdas we write, whether they have external/local dependencies or not, they need to be structured as so:

```
lambdas # Our top-level Lambdas directory
└── <lambda-name> # A container directory for our Lambda
    ├── Pipfile # Pipfile for aws-lambda-python
    ├── Pipfile.lock # Lockfile to go along with our Pipfile
    ├── index.py # The entrypoint to our Lambda
    └── tests
        ├── __init__.py # Allows us to import our Lambdas functions
        └── test_handler.py # Unit tests
```

Packages are installed as follows with `pipenv`:

* Local modules (to be layers) - Editable, relative `[dev-packages]` dependencies
* External packages (available via layers) - `[dev-packages]` dependencies
* External packages (to be bundled on deploy) - Standard `[packages]` dependencies (Beware of Lambda sizes!)

An example `Pipfile` is illustrated below for a Lambda which depends on:
* A local `helpers` module
* The `rasterio` package (via a Layer when deployed)
* The `requests` package (bundled on deployment)
* The `pytests` package for unit tests

```
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "==2.25.1"

[dev-packages]
rasterio = "==1.2.0"
pytest = "==6.2.2"
helpers = {editable = true, path = "./../../layers/helpers"}

[requires]
python_version = "3.8"
```

---

### CDK

So when it comes to deploying our Layers and Lambdas, our CDK looks like:

```python
from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_python as lambda_python

# Package our common dependencies as layers
our_layer = lambda_python.PythonLayerVersion(
    self,
    "example_module layer",
    entry="layers/example_module",
    compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
)

# Deploy <a-name> Lambda which relies on `example_module` (which is deployed as a Layer)
_ = lambda_python.PythonFunction(
    self,
    "example_lambda",
    entry="lambdas/example_lambda",
    handler="handler",
    layers=[our_layer],
    runtime=aws_lambda.Runtime.PYTHON_3_8,
)
```

# Development

## Requirements

To develop on this project, you should install:

* NVM [Node Version Manager](https://github.com/nvm-sh/nvm) / Node 14
* [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) - There is a `package.json` in the repository, it's recommended to run `npm install` in the repository root and make use of `npx <command>` rather than globally installing AWS CDK
* [pyenv](https://github.com/pyenv/pyenv) / Python 3.8.6
* [pipenv](https://github.com/pypa/pipenv)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

---

## Getting started 🏃‍♀️

To get setup for overall development, ensure you've installed all the above [requirements](#Requirements), run the following commands in the root of the repository and you'll be good to go!

```bash
$ nvm install # This sets up your node environment
$ npm install # This installs any node packages that are within package.json (CDK etc.)
$ pipenv install --dev # This installs any python packages that are within Pipfile
```

**Note** It's also useful (and recommended) to set `PIPENV_NO_INHERIT=TRUE` as an environment variable, this prevents our Layer/Lambda level `pipenv` calls from using any other `pipenv` environments we have, making sure that we have everything isolated. Otherwise, you might have to prepend your `pipenv` calls with the environment variable (which is a PITA!)

---

## Making a new module

So you've identified that you need to write a new module and it's likely to be used across many of your Lambda functions, we'll call ours `todo-fetcher`:

1. Create a new directory tree for your module:
    ```bash
    $ mkdir -p layers/todo-fetcher/todo_fetcher
    ```
1. Create a `setup.py` for your module under `layers/todo-fetcher/setup.py`, a simple example is:
    ```python
    import setuptools

    setuptools.setup(
        name="todo_fetcher",
        version="0.0.1",
        packages=setuptools.find_packages(),
        python_requires=">=3.8",
        install_requires=["requests>=2.25.1"],
    )
    ```
1. Make sure your module has a `__init__.py` under `layers/todo-fetcher/todo_fetcher/`:
    ```bash
    $ touch layers/todo-fetcher/todo_fetcher/__init__.py
    ```
1. Create your 'business' logic under `layers/todo-fetcher/todo_fetcher/fetch.py`:
    ```python
    import requests

    def get_todo(number: int) -> dict:
        return requests.get(f"https://jsonplaceholder.typicode.com/todos/{number}").json()
    ```
1. Setup your Pipfile under `layers/todo-fetcher/`:
    ```bash
    $ pipenv install .
    ```

Following the above steps, you should now have a module `todo-fetcher` that is ready to be used in local Lambda development **and** is ready to be deployed as a Lambda Layer with CDK

---

## Making a new Lambda

For the purposes of this explanation, we'll assume you've created a module similar to `todo-fetcher` [here](#making-a-new-module). We're going to make a Lambda that takes an input, calls `todo-fetcher` and returns the `title` of the todo.

1. Create a new directory tree for your Lambda:
    ```bash
    $ mkdir -p lambdas/todo-fetcher/tests
    ```
1. Create your unit test `__init__.py` so that we can import our Lambdas functions:
    ```bash
    $ touch lambdas/todo-fetcher/tests/__init__.py
    ```
1. Install your local development dependencies under `lambdas/todo-fetcher`:
    ```bash
    $ pipenv install --dev -e ../../layers/todo-fetcher # Install the todo-fetcher module
    $ pipenv install --dev "pytest==6.2.2" "responses==0.12.1" # For unit testing our handler
    ```
1. Create your Lambdas `index.py` under `lambdas/todo-fetcher/`:
    ```python
    from todo_fetcher.fetch import get_todo


    def handler(event, context):
        return get_todo(event["number"])["title"]
    ```
1. Create your tests `test_handler.py` under `lambdas/todo-fetcher/tests/`:
    ```python
    from index import handler

    import responses


    @responses.activate
    def test_that_title_returned():
        responses.add(
            responses.GET,
            "https://jsonplaceholder.typicode.com/todos/1337",
            json={"title": "Woohoo!", "ping": "pong"},
            status=200
        )

        title = handler({"number": 1337}, None)

        assert title == "Woohoo!"
    ```
1. Run your test under `lambdas/todo-fetcher/`:
    ```bash
    $ pipenv run pytest
    ```

At this point, you've successfully created a Lambda function locally that depends on your `todo-fetcher` module.
The import statement in `index.py` works the same locally (when we run our tests) as it will in our deployed Lambda.

---

## Deploying your module and Lambda

At this point, we're assuming you've made your module and Lambda as explained above. Now, using `aws-lambda-python` you can deploy both of these with:

```python
# Any other imports you have in your app
from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_python as lambda_python

# ... Your CDK Code ...

# Deploy our `todo-fetcher` Layer
todo_layer = lambda_python.PythonLayerVersion(
    self,
    "todo-fetcher layer",
    entry="layers/todo-fetcher",
    compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
)

# Deploy our `todo-fetcher` Lambda
todo_function = lambda_python.PythonFunction(
    self,
    "todo-fetcher lambda",
    entry="lambdas/todo-fetcher",
    handler="handler",
    layers=[todo_layer],
    runtime=aws_lambda.Runtime.PYTHON_3_8,
)
```
