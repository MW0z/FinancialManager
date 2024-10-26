from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import hashlib


from kivy.uix.screenmanager import ScreenManager, Screen

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        #self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        self.login_button = Button(text="Login", size_hint=(1, 0.5))
        self.login_button.bind(on_press=self.login_screen)
        self.add_widget(self.login_button)
    
        self.register_button = Button(text="Register", size_hint=(1, 0.5))
        self.register_button.bind(on_press=self.register_screen)
        self.add_widget(self.register_button)
    



    """
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10
        
        # Title label
        self.add_widget(Label(text="Login", font_size=32, color=(0, 0, 0, 1)))
        
        # Email input
        self.email_input = TextInput(hint_text="Enter email", multiline=False)
        self.add_widget(self.email_input)
        
        # Password input
        self.password_input = TextInput(hint_text="Enter password", multiline=False, password=True)
        self.add_widget(self.password_input)
        
        # Login button
        self.login_button = Button(text="Login", size_hint=(1, 0.5))
        self.login_button.bind(on_press=self.validate_login)
        self.add_widget(self.login_button)
        
        # Status label
        self.status_label = Label(text="", color=(1, 0, 0, 1))
        self.add_widget(self.status_label)
    """

    def login_screen(self,instance):
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10
        
        # Title label
        self.add_widget(Label(text="Login", font_size=32, color=(0, 0, 0, 1)))
        
        # Email input
        self.email_input = TextInput(hint_text="Enter email", multiline=False)
        self.add_widget(self.email_input)
        
        # Password input
        self.password_input = TextInput(hint_text="Enter password", multiline=False, password=True)
        self.add_widget(self.password_input)
        
        # Login button
        self.login_button = Button(text="Login", size_hint=(1, 0.5))
        self.login_button.bind(on_press=self.validate_login)
        self.add_widget(self.login_button)
        
        # Status label
        self.status_label = Label(text="", color=(1, 0, 0, 1))
        self.add_widget(self.status_label)
    def register_screen(self,instance):
        pass

    
    def validate_login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        
        # Hash the entered password
        auth_hash = hashlib.md5(password.encode()).hexdigest()
        
        try:
            # Read the stored credentials
            with open("credentials.txt", "r") as f:
                stored_email, stored_password = f.read().split(" ")
            
            # Verify email and password
            if email == stored_email and auth_hash == stored_password:
                self.status_label.text = "Logged in Successfully!"
                self.status_label.color = (0, 1, 0, 1)  # Green for success
            else:
                self.status_label.text = "Invalid email or password!"
                self.status_label.color = (1, 0, 0, 1)  # Red for failure
        
        except FileNotFoundError:
            self.status_label.text = "No credentials found. Please sign up first."
            self.status_label.color = (1, 0, 0, 1)
    def register_login (self,instance):
        username = self.username_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text



class LoginApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    LoginApp().run()
