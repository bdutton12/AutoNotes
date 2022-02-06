from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

import imutils
from imutils.contours import sort_contours
import numpy as np

import resnet

import time

from matplotlib import cm

def process_image(img):
    # Convert img to grayscale, crop, and blur
    alpha = 1.8
    gamma = 3
    img = cv2.addWeighted(img, alpha, img, 0, gamma)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, bw) = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    blurred = cv2.GaussianBlur(bw, (5, 5), 0)

    cv2.imshow('Window',blurred)
    cv2.waitKey
    

    # Edge detection, find contour in edge map, sort countours left to right
    edged = cv2.Canny(blurred, 0,2) #low_threshold, high_threshold
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]
    chars = []
    # Iterate over contours
    for c in cnts:
        # Calculate bounding box of letter, get region of interest
        (x, y, w, h) = cv2.boundingRect(c)
        roi = gray[y:y + h, x:x + w]
        
        # Convert image data to 0-1 instead of 0-255
        thresh = cv2.threshold(roi, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Resize largest dimension to 28
        (tW, tH) = thresh.shape
        if tW > tH:
            thresh = imutils.resize(thresh, width=32)
        else:
            thresh = imutils.resize(thresh, height=32)

        # Calculate padding
        tW, tH = thresh.shape
        dX = int(max(0, 28 - tW) / 2.0)
        dY = int(max(0, 28 - tH) / 2.0)

        # Pad and force 28x28
        padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
            left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
            value=(0, 0, 0))
        padded = cv2.resize(padded, (32, 32))

        # Reshape and rescale padded image to model standards
        padded = padded.astype("float32") / 255.0
        padded = np.expand_dims(padded, axis=-1)

        # Add image and bounding box to chars list
        chars.append((padded, (x, y, w, h)))
    
    return chars

def main():
    # Load trained NN
    model = load_model('D:\AutoNotes\handwriting.model')

    # Load img of handwriting
    img_path = 'D:\AutoNotes\handwriting.jpg'
    img = cv2.imread(img_path)
    img = img[50:-50,50:-100]

    chars = process_image(img)

    boxes = [b[1] for b in chars]
    chars = np.array([c[0] for c in chars], dtype="float32")
    
    # Get predictions of letters from model
    preds = model.predict(chars)

    # Define list of label names
    labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Iterate through predicted characters and create string
    notesText = []
    for (pred, (x, y, w, h)) in zip(preds, boxes):
        # Predicted char is the one with the highest probability in pred
        i = np.argmax(pred)
        prob = pred[i]
        print(pred)
        c = labelNames[i]
        if prob > .05:
            notesText.append(c)
        
    
    for (pred, (x, y, w, h)) in zip(preds, boxes):
    	# find the index of the label with the largest corresponding
    	# probability, then extract the probability and label
      i = np.argmax(pred)
      prob = pred[i]
      label = labelNames[i]
      # draw the prediction on the image and it's probability
      label_text = f"{label},{prob * 100:.1f}%"
      cv2.rectangle(img, (x, y), (x + w, y + h), (0,255 , 0), 2)
      cv2.putText(img, label_text, (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255, 0), 1)
    # show the image
    plt.figure(figsize=(15,10))
    plt.imshow(img)
    
    print(notesText)

if __name__=="__main__":
    main()