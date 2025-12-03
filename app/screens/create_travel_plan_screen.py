import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import datetime

# Takvim için (varsa kullanırız)
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None


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


class CreateTravelPlanScreen(tk.Frame):
    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.on_back = on_back

        # ==== BACKGROUND ====
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "create_plan_screenn.jpg"
        )

        img = Image.open(img_path)
        img = img.resize((1200, 700))
        self.bg_image = ImageTk.PhotoImage(img)

        bg = tk.Label(self, image=self.bg_image)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # =======================================================
        #          SADECE INPUT ALANLARI (LABEL YOK)
        #   (Plan Name, Country, City, People, Budget, Dates)
        # =======================================================

        # 1) PLAN NAME
        self.plan_name_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.plan_name_entry.place(relx=0.35, rely=0.30, anchor="w")

        # 2) COUNTRY
        self.country_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.country_entry.place(relx=0.35, rely=0.38, anchor="w")

        # 3) CITY
        self.city_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 13),
            bd=2,
            relief="groove"
        )
        self.city_entry.place(relx=0.35, rely=0.46, anchor="w")

        # 4) NUMBER OF PEOPLE (Spinbox)
        self.people_spin = tk.Spinbox(
            self,
            from_=1,
            to=20,
            width=5,
            font=("Arial", 13)
        )
        self.people_spin.place(relx=0.35, rely=0.52, anchor="w")

        # 5) BUDGET (Combobox / dropdown)
        budget_options = [
            "< 500",
            "500 - 1,000",
            "1,000 - 2,000",
            "2,000 - 5,000",
            "> 5,000"
        ]

        self.budget_combo = ttk.Combobox(
            self,
            values=budget_options,
            state="readonly",
            width=20,
            font=("Arial", 12)
        )
        self.budget_combo.place(relx=0.35, rely=0.60, anchor="w")
        self.budget_combo.set("Select budget range")

        # 6) START DATE
        if DateEntry is not None:
            self.start_date_input = DateEntry(
                self,
                width=18,
                font=("Arial", 12),
                date_pattern="yyyy-mm-dd",
            )
        else:
            self.start_date_input = tk.Entry(
                self,
                width=20,
                font=("Arial", 12),
                bd=2,
                relief="groove"
            )
            self.start_date_input.insert(0, "YYYY-MM-DD")

        self.start_date_input.place(relx=0.35, rely=0.69, anchor="w")

        # 7) END DATE
        if DateEntry is not None:
            self.end_date_input = DateEntry(
                self,
                width=18,
                font=("Arial", 12),
                date_pattern="yyyy-mm-dd",
            )
        else:
            self.end_date_input = tk.Entry(
                self,
                width=20,
                font=("Arial", 12),
                bd=2,
                relief="groove"
            )
            self.end_date_input.insert(0, "YYYY-MM-DD")

        self.end_date_input.place(relx=0.35, rely=0.78, anchor="w")

        # ======================
        #       BUTTONS
        # ======================

        # BACK (sol alt)
        back_btn = ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back
        )
        back_btn.place(relx=0.23, rely=0.83, anchor="center")

        # CREATE PLAN (sağ alt)
        create_btn = ModernButton(
            self,
            text="CREATE PLAN",
            width=16,
            command=self.save_plan
        )
        create_btn.place(relx=0.70, rely=0.83, anchor="center")

    # =============================
    #     VALIDATION & SAVE
    # =============================
    def save_plan(self):
        plan_name = self.plan_name_entry.get().strip()
        country = self.country_entry.get().strip()
        city = self.city_entry.get().strip()
        people = self.people_spin.get().strip()
        budget = self.budget_combo.get().strip()

        start_str = self._get_date_string(self.start_date_input)
        end_str = self._get_date_string(self.end_date_input)

        # Boş alan kontrolü
        if not plan_name or not country or not city or not people or not budget or not start_str or not end_str:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Budget seçilmemiş
        if budget == "Select budget range":
            messagebox.showerror("Error", "Please select a budget range.")
            return

        # Tarih formatı ve mantık
        try:
            start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Dates must be in YYYY-MM-DD format.")
            return

        today = datetime.date.today()

        if start_date < today:
            messagebox.showerror("Error", "Start date cannot be before today.")
            return

        if end_date < start_date:
            messagebox.showerror("Error", "End date cannot be before start date.")
            return

        # Şimdilik sadece bilgi gösteriyoruz, sonra MSSQL'e kaydedersin
        messagebox.showinfo(
            "Success",
            "Travel plan created successfully!\n\n"
            f"Plan: {plan_name}\n"
            f"Country: {country}\n"
            f"City: {city}\n"
            f"People: {people}\n"
            f"Budget: {budget}\n"
            f"Start: {start_date}\n"
            f"End: {end_date}"
        )

    def _get_date_string(self, widget):
        """DateEntry varsa ordan, yoksa normal Entry'den string alır."""
        if DateEntry is not None and isinstance(widget, DateEntry):
            return widget.get()
        else:
            return widget.get().strip()
