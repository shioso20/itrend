from PIL import Image
import numpy as np
import pyzbar.pyzbar as pyzbar
code=[]
def load_receipt(file):
    image =Image.open(file)
    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        code.append(obj.data)
    return code[0].decode()
