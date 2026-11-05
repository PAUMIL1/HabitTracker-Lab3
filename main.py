import tkinter as tk
from tkinter import ttk


class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер привычек и водного баланса")
        self.root.geometry("620x700")
        self.goal_ml = 2000
        self.water_ml = 0
        self._create_menu()
        self._create_widgets()
        self._update_water()

    def _create_menu(self):
        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Выход", command=self.root.destroy)
        menu.add_cascade(label="Файл", menu=file_menu)

        view_menu = tk.Menu(menu, tearoff=False)
        view_menu.add_command(
            label="Компактное окно", command=lambda: self._set_size(540, 660)
        )
        view_menu.add_command(
            label="Обычное окно", command=lambda: self._set_size(620, 700)
        )
        view_menu.add_command(
            label="Широкое окно", command=lambda: self._set_size(760, 800)
        )
        menu.add_cascade(label="Вид", menu=view_menu)
        self.root.config(menu=menu)

    def _create_widgets(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        water = ttk.LabelFrame(main, text="Водный баланс", padding=10)
        water.pack(fill=tk.X, pady=(0, 10))
        self.water_status = ttk.Label(water, text="")
        self.water_status.pack(anchor=tk.W, pady=(0, 8))

        buttons = ttk.Frame(water)
        buttons.pack(fill=tk.X)
        for amount in (150, 250, 500):
            ttk.Button(
                buttons, text=f"+{amount} мл",
                command=lambda value=amount: self._add_water(value),
            ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        ttk.Label(
            main, text="Список привычек добавим на следующем этапе."
        ).pack(anchor=tk.W, pady=8)

    def _add_water(self, amount):
        self.water_ml += amount
        self._update_water()

    def _update_water(self):
        self.water_status.config(
            text=f"Выпито: {self.water_ml} / {self.goal_ml} мл"
        )

    def _set_size(self, width, height):
        self.root.geometry(f"{width}x{height}")


if __name__ == "__main__":
    window = tk.Tk()
    HabitTrackerApp(window)
    window.mainloop()
