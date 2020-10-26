import ibm_boto3
import json
from ibm_botocore.client import Config, ClientError

import re
# Constants for IBM COS values
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "3jVz59oiChrg3ngobrrpwRY8Vu_IOFJ6D2QcHineF9Xm" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/ba242e097299224620d429e0d2fe9b92:e625ff0b-36ba-4669-aba4-7c3343bff0d5::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    ibm_auth_endpoint="https://iam.bluemix.net/oidc/token",
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT   
)

cos2 = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)
#print(cos)

#Bucket creation scipt
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
# with open('buckets/test.json') as f:
#   data = json.load(f)
# #print(data[0])
# for x in data :
#     create_bucket(x)

def get_buckets():
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        for bucket in buckets:
            if (re.findall("prf", bucket.name)):
                buckets_for_deletion.append(bucket.name)
            #print("Bucket Name: {0}".format(bucket.name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))

def delete_item(bucket_name, object_name):
    try:
        cos2.delete_object(Bucket=bucket_name, Key=object_name)
        print("Item: {0} deleted!\n".format(object_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete object: {0}".format(e))

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        object_list = []
        for file in files:
            object_list.append(file.key)
            #print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return  object_list
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))


def delete_bucket(bucket_name):
    print("Deleting bucket: {0}".format(bucket_name))
    try:
        cos.Bucket(bucket_name).delete()
        print("Bucket: {0} deleted!".format(bucket_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete bucket: {0}".format(e))
buckets_for_deletion=[]
get_buckets()
#print(buckets_for_deletion)

for bucket_name in buckets_for_deletion:
    object_list = get_bucket_contents(bucket_name)
    for object_ in object_list:
        delete_item(bucket_name,object_) 
    #new_bucket_name = bucket_name.replace("prf","perf")
    #create_bucket(new_bucket_name)
    delete_bucket(bucket_name)
    



