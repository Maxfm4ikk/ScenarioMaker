import tkinter as tk
from tkinter import messagebox, filedialog
import time
import pygame
import threading

class ErrorScenarioApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Error Scenario App")
        self.root.geometry("600x400")

        self.scenarios = []
        self.language = "Русский"  # Default language
        self.hide_during_scenarios = tk.BooleanVar(value=False)  # Variable for hiding window
        self.use_sound = tk.BooleanVar(value=False)  # Variable for using sound
        self.selected_sound = None  # Path to the selected sound file

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

    def toggle_language(self):
        if self.language == "Русский":
            self.language = "English"
            self.language_button.config(text="Switch to Russian")
            self.hide_checkbox.config(text="Hide program when running scenarios?")
            self.sound_checkbox.config(text="Use custom sound?")
            self.select_sound_button.config(text="Select Sound")
            self.run_button.config(text="Run Scenarios")
        else:
            self.language = "Русский"
            self.language_button.config(text="Изменить на English")
            self.hide_checkbox.config(text="Закрывать программу при запуске сценария?")
            self.sound_checkbox.config(text="Использовать пользовательский звук?")
            self.select_sound_button.config(text="Выбрать звук")
            self.run_button.config(text="Запустить сценарии")

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
        if self.hide_during_scenarios.get():
            self.root.withdraw()

        if self.selected_sound and self.use_sound.get():
            self.play_sound()

        def execute_scenarios():
            for i, scenario in enumerate(self.scenarios):
                time.sleep(1)  # Simulate delay between scenarios
                messagebox.showinfo(f"Сценарий {i + 1}", f"Сообщение сценария {i + 1}")
            self.on_scenarios_complete()

        threading.Thread(target=execute_scenarios, daemon=True).start()

    def on_scenarios_complete(self):
        self.stop_sound()
        if self.hide_during_scenarios.get():
            self.root.deiconify()

    def add_scenario(self, title, message):
        self.scenarios.append((title, message))
        self.scenario_listbox.insert(tk.END, title)

    def run(self):
        self.root.mainloop()


app = ErrorScenarioApp()
app.add_scenario("Ошибка 1", "Текст ошибки 1")
app.add_scenario("Ошибка 2", "Текст ошибки 2")
app.run()
