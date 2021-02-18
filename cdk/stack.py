from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_python as lambda_python
from aws_cdk import core


class AppStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Package our common dependencies as layers
        db_layer = lambda_python.PythonLayerVersion(
            self,
            "DB lib",
            entry="layers/db-utils",
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
        )

        # Deploy Lambda 1 which relies on db_utils (which is deployed as a Layer)
        _ = lambda_python.PythonFunction(
            self,
            "Lambda 1",
            entry="lambdas/lambda_1",
            handler="handler",
            layers=[db_layer],
            memory_size=128,
            timeout=core.Duration.seconds(10),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
        )

        # Deploy Lambda 2, which has no local dependencies, but does install Numpy on
        # deployment
        _ = lambda_python.PythonFunction(
            self,
            "Lambda 2",
            entry="lambdas/lambda_2",
            handler="handler",
            memory_size=128,
            timeout=core.Duration.seconds(10),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
        )
