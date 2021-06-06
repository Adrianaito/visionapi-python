from google.cloud.storage import bucket


try:
    import io
    from io import BytesIO
    # import pandas as pd
    import uuid
    from google.cloud import storage
except Exception as e:
    print("Some Modules are missing {}".format(e))

storage_client = storage.Client.from_service_account_json(
    "ServiceAccountToken.json")

bucket = storage_client.get_bucket("pdf_ex123")

id = str(uuid.uuid1())[:4]

fileName = "%s/%s" % ('', f"{id}.png")
blob = bucket.blob(fileName)

with open('resources/meme.png', 'rb') as f:
    blob.upload_from_file(f)

print("Upload complete")
