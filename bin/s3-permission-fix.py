import boto3
import sys

### This changes the owner of the files in a bucket to the owner of the bucket
## Takes a single key as an argument and works recursively

# Constants
BUCKET='biomed-data'

client = boto3.client('s3')

def process_s3_objects(prefix):
    """Get a list of all keys in an S3 bucket."""
    kwargs = {'Bucket': BUCKET, 'Prefix': prefix}
    failures = []
    while_true = True
    while while_true:
      resp = client.list_objects_v2(**kwargs)
      for obj in resp['result']:
        try:
            print(obj['Key'])
            set_acl(obj['Key'])
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            while_true = False
        except Exception:
            failures.append(obj["Key"])
            continue

    print("failures :", failures)

def set_acl(key):
  client.put_object_acl(
    ACL='bucket-owner-full-control',
    Bucket=BUCKET,
    Key=key
)

process_s3_objects(sys.argv[1])
