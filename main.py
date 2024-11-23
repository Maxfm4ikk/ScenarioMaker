import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import pygame
import os


class ErrorScenarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Error Scenario")

        self.language = "Русский"
        self.scenarios = []
        self.selected_scenario_index = None
        self.audio_file = None
        self.is_music_playing = False
        self.use_custom_sound = tk.BooleanVar(value=False)

        self.init_ui()
        pygame.mixer.init()

    def init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.frame_main = ttk.Frame(self.root, padding=10)
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame_main, text=self.translate("Заголовок:")).grid(row=0, column=0, sticky=tk.W)
        self.entry_title = ttk.Entry(self.frame_main, width=40)
        self.entry_title.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame_main, text=self.translate("Текст сообщения:")).grid(row=1, column=0, sticky=tk.W)
        self.entry_message = ttk.Entry(self.frame_main, width=40)
        self.entry_message.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.frame_main, text=self.translate("Тип иконки (info, warning, error):")).grid(row=2, column=0, sticky=tk.W)
        self.entry_icon = ttk.Entry(self.frame_main, width=40)
        self.entry_icon.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.frame_main, text=self.translate("Тип кнопок (ok, okcancel, yesno):")).grid(row=3, column=0, sticky=tk.W)
        self.entry_buttons = ttk.Entry(self.frame_main, width=40)
        self.entry_buttons.grid(row=3, column=1, sticky=tk.W)

        self.listbox_scenarios = tk.Listbox(self.frame_main, height=10)
        self.listbox_scenarios.grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E, pady=5)
        self.listbox_scenarios.bind('<<ListboxSelect>>', self.select_scenario)

        self.button_add = ttk.Button(self.frame_main, text=self.translate("Добавить сценарий"), command=self.add_scenario)
        self.button_add.grid(row=5, column=0, sticky=tk.W)

        self.button_run = ttk.Button(self.frame_main, text=self.translate("Запустить сценарии"), command=self.run_scenarios)
        self.button_run.grid(row=5, column=1, sticky=tk.E)

        self.check_sound = ttk.Checkbutton(self.frame_main, text=self.translate("Использовать пользовательский звук?"), variable=self.use_custom_sound, command=self.toggle_audio_file)
        self.check_sound.grid(row=6, column=0, columnspan=2, sticky=tk.W)

        self.button_select_audio = ttk.Button(self.frame_main, text=self.translate("Выбрать звук"), command=self.select_audio_file, state=tk.DISABLED)
        self.button_select_audio.grid(row=7, column=0, columnspan=2, sticky=tk.W)

        self.button_language = ttk.Button(self.frame_main, text=self.translate("Изменить на Русский"), command=self.switch_language)
        self.button_language.grid(row=8, column=0, columnspan=2)

        self.update_scenarios_list()

    def translate(self, text):
        translations = {
            "Заголовок:": "Title:",
            "Текст сообщения:": "Message text:",
            "Тип иконки (info, warning, error):": "Icon type (info, warning, error):",
            "Тип кнопок (ok, okcancel, yesno):": "Button type (ok, okcancel, yesno):",
            "Добавить сценарий": "Add Scenario",
            "Запустить сценарии": "Run Scenarios",
            "Использовать пользовательский звук?": "Use custom sound?",
            "Выбрать звук": "Select Sound",
            "Изменить на Русский": "Switch to English",
            "Switch to English": "Изменить на Русский"
        }
        if self.language == "English":
            return translations.get(text, text)
        else:
            reverse_translations = {v: k for k, v in translations.items()}
            return reverse_translations.get(text, text)

    def switch_language(self):
        self.language = "English" if self.language == "Русский" else "Русский"
        self.init_ui()

    def toggle_audio_file(self):
        if self.use_custom_sound.get():
            self.button_select_audio.config(state=tk.NORMAL)
            if self.audio_file and not self.is_music_playing:
                self.play_music()
        else:
            self.button_select_audio.config(state=tk.DISABLED)

    def select_audio_file(self):
        self.audio_file = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if self.audio_file:
            messagebox.showinfo(self.translate("Выбор звука"), self.translate("Файл выбран: ") + os.path.basename(self.audio_file))

    def add_scenario(self):
        title = self.entry_title.get()
        message = self.entry_message.get()
        icon = self.entry_icon.get()
        buttons = self.entry_buttons.get()

        if not title or not message or icon not in ["info", "warning", "error"] or buttons not in ["ok", "okcancel", "yesno"]:
            messagebox.showerror(self.translate("Ошибка"), self.translate("Проверьте введённые данные."))
            return

        self.scenarios.append({"title": title, "message": message, "icon": icon, "buttons": buttons, "delay": 1000})
        self.update_scenarios_list()

    def update_scenarios_list(self):
        self.listbox_scenarios.delete(0, tk.END)
        for scenario in self.scenarios:
            self.listbox_scenarios.insert(tk.END, f"{scenario['title']} - {scenario['message']}")

    def select_scenario(self, event):
        selected_index = self.listbox_scenarios.curselection()
        if selected_index:
            self.selected_scenario_index = selected_index[0]
            scenario = self.scenarios[self.selected_scenario_index]
            self.open_scenario_settings(scenario)

    def open_scenario_settings(self, scenario):
        settings_window = tk.Toplevel(self.root)
        settings_window.title(self.translate("Настройки сценария"))

        ttk.Label(settings_window, text=self.translate("Задержка (мс):")).pack(pady=5)
        delay_entry = ttk.Entry(settings_window, width=20)
        delay_entry.insert(0, scenario["delay"])
        delay_entry.pack(pady=5)

        def save_settings():
            try:
                delay = int(delay_entry.get())
                if delay < 0:
                    raise ValueError
                self.scenarios[self.selected_scenario_index]["delay"] = delay
                settings_window.destroy()
            except ValueError:
                messagebox.showerror(self.translate("Ошибка"), self.translate("Введите корректное число."))

        ttk.Button(settings_window, text=self.translate("Сохранить"), command=save_settings).pack(pady=10)

        def delete_scenario():
            if messagebox.askyesno(self.translate("Удалить сценарий?"), self.translate("Вы уверены, что хотите удалить этот сценарий?")):
                del self.scenarios[self.selected_scenario_index]
                self.update_scenarios_list()
                settings_window.destroy()

        ttk.Button(settings_window, text=self.translate("Удалить сценарий"), command=delete_scenario).pack(pady=5)

    def run_scenarios(self):
        if self.use_custom_sound.get() and not self.audio_file:
            messagebox.showerror(self.translate("Ошибка"), self.translate("Вы не выбрали звук."))
            return

        if self.audio_file and self.use_custom_sound.get() and not self.is_music_playing:
            self.play_music()

        self.show_next_error(0)

    def play_music(self):
        if self.audio_file:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play(loops=-1, start=0.0)
            self.is_music_playing = True

    def stop_music(self):
        if self.is_music_playing:
            pygame.mixer.music.stop()
            self.is_music_playing = False

    def show_next_error(self, index):
        if index < len(self.scenarios):
            scenario = self.scenarios[index]

            if scenario["buttons"] == "ok":
                messagebox.showinfo(scenario["title"], scenario["message"], icon=scenario["icon"])
            elif scenario["buttons"] == "okcancel":
                messagebox.askokcancel(scenario["title"], scenario["message"], icon=scenario["icon"])
            elif scenario["buttons"] == "yesno":
                messagebox.askyesno(scenario["title"], scenario["message"], icon=scenario["icon"])

            time.sleep(scenario["delay"] / 1000)
            self.show_next_error(index + 1)
        else:
            if self.is_music_playing:
                self.stop_music()


root = tk.Tk()
app = ErrorScenarioApp(root)
root.mainloop()
