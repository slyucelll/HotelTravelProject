import tkinter as tk
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
        self.bind("<Enter>", lambda e: self.config(bg="#f0f0f0"))
        self.bind("<Leave>", lambda e: self.config(bg="#ffffff"))


class AdminMenuScreen(tk.Frame):
    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.on_back = on_back

        # ==== BACKGROUND ====
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "admin_menu_screen.jpg"
        )

        if os.path.exists(img_path):
            img = Image.open(img_path).resize((1200, 700))
            self.bg_image = ImageTk.PhotoImage(img)
            tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.configure(bg="white")

        # ===============================
        #        MANAGEMENT BUTTONS
        # ===============================

        # Left column
        ModernButton(
            self,
            text="Country & City Management",
            width=25,
            command=self.master.show_country_city_mgmt
        ).place(relx=0.18, rely=0.52, anchor="w")

        ModernButton(
            self,
            text="Hotel Management",
            width=25,
            command=self.master.show_hotel_mgmt
        ).place(relx=0.18, rely=0.61, anchor="w")

        ModernButton(
            self,
            text="Users Management",
            width=25,
            command=self.master.show_users_mgmt
        ).place(relx=0.18, rely=0.70, anchor="w")

        # Right column
        ModernButton(
            self,
            text="Reservations Management",
            width=25,
            command=self.master.show_reservations_mgmt
        ).place(relx=0.55, rely=0.52, anchor="w")

        ModernButton(
            self,
            text="Room Management",
            width=25,
            command=self.master.show_room_mgmt
        ).place(relx=0.55, rely=0.61, anchor="w")

        # ===============================
        #          BACK BUTTON
        # ===============================
        ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back
        ).place(relx=0.15, rely=0.85, anchor="w")