from tflite_runtime.interpreter import Interpreter 
from PIL import Image
from load_labels import load_labels
from classify_image import classify_image
from cv2_init import cv2_init
import cv2
import numpy as np
import time

#====================================================================================#
cap = cv2_init(224, 224)
model_path = "models_and_labels./model2.tflite"
label_path = "models_and_labels./labels2.txt"

# Read class labels.
labels = load_labels(label_path)

interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Image Shape (", width, ",", height, ")")
init_time = time.time()
while(True):

  ret, frame = cap.read()
  cv2.imshow('frame', frame )

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  if time.time() - init_time >= 2:
    #image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)) # convert opencv(frame) to PIL(image)
    frame = frame[:,:,::-1]
    image = Image.fromarray(frame)
    image = image.resize((width, height)) # resize image to (224, 224)
    label_id, prob = classify_image(interpreter, image)
    init_time = time.time()

    # Return the classification label of the image.
    classification_label = labels[label_id]
    print("Image Label is :", classification_label, ", with Accuracy :", np.round(prob*100, 2), "%.")