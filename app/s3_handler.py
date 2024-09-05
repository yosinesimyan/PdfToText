import boto3

# AWS S3 configuration
S3_BUCKET = 'firstbucket-yosi'
S3_REGION = 'us-east-1' 

# Initialize S3 client
s3 = boto3.client('s3', region_name=S3_REGION)

## Upload file to S3
def upload_file_to_s3(fullpathfn, filename):
    s3.upload_file(
         fullpathfn,
         S3_BUCKET,
         filename
    )

def download_file_from_s3(fullpathdfn, filename):
    s3.download_file(
        Filename=fullpathdfn,
        Bucket=S3_BUCKET,
        Key=filename      
    )

def delete_file_from_s3(filename):
    s3.delete_object(Bucket=S3_BUCKET, Key=filename)
    
