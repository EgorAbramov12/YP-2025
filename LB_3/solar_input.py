# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet, Satellite
from solar_model import PhysicsModel
import math
import numpy as np


class SpaceObjectReader:
    """Класс для чтения/записи данных о космических объектах"""

    def __init__(self):
        self.orbit_cache = {}
        self.orbit_group_counter = 0

    def read_space_objects_data_from_file(self, input_filename):
        """Считывает данные из файла с распределением на орбитах"""
        objects = []
        current_star = None
        current_planet = None
        orbit_groups = {}

        # Чтение объектов из файла
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                if not line.strip() or line.startswith('#'):
                    continue

                parts = line.split()
                obj_type = parts[0].lower()

                if obj_type == "star":
                    obj = Star()
                    self._parse_parameters(parts, obj)
                    objects.append(obj)
                    current_star = obj
                    current_planet = None

                elif obj_type == "planet":
                    obj = Planet()
                    self._parse_parameters(parts, obj)
                    objects.append(obj)
                    obj.central_body = current_star
                    current_planet = obj

                elif obj_type == "satellite":
                    obj = Satellite()
                    self._parse_parameters(parts, obj)
                    objects.append(obj)
                    obj.central_body = current_planet

                else:
                    print(f"Unknown space object: {obj_type}")

        # Рассчитываем орбитальные параметры
        self._calculate_orbital_parameters(objects)
        return objects

    def _calculate_orbital_parameters(self, objects):
        """Вычисляет орбитальные параметры с предотвращением столкновений"""
        G = PhysicsModel.gravitational_constant
        orbit_groups = {}
        orbit_radii = {}

        # Группировка объектов по центральным телам и радиусам
        for obj in objects:
            if obj.central_body is None:
                continue

            dx = obj.x - obj.central_body.x
            dy = obj.y - obj.central_body.y
            base_radius = math.sqrt(dx ** 2 + dy ** 2)

            # Создаем уникальный радиус для предотвращения столкновений
            unique_radius = self._get_unique_radius(orbit_radii, obj.central_body, base_radius)
            obj.orbit_radius = unique_radius

            # Группируем объекты по орбитам
            orbit_key = (obj.central_body, round(unique_radius, -9))
            if orbit_key not in orbit_groups:
                orbit_groups[orbit_key] = []
            orbit_groups[orbit_key].append(obj)

        # Расчет параметров орбит
        for (central, radius), group in orbit_groups.items():
            group_size = len(group)
            angular_velocity = math.sqrt(G * central.m / radius ** 3)

            # Распределение объектов на орбите
            for i, obj in enumerate(group):
                phase = i * (2 * math.pi / group_size)
                obj.orbit_phase = phase
                obj.angular_velocity = angular_velocity

                # Расчет начальной позиции
                obj.x = central.x + radius * math.cos(phase)
                obj.y = central.y + radius * math.sin(phase)

                # Расчет начальной скорости
                V = angular_velocity * radius
                obj.Vx = central.Vx - V * math.sin(phase)
                obj.Vy = central.Vy + V * math.cos(phase)

    def _get_unique_radius(self, orbit_radii, central_body, base_radius):
        """Генерирует уникальный радиус орбиты для предотвращения столкновений"""
        key = id(central_body)
        if key not in orbit_radii:
            orbit_radii[key] = {}

        # Поиск ближайшего свободного радиуса
        radius = base_radius
        step = 1e9  # Шаг 1000 км
        safety_margin = 5e9  # Минимальное расстояние между орбитами

        while True:
            # Проверяем, свободен ли текущий радиус
            radius_free = True
            for r in orbit_radii[key].keys():
                if abs(r - radius) < safety_margin:
                    radius_free = False
                    break

            if radius_free:
                orbit_radii[key][radius] = True
                return radius

            # Пробуем следующий радиус
            radius += step

    def _parse_parameters(self, parts, obj):
        """Парсит параметры объекта"""
        if len(parts) < 8:
            raise ValueError("Invalid parameters count")
        obj.R = float(parts[1])
        obj.color = parts[2]
        obj.m = float(parts[3])
        obj.x = float(parts[4])
        obj.y = float(parts[5])
        obj.Vx = float(parts[6])
        obj.Vy = float(parts[7])

    def write_space_objects_data_to_file(self, output_filename, space_objects):
        """Сохраняет данные в файл"""
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            for obj in space_objects:
                line = f"{obj.type.capitalize()} {obj.R} {obj.color} {obj.m:.6E} "
                line += f"{obj.x:.6E} {obj.y:.6E} {obj.Vx:.6E} {obj.Vy:.6E}\n"
                out_file.write(line)