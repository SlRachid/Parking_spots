import numpy
import os
import tensorflow as tf
import numpy as np

from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as k
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from keras_vggface import utils
import sklearn
from zipfile import ZipFile
import joblib
import gzip
import shutil


files_train = 0
files_validation = 0

cwd = os.getcwd()
# on définit le dossier sur lequel le modèle va s'entraîner
folder = '../data/Train_data/train'
for sub_folder in os.listdir(folder):
    path, dirs, files = next(os.walk(os.path.join(folder, sub_folder)))
    files_train += len(files)

# on définit le dossier sur lequel le modèle va se tester
folder = '../data/Train_data/test'
for sub_folder in os.listdir(folder):
    path, dirs, files = next(os.walk(os.path.join(folder, sub_folder)))
    files_validation += len(files)


img_width, img_height = 48, 48
train_data_dir = "../data/Train_data/train"
validation_data_dir = "../data/Train_data/test"
nb_train_samples = files_train
nb_validation_samples = files_validation
batch_size = 32
epochs = 15
num_classes = 2

model = applications.VGG16(
    weights="imagenet", include_top=False, input_shape=(img_width, img_height, 3))
# On gèle les couches qu'on ne veut pas entraîner. Ici, on gèle les 10 premières couches.
for layer in model.layers[:10]:
    layer.trainable = False


x = model.output
x = Flatten()(x)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
predictions = Dense(num_classes, activation="softmax")(x)

# Création du modèle final
model_final = Model(model.input, predictions)

# Compilation du modèle
model_final.compile(loss="categorical_crossentropy",
                    optimizer=optimizers.SGD(learning_rate=0.0001, momentum=0.9),
                    metrics=["accuracy"])  # See learning rate is very low


# Initiate the train and test generators with data Augumentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    fill_mode="nearest",
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5)


test_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    fill_mode="nearest",
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical")

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_height, img_width),
    class_mode="categorical")


# Save the model according to the conditions
checkpoint = ModelCheckpoint("./trained_model/car.h5", monitor='val_acc', verbose=1,
                             save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0,
                      patience=10, verbose=1, mode='auto')


# Start training!
'''history_object = model_final.fit_generator(
  train_generator, epochs=3, validation_data=validation_generator, callbacks=[checkpoint, early])'''


# Save the model 
'''joblib.dump(model_final, 'trained_model.pkl')'''

# Compress the model file
'''with open('trained_model.pkl', 'rb') as f_in:
    with gzip.open('trained_model.pkl.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
'''
# Clean up: Remove the uncompressed model file if needed
# Optional, depends on whether you want to keep the uncompressed file

'''os.remove('trained_model.pkl')'''

with gzip.open('trained_model.pkl.gz', 'rb') as f_in:
    with open('trained_model.pkl', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Load the model
restored_keras_model = joblib.load('trained_model.pkl')

os.remove('trained_model.pkl')




def pred(img_url):
    img = tf.keras.utils.load_img(img_url, target_size=(48, 48))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = utils.preprocess_input(x, version=1)

    preds = restored_keras_model.predict(x)
    predictions = list(preds[0])
   
    if predictions[0] > predictions[1]:
        return "empty"
    return "occupied"


#parcours un dossier et retourne les predictions pour chaque place dans le dossier
def pred_folder(fold_url):
    places=[]
    for img_url in os.listdir(fold_url):
            places.append((img_url[:-4],pred(fold_url+'/'+img_url)))
    return places

#C'est juste une representation de donnees adaptee au site
def final(pred_res,coord_rectangles):
    occupied=[]
    empty=[]
    for pred in pred_res:
        x = pred[0]
        for rect in coord_rectangles:
            if x == rect[2]:  # pour identifier chaque spot aux coordonnees correctes
                D={}
                Y =[pred[0],pred[1],rect[0]] # le Y caracterise un spot sous forme [indice,statut,pos_rectangles]
                D['id'],D['statut'],D['rectangle']=Y[0],Y[1],Y[2]
                if Y[1]=="empty":

                    empty.append(D)
                else :
                    occupied.append(D)
    return [empty,occupied]




if __name__ == "__main__":
    folder = '../data/test_data'

    for img_url in os.listdir(folder)[:14]:
        print((img_url, pred('../data/test_data/'+img_url)))
