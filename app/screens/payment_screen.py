import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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


class PaymentScreen(tk.Frame):
    """
    MyReservationsScreen'den reservation objesi ile açılır.
    Arka plandaki görsel hazır; biz sadece input alanlarını ekliyoruz.
    """

    def __init__(self, master, reservation, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.reservation = reservation
        self.on_back = on_back

        # ===== BACKGROUND RESİM =====
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "payment_screen.jpg"
        )

        if os.path.exists(img_path):
            original = Image.open(img_path)
            resized = original.resize((1200, 700))
            self.bg_image = ImageTk.PhotoImage(resized)
            bg = tk.Label(self, image=self.bg_image)
            bg.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.configure(bg="white")

        # ==============================
        # INPUT ALANLARI (LABELS CANVA'DA)
        # ==============================

        # ---- Card Number ----
        self.card_number_entry = tk.Entry(
            self,
            width=25,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.card_number_entry.place(relx=0.40, rely=0.40, anchor="w")

        # ---- CardHolder Name ----
        self.card_holder_entry = tk.Entry(
            self,
            width=25,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.card_holder_entry.place(relx=0.40, rely=0.47, anchor="w")

        # ---- Month ----
        self.month_entry = tk.Entry(
            self,
            width=5,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.month_entry.place(relx=0.40, rely=0.53, anchor="w")

        # ---- Year ----
        self.year_entry = tk.Entry(
            self,
            width=7,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.year_entry.place(relx=0.45, rely=0.53, anchor="w")

        # ---- CVV ----
        self.cvv_entry = tk.Entry(
            self,
            width=6,
            font=("Arial", 13),
            bd=2,
            relief="groove",
            show="*"
        )
        self.cvv_entry.place(relx=0.40, rely=0.61, anchor="w")

        # ==============================
        #        BUTONLAR
        # ==============================

        pay_btn = ModernButton(
            self,
            text="COMPLETE AND CONFIRM PAYMENT",
            width=28,
            command=self.pay_now
        )
        pay_btn.place(relx=0.69, rely=0.78, anchor="center")

        back_btn = ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back
        )
        back_btn.place(relx=0.23, rely=0.78, anchor="center")

    # =================================
    #         PAYMENT LOGIC
    # =================================
    def pay_now(self):
        card_number = self.card_number_entry.get().replace(" ", "")
        holder = self.card_holder_entry.get().strip()
        month = self.month_entry.get().strip()
        year = self.year_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        # ---- Validation ----
        if not card_number or not holder or not month or not year or not cvv:
            messagebox.showerror("Payment", "Please fill in all card information.")
            return

        if not card_number.isdigit() or len(card_number) not in (13, 16):
            messagebox.showerror("Payment", "Card number is not valid.")
            return

        if not month.isdigit() or not (1 <= int(month) <= 12):
            messagebox.showerror("Payment", "Month must be between 1 and 12.")
            return

        if not year.isdigit() or len(year) not in (2, 4):
            messagebox.showerror("Payment", "Year is not valid.")
            return

        if not cvv.isdigit() or len(cvv) not in (3, 4):
            messagebox.showerror("Payment", "CVV must be 3 or 4 digits.")
            return

        # ---- Payment Success ----
        if self.reservation:
            self.reservation["payment_status"] = "Paid"

            # App'in içindeki listeyi güncelle
            if hasattr(self.master, "reservations"):
                for r in self.master.reservations:
                    if str(r.get("id")) == str(self.reservation.get("id")):
                        r["payment_status"] = "Paid"
                        break

        # ---- Messages ----
        messagebox.showinfo("Payment", "Payment completed successfully! 🎉")
        messagebox.showinfo("Reservation", "Reservation created successfully! ✔️")

        # ---- Back to reservations screen ----
        self.on_back()