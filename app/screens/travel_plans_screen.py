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


class MyTravelPlansScreen(tk.Frame):
    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.on_back = on_back

        # --- basit dummy plan listesi (sonra MSSQL gelecek) ---
        self.plans = [
            {
                "name": "Summer in Rome",
                "destination": "Italy - Rome",
                "dates": "2026-07-10 → 2026-07-18",
                "guests": "2",
                "budget": "1,000 - 2,000",
            },
            {
                "name": "Weekend in Paris",
                "destination": "France - Paris",
                "dates": "2026-05-01 → 2026-05-03",
                "guests": "1",
                "budget": "< 500",
            },
            {
                "name": "Trip to Istanbul",
                "destination": "Turkey - Istanbul",
                "dates": "2026-09-10 → 2026-09-15",
                "guests": "4",
                "budget": "500 - 1,000",
            },
        ]
        self.current_index = None  # şu an hangi plan seçili

        # ========= BACKGROUND =========
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "travel_plan_screen.jpg"
        )

        original = Image.open(img_path)
        resized = original.resize((1200, 700))
        self.bg_image = ImageTk.PhotoImage(resized)

        bg = tk.Label(self, image=self.bg_image)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # =====================================================
        #  SOLDİKİ LABEL'LARIN YANINA GELECEK INPUT ALANLARI
        # =====================================================

        # Search By Travel Name
        self.search_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.search_entry.place(relx=0.42, rely=0.30, anchor="w")

        search_btn = ModernButton(
            self,
            text="SEARCH",
            width=10,
            command=self.search_plan
        )
        search_btn.place(relx=0.75, rely=0.30, anchor="center")

        # Plan Name
        self.plan_name_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.plan_name_entry.place(relx=0.42, rely=0.38, anchor="w")

        # Destination
        self.destination_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.destination_entry.place(relx=0.42, rely=0.47, anchor="w")

        # Dates
        self.dates_entry = tk.Entry(
            self,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.dates_entry.place(relx=0.42, rely=0.55, anchor="w")

        # Guests
        self.guests_entry = tk.Entry(
            self,
            width=10,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.guests_entry.place(relx=0.42, rely=0.63, anchor="w")

        # Budget
        self.budget_entry = tk.Entry(
            self,
            width=20,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.budget_entry.place(relx=0.42, rely=0.70, anchor="w")

        # =====================================================
        #                ALTTA BUTONLAR (FRAME YOK!)
        # =====================================================

        # VIEW
        self.view_btn = ModernButton(
            self,
            text="VIEW",
            width=10,
            command=self.view_plan
        )
        self.view_btn.place(relx=0.45, rely=0.80, anchor="center")

        # EDIT
        self.edit_btn = ModernButton(
            self,
            text="EDIT",
            width=10,
            command=self.edit_plan
        )
        self.edit_btn.place(relx=0.60, rely=0.80, anchor="center")

        # DELETE
        self.delete_btn = ModernButton(
            self,
            text="DELETE",
            width=10,
            command=self.delete_plan
        )
        self.delete_btn.place(relx=0.75, rely=0.80, anchor="center")

        # Back (sol altta)
        back_btn = ModernButton(
            self,
            text="← Back",
            width=10,
            command=self.on_back
        )
        back_btn.place(relx=0.24, rely=0.80, anchor="center")

    # ==========================
    #        HELPERS
    # ==========================
    def _fill_entries_from_plan(self, plan):
        """Plan sözlüğündeki değerleri inputlara yazar."""
        self.plan_name_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.dates_entry.delete(0, tk.END)
        self.guests_entry.delete(0, tk.END)
        self.budget_entry.delete(0, tk.END)

        self.plan_name_entry.insert(0, plan["name"])
        self.destination_entry.insert(0, plan["destination"])
        self.dates_entry.insert(0, plan["dates"])
        self.guests_entry.insert(0, plan["guests"])
        self.budget_entry.insert(0, plan["budget"])

    def _clear_entries(self):
        self.plan_name_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.dates_entry.delete(0, tk.END)
        self.guests_entry.delete(0, tk.END)
        self.budget_entry.delete(0, tk.END)

    # ==========================
    #        SEARCH
    # ==========================
    def search_plan(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showinfo("Search", "Please enter a travel name to search.")
            return

        for i, plan in enumerate(self.plans):
            if keyword in plan["name"].lower():
                self.current_index = i
                self._fill_entries_from_plan(plan)
                messagebox.showinfo("Search", f"Plan found: {plan['name']}")
                return

        self.current_index = None
        self._clear_entries()
        messagebox.showwarning("Search", "No travel plan found with that name.")

    # ==========================
    #        VIEW
    # ==========================
    def view_plan(self):
        # Eğer önceden search yapılmışsa current_index bellidir
        if self.current_index is None:
            # Otomatik olarak önce search denesin
            self.search_plan()
            return

        # current_index varsa zaten _fill_entries_from_plan çağrılmış durumda
        # yine de emin olalım:
        plan = self.plans[self.current_index]
        self._fill_entries_from_plan(plan)

    # ==========================
    #        EDIT
    # ==========================
    def edit_plan(self):
        if self.current_index is None:
            messagebox.showwarning("Edit", "Please search and select a travel plan first.")
            return

        # Inputlardan yeni değerleri al
        new_name = self.plan_name_entry.get().strip()
        new_destination = self.destination_entry.get().strip()
        new_dates = self.dates_entry.get().strip()
        new_guests = self.guests_entry.get().strip()
        new_budget = self.budget_entry.get().strip()

        if not new_name:
            messagebox.showerror("Edit", "Plan name cannot be empty.")
            return

        plan = self.plans[self.current_index]
        plan["name"] = new_name
        plan["destination"] = new_destination
        plan["dates"] = new_dates
        plan["guests"] = new_guests
        plan["budget"] = new_budget

        messagebox.showinfo("Edit", "Travel plan updated successfully.")

    # ==========================
    #        DELETE
    # ==========================
    def delete_plan(self):
        if self.current_index is None:
            messagebox.showwarning("Delete", "Please search and select a travel plan first.")
            return

        plan = self.plans[self.current_index]
        confirm = messagebox.askyesno("Delete", f"Delete plan: {plan['name']} ?")
        if confirm:
            self.plans.pop(self.current_index)
            self.current_index = None
            self._clear_entries()
            messagebox.showinfo("Delete", "Plan deleted.")
