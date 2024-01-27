import boto3
import os
import zipfile

class LambdaDeployer:
    def __init__(self, event, context):
        self.s3_bucket = 'your-s3-bucket'
        self.s3_key = 'lambda_function.zip'
        self.templates_folder = '/tmp/cloudformation'

        # Download CloudFormation templates from S3
        self.download_templates()

        # Deploy CloudFormation templates
        self.deploy_cloudformation_templates()

    def download_templates(self):
        s3 = boto3.client('s3')
        
        # Check if S3 bucket exists
        try:
            s3.head_bucket(Bucket=self.s3_bucket)
        except Exception as e:
            print(f"S3 bucket {self.s3_bucket} does not exist. Create the bucket first.")
            raise e

        s3.download_file(self.s3_bucket, self.s3_key, self.templates_folder)

        # Extract the downloaded zip file
        with zipfile.ZipFile(self.templates_folder, 'r') as zip_ref:
            zip_ref.extractall(self.templates_folder)

    def deploy_cloudformation_templates(self):
        for filename in os.listdir(self.templates_folder):
            if filename.endswith(".yaml"):
                template_path = os.path.join(self.templates_folder, filename)
                
                # Deploy CloudFormation template using AWS CLI or Boto3
                os.system(f'aws cloudformation deploy --template-file {template_path} --stack-name {filename.split(".")[0]} --region your-region')
