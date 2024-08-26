import requests
import os
import base64


def get_prediction(prompt, image_data):
    image = base64.b64encode(image_data)
    image = image.decode('utf-8')

    response = requests.post(
        url='http://{}:{}/api/generate'.format(os.environ.get('MODEL_HOST'), os.environ.get('MODEL_PORT')),
        json={
            'model': 'llava',
            'prompt': prompt,
            'stream': False,
            'images': [
                image,
            ],
        }
    )

    return response.json()['response'].strip()
