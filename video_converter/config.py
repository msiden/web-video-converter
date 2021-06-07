import socket
import boto3
from botocore.exceptions import *

ec2 = boto3.resource("ec2")
ec2_instance = ec2.Instance("i-07b3a34e787e133d7")

HOSTNAME = socket.gethostname()
AWS_HOST = "ip-172-31-22-54"
DEV_MODE = HOSTNAME != AWS_HOST
LOCAL_IP = "127.0.0.1:8000"
try:
    PUBLIC_IP = ec2_instance.public_ip_address
except NoCredentialsError:
    DEV_MODE = True
    PUBLIC_IP = None
LOCAL_URL = f"http://{LOCAL_IP}/"
PUBLIC_URL = f"http://{PUBLIC_IP}/"
