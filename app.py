from flask import Flask, request
import re
import cv2
import base64
from PIL import Image
import pytesseract
from pytesseract import Output

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    # im = request.form['book_name']
    # print(im)
    return "Team-Nowshik"

@app.route('/conImage',methods = ['POST'])
def conImage():
    if request.method == 'POST':
        im = request.form['image']
        text= request.form['book_name']
        pattern=list(text.split(" "))
        print(pattern)
        found=False
        imgb=bytes(im, 'ascii')
        img_bytes = base64.decodebytes(imgb)
        with open('input.jpg', 'wb') as ip:
            ip.write(img_bytes)
        img = cv2.imread('input.jpg')
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        keys = list(d.keys())
        print(d)
        n_boxes = len(d['text'])
        print(n_boxes)
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                for j in pattern:
                    if re.match(j.lower(), d['text'][i].lower()):
                        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        found=True
        cv2.imwrite('intr.jpg', img)
        # Specified
        Original_Image = Image.open("intr.jpg")

        # Rotate Image By 270 Degree
        rotated_image1 = Original_Image.rotate(270)
        rotated_image1.save("output.jpg")
        encoded_string=''
        if(found==True):
            with open("output.jpg", "rb") as op:
                encoded_string = base64.b64encode(op.read())
        else:
            with open("notfound.jpg", "rb") as op:
                encoded_string = base64.b64encode(op.read())
        return ""+str(encoded_string,'utf-8')


@app.route('/conImageAll',methods = ['POST'])
def conImageAll():
    if request.method == 'POST':
        im = request.form['image']
        text= request.form['book_name']
        pattern=list(text.split(" "))
        print(im)
        found=False
        imgb=bytes(im, 'ascii')
        img_bytes = base64.decodebytes(imgb)
        with open('input.jpg', 'wb') as ip:
            ip.write(img_bytes)
        img = cv2.imread('input.jpg')
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        keys = list(d.keys())
        print(d)
        n_boxes = len(d['text'])
        print(n_boxes)
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                found=True
        cv2.imwrite('output.jpg', img)
        encoded_string=''
        if(found==True):
            with open("output.jpg", "rb") as op:
                encoded_string = base64.b64encode(op.read())
        else:
            with open("notfound.jpg", "rb") as op:
                encoded_string = base64.b64encode(op.read())
        return ""+str(encoded_string,'utf-8')


@app.route('/conImageStat',methods = ['POST'])
def conImageStat():
    if request.method == 'POST':
        im = request.form['image']
        text= request.form['book_name']
        pattern = list(text.split(" "))
        print(im)
        imgb = bytes(im, 'ascii')
        img_bytes = base64.decodebytes(imgb)
        with open('input.jpg', 'wb') as ip:
            ip.write(img_bytes)
        img = cv2.imread('input.jpg')
        encoded_string=''
        with open("output.jpg", "rb") as op:
            encoded_string = base64.b64encode(op.read())
        return ""+str(encoded_string,'utf-8')



if __name__ == '__main__':
   app.run(host='0.0.0.0')