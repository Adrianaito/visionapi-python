from google.cloud import vision_v1
import io
import os
from google.cloud.vision_v1 import types
import logging


def detect_text_uri(file):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

    client = vision_v1.ImageAnnotatorClient()
    image = vision_v1.Image()
    image.source.image_uri = f"gs://pdf_upload/{file}"

    print('Slowly Reading Files...')

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    # logging.basicConfig(filename="ResponseText.log",
    #                     filemode='a',
    #                     format='%(message)s',
    #                     datefmt='%H:%M:%S',
    #                     level=logging.DEBUG)

    # log = logging.getLogger("MyLogText")
    # log.debug(response)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


detect_text_uri("wakeupcat.jpeg")
