import os
import cv2
import pandas as pd
import numpy as np

# Initialisation des chemins
chemin_images,chemin_descriptors,chemin_key_points,chemin_results = "./images/","./descriptors/","./key_points/","./results/"
if not os.path.exists(chemin_key_points):  os.mkdir(chemin_key_points)
if not os.path.exists(chemin_descriptors): os.mkdir(chemin_descriptors)
if not os.path.exists(chemin_images):  os.mkdir(chemin_images)
if not os.path.exists(chemin_results):  os.mkdir(chemin_results)

sift = cv2.xfeatures2d.SIFT_create()
Eucl = cv2.BFMatcher(cv2.NORM_L2, crossCheck = True)

# Récupérer les desripteurs depuis les fichiers csv déja crées
def get_descriptors(chemin):
    df = pd.read_csv(chemin_descriptors+chemin.split(".")[0]+".csv")
    return np.array(df.values, dtype= "float32")

# Récupérer les key points depuis les fichiers csv déja crées
def get_key_points(chemin):
    df = pd.read_csv(chemin_key_points+chemin.split(".")[0]+".csv")
    keypoint = []
    for i in range(len(df)):
        dic = df.iloc[i]
        
        temp = cv2.KeyPoint(x= float(dic["point1"]),
                            y= float(dic["point2"]),
                            angle = dic["angle"], 
                            size = dic["size"], 
                            octave = int(dic["octave"]), 
                            response = dic['response'], 
                            class_id = int(dic["id"]))
        keypoint.append(temp)
    return keypoint

# Comparer le nouveau iris avec les tout les iris de la base de données
def check(des1): 
    list_images = os.listdir(chemin_images)

    for img in list_images:
        print(img)
        des2 =  get_descriptors(img)

        # Comparaison des iris en utilisant la distance Euclidienne
        matches = Eucl.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        score = len(matches)/ min(len(des1), len(des2))
        if score > 0.97 :
            return 100* score, img, matches
    return 0, "", []

# Dessiner les keypoints
def draw_keys(img, keys,chemin):  
    img = cv2.drawKeypoints(img, keys, None)
    img = cv2.resize(img, (300, 400))
    cv2.imwrite(chemin, img)

# Dessiner le matching entre deux iris
def draw_matches(img1, img2, kp1, kp2, matches):
    end = min(100, len(matches))
    matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:end], None, flags=2)
    matching_result = cv2.resize(matching_result, (400, 400))
    cv2.imwrite(chemin_results + 'matching.png', matching_result)

# La fonction principale qui sera appelée par l'interface
def launcher(url):
    img = cv2.imread(url)
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    print("the image is loaded",)   

    key1, des1 = sift.detectAndCompute(img1, None)
    print("key points and descriptors are extracted from the current image")

    score, img_path, matches = check(des1)
    print("checking is done")

    if score: 
        id_person = int(img_path.split("_")[0][:-1])
        print("the person's id :", id_person)
        
        img2 = cv2.imread(chemin_images + img_path)
        
        key2 = get_key_points(img_path)

        draw_keys(img, key1, chemin_results +"real.png")
        draw_keys(img2, key2, chemin_results + "bdd.png")

        draw_matches(img, img2, key1, key2, matches)
        return (True, id_person, score)
    else:
        
        print("Not in the database")
        return (False, 0, 0)
