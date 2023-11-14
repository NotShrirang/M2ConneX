import boto3
import os
from dotenv import load_dotenv
from typing import Union
import uuid
load_dotenv()

def upload_object(folder_path: str, remote_path: str) -> str:
    '''
    Uploads objects to S3 bucket

    Parameters
    ----------
    folder_path : str
        Path to the folder to be uploaded
    remote_path : str
        Path to the remote folder to be created

    Returns
    -------
    str
        Success message or error message
    '''
    try:
        if os.path.isfile(folder_path):
            s3 = boto3.resource(
                's3', 
                region_name=os.getenv("BUCKET_REGION"), 
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
            )
            s3.meta.client.upload_file(folder_path, os.getenv("BUCKET_NAME"), remote_path)
            return "Uploaded Successfully"
        else:
            return "File not found: " + folder_path
    except Exception as e:
        return str(e)
    
def download_object(remote_path: str, folder_path: str) -> str:
    '''
    Downloads objects from S3 bucket

    Parameters
    ----------
    remote_path : str
        Path to the remote folder to be downloaded
    folder_path : str
        Path to the folder to be created

    Returns
    -------
    str
        Success message or error message
    '''
    try:
        s3 = boto3.resource(
            's3', 
            region_name=os.getenv("BUCKET_REGION"), 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        s3.meta.client.download_file(os.getenv("BUCKET_NAME"), remote_path, folder_path)
        return "Downloaded Successfully"
    except Exception as e:
        return str(e)
    
def delete_object(remote_path: str) -> str:
    '''
    Deletes objects from S3 bucket

    Parameters
    ----------
    remote_path : str
        Path to the remote folder to be deleted

    Returns
    -------
    str
        Success message or error message
    '''
    try:
        s3 = boto3.resource(
            's3', 
            region_name=os.getenv("BUCKET_REGION"), 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        s3.Object(os.getenv("BUCKET_NAME"), remote_path).delete()
        return "Deleted Successfully"
    except Exception as e:
        return str(e)
    
def list_objects(remote_path: str) -> Union[list, str]:
    '''
    Lists objects from S3 bucket

    Parameters
    ----------
    remote_path : str
        Path to the remote folder to be listed

    Returns
    -------
    Union[list | str]
        List of objects or error message
    '''
    try:
        s3 = boto3.resource(
            's3', 
            region_name=os.getenv("BUCKET_REGION"), 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
        return [obj.key for obj in bucket.objects.filter(Prefix=remote_path)]
    except Exception as e:
        return str(e)
    
def get_object_url(remote_path: str) -> str:
    '''
    Gets object url from S3 bucket

    Parameters
    ----------
    remote_path : str
        Path to the remote folder to be listed

    Returns
    -------
    str
        Object url or error message
    '''
    try:
        s3 = boto3.client(
            's3', 
            region_name=os.getenv("BUCKET_REGION"), 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        return s3.generate_presigned_url('get_object', Params = {'Bucket': os.getenv("BUCKET_NAME"), 'Key': remote_path}, ExpiresIn = 3600)
    except Exception as e:
        return str(e)
    
def upload_image(file, folder=None):
    image_id = str(uuid.uuid4())
    file_bytes = file.open()
    if folder is not None and folder != "":
        aws_path = os.path.join("images", folder, f"{image_id}.jpg")
    else:
        aws_path = os.path.join("images", f"{image_id}.jpg")
    try:
        s3 = boto3.client(
            's3', 
            region_name=os.getenv("BUCKET_REGION"), 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        s3.upload_fileobj(
            file_bytes,
            Params = {'Bucket': os.getenv("BUCKET_NAME"), 'Key': aws_path},
            ExtraArgs={'ACL': 'public-read'})
        url = f"{os.getenv('AWS_URL')}/{aws_path}"
        return url
    except Exception as e:
        print("ERROR while uploading image: ", e, flush=True)
        return None