import cv2
import pickle
import keyboard
import string
# insérer la longueur et la largeur de chacun des rectangles délimitant les places du parking
rectW = 55
rectH = 120

try:
    with open('carparkposition', 'rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []  # on définit une liste des différentes positions des rectangles qui délimitent les places du parking


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # si l'évènement de la souris est un clic gauche
        # on ajoute le couple définissant la position du rectangle à la liste
        poslist.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:  # si l'évènement de la souris est un clic droit
        for i, pos in enumerate(poslist):
            x1, y1 = pos
            # si on clique quelque part à l'intérieur de l'un des rectangles enregistrés
            if x1 < x < x1+rectW and y1 < y < y1+rectH:
                # le rectangle sélectionné est éliminé de la liste
                poslist.pop(i)
    with open('carparkposition', 'wb') as f:
        pickle.dump(poslist, f)


def test(imgurl):
    # tant qu'on ne clique pas sur echap, l'image reste ouverte.
    while keyboard.is_pressed("x") == False:
        img = cv2.imread(imgurl)
        # k = len(poslist)//n  # nb_de_lignes
        for index, pos in enumerate(poslist):
            cv2.rectangle(
                img, pos, (pos[0]+rectW, pos[1]+rectH), (0, 0, 255), 2)

        cv2.imshow('image', img)
    # cette fonction sert à gérer les évènements qui accompagnent un clic, notamment dans notre cas un ajout ou une suppression d'un couple de la liste.
        cv2.setMouseCallback('image', mouseClick)
        cv2.waitKey(1)
    cv2.imwrite('./static/images/parking_spots.jpg',img)

# dessiner des rectangles modélisant les places du parking


def labels(imgurl, poslist, nb_colonnes):  # nb_colonnes est le nombre de colonnes du parking,
    # on suppose qu'il est fixe i.e toutes les lignes contiennent le même nombre de colonnes.
    img = cv2.imread(imgurl)
    L = string.ascii_uppercase
    for index, pos in enumerate(poslist):
        p = index//nb_colonnes
        cv2.rectangle(img, pos, (pos[0]+rectW, pos[1]+rectH), (0, 0, 255), 2)
        # dessiner des rectangles modélisant les places du parking
        p = index//nb_colonnes
        cv2.putText(img=img, text=L[p]+str(index % nb_colonnes), org=(pos[0], pos[1]),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0), thickness=1)
    return img


def pos_rectangles(imgurl):
    test(imgurl)
    # on retourne la liste des couples qui définissent le top left de chaque rectangle dessiné i.e de chaque place du parking.
    return poslist


# # determine le nombre de colonnes du parking à partir de la selection des spots
# def nbr_colonnes(poslist):
#     # on suppose que toutes les lignes du parking ont le même nombre de colonnes
#     # sur la première ligne, les abcisses des points de postlist sont croissants, on commence par le premier point de la première ligne
#     x = poslist[0][0]
#     c = 1  # compte le nombre de colonnes
#     for i in range(1, len(poslist)):
#         if x < poslist[i][0]:  # tant que les x sont croissants, on est sur la même ligne
#             x = poslist[i][0]
#             c += 1
#         else:
#             return c  # dès que les x décroissent, on est déplacé à une nouvelle ligne, on arrête alors la boucle
