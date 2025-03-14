from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class PinPopup:
    def __init__(self, title, hint_text, confirm_callback):
        self.title = title
        self.hint_text = hint_text
        self.confirm_callback = confirm_callback
        self.popup = None
        self.popup_pin_input = None

    def open(self):
        content = BoxLayout(orientation='vertical', spacing=5, padding=5)
        self.popup_pin_input = TextInput(password=True, font_size='14sp',
                                          hint_text=self.hint_text, multiline=False,
                                          size_hint_y=None, height=40)
        content.add_widget(self.popup_pin_input)
        
        confirm_button = Button(text="Enter", size_hint_y=None, height=40)
        confirm_button.bind(on_press=self.confirm)
        content.add_widget(confirm_button)
        
        self.popup = Popup(title=self.title, content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def confirm(self, instance):
        self.confirm_callback(self.popup_pin_input.text)
        self.popup.dismiss()

class MessagePopup:
    def __init__(self, title, message):
        self.popup = Popup(title=title, content=Label(text=message, font_size='12sp'), size_hint=(0.6, 0.4))

    def open(self):
        self.popup.open()