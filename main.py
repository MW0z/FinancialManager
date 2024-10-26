from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import hashlib


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class MyApp(App):

    def build(self):
        return LoginScreen()


def signup():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    conf_pwd = input("Confirm password: ")
    
    if conf_pwd == pwd:
        enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        
        with open("credentials.txt", "w") as f:
            f.write(email + "\n")
            f.write(hash1)
        
        print("You have registered successfully!")
    else:
        print("Password is not the same as above! \n")


def login():
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    
    # Hash the password provided by the user
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    
    try:
        with open("credentials.txt", "r") as f:
            stored_email, stored_pwd = f.read().split('\n')
        
        # Check if provided credentials match stored credentials
        if email == stored_email and auth_hash == stored_pwd:
            print("Logged in Successfully!")
        else:
            print("Login failed! \n")
    
    except FileNotFoundError:
        print("No credentials found. Please sign up first.\n")


if __name__ == '__main__':
    MyApp().run()