from subprocess import call
import cv2

filename = "codejam_matrox_2023_noisy"

command = f"mp4box"
call([command]+ f"-add {filename}.h264 {filename}.mp4".split(" "), shell=True)
print("vid conv")


video_capture = cv2.VideoCapture(filename+'.mp4')

if not video_capture.isOpened():
    print("error opening file")
    exit()

fps = video_capture.get(cv2.CAP_PROP_FPS)
frame_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

output_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size, isColor=True)


while True:
    # Read a frame from the video file
    ret, frame = video_capture.read()

    # Break the loop if the video has ended
    if not ret:
        break

    # Apply median blur to the frame
    blurred_frame = cv2.medianBlur(frame, ksize=5)  # You can adjust the kernel size as needed

    # Write the blurred frame to the output video
    output_video.write(blurred_frame)

video_capture.release()
output_video.release()