import os
import hashlib
import cv2
import traceback
import numpy as np

def draw_text(text,size=2):
    img=np.zeros((82,218,3),dtype=np.uint8)
    img[:]=255
    cv2.putText(img,text,(0,70),cv2.FONT_HERSHEY_SIMPLEX,size,(0,0,255),2)
    return img

def input_num(img,pre=None):
    data=[]
    if (pre is not None) and (len(pre)==5):
        data=[ord(i) for i in pre]
    else:
        pre=''
    cv2.namedWindow('show_picture')
    num_img=draw_text(pre)
    result=cv2.vconcat([img,num_img])
    cv2.imshow('show_picture',result)
    input_char=cv2.waitKey() #enter=13; backspace=8;1=49;
    while not((input_char==13 and len(data)==5) or input_char==27):
        if input_char==8: #backspace
            del data[-1]
        else:
            data.append(input_char)
        text=''
        for char in data:
            text+=chr(char)
        num_img=draw_text(text)
        show_img=cv2.vconcat([img,num_img])
        cv2.imshow('show_picture',show_img)
        input_char=cv2.waitKey()
    cv2.destroyAllWindows()
    result=''
    for char in data:
        result+=chr(char)
    return result

if __name__ == "__main__":
    for root, dirs, files in os.walk('./data'):
        for file_name in files:
            try:
                img=cv2.imread(root+'/'+file_name)
                try:
                    label=os.path.splitext(file_name)[0].split('_')[-1]
                except:
                    label=''
                result=input_num(img,label)
            except Exception as e:
                cv2.destroyAllWindows()
                traceback.print_exc()
                continue
            with open(root+'/'+file_name,'rb') as f:
                md5=hashlib.md5(f.read())
            hash_short=md5.hexdigest()[:6]
            os.rename(root+'/'+file_name,root+'/{}_{}.jpg'.format(hash_short,result))