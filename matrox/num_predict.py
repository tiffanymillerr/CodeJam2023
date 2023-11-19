
import cv2
from google.cloud import vision
client = vision.ImageAnnotatorClient()


filename = "codejam_matrox_2023_noisy"

cap = cv2.VideoCapture(f'{filename}_denoised.mp4')

fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

output_grayscale = cv2.VideoWriter(f'{filename}_grayscale.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size, isColor=True)
output_contrast = cv2.VideoWriter(f'{filename}_contrast.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size, isColor=True)

allTexts = []
fi = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    fi += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output_grayscale.write(gray)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_output = clahe.apply(gray)
    output_contrast.write(clahe_output)

    _, img_buffer = cv2.imencode('.jpg', clahe_output)


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