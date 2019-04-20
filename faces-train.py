import cv2
import os
import numpy as np
from PIL import Image
import pickle


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #faces-train.py file's path is BASE_DIR
image_dir = os.path.join(BASE_DIR, "images") # the path for the images directory

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"): # if files end with png or jpg 
			path = os.path.join(root, file) # ^^take the path for both of them
			label = os.path.basename(root).replace(" ", "-").lower() #labeling for all path of images' directories
			#print(label, path) # print path for all of them 
			if not label in label_ids:
				label_ids[label] = current_id
				current_id +=1
			id_ = label_ids[label]
			#print(label_ids)
			#y_labels.append(label) #some number
			#x_train.append(path) #verify this image, turn into a NUMPY array, GRAY
			pil_image = Image.open(path).convert("L") # gray scale
			size = (550, 550)
			final_image = pil_image.resize(size, Image.ANTIALIAS)
			image_array = np.array(final_image, "uint8")
			#print(image_array)
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

			for(x, y, w, h) in faces:
				roi = image_array[y:y+h, x:x+w]
				x_train.append(roi)
				y_labels.append(id_)
#print(y_labels)
#print(x_train)

with open("labels.pickle", 'wb') as f:
	pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")