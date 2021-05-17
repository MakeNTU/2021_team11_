from tflite_runtime.interpreter import Interpreter 
from PIL import Image
from load_labels import load_labels
from classify_image import classify_image
import numpy as np
import time

data_folder = "./models_and_labels/"
img_folder = "./test_img/"

model_path = data_folder + "model2.tflite"
label_path = data_folder + "labels2.txt"

model2_path = data_folder + "model3.tflite"
label2_path = data_folder + "labels3.txt"

interpreter = Interpreter(model_path)
interpreter2 = Interpreter(model2_path)
#print("Model Loaded Successfully.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
#print("Image Shape (", width, ",", height, ")")

interpreter2.allocate_tensors()
_, height, width, _ = interpreter2.get_input_details()[0]['shape']

# Load an image to be classified.
image = Image.open(img_folder + "dog.jpg").convert('RGB').resize((width, height))

# Classify the image.
time1 = time.time()
label_id, prob = classify_image(interpreter, image)
label_id2, prob2 = classify_image(interpreter2, image)
time2 = time.time()
classification_time = np.round(time2-time1, 3)
#print("Classificaiton Time =", classification_time, "seconds.")

# Read class labels.
labels = load_labels(label_path)
labels2 = load_labels(label2_path)
# Return the classification label of the image.
classification_label = labels[label_id].split(" ")[1]
classification_label2 = labels2[label_id2].split(" ")[1]
print("Image Label is :", classification_label, ", with Accuracy :", np.round(prob*100, 2), "% by interpreter1")
print("Image Label is :", classification_label2, ", with Accuracy :", np.round(prob2*100, 2), "% by interpreter2")
