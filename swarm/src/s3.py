import os
import json
import io
from minio import Minio


BUCKET_NAME = 'images'


def get_client():
    return Minio(
        '{}:{}'.format(os.environ.get('S3_HOST'), os.environ.get('S3_PORT')),
        access_key=os.environ.get('S3_ACCESS_KEY'),
        secret_key=os.environ.get('S3_SECRET_KEY'),
        secure=False
    )


def create_backet():
    client = get_client()

    for bucket in client.list_buckets():
        if BUCKET_NAME == bucket.name:
            return

    client.make_bucket(BUCKET_NAME)

    policy = {
        'Version':'2012-10-17',
        'Statement':[
            {
            'Sid':'',
            'Effect':'Allow',
            'Principal':{'AWS':'*'},
            'Action':'s3:GetBucketLocation',
            'Resource':f'arn:aws:s3:::{BUCKET_NAME}'
            },
            {
            'Sid':'',
            'Effect':'Allow',
            'Principal':{'AWS':'*'},
            'Action':'s3:ListBucket',
            'Resource':f'arn:aws:s3:::{BUCKET_NAME}'
            },
            {
            'Sid':'',
            'Effect':'Allow',
            'Principal':{'AWS':'*'},
            'Action':'s3:GetObject',
            'Resource':f'arn:aws:s3:::{BUCKET_NAME}/*'
            },
            {
            'Sid':'',
            'Effect':'Allow',
            'Principal':{'AWS':'*'},
            'Action':'s3:PutObject',
            'Resource':f'arn:aws:s3:::{BUCKET_NAME}/*'
            }
        ]
    }
    client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))


def get_all_images():
    client = get_client()
    return list(map(lambda obj: obj.object_name, client.list_objects(BUCKET_NAME, recursive=False)))


def save_image(image_name, image_data):
    client = get_client()
    if image_name in get_all_images():
        return
    image = io.BytesIO(image_data)
    client.put_object(BUCKET_NAME, image_name, image, image.getbuffer().nbytes)
