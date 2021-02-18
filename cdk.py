import os

from aws_cdk import core

from cdk.stack import AppStack

app = core.App()

AppStack(app, f"lambda-monorepo-example-{os.environ['IDENTIFIER']}")

for k, v in {
    "Project": "lambda-monorepo-example",
    "Stack": os.environ["STAGE"],
    "Owner": os.environ["OWNER"],
}.items():
    core.Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
