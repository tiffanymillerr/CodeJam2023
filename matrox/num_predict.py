
import cv2
from google.cloud import vision
client = vision.ImageAnnotatorClient()

cap = cv2.VideoCapture('output_video.mp4')
allTexts = []
fi = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    fi += 1

    _, img_buffer = cv2.imencode('.jpg', frame)


    content = img_buffer.tobytes()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        continue

    texts = response.text_annotations
    for text in texts[:-1]:
        allTexts.append(text.description)

    if fi >= 8: break

print(allTexts)