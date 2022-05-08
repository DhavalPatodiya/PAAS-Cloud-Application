# PAAS-Cloud-Application

**Problem Statement**

Cloud computing is improving day by day. With the development of PaaS, architecture users are able to deploy applications to the cloud without worrying about autoscaling, underlying hardware architecture, etc. This has helped the users focus on the development of the applications. But users still have to keep the server running and pay the cost even if there are no active users for the application. This has led to the development of FaaS, an advanced version of PaaS. FaaS is an example of serverless computing where the server doesn’t need to keep the server running at all times, only the functions which are used by the user will be invoked through some triggers and will autoscale itself on the basis of demand. This has helped the cloud user to minimize the cost of using the FaaS cloud. The main aim of this project is to create a FaaS cloud application that will be cost-effective for users. The application will provide a face recognition service to it the user, by using cloud resources to perform deep learning images provided by the users. Images are sent from an IoT device. The application will use AWS cloud resources like ECR, S3, API Gateway, DynamoDB, and Lambda to respond to users as soon as possible. Docker is used for making images.

**Design and Architecture Architecture**
<img width="598" alt="Screenshot 2022-05-07 at 23 54 11" src="https://user-images.githubusercontent.com/37049494/167285413-18bf1020-ab4b-44e6-885e-c61138a1c381.png">

Raspberry Pi records a video using an open cv2 library. From live recording, frames are extracted and sent to lambda after every 0.5 seconds. Lambda Function is deployed as a Docker image containing all the necessary code for doing facial recognition (provided by the professor) which does the facial recognition of the images or frames sent by the user. It triggers from API Gateway. From the result of facial recognition, it fetches the detail of the person from the DynamoDB and returns back the result in the form of a JSON object. After the videos are recorded for approximately 0.5 seconds and when the pi stops recording and all are uploaded to the S3 bucket. The program waits till all the results are returned back to the pi and then terminates.

Lambda Function uses the Docker image that is fetched from the ECR repository for making containers and runs the required code for image processing.

Docker image contains the model, required libraries, code, and files required for the facial recognition of the image sent by pi.


**Concurrency and Latency**

Concurrency is achieved through multithreading for sending the frames, and videos and for fetching the result of each corresponding request. While for lambda or the server-side the AWS auto scales the lambda function on the basis of the request. It also keeps the lambda functions running for a particular amount of time after processing the request so that the next request can be processed in the same lambda function which helps in reducing the cold starts of the lambda function.

Latency is calculated by noting the time in milliseconds when the frame is sent to lambda (sent_time) and when the lambda returns the response the time of response (resp_time) is noted and the latency is calculated by the given formula for each request.
Latency = resp_time - sent_time

**Testing and Evaluation**

The application was tested at least 10 times before the demo. The application was tested on the basis of the following points.
- The frames are sent from the Pi to the cloud continuously
  - The frames were extracted from the live recording of the video and sent to the cloud after every 0.5 seconds.
- All the received videos in the cloud are properly saved in S3
  - Videos of approx 0.5 seconds are uploaded to S3 after the application is stopped. 
- All the faces in the sent videos are recognized.
  - By calculating the difference between the latency of two responses, it was made sure that the results are returned to pi every 0.5 seconds.
- The face recognition results are correct. More than 60% of the face recognition results are correct.
  - The model accuracy is found to be 85% after training the provided model with the team member’s images.
- The Lambda functions are autoscaled correctly
  - It was checked using the metrics of the AWS and yes the functions were autoscaling.
- The student’s academic information is stored properly in DynamoDB
  - Information was stored in the DynamoDB beforehand and it was checked by fetching the result from DynamoDB through testing code.
- All the recognized students’ academic information is correctly returned to the Pi
  - Yes, the information was returned correctly to the PI. It was verified by printing the information of the person.
- The end-to-end latency (the time between when a face is recorded by the camera and when the student’s academic information is returned to the Pi) should be reasonably short.
  - The end-to-end latency was found to be between 2.0s to 2.4s for each test.


**Code Explanation**

There are 2 folders named:
  1) Pi Code
      - Record.py
  2) Docker Image Code
      - CSE546-FallA2021-master
          -  Checkpoints
          -  Models
          -  Build_custom_model.py
          -  Dockerfile
          -  Encoding
          -  Entry.sh
          -  Eval_face_recognition.py
          -  Handler.py
          -  Install_requirements.sh
          -  Run.sh
          -  Workload.py



**Record.py**
- Records video
  - It will record a video for a duration of approx 0.5 seconds and will be uploaded to s3.
  - It extracts frames from captured video recordings using OpenCV and sends them to lambda for evaluation.
  - The results returned from lambda are printed on the screen.
  - capture():
    - It captures videos for a duration of 0.5 seconds using OpenCV. And uploads all the video when 300 seconds are passed to S3.
  - send_image_to_lambda(video_file_path):
    - It extracts the frame from the video and sends it to lambda as base64string for processing and when the lambda returns the result. Latency is calculated by calculating the difference between sent_request_time and resp_time. Latency and results are printed on the screen.


**Checkpoint, models, build_custom_model.py, encoding, entry.sh, mapping, run.sh, workload.py**

These files are either provided by the professor or generated during the model training and are required for the evaluation of images(face recognition).

**Eval_face_recognition.py**
  - It prints the result or name of the person whose face is recognized from the image sent to lambda.
 
**Requirements.txt**
  - Here all the required files to be installed are mentioned.

**Dockerfile**
  - Docker image is created on the basis of this file and all the commands which will install required libraries, and copy necessary files are mentioned here.

**Handler.py**
  - It contains the code which will be running on the lambda. face_recognition_handler(event, context):
  - face_recognition_handler(event, context)
     - It will decode the base64 string into images.
     - Then it will run the ‘eval_face_recognition.py’ command using os.popen for face recognition.
     - After reading the result, it will fetch the information related to that person from the DynamoDB and will return the result back to pi.


**How to run code?**
- Train Model
  - Train the model with your team members’ images as mentioned in the guidelines given by the professor.
- Pi Code
  - Either install AWS CLI and configure it or AWS provides credentials while creating clients and resources from boto3.
  - Copying the file to PI from the desktop by connecting it to Pi. Can also use VNC viewer or ssh commands for copying files to PI.
  - Open command prompt in PI
    - Install OpenCV using pip install opencv-python
    - Install other libraries if they are not installed.
    - Create a Videos folder on the desktop
    - Run python record.py
    - Delete the images and recordings before shutting Pi as memory is limited.
- Lambda code
  -  Install docker
  -  Start the docker
  -  Create a docker image using the push command given from the ECR repository.
- AWS
  - AWS role
    - Go to IAM
    - Create a role
    - Add the following permissions shown in the image.
     <img width="527" alt="Screenshot 2022-05-07 at 23 54 22" src="https://user-images.githubusercontent.com/37049494/167285363-307fcc30-9518-47be-9895-1d765810ec9f.png">

 - ECR
  - Create a repository and using the push command upload the docker image.
- Lambda
  - Create a function using the container and select the docker image uploaded to ECR.
  - Select the role containing all the permissions and click on create.
- API Gateway 
  - Create a Post API using Rest API and give integration to the lambda function.
  - Follow the steps shown on the screen.
  - Test the API using AWS.
  - Deploy the API.
  - Get the link and send images to that link for invoking lambda functions
- S3
  - Create a bucket.
- DynamoDB
  - Create a table
  - Add users details
- Replace the name of S3, DynamoDB, etc. in the handler.py and record.py code files.
