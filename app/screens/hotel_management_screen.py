import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os


class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master,
            font=("Arial", 11, "bold"),
            fg="#1f1f1f",
            bg="#ffffff",
            activebackground="#e6e6e6",
            activeforeground="#000000",
            relief="flat",
            bd=1,
            highlightthickness=0,
            padx=10,
            pady=6,
            **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg="#f0f0f0"))
        self.bind("<Leave>", lambda e: self.config(bg="#ffffff"))


class HotelManagementScreen(tk.Frame):

    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.on_back = on_back

        # Background
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "hotel_mg_screen.jpg"
        )
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((1200, 700))
                self.bg_image = ImageTk.PhotoImage(img)
                tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)
            else:
                self.configure(bg="white")
        except:
            self.configure(bg="white")

        # Dummy hotel data
        self.hotels = [
            {
                "id": 1,
                "name": "StayFlow Beach Resort",
                "country": "France",
                "city": "Nice",
                "address": "123 Ocean Road",
                "rooms": 120,
                "price_per_night": 160,
                "status": "Active"
            },
            {
                "id": 2,
                "name": "Grand City Hotel",
                "country": "Turkey",
                "city": "Istanbul",
                "address": "Beyoglu 45",
                "rooms": 80,
                "price_per_night": 110,
                "status": "Active"
            }
        ]
        self.next_hotel_id = 3
        self.current_index = None

        # -----------------------------------
        # LEFT SIDE — HOTEL LIST
        # -----------------------------------
        self.hotels_listbox = tk.Listbox(self, width=49, height=20, font=("Arial", 11))
        self.hotels_listbox.place(relx=0.1, rely=0.24, anchor="nw")
        self.hotels_listbox.bind("<<ListboxSelect>>", self.on_hotel_selected)

        # Search input
        self.search_var = tk.StringVar()
        tk.Entry(self, textvariable=self.search_var, width=28, font=("Arial", 11))\
            .place(relx=0.10, rely=0.64, anchor="nw")

        ModernButton(self, text="Search", width=10, command=self.search_hotels)\
            .place(relx=0.10, rely=0.70, anchor="nw")

        ModernButton(self, text="Reload All", width=12, command=self.reload_hotels_list)\
            .place(relx=0.10, rely=0.75, anchor="nw")

        # -----------------------------------
        # RIGHT SIDE — INPUT FIELDS (NO LABELS)
        # -----------------------------------
        base_x = 0.59
        y = 0.23
        gap = 0.07

        # JUST INPUTS — NO LABELS
        self.name_entry = tk.Entry(self, width=40, font=("Arial", 11))
        self.name_entry.place(relx=0.61, rely=0.23)

        self.country_entry = tk.Entry(self, width=25, font=("Arial", 11))
        self.country_entry.place(relx=0.59, rely=0.31)

        self.city_entry = tk.Entry(self, width=25, font=("Arial", 11))
        self.city_entry.place(relx=0.59, rely=0.40)

        self.address_entry = tk.Entry(self, width=45, font=("Arial", 11))
        self.address_entry.place(relx=base_x, rely=0.47)

        self.rooms_spin = tk.Spinbox(self, from_=1, to=2000, width=6, font=("Arial", 11))
        self.rooms_spin.place(relx=0.63, rely=0.57)

        self.price_entry = tk.Entry(self, width=12, font=("Arial", 11))
        self.price_entry.place(relx=0.62, rely=0.65)

        self.status_combo = ttk.Combobox(self, values=["Active", "Inactive"], width=14, state="readonly")
        self.status_combo.place(relx=0.58, rely=0.74)
        self.status_combo.set("Active")

        # -----------------------------------
        # BUTTONS
        # -----------------------------------
        ModernButton(self, text="Add Hotel", width=14, command=self.add_hotel)\
            .place(relx=0.48, rely=0.83)

        ModernButton(self, text="Update Selected", width=14, command=self.update_hotel)\
            .place(relx=0.65, rely=0.83)

        ModernButton(self, text="Delete Selected", width=14, command=self.delete_hotel)\
            .place(relx=0.80, rely=0.83)

        ModernButton(self, text="Manage Rooms", width=16, command=self.go_manage_rooms)\
            .place(relx=0.20, rely=0.90)

        ModernButton(self, text="← Back", width=10, command=self.on_back)\
            .place(relx=0.06, rely=0.90)

        self.reload_hotels_list()

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------
    def reload_hotels_list(self):
        self.hotels_listbox.delete(0, tk.END)
        for h in self.hotels:
            text = f"{h['id']:04d} — {h['name']} ({h['city']}, {h['country']})"
            self.hotels_listbox.insert(tk.END, text)
        self._clear_inputs()

    def search_hotels(self):
        q = self.search_var.get().strip().lower()
        self.hotels_listbox.delete(0, tk.END)
        for h in self.hotels:
            if q in h["name"].lower() or q in h["city"].lower() or q in h["country"].lower():
                self.hotels_listbox.insert(
                    tk.END, f"{h['id']:04d} — {h['name']} ({h['city']}, {h['country']})"
                )

    def on_hotel_selected(self, event=None):
        sel = self.hotels_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.hotels_listbox.get(idx)

        try:
            hotel_id = int(item.split("—")[0].strip())
        except:
            return

        for i, h in enumerate(self.hotels):
            if h["id"] == hotel_id:
                self.current_index = i
                self._fill_inputs(h)
                return

    def _fill_inputs(self, h):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, h["name"])

        self.country_entry.delete(0, tk.END)
        self.country_entry.insert(0, h["country"])

        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, h["city"])

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, h["address"])

        self.rooms_spin.delete(0, tk.END)
        self.rooms_spin.insert(0, str(h["rooms"]))

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, str(h["price_per_night"]))

        self.status_combo.set(h["status"])

    def _clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.country_entry.delete(0, tk.END)
        self.city_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.rooms_spin.delete(0, tk.END)
        self.rooms_spin.insert(0, "1")
        self.price_entry.delete(0, tk.END)
        self.status_combo.set("Active")

    # -------------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------------
    def add_hotel(self):
        name = self.name_entry.get().strip()
        country = self.country_entry.get().strip()
        city = self.city_entry.get().strip()

        if not name or not country or not city:
            messagebox.showerror("Error", "Name, Country and City are required.")
            return

        try:
            rooms = int(self.rooms_spin.get())
            price = float(self.price_entry.get())
        except:
            messagebox.showerror("Error", "Rooms and Price must be numbers.")
            return

        hotel = {
            "id": self.next_hotel_id,
            "name": name,
            "country": country,
            "city": city,
            "address": self.address_entry.get().strip(),
            "rooms": rooms,
            "price_per_night": price,
            "status": self.status_combo.get()
        }

        self.hotels.append(hotel)
        self.next_hotel_id += 1
        self.reload_hotels_list()
        messagebox.showinfo("Success", f"Hotel '{name}' added.")

    def update_hotel(self):
        if self.current_index is None:
            messagebox.showinfo("Update", "Select a hotel first.")
            return

        try:
            rooms = int(self.rooms_spin.get())
            price = float(self.price_entry.get())
        except:
            messagebox.showerror("Error", "Rooms/Price must be numbers.")
            return

        h = self.hotels[self.current_index]
        h.update({
            "name": self.name_entry.get().strip(),
            "country": self.country_entry.get().strip(),
            "city": self.city_entry.get().strip(),
            "address": self.address_entry.get().strip(),
            "rooms": rooms,
            "price_per_night": price,
            "status": self.status_combo.get()
        })

        self.reload_hotels_list()
        messagebox.showinfo("Success", "Hotel updated.")

    def delete_hotel(self):
        if self.current_index is None:
            messagebox.showinfo("Delete", "Select a hotel first.")
            return

        h = self.hotels[self.current_index]
        ok = messagebox.askyesno("Confirm", f"Delete '{h['name']}'?")
        if not ok:
            return

        self.hotels.pop(self.current_index)
        self.current_index = None
        self.reload_hotels_list()
        messagebox.showinfo("Deleted", "Hotel deleted.")

    # -------------------------------------------------------------------
    # Navigation
    # -------------------------------------------------------------------
    def go_manage_rooms(self):
        try:
            self.master.show_room_mgmt()
        except:
            messagebox.showinfo("Info", "Room management screen not available yet.")