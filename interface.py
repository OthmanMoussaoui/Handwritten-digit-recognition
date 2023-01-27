# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:49:02 2022

@author: otman
"""


import cv2
import numpy as np
from tkinter import *
from PIL import Image,ImageDraw,ImageGrab,ImageTk
from keras.models import load_model

def clear_widget(): 
    global cv # To clear a canvas 
    cv.delete("all") 
def activate_event(event): 
    global lastx, lasty # <81-Motion> 
    cv.bind('<B1-Motion>', draw_lines) 
    lastx, lasty = event.x, event.y 
def draw_lines(event): 
    global lastx, lasty
    x, y = event.x, event.y
    # do the canvas drawings 
    cv.create_line((lastx, lasty, x, y),width=8, fill='black', capstyle=ROUND, smooth=TRUE, splinesteps=12) 
    lastx, lasty = x, y 
def Recognize_Digit(): 
    global image_number 
    predictions = []
    percentage = []
    #image_number = 0 
    filename = f'image (image number).png' 
    widget=cv 
# get the widget coordinates 
    x=root.winfo_rootx()+widget.winfo_x() 
    y=root.winfo_rooty()+widget.winfo_y() 
    x1=x+widget.winfo_width() 
    y1=y+widget.winfo_height() 
#grab the image, crop it according to my requirement and saved it in png format 
    ImageGrab.grab().crop((x,y,x1,y1)).save(filename) 

# read the image in color format 
    image = cv2.imread(filename, cv2.IMREAD_COLOR) 
    # convert the image in grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    # applying Otsu thresholding 
    ret,th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # findContour() function helps in extracting the contours from the image. 
    contours= cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] 


    for cnt in contours: 
        # Get bounding box and extract ROI 
        x,y,w,h = cv2.boundingRect(cnt) 
        # Create rectangle 
        cv2.rectangle(image, (x,y), (x+w, y+h), (127,0,255), 2) 
        top = int(0.05 * th.shape[0]) 
        bottom = top 
        left = int(0.05 * th.shape[1]) 
        right = left
        th_up = cv2.copyMakeBorder(th, top, bottom, left, right, cv2.BORDER_REPLICATE)
        #Extract the image ROI 
        roi= th[y-top:y+h+bottom, x-left:x+w+right] 
        # resize roi image to 28x28 pixels 
        img = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA) 
        #reshaping the image to support our model input 
        img = img.reshape(1,28,28,1) 
        #normalizing the image to support our model input 
        img = img/255.0 
        #its time to predict the result 
        pred = model.predict([img])[0] 
        #numpy.argmax(input array) Returns the indices of the maximum values. 
        final_pred = np.argmax(pred) 
        data = str(final_pred) +' '+ str(int(max(pred)*100))+'%' 
        #cv2.putText() method is used to draw a text string on image. 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        fontScale = 0.7
        color = (255, 20, 0) 
        thickness = 1
        cv2.putText(image, data, (x,y-5), font, fontScale, color, thickness)
        
# Showing the predicted results on new window. cv2.imshow('image., image) cv2.waitKey(0) 
    # cv2.imshow('the results Recognition_ENSAB',image)
    # cv2.waitKey(0)
    cv2.imwrite("newimage1.png", image)
    

# Create the main window
    lk = Toplevel()
    lk.resizable(0,0)
# Set the window title
    lk.title("The results")
    # ima=ImageTk.PhotoImage(Image.open(image))

    # Create a Label widget and set its image attribute to the PhotoImage object
    

# Save the image to a file
    

# Load the image using cv2
    
   
# Convert the image to a PhotoImage object
    image=ImageTk.PhotoImage(Image.open("newimage1.png"))
    # Use the grid geometry manager to place the label in the top-left corner of the window
    label = Label(lk, image=image)
    label.grid(row=2, column=0,sticky='nsew')
    
    lbl = Label(lk, text="The results are:", font=("Tekton Pro", 10))
    lbl.grid(column=0, row=1,sticky='nsew')
    lbl.config(justify='center')

    # # Use the anchor option to center the label within the cell
   

    im=ImageTk.PhotoImage(Image.open("logo-ensa-berrechid.png"))

    # Create a Label widget and set its image attribute to the PhotoImage object
    labeln = Label(lk, image=im)

    # Use the grid geometry manager to place the label in the top-left corner of the window
    labeln.grid(row=0, column=0,sticky='')
    labeln.config(justify='center')

    #☺thanks text 
    lbn = Label(lk, text="Thank you for testing ☺ hope you enjoy it ", font=("Tekton Pro", 10))
    lbn.grid(column=0, row=3,sticky='nsew')
    lbn.config(justify='center')
# Run the Tkinter event loop
    lk.mainloop()

#'C:\Users\otman\Downloads\train_model.h5'
#'C:\Users\otman\Bureau\etudes\s7\python\softmax_digit_classification-master\softmax_digit_classification-master\digit_classification.h5'
model = load_model(r'train_model.h5')
print('model load goood time for app')
#create a main window first (named as root). 
root = Tk()
#Toplevel(),Tk()

root.resizable(0,0)
root.title("Recognition_ENSAB") 
#Initialize few variables 
lastx, lasty = None, None 
image_number = 0 
#create a canvas for drawing 
lbl = Label(root, text="Hello this is an app to recognize Handwriting Numbers", font=("Tekton Pro", 10))
lbl.grid(column=0, row=1,sticky='nsew')
lbl.config(justify='center')

# Use the anchor option to center the label within the cell
lbl.config(anchor='center')
root.columnconfigure(0, weight=1)

image=ImageTk.PhotoImage(Image.open("logo-ensa-berrechid.png"))

# Create a Label widget and set its image attribute to the PhotoImage object
label = Label(root, image=image)

# Use the grid geometry manager to place the label in the top-left corner of the window
label.grid(row=0, column=0,sticky='')
label.config(justify='center')

# Use the anchor option to center the label within the cell
label.config(anchor='center')
root.columnconfigure(0, weight=1)

cv = Canvas(root, width=500, height=500, bg='white')
cv.grid(row=2, column=0, pady=0, sticky='nsew', columnspan=2 ) 
#Tkinter provides a powerful mechanism to let you deal with events yourself.
cv.bind('<Button-1>', activate_event)
#Add Buttons and Labels 
lbl = Label(root, text="by Othman Moussaoui", font=("Tekton Pro", 10))
lbl.grid(column=0, row=3,sticky='nsew')
lbl = Label(root, text="Supervised by Pr:Lahcen MOUMOUN", font=('Helvetica' , 10,'bold'))
lbl.grid(column=0, row=4,sticky='nsew')
btn_save = Button(root,text="Recognize Digit", command=Recognize_Digit)
btn_save.grid(row=5, column=0, pady=1, padx=100,sticky='e') 
button_clear = Button(root,text = "Clear Widget", command = clear_widget) 
button_clear.grid(row=5, column=0, pady=1, padx=100,sticky='w') 
#mainloop() is used when your application is ready to run. 
root.mainloop() 

