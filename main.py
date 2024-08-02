# main.py

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
import time
import random

class ReactionTimeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Enter the number of trials and press Start.")
        self.input_field = TextInput(hint_text="Number of trials", input_filter='int', multiline=False)
        self.start_button = Button(text="Start")
        self.restart_button = Button(text="Restart", disabled=True)

        self.start_button.bind(on_press=self.start_trials)
        self.restart_button.bind(on_press=self.restart_trials)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.input_field)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.restart_button)

        return self.layout

    def start_trials(self, instance):
        try:
            self.num_trials = int(self.input_field.text)
            if self.num_trials <= 0:
                raise ValueError("Number of trials must be positive.")
            self.current_trial = 0
            self.reaction_times = []
            self.start_time = None
            self.end_time = None

            self.label.text = "Press the button to start the trial."
            self.input_field.disabled = True
            self.start_button.text = "Start/Stop"
            self.start_button.unbind(on_press=self.start_trials)
            self.start_button.bind(on_press=self.on_button_press)
            self.restart_button.disabled = False
        except ValueError:
            self.show_popup("Invalid input", "Please enter a positive integer for the number of trials.")

    def on_button_press(self, instance):
        if self.start_time is None:
            if self.current_trial < self.num_trials:
                self.label.text = "Get ready..."
                self.start_button.disabled = True
                delay = random.uniform(1, 3)
                Clock.schedule_once(self.enable_button, delay)
            else:
                self.display_results()
        else:
            self.end_time = time.time()
            reaction_time = self.end_time - self.start_time
            self.reaction_times.append(reaction_time)
            self.current_trial += 1

            if self.current_trial < self.num_trials:
                self.label.text = f"Trial {self.current_trial}: Reaction time: {reaction_time:.3f} seconds\nPress to start the next trial."
            else:
                self.display_results()

            self.start_time = None
            self.end_time = None

    def enable_button(self, dt):
        self.start_button.disabled = False
        self.start_time = time.time()
        self.label.text = "Press the button as soon as you can!"

    def display_results(self):
        results_text = "Reaction times for all trials:\n"
        for i, rt in enumerate(self.reaction_times, start=1):
            results_text += f"Trial {i}: {rt:.3f} seconds\n"
        self.label.text = results_text
        self.start_button.disabled = True

    def restart_trials(self, instance):
        self.label.text = "Enter the number of trials and press Start."
        self.input_field.text = ""
        self.input_field.disabled = False
        self.start_button.text = "Start"
        self.start_button.unbind(on_press=self.on_button_press)
        self.start_button.bind(on_press=self.start_trials)
        self.restart_button.disabled = True
        self.start_button.disabled = False

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        popup_button = Button(text="OK", size_hint=(1, 0.25))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.75, 0.5))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    ReactionTimeApp().run()
