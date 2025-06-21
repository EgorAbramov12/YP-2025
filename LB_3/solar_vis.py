# coding: utf-8
# license: GPLv3

import tkinter

class SpaceVisualizer:
    """Класс для визуализации космических объектов"""
    header_font = "Arial-16"
    window_width = 1500
    window_height = 800

    def __init__(self):
        self.scale_factor = None
        self.space_canvas = None
        self.orbit_lines = {}
        self.show_orbits = False
        self.min_scale = 1e-10
        self.max_scale = 1e10
        self.offset_x = 0
        self.offset_y = 0
        self.last_drag_x = 0
        self.last_drag_y = 0
        self.is_dragging = False

    def calculate_scale_factor(self, max_distance):
        """Вычисляет масштабный коэффициент"""
        self.scale_factor = 0.4 * min(self.window_height, self.window_width) / max_distance

    def scale_x(self, x):
        """Преобразует x-координату с учетом смещения"""
        return int((x + self.offset_x) * self.scale_factor) + self.window_width // 2

    def scale_y(self, y):
        """Преобразует y-координату с учетом смещения"""
        return self.window_height // 2 - int((y + self.offset_y) * self.scale_factor)

    def create_star_image(self, star):
        """Создает изображение звезды"""
        x = self.scale_x(star.x)
        y = self.scale_y(star.y)
        r = star.R
        star.image = self.space_canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=star.color
        )

    def create_planet_image(self, planet):
        """Создает изображение планеты"""
        x = self.scale_x(planet.x)
        y = self.scale_y(planet.y)
        r = max(planet.R, 3)
        planet.image = self.space_canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=planet.color
        )
        if planet not in self.orbit_lines:
            self.orbit_lines[planet] = []

    def create_satellite_image(self, satellite):
        """Создает изображение спутника"""
        x = self.scale_x(satellite.x)
        y = self.scale_y(satellite.y)
        r = max(satellite.R, 2)
        satellite.image = self.space_canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=satellite.color
        )
        if satellite not in self.orbit_lines:
            self.orbit_lines[satellite] = []

    def update_object_position(self, body):
        """Обновляет позицию объекта на холсте"""
        if body.type == 'planet':
            r = max(body.R, 3)
        elif body.type == 'satellite':
            r = max(body.R, 2)
        else:
            r = body.R

        x = self.scale_x(body.x)
        y = self.scale_y(body.y)

        if (x + r < 0 or x - r > self.window_width or
                y + r < 0 or y - r > self.window_height):
            # Объект за пределами экрана
            self.space_canvas.coords(
                body.image,
                self.window_width + r,
                self.window_height + r,
                self.window_width + 2 * r,
                self.window_height + 2 * r
            )
        else:
            self.space_canvas.coords(
                body.image,
                x - r, y - r, x + r, y + r
            )

        # Обновление орбиты для планет и спутников
        if (body.type == 'planet' or body.type == 'satellite') and self.show_orbits:
            if body in self.orbit_lines:
                orbit_points = self.orbit_lines[body]
                orbit_points.append((x, y))

                if len(orbit_points) > 1000:
                    orbit_points.pop(0)

                if len(orbit_points) >= 2:
                    if hasattr(body, 'orbit_id'):
                        self.space_canvas.delete(body.orbit_id)
                    body.orbit_id = self.space_canvas.create_line(
                        *[coord for point in orbit_points for coord in point],
                        fill="white", width=1, tags="orbit"
                    )

    def clear_orbits(self):
        """Очищает все орбиты"""
        for obj in list(self.orbit_lines.keys()):
            if hasattr(obj, 'orbit_id'):
                self.space_canvas.delete(obj.orbit_id)
                del obj.orbit_id
            self.orbit_lines[obj] = []

    def toggle_orbits(self, show):
        """Включает/выключает отображение орбит"""
        self.show_orbits = show
        if not show:
            self.clear_orbits()

    def set_canvas(self, canvas):
        """Устанавливает холст для рисования"""
        self.space_canvas = canvas

    def handle_zoom(self, event, space_objects):
        """Обрабатывает масштабирование колесиком мыши"""
        if event.num == 4:
            zoom_factor = 1.1
        elif event.num == 5:
            zoom_factor = 0.9
        else:
            zoom_factor = 1.1 if event.delta > 0 else 0.9

        new_scale = self.scale_factor * zoom_factor
        if new_scale < self.min_scale:
            new_scale = self.min_scale
        elif new_scale > self.max_scale:
            new_scale = self.max_scale

        self.scale_factor = new_scale

        for body in space_objects:
            self.update_object_position(body)

        self.clear_orbits()

    def start_drag(self, event):
        """Начало перемещения (панорамирования)"""
        self.last_drag_x = event.x
        self.last_drag_y = event.y
        self.is_dragging = True
        self.space_canvas.config(cursor="fleur")

    def do_drag(self, event, space_objects):
        """Обработка перемещения мыши при зажатой кнопке"""
        if not self.is_dragging:
            return

        dx = event.x - self.last_drag_x
        dy = event.y - self.last_drag_y

        self.last_drag_x = event.x
        self.last_drag_y = event.y

        self.offset_x += dx / self.scale_factor
        self.offset_y -= dy / self.scale_factor

        for body in space_objects:
            self.update_object_position(body)

        if self.show_orbits:
            self.clear_orbits()
            for body in space_objects:
                if body.type == 'planet' or body.type == 'satellite':
                    self.orbit_lines[body] = []