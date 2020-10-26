import ibm_boto3
import json
from ibm_botocore.client import Config, ClientError

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "3uzOySxV69_MGvCltDYjWRkCr-PejfERE6JIFYiAogUc" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/ba242e097299224620d429e0d2fe9b92:05649a80-4e35-4043-b97b-dda8e7eb3ceb::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    ibm_auth_endpoint="https://iam.bluemix.net/oidc/token",
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT   
)
#print(cos)
def create_bucket(bucket_name):
    print("Creating new bucket: {0}".format(bucket_name))
    try:
        cos.Bucket(bucket_name).create(
            CreateBucketConfiguration={
                "LocationConstraint":"us-south"
            }
        )
        print("Bucket: {0} created!".format(bucket_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create bucket: {0}".format(e))
# bucket_list.json will contain a json array with the list of buckets
with open('buckets/test.json') as f:
  data = json.load(f)
#print(data[0])
for x in data :
    create_bucket(x)
#map(create_bucket,data)
#create_bucket("first-test-nihal")
