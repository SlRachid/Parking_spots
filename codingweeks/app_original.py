from flask import Flask, render_template, Response,request ,make_response, flash, redirect, url_for, render_template
#from data import GetTodoList
import os
import cv2
import numpy as np
#import traitement as tr
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import pickle
import main as pm
import select_rectangles as rm
import urllib.request
from werkzeug.utils import secure_filename
import cv2
import pickle


if not os.path.exists('./new_data/'):
        os.mkdir('./new_data/')
app = Flask(__name__ , static_url_path='/static')
image_folder= os.path.join('static','images')
app.config['Gal_FOLDER'] = image_folder




 
UPLOAD_FOLDER = 'static/uploads/'
DOWNLOAD_FOLDER = 'static/downloads/'


app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
#cette partie pour montrer comment lier a une camera but supplementaire
# camera=cv2.VideoCapture(0)

# def generate_frames():
#     while True:
            
#         ## read the camera frame
#         success,frame=camera.read()
#         if not success:
#             break
#         else:
#             ret,buffer=cv2.imencode('.jpg',frame)
#             frame=buffer.tobytes()

#         yield(b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def home():
    return render_template('home.html')
# Index
@app.route('/Contact')
def about():
    return render_template('contact.html')

#site de services de drivers

@app.route('/drivers')
def drivers():
    return render_template('drivers.html')

#site de services de owners

@app.route('/owners')
def owners():
    return render_template('owners.html')

#site pour la detection des spots 

@app.route('/owner_action',methods=['GET','POST'])
def owner_action():
    
    return render_template('owner_action.html')




(rectW,rectH)=(55,120)
#la fonction pour telecharger l'image du parking vide

@app.route('/upload', methods=['POST','GET'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], 'parking_vide.jpg')
        file.save(save_location)
        
        flash('Image successfully uploaded, processed and displayed below')
        f_n="processed"+filename
        return render_template('upload.html', filename=filename) 

    
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
#la partie qui affiche l'image du parking vide

@app.route('/image1')
def image1():
    img = cv2.imread('./static/uploads/parking_vide.jpg')
    ret, jpeg = cv2.imencode('.jpeg', img)
    response = make_response(jpeg.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response 


#afficher la fenetre pour selectionner les spots

@app.route('/image')
def image():
    global poslist
    poslist = rm.pos_rectangles('./static/uploads/parking_vide.jpg')
    img = cv2.imread('./static/images/parking_spots.jpg')
    ret, jpeg = cv2.imencode('.jpeg', img)
    response = make_response(jpeg.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response 

#apres la selection des spots  les position des top left corners est stocke  dans le cache on la recupere 
try:
    with open('carparkposition', 'rb') as f:
            poslist = pickle.load(f)
except :
    poslist=[]
#just pour alleger l'ecriture

L = poslist


#on importe la data classifie, ceci apres la detection des spots libres sous la forme [data_empty,data_occupied]
#et les deux contiennent des dictionnaires decrivant un spot ayant pour cles id,statut,rectangle(position du top left)

Data= pm.main("./static/uploads/parking_rempli.jpg",L,55,120,14)

#la page qui affiche les spots disponibles

#Data = GetTodoList()

@app.route('/driver_action',methods=['GET','POST'])
def driver_action():
    
    return render_template('Driver_action.html')
    #return render_template('drivers_action_video.html', Data=Data)







#puisqu'on n'a pas lie le site a une camera on utilise ici un boutton upload pour telecharger une image representant l'image a un instant qlq

@app.route('/', methods=['POST','GET'])
def upload_image1():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        
        filename = secure_filename(file.filename)
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], 'parking_rempli.jpg')
        file.save(save_location)
        output_image = rm.labels(save_location,L,14)
   
        cv2.imwrite(os.path.join(app.config['DOWNLOAD_FOLDER'], "processed"+filename),output_image)   
        print(output_image.shape)
        flash('Image successfully uploaded, processed and displayed below')
        f_n="processed"+filename
        
        return render_template('upload1.html', filename=f_n, Data=Data[0])
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


# #display de l'image rempli qui est donne apres upload en y donnant les coordonnees des spots
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='downloads/' + filename), code=301)









# #ici on fai appaitre le video
# @app.route('/video')
# def video():
#    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')







if __name__ == '__main__':
    app.run(debug = True)
