from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import hashlib


# Define the Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        
        # Title label
        layout.add_widget(Label(text="Login", font_size=32))
        
        # Email input
        self.email_input = TextInput(hint_text="Enter email", multiline=False)
        layout.add_widget(self.email_input)
        
        # Password input
        self.password_input = TextInput(hint_text="Enter password", multiline=False, password=True)
        layout.add_widget(self.password_input)
        
        # Login button
        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.validate_login)
        layout.add_widget(self.login_button)
        
        # Register button
        self.register_button = Button(text="Register")
        self.register_button.bind(on_press=self.go_to_register)
        layout.add_widget(self.register_button)
        
        # Status label
        self.status_label = Label(text="")
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

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
            self.status_label.text = "No credentials found. Please register first."
            self.status_label.color = (1, 0, 0, 1)

    def go_to_register(self, instance):
        # Switch to the register screen
        self.manager.current = "register"


# Define the Register Screen
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        
        # Title label
        layout.add_widget(Label(text="Register", font_size=32))
        
        # Email input
        self.email_input = TextInput(hint_text="Enter email", multiline=False)
        layout.add_widget(self.email_input)
        
        # Password input
        self.password_input = TextInput(hint_text="Enter password", multiline=False, password=True)
        layout.add_widget(self.password_input)
        
        # Confirm Password input
        self.confirm_password_input = TextInput(hint_text="Confirm password", multiline=False, password=True)
        layout.add_widget(self.confirm_password_input)
        
        # Register button
        self.register_button = Button(text="Register")
        self.register_button.bind(on_press=self.register_user)
        layout.add_widget(self.register_button)
        
        # Back to Login button
        self.back_to_login_button = Button(text="Back to Login")
        self.back_to_login_button.bind(on_press=self.go_to_login)
        layout.add_widget(self.back_to_login_button)
        
        # Status label
        self.status_label = Label(text="")
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def register_user(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if password == confirm_password:
            auth_hash = hashlib.md5(password.encode()).hexdigest()
            with open("credentials.txt", "w") as f:
                f.write(f"{email} {auth_hash}")
            self.status_label.text = "Registered successfully!"
            self.status_label.color = (0, 1, 0, 1)  # Green for success
        else:
            self.status_label.text = "Passwords do not match!"
            self.status_label.color = (1, 0, 0, 1)  # Red for failure

    def go_to_login(self, instance):
        # Switch back to the login screen
        self.manager.current = "login"


# Define the main app
class LoginApp(App):
    def build(self):
        # Create the ScreenManager
        sm = ScreenManager()
        
        # Add both screens to the manager
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        
        return sm


if __name__ == "__main__":
    LoginApp().run()
