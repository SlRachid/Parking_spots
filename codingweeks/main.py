import select_rectangles as rm
import crop as cr
import detection_de_voitures as sr





def main(imgurl,L,rectW,rectH,nmbr_colonnes):
    
    
    
    cr.part_final(imgurl, L, rectW,rectH, nmbr_colonnes) # cette_partie_crée_un_dossier_avec_les_images_des_spots_du_parking
    folder = './new_data' # le dossier qui contient les images découpées
    places = sr.pred_folder(folder) # retourne le résultat de la prédiction du folder
    coor = cr.coord_rectangles(L,rectW,rectH,nmbr_colonnes) # retourne une liste contenant les coordonnées des rec à découper et leurs labels
    res = sr.final(places,coor) # retourne une liste qui isole les places occupées et les places libres
    return res 

def display(imgurl,L,nbr_colonnes=14):
    return rm.labels(imgurl, L, nbr_colonnes) # affiche la photo du parking avec les rectangles 


if __name__=="__main__":
    L = rm.pos_rectangles('./static/uploads/parking_vide.jpg')
    #print(main("../static/uploads/park.jpeg",L,55,120))


    #Data= main("../static/uploads/parking_rempli.jpg",L,55,120)[0]
    display('./static/uploads/parking_rempli.jpg',L,nbr_colonnes=14)
    #print(Data)




    









