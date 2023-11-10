import boto3
from dotenv import load_dotenv
import os
from typing import Union

load_dotenv()

def create_rds_instance(db_instance_identifier: str, db_instance_class: str, master_username: str, master_password: str, allocated_storage: int, engine: str, availability_zone: str) -> str:
    '''
    Creates an Amazon RDS instance

    Parameters
    ----------
    db_instance_identifier : str
        Identifier for the DB instance
    db_instance_class : str
        The compute and memory capacity of the DB instance
    master_username : str
        Username for the master user
    master_password : str
        Password for the master user
    allocated_storage : int
        The amount of storage (in gibibytes) to allocate to the DB instance
    engine : str
        The name of the database engine to be used for this DB instance
    availability_zone : str
        The name of the Availability Zone where the DB instance will be created

    Returns
    -------
    str
        Success message or error message
    '''
    try:
        rds = boto3.client(
            'rds',
            region_name=os.getenv("RDS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        response = rds.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            AllocatedStorage=allocated_storage,
            DBInstanceClass=db_instance_class,
            Engine=engine,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            AvailabilityZone=availability_zone
        )

        return "RDS instance created successfully"
    except Exception as e:
        return str(e)

def delete_rds_instance(db_instance_identifier: str) -> str:
    '''
    Deletes an Amazon RDS instance

    Parameters
    ----------
    db_instance_identifier : str
        Identifier for the DB instance to be deleted

    Returns
    -------
    str
        Success message or error message
    '''
    try:
        rds = boto3.client(
            'rds',
            region_name=os.getenv("RDS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        response = rds.delete_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            SkipFinalSnapshot=True
        )

        return "RDS instance deleted successfully"
    except Exception as e:
        return str(e)

def list_rds_instances() -> Union[list, str]:
    '''
    Lists Amazon RDS instances

    Returns
    -------
    Union[list | str]
        List of RDS instances or error message
    '''
    try:
        rds = boto3.client(
            'rds',
            region_name=os.getenv("RDS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        response = rds.describe_db_instances()

        return [instance['DBInstanceIdentifier'] for instance in response['DBInstances']]
    except Exception as e:
        return str(e)
