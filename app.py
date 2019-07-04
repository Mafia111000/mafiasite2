#from __future__ import division,print_function'''
from flask import Flask,render_template,url_for
from flask import request

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image  
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/path/to/the/uploads'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''
def fil(f):
    
    basepath=os.path.dirname(__file__)
    file_path=os.path.join(basepath,"uploads",secure_filename(f.secure_filename))
    f.save(file_path)
    return file_path'''

   
    
   


@app.route('/',methods=['GET'])
def upload_file():
    return render_template("home.html")
    
@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        f=request.files['file']
        basepath=os.path.dirname(__file__)
        
        file_path=os.path.join(basepath,"uploads",secure_filename(f.filename))
        f.save(file_path)
        print(f.filename, file_path)
        img_path=file_path
        img =image.load_img(img_path, target_size=(224, 224))
        model = ResNet50(weights='imagenet')
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        my_prediction=decode_predictions(preds, top=6)[0]
        return render_template('result.html',prediction = my_prediction,filename=f.filename)


if __name__ == '__main__':
    app.run(debug=True)





