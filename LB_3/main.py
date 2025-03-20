import pygame
import math

# Initialize Pygame
pygame.init()

# Window dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Python is Really Amazing!")

# Colors
white = (255, 255, 255)
skin_color = (255, 204, 153)  # Flesh Tone.
green = (0, 128, 0)  # Dark green
orange = (255, 165, 0)  # Orange shirt color
yellow = (255, 255, 0)  # Hair and shapes color
purple = (128, 0, 128)  # Hair color for the figure
blue = (0, 0, 255)  # Eyes
red = (255, 0, 0)  # Mouth
brown = (139, 69, 19)  # Noses
text_background = (57, 255, 20)  # Bright green.
black = (0, 0, 0)  # Black for outlines and pupils


# Function for Drawing the Figure
def draw_figure(surface, x, y, hair_color, shirt_color, eye_color, triangle_color):

    # Body - Circle
    body_radius = 180
    body_y_offset = 170
    pygame.draw.circle(surface, shirt_color, (x, y + body_y_offset), body_radius)
    pygame.draw.circle(surface, black, (x, y + body_y_offset), body_radius, 2)

    # Shoulders - Pentagons
    shoulder_radius = 40
    shoulder_points_left = []
    shoulder_points_right = []
    for i in range(5):
        angle = i * (2 * math.pi / 5)
        shoulder_x_left = x - 130 + int(shoulder_radius * math.cos(angle))
        shoulder_y_left = y - 100 + body_y_offset + int(shoulder_radius * math.sin(angle))
        shoulder_points_left.append((shoulder_x_left, shoulder_y_left))

        shoulder_x_right = x + 130 + int(shoulder_radius * math.cos(angle))
        shoulder_y_right = y - 100 + body_y_offset + int(shoulder_radius * math.sin(angle))
        shoulder_points_right.append((shoulder_x_right, shoulder_y_right))

    pygame.draw.polygon(surface, shirt_color, shoulder_points_left)
    pygame.draw.polygon(surface, shirt_color, shoulder_points_right)
    pygame.draw.polygon(surface, black, shoulder_points_left, 2)  # Outline
    pygame.draw.polygon(surface, black, shoulder_points_right, 2)  # Outline

    # Head - Circle
    head_radius = 120
    pygame.draw.circle(surface, skin_color, (x, y - 80), head_radius)  # No Outline
    triangle_size = 20

    # Calculate and draw colored triangles
    num_triangles = 10
    for i in range(num_triangles):
        angle = math.pi + (i * (math.pi / (num_triangles - 1)))
        triangle_x = x + head_radius * math.cos(angle)
        triangle_y = y - 80 + head_radius * math.sin(angle)  # Adjust based on y

        # Define triangle vertices
        point1 = (triangle_x, triangle_y - triangle_size)  # Top point of triangle
        point2 = (triangle_x - triangle_size / 2, triangle_y + triangle_size / 2)  # Bottom Left
        point3 = (triangle_x + triangle_size / 2, triangle_y + triangle_size / 2)  # Bottom Right

        pygame.draw.polygon(surface, triangle_color, [point1, point2, point3])  # Triangle filled

    # Eyes
    eye_radius = 15
    pupil_radius = 5
    pygame.draw.circle(surface, eye_color, (x - 40, y - 100), eye_radius)
    pygame.draw.circle(surface, black, (x - 40, y - 100), eye_radius, 2)
    pygame.draw.circle(surface, black, (x - 40, y - 100), pupil_radius)

    pygame.draw.circle(surface, eye_color, (x + 40, y - 100), eye_radius)
    pygame.draw.circle(surface, black, (x + 40, y - 100), eye_radius, 2)
    pygame.draw.circle(surface, black, (x + 40, y - 100), pupil_radius)

    # Nose
    pygame.draw.polygon(surface, brown, [(x - 8, y - 70), (x, y - 60), (x + 8, y - 70)])

    # Mouth
    pygame.draw.polygon(surface, red, [(x - 40, y - 40), (x, y - 20), (x + 40, y - 40)])

    return x, y  # Returning the values

# --- DRAWING HELPERS ----

def draw_arms(x, y, surface):
    body_y_offset = 20
    pygame.draw.line(surface, skin_color, (x - 120, y + 20 + body_y_offset), (x - 200, 50), 15)
    pygame.draw.line(surface, skin_color, (x + 120, y + 20 + body_y_offset), (x + 200, 50), 15)

# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing on to screen
    screen.fill(white)  # White Background

    # Positioning the single figure in the center
    figure_x = width // 2
    figure_y = height // 2

    # Draw the figure
    draw_figure(screen, figure_x, figure_y, yellow, green, (100, 100, 100), purple)  # Single figure with purple triangles

    # Draw arms for the figure
    draw_arms(figure_x, figure_y, screen)

    # Banner + text
    font_size = 50
    font = pygame.font.Font(None, font_size)
    text = font.render("PYTHON is REALLY AMAZING!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(width // 2, 50))
    text_rect.width += 20
    text_rect.height += 10

    pygame.draw.rect(screen, text_background, (0, 0, width, text_rect.height + 40))
    pygame.draw.rect(screen, black, (0, 0, width, text_rect.height + 40), 3)
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()