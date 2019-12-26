from keras.models import load_model
import os
import numpy as np
from keras.preprocessing import image

# 成功率 55%



def buildmodel():
    mod = load_model('./predict403/All.h5')
    return mod
def pred(img):
    model=buildmodel()
    print(img)
    img = image.load_img(img, target_size=(150,150))
    
    #img = img.rotate(-90)
    img.show()

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    #x = preprocess_input(x)

    result = model.predict(x)
    #print(result)


    Max = 0.0
    for j in result:
        for i, c in enumerate(j):
            if c > Max:
                print(c, Max)
                Max = i
                a = i

    ss=["Timberland","adidas","pierre cardin",'幸福台灣','春水堂']
    print(ss[a])
    return (ss[a])
   