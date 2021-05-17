import cv2
import time
from PIL import Image
import numpy

cap = cv2.VideoCapture(1)
# 0 : default為筆電的鏡頭
# 1 : USBcamera2
# 2 ：USBcamera3 以此類推
# -1：代表最新插入的USBdevice
#Check whether user selected camera is opened successfully.

if not (cap.isOpened()):
	print('Could not open video device')
else:
	print('Video device opened')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

while(True):
  ret, frame = cap.read()

  # 將圖片轉為灰階
  #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  #cv2.imwrite('test.jpg', frame)
  image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)) # convert opencv(frame) to PIL(image)
  img = cv2.cvtColor(numpy.asarray(image),cv2.COLOR_RGB2BGR)


  cv2.imshow('frame', img )

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()