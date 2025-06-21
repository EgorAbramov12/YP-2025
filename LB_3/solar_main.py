# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from solar_vis import SpaceVisualizer
from solar_model import PhysicsModel
from solar_input import SpaceObjectReader

class SolarSystemApp:
    """Главный класс приложения"""

    def __init__(self):
        self.perform_execution = False
        self.physical_time = 0
        self.model = PhysicsModel()
        self.visualizer = SpaceVisualizer()
        self.reader = SpaceObjectReader()
        self.displayed_time = None
        self.time_step = None
        self.time_speed = None
        self.start_button = None
        self.orbits_button = None
        self.root = None
        self.show_orbits = False

    def execution(self):
        """Основной цикл выполнения"""
        if not self.perform_execution:
            return

        self.model.recalculate_positions(self.time_step.get())
        for body in self.model.space_objects:
            self.visualizer.update_object_position(body)

        self.physical_time += self.time_step.get()
        self.displayed_time.set(f"{self.physical_time:.1f} seconds gone")

        if self.perform_execution:
            self.root.after(101 - int(self.time_speed.get()), self.execution)

    def start_execution(self):
        """Запуск симуляции"""
        self.perform_execution = True
        self.start_button.config(text="Pause", command=self.stop_execution)
        self.execution()

    def stop_execution(self):
        """Остановка симуляции"""
        self.perform_execution = False
        self.start_button.config(text="Start", command=self.start_execution)

    def open_file_dialog(self):
        """Открытие файла с системой"""
        self.perform_execution = False
        if self.start_button:
            self.start_button.config(text="Start", command=self.start_execution)

        for obj in self.model.space_objects:
            self.visualizer.space_canvas.delete(obj.image)
            if hasattr(obj, 'orbit_id'):
                self.visualizer.space_canvas.delete(obj.orbit_id)

        filename = askopenfilename(filetypes=(("Text file", ".txt"),))
        if not filename:
            return

        self.model.space_objects = self.reader.read_space_objects_data_from_file(filename)
        max_distance = max(max(abs(obj.x), abs(obj.y)) for obj in self.model.space_objects) or 1
        self.visualizer.calculate_scale_factor(max_distance)
        self.visualizer.offset_x = 0
        self.visualizer.offset_y = 0

        for obj in self.model.space_objects:
            if obj.type == 'star':
                self.visualizer.create_star_image(obj)
            elif obj.type == 'planet':
                self.visualizer.create_planet_image(obj)
            elif obj.type == 'satellite':
                self.visualizer.create_satellite_image(obj)

        self.physical_time = 0
        self.displayed_time.set(f"{self.physical_time:.1f} seconds gone")
        self.visualizer.clear_orbits()

    def save_file_dialog(self):
        """Сохранение текущей системы"""
        filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
        if filename:
            self.reader.write_space_objects_data_to_file(filename, self.model.space_objects)

    def toggle_orbits(self):
        """Переключает отображение орбит"""
        self.show_orbits = not self.show_orbits
        self.visualizer.toggle_orbits(self.show_orbits)
        if self.show_orbits:
            self.orbits_button.config(text="Hide Orbits")
        else:
            self.orbits_button.config(text="Show Orbits")

    def main(self):
        """Запуск главного окна"""
        self.root = tkinter.Tk()
        self.root.title("Solar System Simulation")

        canvas = tkinter.Canvas(
            self.root,
            width=self.visualizer.window_width,
            height=self.visualizer.window_height,
            bg="black"
        )
        canvas.pack(side=tkinter.TOP)
        self.visualizer.set_canvas(canvas)

        default_file = "Bilet 7.1.txt"
        try:
            self.model.space_objects = self.reader.read_space_objects_data_from_file(default_file)
            max_distance = max(max(abs(obj.x), abs(obj.y)) for obj in self.model.space_objects) or 1
            self.visualizer.calculate_scale_factor(max_distance)
            self.visualizer.offset_x = 0
            self.visualizer.offset_y = 0

            for obj in self.model.space_objects:
                if obj.type == 'star':
                    self.visualizer.create_star_image(obj)
                elif obj.type == 'planet':
                    self.visualizer.create_planet_image(obj)
                elif obj.type == 'satellite':
                    self.visualizer.create_satellite_image(obj)
        except FileNotFoundError:
            print(f"Файл {default_file} не найден. Загрузите систему вручную.")
        except Exception as e:
            print(f"Ошибка при загрузке {default_file}: {e}")

        frame = tkinter.Frame(self.root)
        frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.start_button = tkinter.Button(frame, text="Start", command=self.start_execution, width=6)
        self.start_button.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.orbits_button = tkinter.Button(frame, text="Show Orbits", command=self.toggle_orbits)
        self.orbits_button.pack(side=tkinter.LEFT, padx=5, pady=5)

        time_step_label = tkinter.Label(frame, text="Time step:")
        time_step_label.pack(side=tkinter.LEFT, padx=5)

        self.time_step = tkinter.DoubleVar(value=1.0)
        time_step_entry = tkinter.Entry(frame, textvariable=self.time_step, width=8)
        time_step_entry.pack(side=tkinter.LEFT, padx=5)

        speed_label = tkinter.Label(frame, text="Speed:")
        speed_label.pack(side=tkinter.LEFT, padx=5)

        self.time_speed = tkinter.DoubleVar(value=50)
        speed_scale = tkinter.Scale(
            frame, variable=self.time_speed,
            orient=tkinter.HORIZONTAL, from_=1, to=100
        )
        speed_scale.pack(side=tkinter.LEFT, padx=5)

        open_button = tkinter.Button(frame, text="Open file...", command=self.open_file_dialog)
        open_button.pack(side=tkinter.LEFT, padx=5)

        save_button = tkinter.Button(frame, text="Save to file...", command=self.save_file_dialog)
        save_button.pack(side=tkinter.LEFT, padx=5)

        self.displayed_time = tkinter.StringVar()
        self.displayed_time.set("0.0 seconds gone")
        time_label = tkinter.Label(frame, textvariable=self.displayed_time, width=25)
        time_label.pack(side=tkinter.RIGHT, padx=10)

        canvas.bind("<MouseWheel>", lambda event: self.visualizer.handle_zoom(event, self.model.space_objects))
        canvas.bind("<Button-4>", lambda event: self.visualizer.handle_zoom(event, self.model.space_objects))
        canvas.bind("<Button-5>", lambda event: self.visualizer.handle_zoom(event, self.model.space_objects))
        canvas.bind("<ButtonPress-1>", self.visualizer.start_drag)
        canvas.bind("<B1-Motion>", lambda event: self.visualizer.do_drag(event, self.model.space_objects))

        self.root.mainloop()

if __name__ == "__main__":
    app = SolarSystemApp()
    app.main()