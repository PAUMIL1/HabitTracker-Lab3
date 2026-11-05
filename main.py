import tkinter as tk
from tkinter import messagebox, ttk


class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер привычек и водного баланса")
        self.root.geometry("620x700")
        self.goal_ml = 2000
        self.water_ml = 0
        self.habits = [
            {"title": "Прогулка", "done": False},
            {"title": "Чтение", "done": False},
        ]
        self._create_menu()
        self._create_widgets()
        self._update_water()

    def _create_menu(self):
        menu = tk.Menu(self.root)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Сбросить день", command=self._reset_day)
        file_menu.add_separator()
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
        self.resize_enabled = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(
            label="Разрешить менять размер", variable=self.resize_enabled,
            command=self._toggle_resizable,
        )
        menu.add_cascade(label="Вид", menu=view_menu)

        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label="О программе", command=self._show_about)
        menu.add_cascade(label="Справка", menu=help_menu)
        self.root.config(menu=menu)
    def _create_widgets(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        goal = ttk.LabelFrame(main, text="Дневная цель", padding=10)
        goal.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(goal, text="Цель (мл):").pack(side=tk.LEFT)
        self.goal_entry = ttk.Entry(goal, width=10)
        self.goal_entry.insert(0, str(self.goal_ml))
        self.goal_entry.pack(side=tk.LEFT, padx=6)
        ttk.Button(goal, text="Задать цель", command=self._set_goal).pack(
            side=tk.LEFT
        )

        water = ttk.LabelFrame(main, text="Водный баланс", padding=10)
        water.pack(fill=tk.X, pady=(0, 10))
        self.water_status = ttk.Label(water, text="")
        self.water_status.pack(anchor=tk.W, pady=(0, 8))
        self.progress = ttk.Progressbar(water, maximum=100)
        self.progress.pack(fill=tk.X, pady=(0, 10))

        buttons = ttk.Frame(water)
        buttons.pack(fill=tk.X, pady=(0, 8))
        for amount in (150, 250, 500):
            ttk.Button(
                buttons, text=f"+{amount} мл",
                command=lambda value=amount: self._add_water(value),
            ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

        custom = ttk.Frame(water)
        custom.pack(fill=tk.X)
        ttk.Label(custom, text="Свой объём (мл):").pack(side=tk.LEFT)
        self.water_entry = ttk.Entry(custom, width=10)
        self.water_entry.pack(side=tk.LEFT, padx=6)
        ttk.Button(custom, text="Добавить", command=self._add_water).pack(
            side=tk.LEFT
        )

        habits = ttk.LabelFrame(main, text="Привычки на сегодня", padding=10)
        habits.pack(fill=tk.BOTH, expand=True)
        add_row = ttk.Frame(habits)
        add_row.pack(fill=tk.X, pady=(0, 8))
        self.habit_entry = ttk.Entry(add_row)
        self.habit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(add_row, text="Добавить", command=self._add_habit).pack(
            side=tk.LEFT, padx=(6, 0)
        )
        list_frame = ttk.Frame(habits)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self.habit_list = tk.Listbox(list_frame, height=6)
        scroll = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.habit_list.yview
        )
        self.habit_list.configure(yscrollcommand=scroll.set)
        self.habit_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        actions = ttk.Frame(habits)
        actions.pack(fill=tk.X)
        ttk.Button(
            actions, text="Выполнено / не выполнено",
            command=self._toggle_habit,
        ).pack(side=tk.LEFT)
        ttk.Button(
            actions, text="Удалить", command=self._delete_habit
        ).pack(side=tk.RIGHT)
        self._update_habits()

    def _set_goal(self):
        try:
            goal = int(self.goal_entry.get().strip())
            if goal <= 0:
                raise ValueError("Цель должна быть больше нуля.")
            self.goal_ml = goal
            self._update_water()
        except ValueError as error:
            messagebox.showerror("Некорректная цель", str(error))

    def _add_water(self, amount=None):
        try:
            is_custom = amount is None
            value = int(self.water_entry.get().strip()) if is_custom else amount
            if value <= 0:
                raise ValueError("Введите положительное число миллилитров.")
            self.water_ml += value
            if is_custom:
                self.water_entry.delete(0, tk.END)
            self._update_water()
        except ValueError as error:
            messagebox.showerror("Некорректный объём", str(error))

    def _update_water(self):
        percent = min(100, int(self.water_ml * 100 / max(self.goal_ml, 1)))
        self.water_status.config(
            text=f"Выпито: {self.water_ml} / {self.goal_ml} мл ({percent}%)"
        )
        self.progress["value"] = percent

    def _add_habit(self):
        title = self.habit_entry.get().strip()
        if not title:
            messagebox.showwarning("Привычка", "Введите название.")
            return
        self.habits.append({"title": title, "done": False})
        self.habit_entry.delete(0, tk.END)
        self._update_habits()

    def _selected_habit_index(self):
        selection = self.habit_list.curselection()
        if not selection:
            raise IndexError("Сначала выберите привычку в списке.")
        return selection[0]

    def _toggle_habit(self):
        try:
            index = self._selected_habit_index()
            self.habits[index]["done"] = not self.habits[index]["done"]
            self._update_habits()
            self.habit_list.selection_set(index)
        except IndexError as error:
            messagebox.showwarning("Привычка не выбрана", str(error))

    def _delete_habit(self):
        try:
            self.habits.pop(self._selected_habit_index())
            self._update_habits()
        except IndexError as error:
            messagebox.showwarning("Привычка не выбрана", str(error))

    def _update_habits(self):
        self.habit_list.delete(0, tk.END)
        for habit in self.habits:
            mark = "[x]" if habit["done"] else "[ ]"
            self.habit_list.insert(
                tk.END, f"{mark} {habit['title']}"
            )

    def _set_size(self, width, height):
        self.root.geometry(f"{width}x{height}")

    def _toggle_resizable(self):
        allowed = self.resize_enabled.get()
        self.root.resizable(allowed, allowed)

    def _reset_day(self):
        confirmed = messagebox.askyesno(
            "Сбросить день", "Обнулить воду и отметки привычек?"
        )
        if not confirmed:
            return
        self.water_ml = 0
        for habit in self.habits:
            habit["done"] = False
        self._update_water()
        self._update_habits()

    def _show_about(self):
        messagebox.showinfo(
            "О программе",
            "Трекер привычек и водного баланса.\nЛабораторная работа №3.",
        )


if __name__ == "__main__":
    window = tk.Tk()
    HabitTrackerApp(window)
    window.mainloop()
