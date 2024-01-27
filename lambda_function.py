from lambda_deployer import LambdaDeployer

def lambda_handler(event, context):
    deployer = LambdaDeployer(event, context)