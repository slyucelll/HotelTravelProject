import tkinter as tk

from app.screens import travel_menu_screen
from app.screens.welcome_screen import WelcomeScreen
from app.screens.admin_login_screen import AdminLoginScreen
from app.screens.user_login_screen import UserLoginScreen
from app.screens.register_screen import RegisterScreen
from app.screens.travel_menu_screen import TravelMenuScreen
from app.screens.create_travel_plan_screen import CreateTravelPlanScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Travel Planning & Hotel Reservation")
        self.geometry("1200x700")
        self.configure(bg="white")

        self.current_screen = None
        self.show_welcome()

    def clear_screen(self):
        """Ekrandaki mevcut ekranı siler."""
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None

    # ==========================================
    # 1) WELCOME SCREEN
    # ==========================================
    def show_welcome(self):
        self.clear_screen()
        self.current_screen = WelcomeScreen(
            master=self,
            on_admin_login=self.show_admin_login,
            on_user_login=self.show_user_login
        )
        self.current_screen.pack(fill="both", expand=True)

    # ==========================================
    # 2) ADMIN LOGIN
    # ==========================================
    def show_admin_login(self):
        self.clear_screen()
        self.current_screen = AdminLoginScreen(
            master=self,
            on_back=self.show_welcome
        )
        self.current_screen.pack(fill="both", expand=True)

    # ==========================================
    # 3) USER LOGIN
    # ==========================================
    def show_user_login(self):
        self.clear_screen()
        self.current_screen = UserLoginScreen(
            master=self,
            on_back=self.show_welcome
        )
        self.current_screen.pack(fill="both", expand=True)

    # ==========================================
    # 4) REGISTER SCREEN
    # ==========================================
    def show_register(self):
        self.clear_screen()
        self.current_screen = RegisterScreen(
            master=self,
            on_back_to_login=self.show_user_login,   # register → login'e geri dön
            on_register=self.register_user           # gerçek kayıt burada yapılır
        )
        self.current_screen.pack(fill="both", expand=True)

    # ==========================================
    # 5) Register işlemi (şimdilik konsola yazıyoruz)
    # ==========================================
    def register_user(self, fname, lname, email, pw, dob):
        print("Yeni kullanıcı kaydedildi:")
        print("Ad:", fname)
        print("Soyad:", lname)
        print("Email:", email)
        print("Doğum tarihi:", dob)
        # İLERİDE buraya MSSQL INSERT yazacağız

    def show_travel_menu(self):
        self.clear_screen()
        self.current_screen = travel_menu_screen.TravelMenuScreen(
            master=self,
            on_back=self.show_user_login
        )
        self.current_screen.pack(fill="both", expand=True)
    def show_create_travel_plan(self):
        self.clear_screen()
        self.current_screen = CreateTravelPlanScreen(
            master=self,
            on_back=self.show_travel_menu   # geri dönünce travel menu'ye
        )
        self.current_screen.pack(fill="both", expand=True)


# Uygulamayı çalıştır
if __name__ == "__main__":
    app = App()
    app.mainloop()
