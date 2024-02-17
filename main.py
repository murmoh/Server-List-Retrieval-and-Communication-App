from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty


from serverlist import MainApp as ServerApp


# Get the path of the directory where the font files are located


class RotatingImage(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(RotatingImage, self).__init__(**kwargs)
        anim = Animation(angle=360, duration=2)
        anim += Animation(angle=0, duration=0)
        anim.repeat = True
        anim.start(self)


class LoadingScreen(Screen):
    def on_enter(self, *args):
        layout = FloatLayout()  # Use FloatLayout to have more control over widget positions

        # Splash image or logo
        splash = Image(source='logo.png',
                       pos_hint={'center_x': .5, 'center_y': .7})  # Assuming the logo.png file is in the same directory
        layout.add_widget(splash)

        # Customized label
        label = Label(text="Loading...", font_name='Comic', font_size='20sp', color=(0, 0, 0, 1),
                      pos_hint={'center_x': .5, 'center_y': .5})
        layout.add_widget(label)

        # Progress bar at the bottom of the screen
        bar = ProgressBar(max=100, pos_hint={'center_x': .5, 'y': .1}, size_hint_x=0.6)
        layout.add_widget(bar)

        # Start the animations
        label_anim = Animation(opacity=0, duration=1) + Animation(opacity=1, duration=1)
        label_anim.repeat = True
        label_anim.start(label)
        bar_anim = Animation(value=100, duration=3)
        bar_anim.start(bar)

        self.add_widget(layout)
        Clock.schedule_once(self.change_screen, 5)

    def change_screen(self, dt):
        self.manager.current = 'main'



class MainScreen(Screen):
    def on_enter(self, *args):
        self.server_app = ServerApp()
        server_list_widget = self.server_app.build()
        self.server_app.update_server_list(None)
        self.add_widget(server_list_widget)


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        loading_screen = LoadingScreen(name='loading')
        main_screen = MainScreen(name='main')
        sm.add_widget(loading_screen)
        sm.add_widget(main_screen)
        return sm


if __name__ == '__main__':
    MainApp().run()
