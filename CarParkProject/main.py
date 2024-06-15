import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
        pos_list = pickle.load(f)
width,height = 107,48

def check_Parking_space(image_process):
    space_Counter = 0
    for pos in pos_list:
        x,y = pos
        
        imgCrop = image_process[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1, thickness=2, offset=0, colorR=(0,0,255))

        if count < 800:
            color = (0, 255, 0)
            tickness = 5
            space_Counter+=1
        else:
            color = (0, 0, 255) 
            tickness = 2
        
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,tickness)

    cvzone.putTextRect(img,f'Free Spaces: {space_Counter}/{len(pos_list)}',(80,40),scale=3, thickness=3, offset=0,colorR=(0,50,0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5) 
    kernel =np.ones((3,3), np.int8)
    imgDialate =  cv2.dilate(imgMedian, kernel , iterations=1)
    
    check_Parking_space(imgDialate)
    # for pos in pos_list:
        
    cv2.imshow("Image",img)
    cv2.imshow("ImageBlur",imgBlur)
    cv2.imshow("Imagethres",imgMedian)
    if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to quit the loop
        break