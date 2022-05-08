import numpy as np
import cv2
import time
import os
import boto3
import base64
import threading
import requests
import json

dict1 = {}
s3_resource = boto3.resource('s3', region_name='us-east-1', aws_access_key_id='',
    aws_secret_access_key='')
s3_client1 = boto3.client('s3', aws_access_key_id='',
    aws_secret_access_key='')


bucket_name = 'cse546.project2.video'
s3Bucket = s3_resource.Bucket(bucket_name)

count = 1
count1 = 1
start_time = time.time()

def send_image_to_lambda(video_file_path):
    global count, dict1, count1
    cap = cv2.VideoCapture(video_file_path)
    image_name = os.path.join("/home/pi/Desktop/Images/image_" + str(int(time.time() * 1000)) + ".png")
    while(cap.isOpened()):
        ret, frame = cap.read(())
        frame = cv2.resize(frame, (160, 160))
        cv2.imwrite(image_name, frame)
        break
    cap.release()

    fh = open(image_name, "rb")
    encoded_img = base64.b64encode(fh.read())
    fh.close()

    encoded_img = encoded_img.decode('utf-8')
    start_time = int(time.time()*1000)
    response = requests.post('https://5sjp6jyku5.execute-api.us-east-1.amazonaws.com/Test', json={'fileName' : str(start_time)  + '.png',
                                                                                            'image' : encoded_img})

    print(response.json()['body'])
    print('latency = ', (int(time.time()*1000)-start_time)/1000)
    dict1[count1] = count1
    count1 = count1 +1


def capture():
    global count, start_time, dict1

    #OPENCV
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    start = time.time()
    video_start_time = time.time()

    #SAVING VIDEO TO THIS PATH
    video_file_path = os.path.join("/home/pi/Desktop/Images/video" + str(count) + ".mp4")
    out = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*'XVID'),25, size)

    while cap.isOpened():
        #FRAME READ
        ret, frame = cap.read()
        #WRITING FRAME
        out.write(frame)

        #RESIZE AND SHOW
        #frame = cv2.resize(frame, (160,160))
        cv2.imshow('frame', frame)

        if ret == True:
            #SAVING VIDEOS AT 0.5 SECONDS
            if time.time() - start > 0.47:
                start = time.time()
                count += 1
                # cv2.imwrite(image_file_path, frame)
                video_file_path = os.path.join("/home/pi/Desktop/Images/video" + str(count) + ".mp4")
                out = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*'XVID'), 10, size)
                threading.Thread(target=send_image_to_lambda, args=(
                    os.path.join("/home/pi/Desktop/Images/video" + str(count-1) + ".mp4"),)).start()

            if time.time() - video_start_time > 300: #255:
                count = count + 1
                out = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*'XVID'), 10, size)
                threading.Thread(target=send_image_to_lambda, args=(
                os.path.join("/home/pi/Desktop/Images/video" + str(count - 1) + ".mp4"),)).start()
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()

    for i in range(1, count):
        s3Bucket.upload_file(os.path.join("/home/pi/Desktop/Images/video" + str(i) + ".mp4"),"video" + str(i) + ".mp4")

capture()