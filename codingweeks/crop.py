import cv2
from select_rectangles import *
import string
import os


# renvoie une liste dont les éléments sont sous la forme [topleftcorner,bottomrightcorner,label] de chaque rectangle
def coord_rectangles(list, larg, long, nbr_colonnes):
    res = []
    n = nbr_colonnes
    L = string.ascii_uppercase
    for k in range(len(list)):
        (i, j) = list[k]
        p = k//n
        res.append([(i, j), (i+larg, j+long), L[p]+'_'+str(k-p*n)])
    return res


# la liste prise en paramètre a la forme [topleftcorner,bottomrightcorner,label] et enregistre à l'intérieur d'un dossier l'image du rectangle considéré
def crop_rec(list, path):
    
    pt1 = list[:2][0]
    pt2 = list[:2][1]
    k = list[2]
    img = cv2.imread(path)
    img_cropped = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    cv2.imwrite('./new_data/'+k+'.jpg', img_cropped)


# la liste prise en paramètre a la forme de poslist de la fct pos_rectangles du module select_rectangles.
def part_final(path, list, larg, long, nbr_colonnes=14):
    labelisation = coord_rectangles(list, larg, long, nbr_colonnes)
    
    for crop in labelisation:
        # enregistrer dans un dossier les images des différents rectangles ie différentes places du parking
        crop_rec(crop, path)
