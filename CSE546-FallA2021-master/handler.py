import base64
import json
from boto3 import resource as boto3_resource
import os
from io import BytesIO
from PIL import Image

dynamodb = boto3_resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('output.table')

def face_recognition_handler(event, context):
    #decoding the images
    fileName = event['fileName']
    image_bytes = event['image']
    img_b64dec = base64.b64decode(image_bytes)
    img_byteIO = BytesIO(img_b64dec)
    image = Image.open(img_byteIO)

    #Saving files in tmp folder
    output_filename = '/tmp/' + fileName
    image.save(output_filename)

    stdout = os.popen('python3 eval_face_recognition.py --img_path ' + output_filename)
    result = stdout.read().strip()
    result = result.replace('(', '').replace(')', '')
    print("result = ", result)

    #fetching details from dynamodb
    response = table.get_item(
        Key={
            'Name': result
        }
    )
    print("response = ",response)
    response = str(response['Item'])
    print("response = ", response)

    return {
        'statusCode' : 200,
        'body' : json.dumps(response)
    }
