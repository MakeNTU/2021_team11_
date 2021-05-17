import cv2

def cv2_init(frame_width, frame_height):
  cap = cv2.VideoCapture(-1)
  # 0 : default為筆電的鏡頭
  # 1 : USBcamera2
  # 2 ：USBcamera3 以此類推
  # -1：代表最新插入的USBdevice
  #Check whether user selected camera is opened successfully.

#   if not (cap.isOpened()):
#       print('Could not open video device')
#   else:
#       print('Video device opened')

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

  return cap
