import os
import zipfile
import pandas as pd
import cv2

# Initialisation des chemins

chemin_database,chemin_images,chemin_descriptors,chemin_key_points = "./database/","./images/","./descriptors/","./key_points/"
if not os.path.exists(chemin_key_points):  os.mkdir(chemin_key_points)
if not os.path.exists(chemin_descriptors): os.mkdir(chemin_descriptors)
if not os.path.exists(chemin_images):  os.mkdir(chemin_images)

SIFT = cv2.xfeatures2d.SIFT_create()

# extraction des images depuis les fichiers rar
def extract(chemin_database, chemin_images):
    list_zips = os.listdir(chemin_database) 
    list_zips = [x for x in list_zips if ".zip"in x]
    for fichier in list_zips:
        path_to_zip_file = chemin_database + fichier 
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(chemin_images)

# Sauvegarde des descripteurs dans un fichier csv
def descriptors_csv(descriptors, img):
    chem_fichier = chemin_descriptors+ str(img.split('.')[0]) + ".csv"
    df = pd.DataFrame(descriptors)
    df.to_csv(chem_fichier, index= False)

# Sauvegarde des key points dans un fichier csv
def key_points_csv(key_points, img):
    chem_fichier = chemin_key_points + str(img.split('.')[0]) + ".csv"
    df = pd.DataFrame()
    for point in key_points:
        temp = { 
                "point1": point.pt[0],
                "point2":point.pt[1], 
                "size" : point.size, 
                "angle" :point.angle, 
                "response" : point.response, 
                "octave" : point.octave, 
                "id" : point.class_id
                }
        df = df.append(temp, ignore_index= True)
    df.to_csv(chem_fichier, index = False)    

# Extraction des images depuis la base et sauvegarde des key points et descriptors dans des fichiers csv
extract(chemin_database, chemin_images)
list_images = os.listdir(chemin_images)
for pic in list_images:
    print(pic)
    img = cv2.imread(chemin_images+pic)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key_points, descriptors = SIFT.detectAndCompute(gray, None)
    key_points_csv(key_points, pic)
    descriptors_csv(descriptors, pic)