# Development

## Requirements

To develop on this project, you should install:

* NVM [Node Version Manager](https://github.com/nvm-sh/nvm) / Node 14
* [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) - There is a `package.json` in the repository, it's recommended to run `npm install` in the repository root and make use of `npx <command>` rather than globally installing AWS CDK
* [pyenv](https://github.com/pyenv/pyenv) / Python 3.8.6
* [pipenv](https://github.com/pypa/pipenv)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

## Getting started 🏃‍♀️

To get setup for overall development, ensure you've installed all the above [requirements](#Requirements), run the following commands in the root of the repository and you'll be good to go!

```bash
$ nvm install # This sets up your node environment
$ npm install # This installs any node packages that are within package.json (CDK etc.)
$ pipenv install --dev # This installs any python packages that are within Pipfile
```
