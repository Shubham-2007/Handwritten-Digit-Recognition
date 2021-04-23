from keras.models import load_model
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
from PIL import ImageDraw
import cv2

model=load_model("digitdemo1.h5")

def predict_digit(img):
  #resize image to 28x28 pixels
#   img=img.resize((28,28))
  img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
  print(img.size)
  #convert rgb to grayscale
  cv2.imshow('img',img)
  img = img.reshape(1, 28, 28, 1)
  # normalizing the image to support our model input
  img = img / 255.0
#   img=img.convert('L')
#   img=np.array(img)
#   print(img)
  #reshaping to support our model and normalizing
#   img=img.reshape(1,28,28,1)
#   img=img/255.0
#   print(img.size)
#   temp=np.array(img)
#   flat=temp.ravel()
#   print(flat.size)
  #predicting the class
  res=model.predict([img])[0]
  return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
      tk.Tk.__init__(self)
      self.x=self.y=0
      self.image1 = Image.new("RGB", (500, 500), 'white')
      self.draw = ImageDraw.Draw(self.image1)
      #creating elements
      self.Canvas=tk.Canvas(self,width=500,height=500,bg="white",cursor="cross")
      self.classify_btn=tk.Button(self,text="recognise",command=self.classify_handwriting)
      self.button_clear=tk.Button(self,text="Clear",command=self.clear_all)
      self.Canvas.grid(row=0,column=0,columnspan=2)
      self.button_clear.grid(row=1,column=0)
      self.classify_btn.grid(row=1,column=1)
      self.Canvas.bind("<B1-Motion>",self.draw_lines)

    def clear_all(self):
        self.Canvas.delete("all")
        self.draw.rectangle((0, 0, 500, 500), fill='white')

    def classify_handwriting(self):
#         x=self.tk.winfo_rootx()+self.Canvas.winfo_x()
#         y=self.tk.winfo_rooty()+self.Canvas.winfo_y()
#         x1=x+self.Canvas.winfo_width()
#         y1=y+self.Canvas.winfo_height()
#         im=ImageGrab.grab().crop((x,y,x1,y1))
#         HWND=self.Canvas.winfo_id()#to get the handle of the Canvas
#         rec=win32gui.GetWindowRect(HWND)#get the coordinates of the Canvas
#         a,b,c,d = rec
#         print(a,b,c,d)
#         rec=(a,b,c,d)
#         im=ImageGrab.grab(rec)
#         self.image1.show()
        img = np.array(self.image1)
        # convert the image into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # apply thresholding
        ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU)
        # find the contours
        contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cnt in contours:
            # get bounding box and exact region of interest
            x, y, w, h = cv2.boundingRect(cnt)
            # create rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            top = int(0.05 * th.shape[0])
            bottom = top
            left = int(0.05 * th.shape[1])
            right = left
            th_up = cv2.copyMakeBorder(th, top, bottom, left, right, cv2.BORDER_REPLICATE)
            # Extract the image's region of interest
            roi = th[y - top:y + h + bottom, x - left:x + w + right] 
            digit,acc=predict_digit(roi)
            print(digit)
            cv2.destroyAllWindows()

    def draw_lines(self,event):
        self.x=event.x
        self.y=event.y
        r=20
        self.Canvas.create_oval(self.x-r,self.y-r,self.x+r,self.y+r,fill='black')
        self.draw.ellipse([(self.x-r,self.y-r),(self.x+r,self.y+r)],fill='black')

app=App()
mainloop()
