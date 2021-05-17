from tflite_runtime.interpreter import Interpreter 
from PIL import Image
from load_labels import load_labels
from classify_image import classify_image
from cv2_init import cv2_init
import cv2
import RPi.GPIO as GPIO
from servo_setup import set_angle
import numpy as np
import time
import requests
import websockets
import asyncio
import json

#====================================================================================#
async def init_ws(ws_url):
    websocket = await websockets.connect(ws_url, ping_interval = None)
    return websocket

async def ws_send(websocket, msg):
    await websocket.send(msg)


async def ws_recv(websocket):
    response = await websocket.recv()
    return response

#init opencv2
cap = cv2_init(224, 224)

#set models and labels1 path
model_paths = ["../models_and_labels/model_table.tflite", "models_and_labels/model_bed.tflite"]
label_paths = ["../models_and_labels/labels_table.txt", "models_and_labels/labels_bed.txt"]

# Read class labels1.
labels1 = load_labels(label_paths[0])
labels2 = load_labels(label_paths[1])

# Load interpreters
interpreter1 = Interpreter(model_paths[0])
interpreter2 = Interpreter(model_paths[1])

# Allocate memory for interpreters
interpreter1.allocate_tensors()
interpreter2.allocate_tensors()
_, height, width, _ = interpreter1.get_input_details()[0]['shape']

# Set parameters
current_event = None
classified_event = None
time_interval = 30      #set interval of image classification(sec)
ws_url = "ws://192.168.100.43:4000"   #servo ip address
websocket = asyncio.get_event_loop().run_until_complete(init_ws(ws_url))
initial_msg = '["boardInfo",{"type":"device", "name":"testname", "OK":"true", "msg":"Success", "deviceType":"identifier"}]'

# Setup servo
servo_channel = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(servo_channel,GPIO.OUT)
pwm = GPIO.PWM(servo_channel, 50)
pwm.start(0)

print("Initializing...")
asyncio.get_event_loop().run_until_complete(ws_send(websocket, initial_msg))

while(True):
    ws_response = asyncio.get_event_loop().run_until_complete(ws_recv(websocket))
    [_, events] = json.loads(ws_response)
    print(events)
    events = sorted(events, key = lambda s: s["StartTime"])
    print(events)
    current_event = events[0]
    time_left = (current_event["EndTime"] - current_event["StartTime"])/1000 #sec
    start_time = current_event["StartTime"]/1000 #sec
    print(start_time - time.time(), "secs to start.")
    #if current_event["Event"] == "Sleep in bed" and start_time > time.time():
        
    #set_angle(35, servo_channel, pwm)
        
    while(time_left > 0):
        ret, frame = cap.read()
        #cv2.imshow('frame', frame )

        if time.time() - start_time >= time_interval:

            frame = frame[:,:,::-1]     #change color from BGR to RGB
            image = Image.fromarray(frame)
            image = image.resize((width, height)) # resize image to (224, 224)
            set_angle(90, servo_channel, pwm)
            label_id1, prob1 = classify_image(interpreter1, image)
            set_angle(35, servo_channel, pwm)
            label_id2, prob2 = classify_image(interpreter2, image)
            if labels2[label_id2][2:] == "sleep in bed":
              classification_result = "sleep in bed"
            else:
              classification_result = labels1[label_id1][2:] 
            start_time = time.time()
            time_left -= time_interval

            # Return the classification label of the image.
            #classification_result = labels1[label_id1][2:]
            send_msg = ["classifiedResult",{"origin": current_event,"classified_result": classification_result, "lasting_time": time_interval}]
            if time_left >= time_interval:
                asyncio.get_event_loop().run_until_complete(ws_send(websocket, json.dumps(send_msg)))
            print(classification_result)
            print('time_left:', time_left)
    time.sleep(10)        
    send_msg = ["endEvent"]
    asyncio.get_event_loop().run_until_complete(ws_send(websocket, json.dumps(send_msg)))
    
#    elif start_time > time.time():
#        
#        set_angle(100, servo_channel, pwm)
#        
#        while(time_left > 0):
#            ret, frame = cap.read()
#            #cv2.imshow('frame', frame )
#    
#            if time.time() - start_time >= time_interval:
#    
#                frame = frame[:,:,::-1]     #change color from BGR to RGB
#                image = Image.fromarray(frame)
#                image = image.resize((width, height)) # resize image to (224, 224)
#                label_id, prob = classify_image(interpreter1, image)
#                start_time = time.time()
#                time_left -= time_interval
#    
#                # Return the classification label of the image.
#                classification_result = labels1[label_id][2:]
#                send_msg = ["classifiedResult",{"origin": current_event,"classified_result": classification_result,"lasting_time": time_interval}]
#                if time_left >= time_interval:    
#                    asyncio.get_event_loop().run_until_complete(ws_send(websocket, json.dumps(send_msg)))
#                print(classification_result)
#                print('time_left:', time_left)
#        time.sleep(10)        
#        send_msg = ["endEvent"]
#        asyncio.get_event_loop().run_until_complete(ws_send(websocket, json.dumps(send_msg)))
#    else:
#      pass
#    
    
    if time_left < 0 :
        time_left = 0
    current_event = None    
