import crop as cr
import select_rectangles as rm
import main as pm
import detection_de_voitures as sr
import pickle
import os

try:
    with open('carparkposition', 'rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []


def test():
    L = poslist
    
    cr.part_final('./static/uploads/parking_rempli.jpg',L,55,120,14)
    assert len(rm.pos_rectangles('./static/uploads/parking_rempli.jpg')) == 4
    print('oui1')
    assert len(os.listdir('./new_data')) == 4
    print('oui2')
    cr.crop_rec([(204, 179), (259, 299), "BA3_0"], './static/uploads/parking_rempli.jpg')
    assert len(os.listdir('./new_data')) == 5
    print('oui3')




if __name__ == '__main__':

    test()
