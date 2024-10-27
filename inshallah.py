from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar

from kivy.graphics import Ellipse, Color

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.slider import Slider

from kivy.uix.screenmanager import ScreenManager, Screen
import hashlib
import time
import random
from kivy.clock import Clock
from datetime import datetime


SAVING_CHALLENGES = [
    "Save £5 every day this week.",
    "Skip your daily coffee and save £3.",
    "Save all your £1 coins this week.",
    "Cook at home instead of eating out for 3 days.",
    "Set aside £10 for every workout you complete.",
    "Limit your online shopping for a week.",
    "Save £1 for every time you skip a snack."
]




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
                        self.manager.current = "save"
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
class WeeklySave(Screen):
    def __init__(self, **kwargs):
        super(WeeklySave, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Title label
        layout.add_widget(Label(text="How much would you like to save per week?", font_size=32))  # TITLE

        # Slider to choose days
        self.slider = Slider(min=0, max=50, value=25)
        layout.add_widget(self.slider)

        # Label to display slider value
        self.value_label = Label(text=f"Amount to save: £{int(self.slider.value)}")
        layout.add_widget(self.value_label)

        # Bind the slider's value to the label
        self.slider.bind(value=self.on_value_change)

        self.next = Button(text="Next")
        self.next.bind(on_press=self.go_to_dayScreen)
        layout.add_widget(self.next)
        self.add_widget(layout)  # Add the layout to the screen

    def on_value_change(self, instance, value):
        # Update label with the current slider value
        self.value_label.text = f"Amount to save: £{int(value)}" #################### Weekly Save

    def go_to_dayScreen(self,instance):
        self.manager.current = "days"


class DayScreen(Screen):
    def __init__(self, **kwargs):
        super(DayScreen, self).__init__(**kwargs)
        
        # Main vertical layout
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Title label
        layout.add_widget(Label(text="On what days would you like to save?", font_size=32, halign="center"))

        # Centered container for the day buttons
        day_container = BoxLayout(orientation="vertical", size_hint=(1, None), height=100)
        
        # Horizontal layout for day buttons, centered
        day_layout = BoxLayout(orientation="horizontal", spacing=5, size_hint=(None, None), width=400)
        day_layout.pos_hint = {"center_x": 0.5}  # Center horizontally
        
        # List of days
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Track selected days
        self.selected_days = set()
        
        # Create buttons for each day
        for day in days:
            day_button = Button(
                text=day,
                size_hint=(None, None),
                size=(50, 50),
                background_normal="",
                background_color=(0.7, 0.7, 0.7, 1)  # Grey for unselected
            )
            day_button.bind(on_press=self.toggle_day)
            day_layout.add_widget(day_button)
        
        # Add day selection layout to the day container
        day_container.add_widget(day_layout)
        layout.add_widget(day_container)  # Center day buttons vertically

        # Next button to proceed to CoffeeScreen, centered horizontally
        self.next = Button(text="Next", size_hint=(None, None), size=(100, 50), pos_hint={"center_x": 0.5})
        self.next.bind(on_press=self.go_to_coffee_screen)
        layout.add_widget(self.next)

        # Add the layout to the screen
        self.add_widget(layout)
    
    def toggle_day(self, instance):
    # Toggle day selection
        if instance in self.selected_days:
            instance.background_color = (0.7, 0.7, 0.7, 1)  # Unselected color (grey)
            self.selected_days.remove(instance)
        else:
            instance.background_color = (0.3, 0.7, 0.3, 1)  # Selected color (green)
            self.selected_days.add(instance)

    # Print or use selected days as needed
        selected_days_text = [btn.text for btn in self.selected_days]
        print("Selected days:", selected_days_text)
        
        f = open("days.txt","w")
        for i in range (len(selected_days_text)):
            f.write(selected_days_text[i]+ "\n")
        f.close()



    def go_to_coffee_screen(self, instance):
        
        self.manager.current = "coffee"

class CoffeeScreen(Screen):
    def __init__(self, **kwargs):
        super(CoffeeScreen, self).__init__(**kwargs)
        
        # Vertical layout for the question
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Label(text="Do you drink coffee?", font_size=32))  # Title
        
        # Horizontal layout for buttons
        layout2 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=100, spacing=10)

        cof_image = Image(source="coffee.png", size_hint=(1, 0.6))  # Adjust size_hint as needed
        layout.add_widget(cof_image)  # Add the image widget to the layout
        
        # "Yes" button with oval shape
        self.yes = Button(text="Yes", size_hint=(0.5, 1), background_normal='', background_color=(0.3, 0.6, 1, 1))
        self.yes.radius = [50, 50, 50, 50]
        self.yes.bind(on_press=self.go_to_smoke_screen)
        layout2.add_widget(self.yes)
        
        # "No" button with oval shape
        self.no = Button(text="No", size_hint=(0.5, 1), background_normal='', background_color=(1, 0.5, 0.5, 1))
        self.no.radius = [50, 50, 50, 50]
        self.no.bind(on_press=self.go_to_smoke_screen)
        layout2.add_widget(self.no)
        
        # Add the question layout and button layout to the screen
        layout.add_widget(layout2)
        self.add_widget(layout)

    def go_to_smoke_screen(self, instance):
        self.manager.current = "smoke"
      

class SmokeScreen(Screen):
    def __init__(self, **kwargs):
        super(SmokeScreen, self).__init__(**kwargs)
        
        # Vertical layout for the question
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Label(text="Do you drink smoke?", font_size=32))  # Title
        
        # Add the image to the layout
        cig_image = Image(source="cig2.png", size_hint=(1, 0.6))  # Adjust size_hint as needed
        layout.add_widget(cig_image)  # Add the image widget to the layout
        
        # Horizontal layout for buttons
        layout2 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=100, spacing=10)

        # "Yes" button with oval shape
        self.yes = Button(text="Yes", size_hint=(0.5, 1), background_normal='', background_color=(0.3, 0.6, 1, 1))
        self.yes.radius = [50, 50, 50, 50]
        self.yes.bind(on_press=self.go_to_eat_out)
        layout2.add_widget(self.yes)
        
        # "No" button with oval shape
        self.no = Button(text="No", size_hint=(0.5, 1), background_normal='', background_color=(1, 0.5, 0.5, 1))
        self.no.radius = [50, 50, 50, 50]
        self.no.bind(on_press=self.go_to_eat_out)
        layout2.add_widget(self.no)
        
        # Add the button layout to the main layout
        layout.add_widget(layout2)
        self.add_widget(layout)

    def go_to_eat_out(self, instance):
        self.manager.current = "eat_out"




class EatOutScreen(Screen):
    def __init__(self, **kwargs):
        super(EatOutScreen, self).__init__(**kwargs)
        
        # Vertical layout for the question
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Label(text="Do you eat out often?", font_size=32))  # Title
        
        # Horizontal layout for buttons
        layout2 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=100, spacing=10)

        burger_image = Image(source="burger.png", size_hint=(1, 0.6))  # Adjust size_hint as needed
        layout.add_widget(burger_image)  # Add the image widget to the layout
        
        # "Yes" button with oval shape
        self.yes = Button(text="Yes", size_hint=(0.5, 1), background_normal='', background_color=(0.3, 0.6, 1, 1))
        self.yes.radius = [50, 50, 50, 50]
        self.yes.bind(on_press=self.go_to_home)
        layout2.add_widget(self.yes)
        
        # "No" button with oval shape
        self.no = Button(text="No", size_hint=(0.5, 1), background_normal='', background_color=(1, 0.5, 0.5, 1))
        self.no.radius = [50, 50, 50, 50]
        self.no.bind(on_press=self.go_to_home)
        layout2.add_widget(self.no)
        
        # Add the question layout and button layout to the screen
        layout.add_widget(layout2)
        self.add_widget(layout)

    def go_to_home(self, instance):
        self.manager.current = "home"


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.daystreak = 12
        self.moneys = 13
        # Set up the layout and widgets
        self.layout = BoxLayout(orientation="vertical", padding=40, spacing=10)
        self.layout.add_widget(Label(text="Streak: " + str(self.daystreak) + " days", font_size = 45, halign = "right" ))
        img = Image(source = "fire.png", size_hint = (1, 0.6))
        self.layout.add_widget(img)
        self.layout.add_widget(Label(text="Savings: £" + str(13), font_size = 45, halign = "right" ))

        # Set the target and current progress values
        self.aim = 50
        self.current = 5
        self.count = 0
        
        # Create the ProgressBar and add it to the layout once
        self.progress_bar = ProgressBar(max=self.aim, value=self.count)
        self.layout.add_widget(self.progress_bar)

        # Add the layout to the screen's widget tree
        self.add_widget(self.layout)

    def on_enter(self):
        # Schedule the progress bar update when the screen is displayed
        Clock.schedule_interval(self.update_progress, 0.15)

    def update_progress(self, dt):
        # Increment the progress bar's value by 1 each update
        if self.count < self.current:
            self.count += 1
            self.progress_bar.value = self.count
        else:
            # Stop updating when the progress reaches the current value
            Clock.unschedule(self.update_progress)


class ChallengeScreen(Screen):
    def __init__(self, **kwargs):
        super(ChallengeScreen, self).__init__(**kwargs)
        
        # Vertical layout for the challenge display
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        
        # Title label
        layout.add_widget(Label(text="Today's Saving Challenge", font_size=32))
        
        # Challenge label
        self.challenge_label = Label(text=self.get_daily_challenge(), font_size=24)
        layout.add_widget(self.challenge_label)
        
        # Button to go back to the previous screen
        back_button = Button(text="Back", size_hint=(0.5, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def get_daily_challenge(self):
        # Generate a challenge based on today's date
        today = datetime.now().date()  # Get today's date
        random.seed(today.toordinal())  # Use the ordinal value of the date as the seed
        return random.choice(SAVING_CHALLENGES)

    def go_back(self, instance):
        self.manager.current = "days"  # Change this to your desired previous screen




# Define the main app
class LoginApp(App):
    def build(self):
        # Create the ScreenManager
        sm = ScreenManager()
        
        # Add both screens to the manager
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(WeeklySave(name = "save"))
        sm.add_widget(DayScreen(name="days"))        
        sm.add_widget(CoffeeScreen(name= "coffee"))
        sm.add_widget(SmokeScreen(name="smoke"))
        sm.add_widget(EatOutScreen(name="eat_out"))        
        sm.add_widget(HomeScreen(name = "home"))
        sm.add_widget(ChallengeScreen(name = "challenge"))

        
        return sm


if __name__ == "__main__":
    LoginApp().run()
