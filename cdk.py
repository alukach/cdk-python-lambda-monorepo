from aws_cdk import core

from cdk.stack import AppStack


app = core.App()
AppStack(app, "lambda-monorepo-example")

app.synth()
