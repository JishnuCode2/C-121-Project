import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_tips =[8, 12, 16, 20]
thumb_tip= 4

def count_fingers(image,hand_landmarks,hand_no=0):
    if hand_landmarks:
        landmarks = hand_landmarks[hand_no].landmark
        h,w,c = image.shape

        finger_fold_status = []

        for lm in finger_tips:
          f_tip_x = landmarks[lm].x
          f_bottom_x = landmarks[lm-2].x
          f_y = landmarks[lm].y
          if f_tip_x > f_bottom_x:
             finger_fold_status.append(f_y)  

        print(finger_fold_status)

        if len(finger_fold_status) == 4:  
          tip_y = landmarks[thumb_tip].y
          mid_y = landmarks[thumb_tip-1].y
          bottom_y = landmarks[thumb_tip - 2].y
          u_finger_y = finger_fold_status[0]*h
          b_finger_y = finger_fold_status[3]*h
          if u_finger_y > b_finger_y and tip_y > mid_y > bottom_y:
             cv2.putText(img,'DISLIKE',(20,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)     
          elif  b_finger_y > u_finger_y and tip_y < mid_y < bottom_y:
             cv2.putText(img,'LIKE',(20,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
        
    cv2.putText(img,'PLEASE USE RIGHT HAND',(20,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

          
 
      


        
          



def draw_landmarks(image,hand_landmarks):
  if hand_landmarks:
     for landmark in hand_landmarks:
        mp_draw.draw_landmarks(
            image,landmark,mp_hands.HAND_CONNECTIONS, 
            mp_draw.DrawingSpec((0,0,255),4,2),
            mp_draw.DrawingSpec((0,255,0),4,2)
        )

                




while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    results = hands.process(img)
    landmarks = results.multi_hand_landmarks

    draw_landmarks(img,landmarks)
    count_fingers(img,landmarks)
    cv2.imshow("hand tracking", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()