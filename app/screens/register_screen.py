import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import datetime
import re


# ===== MODERN BUTTON =====
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


# ===== REGISTER SCREEN =====
class RegisterScreen(tk.Frame):
    def __init__(self, master, on_back_to_login, on_register, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.on_back_to_login = on_back_to_login
        self.on_register = on_register

        # ==== BACKGROUND ====
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "register_screen.jpg"
        )

        img = Image.open(img_path)
        img = img.resize((1200, 700))
        self.bg_image = ImageTk.PhotoImage(img)

        tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)

        # =========================
        #      INPUT ALANLARI
        # =========================

        self.first_name = tk.Entry(self, width=30, font=("Arial", 13), bd=2, relief="groove")
        self.first_name.place(relx=0.5, rely=0.32, anchor="center")

        self.last_name = tk.Entry(self, width=30, font=("Arial", 13), bd=2, relief="groove")
        self.last_name.place(relx=0.5, rely=0.40, anchor="center")

        self.email = tk.Entry(self, width=30, font=("Arial", 13), bd=2, relief="groove")
        self.email.place(relx=0.5, rely=0.50, anchor="center")

        self.password = tk.Entry(self, width=30, font=("Arial", 13), bd=2, relief="groove", show="*")
        self.password.place(relx=0.5, rely=0.60, anchor="center")

        self.birthdate = tk.Entry(self, width=30, font=("Arial", 13), bd=2, relief="groove")
        self.birthdate.insert(0, "YYYY-MM-DD")
        self.birthdate.place(relx=0.5, rely=0.71, anchor="center")

        # ======================
        #   USER AGREEMENT
        # ======================
        self.accept_terms = tk.BooleanVar()

        check_btn = tk.Checkbutton(
            self,
            text="I accept the User Agreement",
            variable=self.accept_terms,
            fg="white",
            bg="black",
            selectcolor="black",
            activebackground="black",
            font=("Arial", 10, "bold")
        )
        check_btn.place(relx=0.7, rely=0.8, anchor="center")

        # clickable link
        link = tk.Label(
            self,
            text="(Read Agreement)",
            fg="#00ccff",
            cursor="hand2",
            bg="black",
            font=("Arial", 10, "underline")
        )
        link.place(relx=0.58, rely=0.81, anchor="center")
        link.bind("<Button-1>", self.show_agreement_dialog)

        # ======================
        #      REGISTER BTN
        # ======================
        reg_btn = ModernButton(
            self,
            text="REGISTER",
            width=18,
            command=self.validate_and_register
        )
        reg_btn.place(relx=0.7, rely=0.87, anchor="center")

        # BACK BTN
        back_btn = ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back_to_login
        )
        back_btn.place(relx=0.20, rely=0.84)


    # ===== USER AGREEMENT DIALOG =====
    def show_agreement_dialog(self, event=None):
        dialog = tk.Toplevel(self)
        dialog.title("User Agreement")
        dialog.geometry("600x500")
        dialog.grab_set()

        text_box = tk.Text(dialog, wrap="word", font=("Arial", 11))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        agreement_text = """
User Agreement (English)

1. You agree to provide accurate and real personal information.
2. You confirm you are at least 18 years old.
3. You consent to the processing of your data within the StayFlow system.
4. StayFlow is not responsible for incorrect or fraudulent user information.
5. All bookings must comply with the local rules and restrictions.
6. Any misuse of the system may result in account suspension.

Click ACCEPT to confirm you have read and agreed.
"""
        text_box.insert("1.0", agreement_text)
        text_box.config(state="disabled")

        tk.Button(dialog, text="ACCEPT", width=12, command=dialog.destroy).pack(pady=10)

    # ===== VALIDATION + 18 AGE CHECK =====
    def validate_and_register(self):
        fname = self.first_name.get().strip()
        lname = self.last_name.get().strip()
        email = self.email.get().strip()
        pw = self.password.get().strip()
        dob = self.birthdate.get().strip()

        # boş kontrolü
        if not fname or not lname or not email or not pw or not dob:
            messagebox.showerror("Error", "All fields are required.")
            return

        # e-mail format
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            messagebox.showerror("Error", "Invalid e-mail format.")
            return

        # user agreement
        if not self.accept_terms.get():
            messagebox.showerror("Error", "You must accept the User Agreement.")
            return

        # doğum tarihi valid mi
        try:
            year, month, day = map(int, dob.split("-"))
            birth = datetime.date(year, month, day)
        except:
            messagebox.showerror("Error", "Birthdate must be YYYY-MM-DD.")
            return

        # yaş hesaplama
        today = datetime.date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        if age < 18:
            messagebox.showerror("Error", "You must be at least 18 to register.")
            return

        # başarılı → App.register_user(fname, ...)
        self.on_register(fname, lname, email, pw, dob)

        messagebox.showinfo("Success", "Registration successful!")
        self.on_back_to_login()
