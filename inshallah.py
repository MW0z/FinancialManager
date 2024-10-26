from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.slider import Slider

from kivy.uix.screenmanager import ScreenManager, Screen
import hashlib
import time


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
                list_of_records = f.read().split("\n")
                print(list_of_records)

                for i in range (len(list_of_records)-1):
                    co_list_of_records = list_of_records[i].split(" ")
                    print(co_list_of_records)
                    stored_email = co_list_of_records[0]
                    print(stored_email)
                    stored_password = co_list_of_records[1]
                    print(stored_password)
                    print(auth_hash)

                    if email == stored_email and auth_hash == stored_password:
                        self.status_label.text = "Logged in Successfully!"
                        self.status_label.color = (0, 1, 0, 1)  # Green for success
                        self.manager.current = "days"
                        flag = False
                        break
                    else:
                        flag = True
                if flag == True:
                    self.status_label.text = "Invalid email or password!"
                    self.status_label.color = (1, 0, 0, 1)  # Red for failure
        
        except FileNotFoundError:
            self.status_label.text = "No credentials found. Please register first."
            self.status_label.color = (1, 0, 0, 1)


    def go_to_register(self, instance):
        # Switch to the register screen
        self.manager.current = "register"
    def go_to_Day():
        self.manager.current = "days"


# Define the Register Screen
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        
        # Title label
        layout.add_widget(Label(text="Register", font_size=32))
        
        # Email input
        self.email_input = TextInput(hint_text="Enter Username", multiline=False)
        layout.add_widget(self.email_input)
        
        # Password input
        self.password_input = TextInput(hint_text="Enter Password", multiline=False, password=True)
        layout.add_widget(self.password_input)
        
        # Confirm Password input
        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True)
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

        try:
            with open("credentials.txt", "r") as f:
                users = [line.split(" ")[0] for line in f.readlines()]  # Read all usernames
                if email in users:
                    self.status_label.text = "Username already taken!"
                    self.status_label.color = (1, 0, 0, 1)
                    return
        except FileNotFoundError:
        # If the file doesn't exist, we'll create it when registering the first user
            pass

        if password == confirm_password:
            auth_hash = hashlib.md5(password.encode()).hexdigest()
            # This is where we compare the hash value of the password to the password that has been entered.
            with open("credentials.txt", "a") as f:
                f.write(f"{email} {auth_hash}\n")
            self.status_label.text = "Registered successfully!"
            self.status_label.color = (0, 1, 0, 1)  # Green for success
            self.manager.current = "days" # Switch to first screen.
        else:
            self.status_label.text = "Passwords do not match!"
            self.status_label.color = (1, 0, 0, 1)  # Red for failure

    def go_to_login(self, instance):
        # Switch back to the login screen
        self.manager.current = "login"

#Define the DayScreen Screen
class DayScreen(Screen):
    def __init__(self, **kwargs):
        super(DayScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Title label
        layout.add_widget(Label(text="How much would you like to save per week?", font_size=32))  # TITLE

        # Slider to choose days
        self.slider = Slider(min=0, max=100, value=50)
        layout.add_widget(self.slider)

        # Label to display slider value
        self.value_label = Label(text=f"Days to save: {int(self.slider.value)}")
        layout.add_widget(self.value_label)

        # Bind the slider's value to the label
        self.slider.bind(value=self.on_value_change)

        self.add_widget(layout)  # Add the layout to the screen

    def on_value_change(self, instance, value):
        # Update label with the current slider value
        self.value_label.text = f"Days to save: {int(value)}"







# Define the main app
class LoginApp(App):
    def build(self):
        # Create the ScreenManager
        sm = ScreenManager()
        
        # Add both screens to the manager
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))

        sm.add_widget(DayScreen(name="days"))
        """
        sm.add_widget(CoffeeScreen(name= "coffee"))
        sm.add_widget(SmokeScreen(name="smoke"))
        sm.add_widget(EatOutScreen(name="eat_out"))
        sm.add_widget(TransportScreen(name = "transport"))
        sm.add_widget(WeeklyGoalScreen(name = "weekly_goal"))
        sm.add_widget(HomeScreen(name = "home_screen"))
        """
        
        return sm


if __name__ == "__main__":
    LoginApp().run()
