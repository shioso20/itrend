import cv2
from pyzbar.pyzbar import decode
codes=[]
def scan_qr():
    cap=cv2.VideoCapture(0)
    cam=True
    while cam==True:
        _,f=cap.read()
        for val in decode(f):
            codes.append(val.data.decode('utf-8'))
        cv2.imshow('scan receipt',f)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return codes
