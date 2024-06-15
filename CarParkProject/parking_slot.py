import cv2
import pickle


width,height = 107,48
try:
    with open('CarParkPos','rb') as f:
        pos_list = pickle.load(f)
except:
    pos_list = []


def mouse_click(events,x,y,flag,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(pos_list):
            x1,y1 = pos
            if x1<x1+width and y1<y1+height:
                pos_list.pop(i)
                
    with open('CarParkPos','wb') as f:
        pickle.dump(pos_list, f)

while True:
    img = cv2.imread('carParkImg.png')
    # cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)
    for pos in pos_list:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2) 

    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the loop
        break