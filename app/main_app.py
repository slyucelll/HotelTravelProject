import tkinter as tk

from app.screens.welcome_screen import WelcomeScreen
from app.screens.admin_login_screen import AdminLoginScreen
from app.screens.user_login_screen import UserLoginScreen
from app.screens.register_screen import RegisterScreen
from app.screens.travel_menu_screen import TravelMenuScreen
from app.screens.create_travel_plan_screen import CreateTravelPlanScreen
from app.screens.travel_plans_screen import MyTravelPlansScreen
from app.screens.reservations_screen import MyReservationsScreen
from app.screens.search_hotels_screen import SearchHotelScreen
from app.screens.payment_screen import PaymentScreen   # dosyanın en üstüne ekle

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Travel Planning & Hotel Reservation")
        self.geometry("1200x700")
        self.configure(bg="white")

        self.current_screen = None
        self.show_welcome()
        self.current_user_id = 1
        self.reservations = []
        self.next_reservation_id = 1

    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None

    # ========== WELCOME ==========
    def show_welcome(self):
        self.clear_screen()
        self.current_screen = WelcomeScreen(
            master=self,
            on_admin_login=self.show_admin_login,
            on_user_login=self.show_user_login
        )
        self.current_screen.pack(fill="both", expand=True)

    # ========== ADMIN LOGIN ==========
    def show_admin_login(self):
        self.clear_screen()
        self.current_screen = AdminLoginScreen(
            master=self,
            on_back=self.show_welcome
        )
        self.current_screen.pack(fill="both", expand=True)

    # ========== USER LOGIN ==========
    def show_user_login(self):
        self.clear_screen()
        self.current_screen = UserLoginScreen(
            master=self,
            on_back=self.show_welcome
        )
        self.current_screen.pack(fill="both", expand=True)

    # ========== REGISTER ==========
    def show_register(self):
        self.clear_screen()
        self.current_screen = RegisterScreen(
            master=self,
            on_back_to_login=self.show_user_login,
            on_register=self.register_user
        )
        self.current_screen.pack(fill="both", expand=True)

    def register_user(self, fname, lname, email, pw, dob):
        print("Yeni kullanıcı kaydedildi:", fname, lname, email, dob)

    # ========== TRAVEL MENU ==========
    def show_travel_menu(self):
        self.clear_screen()
        self.current_screen = TravelMenuScreen(
            master=self,
            on_back=self.show_user_login
        )
        self.current_screen.pack(fill="both", expand=True)

    # ========== CREATE TRAVEL PLAN ==========
    def show_create_travel_plan(self):
        self.clear_screen()
        self.current_screen = CreateTravelPlanScreen(
            master=self,
            on_back=self.show_travel_menu
        )
        self.current_screen.pack(fill="both", expand=True)

    # ========== MY TRAVEL PLANS ==========
    def show_my_travel_plans(self):
        self.clear_screen()
        self.current_screen = MyTravelPlansScreen(
            master=self,
            on_back=self.show_travel_menu
        )
        self.current_screen.pack(fill="both", expand=True)

    # ========== MY RESERVATIONS ==========
    def show_my_reservations(self):
        self.clear_screen()
        self.current_screen = MyReservationsScreen(
            master=self,
            on_back=self.show_travel_menu
        )
        self.current_screen.pack(fill="both", expand=True)

    def show_search_hotel(self, plan_data=None):
        self.clear_screen()
        self.current_screen = SearchHotelScreen(
            master=self,
            on_back=self.show_travel_menu,
            plan_data=plan_data
        )
        self.current_screen.pack(fill="both", expand=True)

    def add_reservation(self, reservation_data: dict) -> int:
        reservation = {
            "id": self.next_reservation_id,
            "user_id": self.current_user_id,
            **reservation_data
        }
        self.reservations.append(reservation)
        self.next_reservation_id += 1
        return reservation["id"]

    def get_reservations_for_current_user(self):
        return [r for r in self.reservations if r["user_id"] == self.current_user_id]

    def show_payment(self, reservation=None):
        """
        Payment ekranını açar.
        reservation: dict ya da None (şimdilik None da gönderebiliriz).
        """
        self.clear_screen()
        self.current_screen = PaymentScreen(
            master=self,
            reservation=reservation,
            on_back=self.show_my_reservations
        )
        self.current_screen.pack(fill="both", expand=True)
if __name__ == "__main__":
    app = App()
    app.mainloop()