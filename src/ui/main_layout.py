from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock

# Import defaults and saving function from config
from config import PIN_CODE, system_active, save_config

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Use values from config
        self.pin = PIN_CODE
        self.system_active = system_active

        # Update dynamic sizes
        self.update_font_sizes()

        # Header: System Status
        self.status_label = Label(
            text="System Status: " + ("Aktivny" if self.system_active else "Deaktivovany"), 
            font_size=self.font_size, 
            size_hint_y=None, 
            height=30
        )
        self.add_widget(self.status_label)

        # Button Bar: PIN Change, Action, Exit Fullscreen
        self.button_bar = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.pin_button = Button(
            text="Switch to PIN Change", 
            font_size=self.button_font_size
        )
        self.pin_button.bind(on_press=self.open_pin_change)
        self.action_button = Button(
            text="Action", 
            font_size=self.button_font_size
        )
        self.action_button.bind(on_press=self.open_state_toggle)
        self.fullscreen_button = Button(
            text="Exit Fullscreen", 
            font_size=self.button_font_size
        )
        self.fullscreen_button.bind(on_press=self.exit_fullscreen)
        self.button_bar.add_widget(self.pin_button)
        self.button_bar.add_widget(self.action_button)
        self.button_bar.add_widget(self.fullscreen_button)
        self.add_widget(self.button_bar)

        # Indicator area: Scrollable grid with dummy indicators
        self.indicator_scroll = ScrollView(size_hint=(1, None), height=150)
        self.indicator_grid = GridLayout(
            cols=3, spacing=10, size_hint_y=None
        )
        self.indicator_grid.bind(minimum_height=self.indicator_grid.setter('height'))
        for i in range(6):
            lbl = Label(
                text=f"Indicator {i+1}", 
                size_hint_y=None, 
                height=40, 
                font_size=self.button_font_size
            )
            self.indicator_grid.add_widget(lbl)
        self.indicator_scroll.add_widget(self.indicator_grid)
        self.add_widget(self.indicator_scroll)

        # Image display area (placeholder)
        self.image_label = Label(
            text="Image Area", 
            size_hint=(1, None), 
            height=150, 
            font_size=self.button_font_size
        )
        self.add_widget(self.image_label)

        # Bind window resize to adjust layout dynamically
        Window.bind(on_resize=self.adjust_layout)

    def update_font_sizes(self):
        if Window.size[0] < 600:
            self.font_size = '10sp'
            self.button_font_size = '12sp'
        else:
            self.font_size = '12sp'
            self.button_font_size = '14sp'

    def adjust_layout(self, *args):
        self.update_font_sizes()
        self.status_label.font_size = self.font_size
        self.pin_button.font_size = self.button_font_size
        self.action_button.font_size = self.button_font_size
        self.fullscreen_button.font_size = self.button_font_size
        for child in self.indicator_grid.children:
            child.font_size = self.button_font_size
        self.image_label.font_size = self.button_font_size

    def update_status(self, system_active):
        self.status_label.text = "System Status: " + ("Aktivny" if system_active else "Deaktivovany")

    def show_message(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, font_size=self.button_font_size), 
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def open_numpad(self, title, submit_callback):
        """Creates and returns a popup with an on-screen numeric keypad."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        display_label = Label(text="", font_size=self.button_font_size, size_hint=(1, 0.3))
        content.add_widget(display_label)
        
        grid = GridLayout(cols=3, spacing=5, size_hint=(1, 0.6))
        current_number = [""]
        
        def update_display():
            display_label.text = current_number[0]
            
        def on_num_press(instance):
            current_number[0] += instance.text
            update_display()
            
        def on_clear(instance):
            current_number[0] = ""
            update_display()
            
        def on_back(instance):
            current_number[0] = current_number[0][:-1]
            update_display()
        
        for num in range(1, 10):
            btn = Button(text=str(num), font_size=self.button_font_size)
            btn.bind(on_press=on_num_press)
            grid.add_widget(btn)
            
        btn_clear = Button(text="Clear", font_size=self.button_font_size)
        btn_clear.bind(on_press=on_clear)
        grid.add_widget(btn_clear)
        
        btn_zero = Button(text="0", font_size=self.button_font_size)
        btn_zero.bind(on_press=on_num_press)
        grid.add_widget(btn_zero)
        
        btn_back = Button(text="<-", font_size=self.button_font_size)
        btn_back.bind(on_press=on_back)
        grid.add_widget(btn_back)
        
        content.add_widget(grid)
        submit_btn = Button(text="Submit", size_hint=(1, 0.2), font_size=self.button_font_size)
        content.add_widget(submit_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        submit_btn.bind(on_press=lambda instance: (submit_callback(current_number[0]), popup.dismiss()))
        return popup

    def open_pin_change(self, instance):
        """Opens numpad popup to change the PIN."""
        def submit_new_pin(entered):
            if entered:
                self.pin = entered
                self.show_message("PIN Changed", "PIN has been changed successfully.")
                # Update and save config
                from config import save_config
                save_config()  # assumes save_config() uses global PIN_CODE; update accordingly
            else:
                self.show_message("Error", "Please enter a valid PIN.")
        
        numpad = self.open_numpad("Enter New PIN", submit_new_pin)
        numpad.open()

    def open_state_toggle(self, instance):
        """Opens numpad popup to verify PIN and toggle system state."""
        def submit_state_pin(entered):
            if entered == self.pin:
                self.system_active = not self.system_active
                self.update_status(self.system_active)
                state = "Aktivny" if self.system_active else "Deaktivovany"
                self.show_message("System State", f"System state changed to {state}.")
                # Save new state to config
                from config import save_config
                save_config()
            else:
                self.show_message("Error", "Invalid PIN. State not changed.")
        
        numpad = self.open_numpad("Enter PIN to Toggle State", submit_state_pin)
        numpad.open()

    def exit_fullscreen(self, instance):
        Window.fullscreen = False
        self.show_message("Fullscreen", "Exiting fullscreen mode.")