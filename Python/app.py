import cv2
import pygame
import sys
import av
import numpy as np


def adjust_image(image, height_scale, width_scale):
    # Resize the image
    new_width = int(image.get_width() * width_scale)
    new_height = int(image.get_height() * height_scale)
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    return resized_image


if __name__ == '__main__':
    # QR-Code Size Adjustment in %
    height_scale, width_scale = 0.17, 0.17

    pygame.init()
    width, height = 1280, 720  # Set your desired HDMI display resolution with width and height swapped
    display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

    # Open the webcam
    cap = cv2.VideoCapture(0)  # 0 for the default camera (if it's the only camera connected)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Create an H.264 encoder using PyAV
    encoder = av.codec.CodecContext.create('h264', 'w')

    # Load images and fonts
    # QR Code image
    image1 = pygame.image.load("madeirax3.png")  # Load your image
    font = pygame.font.Font(None, 36)  # Choose a font and font size

    running = True  # Add this to control the main loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to a format suitable for encoding
        av_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
        # Convert the frame to 'rgb24' format
        rgb_frame = av_frame.to_ndarray(format='rgb24')

        # Display the resulting rgb_frame

        # Rotate the frame 90 degrees counterclockwise
        rotated_frame = np.rot90(rgb_frame, k=1)

        pygame_frame = pygame.surfarray.make_surface(rotated_frame)

        display.blit(pygame_frame, (300, 100))  # Display the webcam stream

        # Adjust the image
        adjusted_image = adjust_image(image1, height_scale, width_scale)

        # Display the adjusted image
        display.blit(adjusted_image, (100, 100))

        # Display text
        text = font.render("Hello, World!", True, (255, 255, 255))
        display.blit(text, (250, 400))

        pygame.display.flip()

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()