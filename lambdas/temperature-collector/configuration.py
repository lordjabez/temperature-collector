import json
import logging
import os

import boto3


_config_arn = os.environ.get('CONFIG_ARN')

_log = logging.getLogger(__name__)


def get():
    sm = boto3.client('secretsmanager')
    response = sm.get_secret_value(SecretId=_config_arn)
    return json.loads(response['SecretString'])
