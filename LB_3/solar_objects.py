# coding: utf-8
# license: GPLv3

import math


class SpaceObject:
    """Базовый класс для космических объектов"""
    __slots__ = ('type', 'R', 'color', 'm', 'x', 'y', 'Vx', 'Vy',
                 'image', 'orbit_id', 'central_body', 'orbit_radius',
                 'orbit_angle', 'angular_velocity', 'orbit_phase',
                 'orbit_group', 'grid_cell', 'safety_radius')

    def __init__(self, obj_type, radius=5, color="black", mass=0, x=0, y=0, vx=0, vy=0):
        self.type = obj_type
        self.R = radius
        self.color = color
        self.m = mass
        self.x = x
        self.y = y
        self.Vx = vx
        self.Vy = vy
        self.image = None
        self.orbit_id = None
        self.central_body = None
        self.orbit_radius = 0
        self.orbit_angle = 0
        self.angular_velocity = 0
        self.orbit_phase = 0
        self.orbit_group = None
        self.grid_cell = None
        self.safety_radius = max(1e9, radius * 1000)  # Минимальный безопасный радиус

    def update_position(self, dt):
        """Обновляет позицию объекта по круговой орбите"""
        if self.central_body is None:
            return

        # Кэширование вычислений для оптимизации
        new_angle = self.orbit_angle + self.angular_velocity * dt
        cos_angle = math.cos(new_angle + self.orbit_phase)
        sin_angle = math.sin(new_angle + self.orbit_phase)

        # Рассчитываем новую позицию
        self.x = self.central_body.x + self.orbit_radius * cos_angle
        self.y = self.central_body.y + self.orbit_radius * sin_angle

        # Рассчитываем скорость
        V = self.angular_velocity * self.orbit_radius
        self.Vx = self.central_body.Vx - V * sin_angle
        self.Vy = self.central_body.Vy + V * cos_angle

        # Обновляем угол для следующего шага
        self.orbit_angle = new_angle

    def reset_force(self):
        """Пустой метод для совместимости"""
        pass


class Star(SpaceObject):
    """Класс звезды"""

    def __init__(self, radius=5, color="red", mass=0, x=0, y=0, vx=0, vy=0):
        super().__init__("star", radius, color, mass, x, y, vx, vy)
        self.safety_radius = max(1e10, radius * 10000)  # Больший безопасный радиус для звезд

    def update_position(self, dt):
        """Звезда остается неподвижной"""
        pass


class Planet(SpaceObject):
    """Класс планеты"""

    def __init__(self, radius=5, color="green", mass=0, x=0, y=0, vx=0, vy=0):
        super().__init__("planet", radius, color, mass, x, y, vx, vy)


class Satellite(SpaceObject):
    """Класс спутника"""

    def __init__(self, radius=2, color="gray", mass=0, x=0, y=0, vx=0, vy=0):
        super().__init__("satellite", radius, color, mass, x, y, vx, vy)
        self.safety_radius = max(1e8, radius * 5000)  # Спутники имеют меньший безопасный радиус