import os

from aws_cdk import core

from cdk.stack import AppStack


app = core.App()
basename = "lambda-monorepo-example"
STAGE = os.environ.get("STAGE", "dev")

AppStack(
    app,
    f"{basename}-{STAGE}",
    env=core.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

# Tag infrastructure
for key, value in {
    "Project": "monorepo-example",
    "Owner": os.environ.get("OWNER"),
    "Client": "example-client",
    "Stack": STAGE,
}.items():
    core.Tags.of(app).add(key, value, apply_to_launched_instances=True)

app.synth()
