from flask import Flask, render_template, Response,request,session
import os
from werkzeug.utils import secure_filename
from mycode import join_images

UPLOAD_FOLDER=os.path.join('static','uploads')
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key="this is first time"
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/result')
def res():
    return render_template("result.html")
@app.route('/result',methods=['POST','GET'])
def result():
    if request.method == 'POST':
        print(request.files)
        left_image=request.files['left_file']
        right_image=request.files['right_file']
        left_image_file_name=secure_filename(left_image.filename)
        right_image_file_name=secure_filename(right_image.filename)
        left_image.save(os.path.join(app.config['UPLOAD_FOLDER'], left_image_file_name))
        right_image.save(os.path.join(app.config['UPLOAD_FOLDER'],right_image_file_name))
        session['left_uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], left_image_file_name)
        session['right_uploaded_img_file_path']= os.path.join(app.config['UPLOAD_FOLDER'], right_image_file_name)

        
        left_image_file_path=session.get("left_uploaded_img_file_path",None)
        right_image_file_path=session.get("right_uploaded_img_file_path",None)
        output_image_file_path=os.path.join(app.config['UPLOAD_FOLDER'],"output.jpg")
        join_images(left_image_file_path,right_image_file_path,output_image_file_path)
        return render_template("result.html",user_image=output_image_file_path)
if __name__=='__main__':
    app.run(host='0.0.0.0',port = 5000,debug=False)
