import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os


class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master,
            font=("Arial", 12, "bold"),
            fg="#1f1f1f",
            bg="#ffffff",
            activebackground="#e6e6e6",
            activeforeground="#000000",
            relief="flat",
            bd=2,
            highlightthickness=0,
            padx=12,
            pady=6,
            **kwargs
        )
        self.configure(
            borderwidth=1,
            highlightbackground="#bbbbbb",
            highlightcolor="#bbbbbb"
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self["bg"] = "#f0f0f0"

    def on_leave(self, event):
        self["bg"] = "#ffffff"


class SearchHotelScreen(tk.Frame):
    """
    - CreateTravelPlanScreen'den plan_data ile açılabilir
      (destination + tarihler otomatik dolar).
    - Menüden direkt açılabilir (plan_data=None, her şey boş başlar).

    Otel sadece SEARCH'e basınca listelenir.
    Save Reservation:
      -> self.master.add_reservation(reservation_data)
      -> self.master.show_my_reservations()
    """

    def __init__(self, master, on_back, plan_data=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.on_back = on_back
        self.plan_data = plan_data or {}  # None gelirse boş sözlük

        # ==== BACKGROUND ====
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "hotels_screen.jpg"
        )

        if os.path.exists(img_path):
            original = Image.open(img_path)
            resized = original.resize((1200, 700))
            self.bg_image = ImageTk.PhotoImage(resized)
            bg = tk.Label(self, image=self.bg_image)
            bg.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.configure(bg="white")

        # =======================
        #  ÜST TARAF: ARAMA ALANLARI
        # =======================

        # Destination
        self.destination_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.destination_entry.place(relx=0.30, rely=0.32, anchor="w")
        # Create Plan'den geldiysek dolu gelir, menüden geldiysek boş kalır
        self.destination_entry.insert(0, self.plan_data.get("destination", ""))

        # Check-in
        self.checkin_entry = DateEntry(
            self,
            width=15,
            font=("Arial", 12),
            date_pattern="yyyy-MM-dd"
        )
        self.checkin_entry.place(relx=0.33, rely=0.39, anchor="w")
        if self.plan_data.get("start_date"):
            self.checkin_entry.set_date(self.plan_data["start_date"])

        # Check-out
        self.checkout_entry = DateEntry(
            self,
            width=15,
            font=("Arial", 12),
            date_pattern="yyyy-MM-dd"
        )
        self.checkout_entry.place(relx=0.33, rely=0.47, anchor="w")
        if self.plan_data.get("end_date"):
            self.checkout_entry.set_date(self.plan_data["end_date"])

        # SEARCH butonu
        search_btn = ModernButton(
            self,
            text="SEARCH",
            width=12,
            command=self.search_hotels
        )
        search_btn.place(relx=0.60, rely=0.32, anchor="center")

        # =======================
        #  ALT TARAF: SONUÇ LİSTESİ
        # =======================

        self.results_list = tk.Listbox(
            self,
            width=90,
            height=10,
            font=("Arial", 11)
        )
        self.results_list.place(relx=0.23, rely=0.56)

        # Back
        back_btn = ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back
        )
        back_btn.place(relx=0.20, rely=0.83, anchor="center")

        # Save reservation
        save_btn = ModernButton(
            self,
            text="Save Reservation",
            width=18,
            command=self.save_reservation
        )
        save_btn.place(relx=0.72, rely=0.83, anchor="center")

        # ==== Dummy hotel listesi ====
        self.hotels = [
            {
                "hotel_name": "StayFlow Beach Resort",
                "address": "123 Ocean Road, Nice, France",
                "location": "Nice, France",
                "room_type": "Deluxe Sea View",
                "price_per_night": 160
            },
            {
                "hotel_name": "Grand City Hotel",
                "address": "Beyoglu, Istanbul, Turkey",
                "location": "Istanbul, Turkey",
                "room_type": "Standard Double",
                "price_per_night": 110
            },
            {
                "hotel_name": "Alpine View Hotel",
                "address": "Lake Street, Zurich, Switzerland",
                "location": "Zurich, Switzerland",
                "room_type": "Suite",
                "price_per_night": 220
            },
        ]
        # DİKKAT: burada self.search_hotels() ÇAĞIRMIYORUZ
        # yani ekranda otel listesi ancak SEARCH'e basınca dolacak.

    # ==========================
    #     SEARCH HOTELS
    # ==========================
    def search_hotels(self):
        """Destination'a göre basit filtreleme yapıyor."""
        self.results_list.delete(0, tk.END)

        dest = self.destination_entry.get().strip().lower()

        found = False
        for h in self.hotels:
            if dest and dest not in h["location"].lower():
                continue

            line = (
                f"{h['hotel_name']} | {h['location']} | "
                f"{h['room_type']} | {h['price_per_night']} € / night"
            )
            self.results_list.insert(tk.END, line)
            found = True

        if not found:
            self.results_list.insert(tk.END, "No hotels found for this destination.")

    # ==========================
    #   SAVE RESERVATION
    # ==========================
    def save_reservation(self):
        selection = self.results_list.curselection()
        if not selection:
            messagebox.showinfo("Reservation", "Please select a hotel from the list.")
            return

        index = selection[0]

        # Eğer sadece "No hotels found..." satırına tıklanmışsa:
        if index >= len(self.hotels):
            messagebox.showerror("Reservation", "Please select a valid hotel.")
            return

        hotel = self.hotels[index]

        checkin = self.checkin_entry.get_date()
        checkout = self.checkout_entry.get_date()
        if checkout <= checkin:
            messagebox.showerror("Reservation", "Check-out must be after check-in.")
            return

        nights = (checkout - checkin).days
        total_price = hotel["price_per_night"] * nights

        # Plan bilgisi yoksa destination'ı hotel'den doldur
        dest_value = self.plan_data.get("destination")
        if not dest_value:
            dest_value = hotel["location"]

        reservation_data = {
            # plan bilgileri:
            "plan_name": self.plan_data.get("plan_name"),
            "destination": dest_value,
            "guests": self.plan_data.get("guests"),
            "budget_range": self.plan_data.get("budget_range"),
            "check_in": checkin,
            "check_out": checkout,

            # hotel bilgileri:
            "hotel_name": hotel["hotel_name"],
            "address": hotel["address"],
            "location": hotel["location"],
            "room_type": hotel["room_type"],
            "total_price": f"{total_price} €",
            "payment_status": "Not Paid",
        }

        # App içindeki listeye ekle
        try:
            res_id = self.master.add_reservation(reservation_data)
        except AttributeError:
            messagebox.showerror(
                "Error",
                "App içinde add_reservation(reservation_data) fonksiyonu tanımlı değil."
            )
            return

        messagebox.showinfo(
            "Reservation",
            f"Reservation saved.\nReservation ID: {res_id}"
        )

        # Rezervasyonlar ekranına geç
        try:
            self.master.show_my_reservations()
        except AttributeError:
            messagebox.showwarning(
                "Navigation",
                "Reservation saved but show_my_reservations() not found in App."
            )