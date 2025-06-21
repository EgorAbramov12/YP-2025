# coding: utf-8
# license: GPLv3

from solar_objects import SpaceObject
import math


class PhysicsModel:
    """Класс математической модели системы"""
    gravitational_constant = 6.67408E-11
    collision_check_interval = 5  # Проверять столкновения каждые 5 шагов
    grid_size = 2e12  # Размер ячейки пространственной сетки

    def __init__(self):
        self.space_objects = []
        self.step_count = 0
        self.spatial_grid = {}

    def recalculate_positions(self, dt):
        """Пересчитывает позиции всех объектов"""
        # Обновляем позиции
        for body in self.space_objects:
            body.update_position(dt)

        # Периодическая проверка столкновений
        self.step_count += 1
        if self.step_count % self.collision_check_interval == 0:
            self._build_spatial_grid()
            self._check_collisions()

    def _build_spatial_grid(self):
        """Строит пространственную сетку для оптимизации"""
        self.spatial_grid = {}
        for obj in self.space_objects:
            # Определяем ячейку сетки для объекта
            grid_x = int(obj.x / self.grid_size)
            grid_y = int(obj.y / self.grid_size)
            cell_key = (grid_x, grid_y)

            if cell_key not in self.spatial_grid:
                self.spatial_grid[cell_key] = []
            self.spatial_grid[cell_key].append(obj)
            obj.grid_cell = cell_key

    def _check_collisions(self):
        """Проверяет столкновения с использованием пространственной сетки"""
        processed_pairs = set()

        for cell_key, objects in self.spatial_grid.items():
            # Проверяем объекты внутри ячейки
            self._check_objects_in_cell(objects, processed_pairs)

            # Проверяем соседние ячейки
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    neighbor_key = (cell_key[0] + dx, cell_key[1] + dy)
                    if neighbor_key in self.spatial_grid:
                        self._check_objects_between_cells(objects, self.spatial_grid[neighbor_key], processed_pairs)

    def _check_objects_in_cell(self, objects, processed_pairs):
        """Проверяет столкновения внутри одной ячейки"""
        n = len(objects)
        for i in range(n):
            obj1 = objects[i]
            for j in range(i + 1, n):
                obj2 = objects[j]
                pair_key = (min(id(obj1), id(obj2)), max(id(obj1), id(obj2)))
                if pair_key in processed_pairs:
                    continue

                processed_pairs.add(pair_key)
                self._resolve_collision(obj1, obj2)

    def _check_objects_between_cells(self, cell1, cell2, processed_pairs):
        """Проверяет столкновения между двумя ячейками"""
        for obj1 in cell1:
            for obj2 in cell2:
                pair_key = (min(id(obj1), id(obj2)), max(id(obj1), id(obj2)))
                if pair_key in processed_pairs:
                    continue

                processed_pairs.add(pair_key)
                self._resolve_collision(obj1, obj2)

    def _resolve_collision(self, obj1, obj2):
        """Разрешает потенциальные столкновения"""
        dx = obj1.x - obj2.x
        dy = obj1.y - obj2.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        min_distance = obj1.safety_radius + obj2.safety_radius

        if distance < min_distance:
            # Корректируем позиции объектов
            correction = (min_distance - distance) / 2
            angle = math.atan2(dy, dx) if distance > 0 else 0

            # Сдвигаем оба объекта
            obj1.x += correction * math.cos(angle)
            obj1.y += correction * math.sin(angle)
            obj2.x -= correction * math.cos(angle)
            obj2.y -= correction * math.sin(angle)

            # Обновляем орбитальные параметры
            self._adjust_orbit(obj1)
            self._adjust_orbit(obj2)

    def _adjust_orbit(self, obj):
        """Корректирует орбитальные параметры после сдвига"""
        if obj.central_body:
            dx = obj.x - obj.central_body.x
            dy = obj.y - obj.central_body.y
            new_radius = math.sqrt(dx ** 2 + dy ** 2)

            # Сохраняем относительную фазу
            current_angle = math.atan2(dy, dx)
            obj.orbit_phase = current_angle - obj.orbit_angle

            # Обновляем параметры орбиты
            obj.orbit_radius = new_radius
            obj.angular_velocity = math.sqrt(
                self.gravitational_constant * obj.central_body.m / new_radius ** 3
            )