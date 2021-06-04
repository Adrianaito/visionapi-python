# gs://pdf_ex123/領収書サンプル.pdf
# gs://pdf_ex123/sample1.pdf

import pdb
import io
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision_v1 import types
import json
import os
import re


# def async_detect_document(gcs_source_uri, gcs_destination_uri):
"""OCR with PDF/TIFF as source files on GCS"""

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'


client = vision.ImageAnnotatorClient()

# Supported mime_types are: 'application/pdf' and 'image/tiff'
mime_type = 'application/pdf'

# How many pages should be grouped into each json output file.
batch_size = 10

# client = vision.ImageAnnotatorClient()

feature = vision.Feature(
    type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

gcs_source_uri = 'gs://pdf_ex123/sample1.pdf'
gcs_source = vision.GcsSource(uri=gcs_source_uri)
input_config = vision.InputConfig(
    gcs_source=gcs_source, mime_type=mime_type)

gcs_destination_uri = 'gs://pdf_ex123/pdf_result'
gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
output_config = vision.OutputConfig(
    gcs_destination=gcs_destination, batch_size=batch_size)

async_request = vision.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config,
    output_config=output_config)

operation = client.async_batch_annotate_files(
    requests=[async_request])

print('Slowly Reading Files...')
operation.result(timeout=420)

# Once the request has completed and the output has been
# written to GCS, we can list all the output files.
storage_client = storage.Client()

match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
bucket_name = match.group(1)
prefix = match.group(2)

bucket = storage_client.get_bucket(bucket_name)

# List objects with the given prefix.
blob_list = list(bucket.list_blobs(prefix=prefix))
print('Output files:')
for blob in blob_list:
    print(blob.name)

# Process the first output file from GCS.
# Since we specified batch_size=2, the first response contains
# the first two pages of the input file.
output = blob_list
for file in output:

    json_string = file.download_as_string()
    response = json.loads(json_string)

# The actual response for the first page of the input file.
first_page_response = response['responses'][0]
annotation = first_page_response['fullTextAnnotation']
pdb.set_trace()

# print the full text from the first page.
# The response contains more information:
# annotation/pages/blocks/paragraphs/words/symbols
# including confidence scores and bounding boxes
print('Full text:\n')
print(annotation['text'])
