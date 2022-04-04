from crypt import methods
import os
from string import Template
from flask import Flask,request,send_file,render_template
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
pwd=os.path.dirname(__file__)

# define the save path and extension
UP_LOAD_FOLDER = os.path.join(pwd,'save_file')
ADMIN_UP_LOAD_FOLDER = os.path.join(pwd,'translate_file')
ALLOWED_EXTENSIONS={'txt','pdf','jpg','jpeg','gif','avi','mp3'}
app.config['UP_LOAD_FOLDER']=UP_LOAD_FOLDER
app.config['ADMIN_UP_LOAD_FOLDER']=ADMIN_UP_LOAD_FOLDER
# HOST 需要运行前自行设置
# 之后会设置命令行进行传入
HOST = "127.0.0.1"

PORT = 5000

@app.route('/')
def index():
    """
    return a html page
    :return :
    """
    html=render_template('index.html')
    # html=html.substitute({"HOST":HOST,"PORT":PORT})
    return html

def allowed_file(filename):
    """
    judge the extension of file is allowable
    :param filename
    :return
    
    """
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    """
    upload file to save_file folder

    example:
    with open('url','rb') as file_obj:
        rsp = requests.post("http://10.185.122.97:5000/upload',file={'file':file_obj})
        print(rsp.text)--> file uploaded successfully
    """
    if 'file' not in request.files:
        return "No file port"
    name = request.form.get('nm')
    file = request.files['file']
    if file.filename=='':
        return "No selected file"
    if file and allowed_file(file.filename):
        if name == "admin114514":
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['ADMIN_UP_LOAD_FOLDER'],filename))
            return "UPLOAD SUCCESS"
        else:
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UP_LOAD_FOLDER'],filename))
            return render_template("upload.html",name=name)+"<b><a href = '/preview?fileId={}'>click here for previewing</a></b>".format(filename)
    return "Hello {} , file uploaded Fail\n".format(name)

@app.route("/download")
def download_file():
    """
    下载src_file目录下面的文件
    eg.下载当前目录下面的123.tar 文件,eg:http://localhost:5000/download?fileId=123.tar
    :return:
    """
    file_name = request.args.get('fileId')
    file_path = os.path.join(pwd,'translate_file',file_name)
    if os.path.isfile(file_path):
        return send_file(file_path,as_attachment=True)
    else:
        return "The downloaded file does not exist"

@app.route("/preview")
def preview():
    file_name = request.args.get('fileId')
    file_path = os.path.join(pwd,'translate_file',file_name)
    if os.path.isfile(file_path):
        return render_template("preview.html",file_path=file_path,download_path="/download?fileId={}".format(file_name))
    else:
        return "The file has not been translated, please refresh this site later. Your file:{}".format(file_path)
    

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
