import pygame
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Angry Emoji")

# Цвета
gray = (200, 200, 200)
yellow = (255, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

# Координаты и размеры
face_x = width // 2
face_y = height // 2
face_radius = 200
eye_radius = 30
eye_distance = 90
mouth_width = 200
mouth_height = 50
eyebrow_length = 250
eyebrow_thickness = 25
eyebrow_angle = -40  # Угол наклона бровей
eyebrow_length1 = 170
eyebrow_thickness1 = 25
eyebrow_angle1 = -40  # Поменял знак, чтобы бровь наклонялась в другую сторону


# Функция для рисования бровей
def draw_eyebrow(x, y, length, thickness, angle):
    # Преобразование угла в радианы
    angle_rad = math.radians(angle)

    # Вычисление координат начала и конца линии
    x1 = x - (length / 2) * math.cos(angle_rad)
    y1 = y - (length / 2) * math.sin(angle_rad)
    x2 = x + (length / 2) * math.cos(angle_rad)
    y2 = y + (length / 2) * math.sin(angle_rad)

    pygame.draw.line(screen, black, (x1, y1), (x2, y2), thickness)


# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заполнение фона
    screen.fill(gray)

    # Рисуем лицо
    pygame.draw.circle(screen, yellow, (face_x, face_y), face_radius, 0)
    pygame.draw.circle(screen, black, (face_x, face_y), face_radius, 3)  # Контур лица

    # Рисуем глаза
    pygame.draw.circle(screen, red, (face_x - eye_distance, face_y - 50), eye_radius + 5, 0)
    pygame.draw.circle(screen, black, (face_x - eye_distance, face_y - 50), eye_radius + 5, 3)  # Контур глаза

    pygame.draw.circle(screen, red, (face_x + eye_distance, face_y - 50), eye_radius - 5, 0)
    pygame.draw.circle(screen, black, (face_x + eye_distance, face_y - 50), eye_radius - 5, 3)  # Контур глаза

    pygame.draw.circle(screen, black, (face_x - eye_distance, face_y - 50), eye_radius // 2, 0)
    pygame.draw.circle(screen, black, (face_x + eye_distance, face_y - 50), eye_radius // 2, 0)

    # Рисуем рот
    pygame.draw.rect(screen, black, (face_x - mouth_width / 2, face_y + 80, mouth_width, mouth_height))

    # Рисуем брови
    draw_eyebrow(face_x - eye_distance , face_y - 105, eyebrow_length, eyebrow_thickness, -eyebrow_angle)  # Левая бровь
    draw_eyebrow(face_x + eye_distance, face_y - 90, eyebrow_length1, eyebrow_thickness1, eyebrow_angle1)  # Правая бровь

    # Обновление экрана
    pygame.display.flip()

# Выход из Pygame
pygame.quit()
