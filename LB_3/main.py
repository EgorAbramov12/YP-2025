import pygame
import math

# Констант
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (173, 216, 230)
BUNNY_COLOR = (245, 245, 245)
OUTLINE_COLOR = (40, 40, 40)
EAR_INNER_COLOR = (255, 205, 210)
EYE_COLOR = (30, 30, 30)
NOSE_COLOR = (255, 175, 175)
WHISKER_COLOR = (80, 80, 80)
SHADOW_COLOR = (200, 200, 200, 50)
MOUTH_COLOR = (100, 100, 100)

# Пропорции
BODY_WIDTH = 280
BODY_HEIGHT = 380
HEAD_RADIUS = 100
EAR_LENGTH = 160
EAR_WIDTH = 50


def draw_outlined_ellipse(surface, color, rect, outline_width):
    pygame.draw.ellipse(surface, OUTLINE_COLOR, rect.inflate(outline_width * 2, outline_width * 2))
    pygame.draw.ellipse(surface, color, rect)


def draw_outlined_circle(surface, color, center, radius, outline_width):
    pygame.draw.circle(surface, OUTLINE_COLOR, center, radius + outline_width)
    pygame.draw.circle(surface, color, center, radius)


def draw_bunny(surface):
    def draw_shadow():
        shadow_surface = pygame.Surface((400, 200), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, SHADOW_COLOR, (0, 0, 400, 100))
        surface.blit(shadow_surface, (center_x - 200, center_y + 150))

    def draw_body():
        body_rect = pygame.Rect(
            center_x - BODY_WIDTH // 2,
            center_y - BODY_HEIGHT // 3,
            BODY_WIDTH,
            BODY_HEIGHT
        )
        draw_outlined_ellipse(surface, BUNNY_COLOR, body_rect, outline_width)

    def draw_hind_legs():
        for x, y, w, h in [
            (center_x - BODY_WIDTH * 0.45, center_y + BODY_HEIGHT * 0.4, 140, 240),
            (center_x + BODY_WIDTH * 0.45 - 140, center_y + BODY_HEIGHT * 0.4, 140, 240)
        ]:
            leg_rect = pygame.Rect(x, y, w, h)
            draw_outlined_ellipse(surface, BUNNY_COLOR, leg_rect, outline_width)

    def draw_front_legs():
        for x, y, w, h in [
            (center_x - BODY_WIDTH * 0.32, center_y + BODY_HEIGHT * 0.15, 100, 220),
            (center_x + BODY_WIDTH * 0.32 - 100, center_y + BODY_HEIGHT * 0.15, 100, 220)
        ]:
            arm_rect = pygame.Rect(x, y, w, h)
            draw_outlined_ellipse(surface, BUNNY_COLOR, arm_rect, outline_width)

            for i in range(3):
                finger_rect = pygame.Rect(
                    arm_rect.x + 20 + i * 25,
                    arm_rect.bottom - 40,
                    20,
                    60
                )
                draw_outlined_ellipse(surface, BUNNY_COLOR, finger_rect, 1)

    def draw_head():
        draw_outlined_circle(surface, BUNNY_COLOR, head_center, HEAD_RADIUS, outline_width)

    def draw_ears():
        for side in [-1, 1]:
            ear_base_x = head_center[0] + side * HEAD_RADIUS * 0.4
            ear_base_y = head_center[1] - HEAD_RADIUS * 0.9

            ear_rect = pygame.Rect(
                ear_base_x - EAR_WIDTH // 2,
                ear_base_y - EAR_LENGTH,
                EAR_WIDTH,
                EAR_LENGTH
            )
            draw_outlined_ellipse(surface, BUNNY_COLOR, ear_rect, outline_width)

            inner_ear_rect = ear_rect.inflate(-10, -40)
            inner_ear_rect.y += 20
            pygame.draw.ellipse(surface, EAR_INNER_COLOR, inner_ear_rect)

    def draw_eyes():
        for x_offset in [-50, 50]:
            eye_pos = (head_center[0] + x_offset, eye_y_position)
            draw_outlined_circle(surface, (255, 255, 255), eye_pos, 25, outline_width)
            pygame.draw.circle(surface, EYE_COLOR, eye_pos, 15)
            pygame.draw.circle(surface, (0, 0, 0), eye_pos, 7)
            pygame.draw.circle(surface, (255, 255, 255), (eye_pos[0] + 8, eye_pos[1] - 8), 4)

    def draw_nose():
        pygame.draw.polygon(surface, OUTLINE_COLOR, nose_points)
        pygame.draw.polygon(surface, NOSE_COLOR, [
            (head_center[0], eye_y_position + 62),
            (head_center[0] - 22, eye_y_position + 88),
            (head_center[0] + 22, eye_y_position + 88)
        ])

    def draw_mouth():
        pygame.draw.arc(surface, MOUTH_COLOR, mouth_rect, math.pi * 0.7, math.pi * 1.3, 3)

    def draw_whiskers():
        for side in [-1, 1]:
            base_x = head_center[0] + side * 35
            base_y = eye_y_position + 85
            for angle in range(-30, 40, 10):
                rad_angle = math.radians(angle)
                length = 50 + abs(angle) * 2
                end_x = base_x + side * length * math.cos(rad_angle)
                end_y = base_y + length * math.sin(rad_angle)
                pygame.draw.line(surface, WHISKER_COLOR, (base_x, base_y), (end_x, end_y), 2)

    def draw_tail():
        draw_outlined_circle(surface, BUNNY_COLOR, tail_center, 45, outline_width)
        for i in range(20):
            angle = math.radians(i * 18)
            px = tail_center[0] + 35 * math.cos(angle)
            py = tail_center[1] + 35 * math.sin(angle)
            pygame.draw.line(surface, OUTLINE_COLOR, (px, py), (px + 10 * math.cos(angle), py + 10 * math.sin(angle)),
                             2)

    # Основная логика рисования
    center_x = WINDOW_WIDTH // 2
    center_y = WINDOW_HEIGHT // 2 + 50
    outline_width = 3
    head_center = (center_x, center_y - BODY_HEIGHT * 0.3)
    eye_y_position = head_center[1] - 40
    nose_points = [
        (head_center[0], eye_y_position + 60),
        (head_center[0] - 25, eye_y_position + 90),
        (head_center[0] + 25, eye_y_position + 90)
    ]
    mouth_rect = pygame.Rect(
        head_center[0] - 20,
        eye_y_position + 100,
        40,
        30
    )
    tail_center = (center_x + 180, center_y + 120)

    # Порядок отрисовки элементов
    draw_shadow()
    draw_body()
    draw_hind_legs()
    draw_front_legs()
    draw_head()
    draw_ears()
    draw_eyes()
    draw_nose()
    draw_mouth()
    draw_whiskers()
    draw_tail()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Bunny with Mouth")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        draw_bunny(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()