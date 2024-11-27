import tkinter as tk
from tkinter import messagebox, filedialog
import time
import pygame
import threading

class ErrorScenarioApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Error Scenario App")
        self.root.geometry("800x600")

        self.scenarios = []
        self.language = "Русский"
        self.hide_during_scenarios = tk.BooleanVar(value=False)
        self.use_sound = tk.BooleanVar(value=False)
        self.selected_sound = None

        self.init_ui()

    def init_ui(self):
        self.language_button = tk.Button(self.root, text="Изменить на English", command=self.toggle_language)
        self.language_button.pack(pady=10)

        self.hide_checkbox = tk.Checkbutton(
            self.root,
            text="Закрывать программу при запуске сценария?",
            variable=self.hide_during_scenarios
        )
        self.hide_checkbox.pack()

        self.sound_checkbox = tk.Checkbutton(
            self.root,
            text="Использовать пользовательский звук?",
            variable=self.use_sound,
            command=self.toggle_sound
        )
        self.sound_checkbox.pack()

        self.select_sound_button = tk.Button(self.root, text="Выбрать звук", command=self.select_sound)
        self.select_sound_button.pack()
        self.select_sound_button.config(state="disabled")

        self.run_button = tk.Button(self.root, text="Запустить сценарии", command=self.run_scenarios)
        self.run_button.pack(pady=20)

        self.scenario_listbox = tk.Listbox(self.root)
        self.scenario_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_scenario_button = tk.Button(self.root, text="Добавить сценарий", command=self.add_scenario)
        self.add_scenario_button.pack(pady=5)

        self.delete_scenario_button = tk.Button(self.root, text="Удалить выбранный сценарий", command=self.delete_scenario)
        self.delete_scenario_button.pack()

    def toggle_language(self):
        if self.language == "Русский":
            self.language = "English"
            self.language_button.config(text="Switch to Russian")
            self.hide_checkbox.config(text="Hide program when running scenarios?")
            self.sound_checkbox.config(text="Use custom sound?")
            self.select_sound_button.config(text="Select Sound")
            self.run_button.config(text="Run Scenarios")
            self.add_scenario_button.config(text="Add Scenario")
            self.delete_scenario_button.config(text="Delete Selected Scenario")
        else:
            self.language = "Русский"
            self.language_button.config(text="Изменить на English")
            self.hide_checkbox.config(text="Закрывать программу при запуске сценария?")
            self.sound_checkbox.config(text="Использовать пользовательский звук?")
            self.select_sound_button.config(text="Выбрать звук")
            self.run_button.config(text="Запустить сценарии")
            self.add_scenario_button.config(text="Добавить сценарий")
            self.delete_scenario_button.config(text="Удалить выбранный сценарий")

    def toggle_sound(self):
        if self.use_sound.get():
            self.select_sound_button.config(state="normal")
        else:
            self.select_sound_button.config(state="disabled")
            self.selected_sound = None

    def select_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            self.selected_sound = file_path

    def play_sound(self):
        if self.selected_sound and self.use_sound.get():
            pygame.mixer.init()
            pygame.mixer.music.load(self.selected_sound)
            pygame.mixer.music.play()

    def stop_sound(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

    def run_scenarios(self):
        if not self.scenarios:
            messagebox.showinfo("Информация", "Нет доступных сценариев для выполнения.")
            return

        if self.hide_during_scenarios.get():
            self.root.withdraw()

        if self.selected_sound and self.use_sound.get():
            self.play_sound()

        def execute_scenarios():
            for scenario in self.scenarios:
                title, message, icon, buttons, delay = scenario
                time.sleep(delay / 1000)  # delay in milliseconds
                result = messagebox.showinfo(title, message) if icon == "info" else (
                    messagebox.showwarning(title, message) if icon == "warning" else messagebox.showerror(title, message)
                )
                # Handle button responses (e.g., yes/no) if necessary
            self.on_scenarios_complete()

        threading.Thread(target=execute_scenarios, daemon=True).start()

    def on_scenarios_complete(self):
        self.stop_sound()
        if self.hide_during_scenarios.get():
            self.root.deiconify()

    def add_scenario(self):
        def save_scenario():
            title = title_entry.get()
            message = message_entry.get()
            icon = icon_var.get()
            buttons = buttons_var.get()
            try:
                delay = int(delay_entry.get())
            except ValueError:
                delay = 1000  # Default delay
            self.scenarios.append((title, message, icon, buttons, delay))
            self.scenario_listbox.insert(tk.END, title)
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить сценарий")
        tk.Label(add_window, text="Заголовок:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Сообщение:").pack()
        message_entry = tk.Entry(add_window)
        message_entry.pack()

        tk.Label(add_window, text="Иконка:").pack()
        icon_var = tk.StringVar(value="info")
        tk.OptionMenu(add_window, icon_var, "info", "warning", "error").pack()

        tk.Label(add_window, text="Кнопки:").pack()
        buttons_var = tk.StringVar(value="ok")
        tk.OptionMenu(add_window, buttons_var, "ok", "okcancel", "yesno").pack()

        tk.Label(add_window, text="Задержка (мс):").pack()
        delay_entry = tk.Entry(add_window)
        delay_entry.pack()

        tk.Button(add_window, text="Сохранить", command=save_scenario).pack()

    def delete_scenario(self):
        selected_index = self.scenario_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.scenarios[index]
            self.scenario_listbox.delete(index)

    def run(self):
        self.root.mainloop()


app = ErrorScenarioApp()
app.run()
