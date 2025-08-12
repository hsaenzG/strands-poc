#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    Duration,
)
from constructs import Construct


class ChatApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Lambda function from container image
        chat_lambda = _lambda.DockerImageFunction(
            self, "ChatFunction",
            code=_lambda.DockerImageCode.from_image_asset("."),
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "REGION_NAME": "us-east-1",
                "MODEL_ID": "anthropic.claude-3-sonnet-20240229-v1:0",
            }
        )

        # Add Bedrock permissions to Lambda
        chat_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                resources=[
                    f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                    f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
                    f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-opus-20240229-v1:0"
                ]
            )
        )

        # Create REST API Gateway
        api = apigw.RestApi(
            self, "ChatApi",
            rest_api_name="chat-api",
            description="REST API for chat functionality with Claude AI and Strands",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=apigw.Cors.DEFAULT_HEADERS,
                max_age=Duration.days(1),
            )
        )

        # Create Lambda integration
        lambda_integration = apigw.LambdaIntegration(
            chat_lambda,
            request_templates={"application/json": '{"statusCode": "200"}'}
        )

        # Add resources and methods
        chat_resource = api.root.add_resource("chat")
        chat_resource.add_method("POST", lambda_integration)

        health_resource = api.root.add_resource("health")
        health_resource.add_method("GET", lambda_integration)

        # Output the API endpoint
        cdk.CfnOutput(
            self, "ApiEndpoint",
            value=api.url,
            description="API Gateway endpoint URL"
        )

        # Output the model information
        cdk.CfnOutput(
            self, "ModelInfo",
            value=f"Claude 3 Sonnet via Amazon Bedrock with Strands in {self.region}",
            description="AI Model being used"
        )


def main():
    app = cdk.App()
    ChatApiStack(app, "ChatApiStack")
    app.synth()


if __name__ == "__main__":
    main()
