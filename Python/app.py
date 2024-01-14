import cv2
import pygame

# QR-Code Size Adjustment in %
height_scale, width_scale = 0.17, 0.17

pygame.init()
width, height = 1024, 600  # Set your desired HDMI display resolution with width and height swapped
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Webcam Stream")

# Open the webcam
cap = cv2.VideoCapture(0)  # 0 for the default camera (if it's the only camera connected)

# Load images and fonts
#QR Code image
image1 = pygame.image.load("madeirax3.png")  # Load your image
font = pygame.font.Font(None, 36)  # Choose a font and font size

def adjust_image(image, height_scale, width_scale):
    # Resize the image
    new_width = int(image.get_width() * width_scale)
    new_height = int(image.get_height() * height_scale)
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    return resized_image

running = True  # Add this to control the main loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert OpenCV image to RGB format
    frame = cv2.flip(frame, 1)  # Mirror the frame if needed
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    pygame_frame = pygame.surfarray.make_surface(frame)

    display.blit(pygame_frame, (200, 100))  # Display the webcam stream

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
