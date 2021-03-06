import cv2
import pickle

'''
refresh :  0
confirm :  1
lowestprice : 2
time :  3
'''

def get_target(filename):
    return cv2.imread(filename,0)  ##灰度模式打开


refresh = get_target('refresh.png')
confirm = get_target('confirm.bmp')
lowestprice = get_target('lowestprice.bmp')
time = get_target('time.bmp')
firstprice = get_target('firstprice.png')
firstprice_moni = get_target('firstprice_moni.png')

target = [refresh, confirm, lowestprice, time, firstprice, firstprice_moni]



with  open("target.tkl", 'wb') as t:
    pickle.dump(target, t)

