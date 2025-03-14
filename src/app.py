from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from config import load_config, save_config
from network.tcp_listener import start_tcp_listener
from network.udp_listener import start_udp_listener
from network.discovery_listener import start_discovery_listener
from ui.main_layout import MainLayout

class SecuritySystemApp(App):
    def build(self):
        # Start network listeners
        start_discovery_listener()
        start_tcp_listener()
        start_udp_listener()

        # Load configuration
        load_config()

        # Create the main layout
        main_layout = MainLayout()
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(main_layout)
        self.root_layout = scroll_view
        
        Clock.schedule_interval(self.update_status, 0.5)
        return self.root_layout

    def update_status(self, dt):
        # Update the status of the system
        pass

if __name__ == '__main__':
    SecuritySystemApp().run()

"""
    from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from network.discovery_listener import start_discovery_listener
from network.tcp_listener import start_tcp_listener
from network.udp_listener import start_udp_listener
from ui.main_layout import create_main_layout
from config import load_config, save_config

class SecuritySystemApp(App):
    def build(self):
        # Start network listeners
        start_discovery_listener()
        start_tcp_listener()
        start_udp_listener()

        # Load configuration
        load_config()

        # Create the main layout
        self.root_layout = create_main_layout(self)
        
        Clock.schedule_interval(self.update_status, 0.5)
        return self.root_layout

    def update_status(self, dt):
        # Update the status of the system
        pass

if __name__ == '__main__':
    SecuritySystemApp().run()

"""