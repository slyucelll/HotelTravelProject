import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os
import datetime


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


class MyReservationsScreen(tk.Frame):
    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.on_back = on_back
        self.current_index = None

        # ==== BACKGROUND ====
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "reservations_screen.jpg"
        )

        if os.path.exists(img_path):
            original = Image.open(img_path)
            resized = original.resize((1200, 700))
            self.bg_image = ImageTk.PhotoImage(resized)
            bg = tk.Label(self, image=self.bg_image)
            bg.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.configure(bg="white")

        # ==== REZERVASYON LİSTESİ ====
        # App içinden gelen gerçek listeyi kullan
        self.reservations = getattr(self.master, "reservations", [])

        # Eğer hiç yoksa demo amaçlı 2 tane dummy rezervasyon koy
        if not self.reservations:
            self.reservations = [
                {
                    "id": "1001",
                    "hotel_name": "StayFlow Beach Resort",
                    "address": "123 Ocean Road, Nice, France",
                    "location": "Nice, France",
                    "room_type": "Deluxe Sea View",
                    "guests": "2",
                    "check_in": "2026-07-10",
                    "check_out": "2026-07-14",
                    "total_price": "624€",
                    "payment_status": "Not Paid",
                },
                {
                    "id": "1002",
                    "hotel_name": "Grand City Hotel",
                    "address": "Beyoglu, Istanbul, Turkey",
                    "location": "Istanbul, Turkey",
                    "room_type": "Standard Double",
                    "guests": "3",
                    "check_in": "2026-08-01",
                    "check_out": "2026-08-05",
                    "total_price": "420€",
                    "payment_status": "Paid",
                },
            ]
            # App tarafında da olsun
            if hasattr(self.master, "reservations"):
                self.master.reservations = self.reservations

        # ==============================
        #   INPUT ALANLARI
        # ==============================

        # ---- Reservation ID (isteğe bağlı, sadece LOAD için) ----
        vcmd = (self.register(self._validate_int), "%P")

        self.res_id_entry = tk.Entry(
            self,
            width=15,
            font=("Arial", 12),
            bd=2,
            relief="groove",
            validate="key",
            validatecommand=vcmd,
        )
        self.res_id_entry.place(relx=0.41, rely=0.26, anchor="w")

        # ID yanındaki LOAD butonu
        load_btn = ModernButton(
            self,
            text="LOAD",
            width=8,
            command=self.load_reservation_by_id
        )
        load_btn.place(relx=0.58, rely=0.26, anchor="w")

        # ---- Hotel Name ----
        self.hotel_name_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.hotel_name_entry.place(relx=0.56, rely=0.34, anchor="center")

        # ---- Location (sol sütun) ----
        self.location_entry = tk.Entry(
            self,
            width=25,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.location_entry.place(relx=0.31, rely=0.44, anchor="w")

        # ---- Room Type (combo) ----
        self.room_type_combo = ttk.Combobox(
            self,
            values=[
                "Single Room",
                "Double Room",
                "Twin Room",
                "Suite",
                "Deluxe",
                "Family Room",
            ],
            width=23,
            font=("Arial", 12)
        )
        self.room_type_combo.place(relx=0.31, rely=0.54, anchor="w")

        # ---- Total Price ----
        self.total_price_entry = tk.Entry(
            self,
            width=15,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.total_price_entry.place(relx=0.31, rely=0.65, anchor="w")

        # ---- Check-in ----
        self.checkin_entry = DateEntry(
            self,
            width=15,
            font=("Arial", 12),
            date_pattern="yyyy-mm-dd"
        )
        self.checkin_entry.place(relx=0.31, rely=0.75, anchor="w")

        # ---- Address (sağ sütun) ----
        self.address_entry = tk.Entry(
            self,
            width=35,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.address_entry.place(relx=0.64, rely=0.44, anchor="w")

        # ---- Guests (combo) ----
        self.guests_combo = ttk.Combobox(
            self,
            values=["1", "2", "3", "4", "5", "6"],
            width=10,
            font=("Arial", 12)
        )
        self.guests_combo.place(relx=0.63, rely=0.54, anchor="w")

        # ---- Payment Status (combo) ----
        self.payment_status_combo = ttk.Combobox(
            self,
            values=["Not Paid", "Paid"],
            width=12,
            font=("Arial", 12)
        )
        self.payment_status_combo.place(relx=0.70, rely=0.64, anchor="w")

        # ---- Check-out ----
        self.checkout_entry = DateEntry(
            self,
            width=15,
            font=("Arial", 12),
            date_pattern="yyyy-mm-dd"
        )
        self.checkout_entry.place(relx=0.66, rely=0.75, anchor="w")

        # ==============================
        #       BUTONLAR (ALTA)
        # ==============================

        # Back → Travel Menu
        back_btn = ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back
        )
        back_btn.place(relx=0.20, rely=0.86, anchor="center")

        # Go To Payment (ID zorunlu değil)
        pay_btn = ModernButton(
            self,
            text="Go To Payment",
            width=16,
            command=self.go_to_payment
        )
        pay_btn.place(relx=0.50, rely=0.86, anchor="center")

        # Cancel Reservation
        cancel_btn = ModernButton(
            self,
            text="Cancel Reservation",
            width=18,
            command=self.cancel_reservation
        )
        cancel_btn.place(relx=0.80, rely=0.86, anchor="center")

    # ==============================
    #       HELPER FONKSİYONLAR
    # ==============================

    def _validate_int(self, new_value: str) -> bool:
        """Reservation ID alanına sadece integer girilsin (boş da olabilir)."""
        if new_value == "":
            return True
        return new_value.isdigit()

    def _fill_from_reservation(self, res: dict):
        self.res_id_entry.delete(0, tk.END)
        if res.get("id") is not None:
            self.res_id_entry.insert(0, str(res["id"]))

        self.hotel_name_entry.delete(0, tk.END)
        self.hotel_name_entry.insert(0, res.get("hotel_name", ""))

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, res.get("address", ""))

        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, res.get("location", ""))

        self.room_type_combo.set(res.get("room_type", ""))
        self.guests_combo.set(str(res.get("guests", "")))
        self.payment_status_combo.set(res.get("payment_status", ""))

        try:
            self.checkin_entry.set_date(res.get("check_in", datetime.date.today()))
            self.checkout_entry.set_date(res.get("check_out", datetime.date.today()))
        except Exception:
            today = datetime.date.today()
            self.checkin_entry.set_date(today)
            self.checkout_entry.set_date(today)

        self.total_price_entry.delete(0, tk.END)
        self.total_price_entry.insert(0, res.get("total_price", ""))

    # ---- LOAD BUTTON ----
    def load_reservation_by_id(self):
        """Reservation ID girilip LOAD'e basılınca çağrılır."""
        res_id = self.res_id_entry.get().strip()

        if not res_id:
            messagebox.showinfo("Load", "Please enter a reservation ID.")
            return

        if not res_id.isdigit():
            messagebox.showerror("Load", "Reservation ID must be a number.")
            return

        for i, res in enumerate(self.reservations):
            if str(res.get("id")) == res_id:
                self.current_index = i
                self._fill_from_reservation(res)
                messagebox.showinfo("Load", f"Reservation {res_id} loaded.")
                return

        self.current_index = None
        messagebox.showwarning("Load", "No reservation found with this ID.")

    # ---- FORMDAKİ VERİDEN REZERVASYON OBJESİ OLUŞTUR ----
    def _get_reservation_from_form(self) -> dict:
        """Şu anda ekranda görünen alanlardan bir reservation dict'i üretir."""
        try:
            check_in = self.checkin_entry.get_date()
            check_out = self.checkout_entry.get_date()
        except Exception:
            today = datetime.date.today()
            check_in = check_out = today

        return {
            "id": self.res_id_entry.get().strip() or None,
            "hotel_name": self.hotel_name_entry.get().strip(),
            "address": self.address_entry.get().strip(),
            "location": self.location_entry.get().strip(),
            "room_type": self.room_type_combo.get().strip(),
            "guests": self.guests_combo.get().strip(),
            "check_in": check_in,
            "check_out": check_out,
            "total_price": self.total_price_entry.get().strip(),
            "payment_status": self.payment_status_combo.get().strip() or "Not Paid",
        }

    # ==============================
    #       GO TO PAYMENT
    # ==============================
    def go_to_payment(self):
        """Hiçbir kontrol yapmadan Payment ekranına geç."""
        try:
            # Reservation göndermiyoruz, sadece ekranı açıyoruz
            self.master.show_payment(None)
        except AttributeError:
            messagebox.showerror(
                "Navigation error",
                "App içinde show_payment(...) fonksiyonu tanımlı değil."
            )
    # ==============================
    #       CANCEL FONKSİYONU
    # ==============================
    def cancel_reservation(self):
        if messagebox.askyesno(
            "Cancel Reservation",
            "Are you sure you want to cancel this reservation?"
        ):
            self.payment_status_combo.set("Not Paid")
            messagebox.showinfo("Cancelled", "Reservation is marked as cancelled.")