#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: upload pic to Azure Storage
@file_name: azure_upload.py
@project: workplace
@version: 1.0
@date: 2023/7/23 21:28
@author: air
"""

import argparse
import re
import configparser

# Azure SDK
from azure.storage.blob import BlobServiceClient

# re rule
name_regex = re.compile('[^a-z0-9]')

# Parse commandline arguments
parser = argparse.ArgumentParser(description="Upload image to the Azure Image Host.")
parser.add_argument("File", nargs='+', help="The pic to be uploaded. Must include at least ONE.")
args = vars(parser.parse_args())
file_collection = args["File"]

# Save config

# config = configparser.ConfigParser()
# config['Azure'] = {}
# config['Azure']['URL'] = 'your_storage_account_url'
# config['Azure']['CONTAINER'] = 'your_container_name'
# config['Azure']['CONNECTION'] = 'your_connection_string'
# with open('config.ini', 'w') as configfile:
#     config.write(configfile)

# Load config
config = configparser.ConfigParser()
CONFIG_PATH = 'config.ini'
config.read(CONFIG_PATH)
url = config['Azure']['URL']
container_name = config['Azure']['CONTAINER']
connection_string = config['Azure']['CONNECTION']

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Upload pic to Azure Storage
for path in file_collection:
    file_type = path.split(".")[-1]
    blob_name = name_regex.sub('-', path.split("/")[-1].lower()) + "." + file_type
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(path, "rb") as data:
        blob_client.upload_blob(data)
    if url:
        print(url + container_name + "/" + blob_name)
