# app/screens/room_management_screen.py
import tkinter as tk
from tkinter import messagebox, ttk
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


class RoomManagementScreen(tk.Frame):
    """
    Inputlar tek tek x-y verilmiş:
      - hotel_combo
      - room_number_entry (readonly)
      - room_type_combo
      - capacity_combo
      - price_entry
    """

    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.on_back = on_back

        # OPTIONAL BACKGROUND
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "room_mg_screen.jpg"
        )
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path).resize((1200, 700))
                self.bg_image = ImageTk.PhotoImage(img)
                tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)
            except:
                self.configure(bg="white")
        else:
            self.configure(bg="white")

        # Dummy data
        self.rooms = [
            {"id": 1, "hotel": "Hilton",   "room_number": "101", "type": "Single", "capacity": "1", "price": "120"},
            {"id": 2, "hotel": "Hilton",   "room_number": "102", "type": "Double", "capacity": "2", "price": "190"},
            {"id": 3, "hotel": "Marriott", "room_number": "201", "type": "Suite",  "capacity": "4", "price": "350"},
        ]
        self.next_room_id = max(int(r["room_number"]) for r in self.rooms) + 1
        self.current_index = None

        # ---------------- LEFT LISTBOX ----------------
        self.room_listbox = tk.Listbox(self, width=45, height=20, font=("Arial", 12))
        self.room_listbox.place(x=100, y=200)
        self.room_listbox.bind("<<ListboxSelect>>", self.on_select)

        # ---------------- INPUTS (CUSTOM X/Y) ----------------
        # Sana yer değiştirmeyi kolaylaştırmak için HER BİRİ bağımsız koordinatla

        self.hotel_combo = ttk.Combobox(self, values=self._get_hotels(),
                                        state="readonly", width=28, font=("Arial", 12))
        self.hotel_combo.place(x=760, y=195)

        self.room_number_var = tk.StringVar()
        self.room_number_entry = tk.Entry(self, textvariable=self.room_number_var,
                                          width=30, font=("Arial", 13), state="readonly")
        self.room_number_entry.place(x=735, y=253)

        self.room_type_combo = ttk.Combobox(
            self, values=["Single", "Double", "Suite", "Family", "Deluxe"],
            state="readonly", width=27, font=("Arial", 12)
        )
        self.room_type_combo.place(x=760, y=310)

        self.capacity_combo = ttk.Combobox(
            self, values=["1", "2", "3", "4", "5", "6"],
            state="readonly", width=10, font=("Arial", 12)
        )
        self.capacity_combo.place(x=760, y=445)

        self.price_entry = tk.Entry(self, width=18, font=("Arial", 13))
        self.price_entry.place(x=760, y=375)

        # ---------------- BUTTONS ----------------
        ModernButton(self, text="Add Room", width=16, command=self.add_room)\
            .place(x=600, y=510)

        ModernButton(self, text="Update Selected ", width=16, command=self.update_room)\
            .place(x=800, y=510)

        ModernButton(self, text="Delete Selected", width=16, command=self.delete_room)\
            .place(x=1000, y=510)

        ModernButton(self, text="Review All", width=14, command=self.review_all)\
            .place(x=250, y=540)

        ModernButton(self, text="← Back", width=12, command=self.on_back)\
            .place(x=60, y=540)

        # Load list
        self.reload_listbox()

    # -----------------------------------
    # HELPERS
    # -----------------------------------
    def _get_hotels(self):
        hotels = sorted({r["hotel"] for r in self.rooms})
        if not hotels:
            hotels = ["Hilton", "Marriott", "StayFlow"]
        return hotels

    def reload_listbox(self):
        self.room_listbox.delete(0, tk.END)
        for r in self.rooms:
            self.room_listbox.insert(
                tk.END,
                f"{r['room_number']} • {r['hotel']} • {r['type']} • {r['capacity']}p • €{r['price']}"
            )
        self.current_index = None
        self.clear_inputs()

    def clear_inputs(self):
        self.room_number_var.set(str(self.next_room_id))
        self.hotel_combo.set("")
        self.room_type_combo.set("")
        self.capacity_combo.set("")
        self.price_entry.delete(0, tk.END)

    # -----------------------------------
    # SELECT
    # -----------------------------------
    def on_select(self, event):
        sel = self.room_listbox.curselection()
        if not sel:
            return

        idx = sel[0]
        self.current_index = idx
        r = self.rooms[idx]

        self.room_number_var.set(r["room_number"])
        self.hotel_combo.set(r["hotel"])
        self.room_type_combo.set(r["type"])
        self.capacity_combo.set(r["capacity"])
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, r["price"])

    # -----------------------------------
    # ADD
    # -----------------------------------
    def add_room(self):
        hotel = self.hotel_combo.get()
        room_type = self.room_type_combo.get()
        capacity = self.capacity_combo.get()
        price_text = self.price_entry.get().strip()

        if not hotel or not room_type or not capacity:
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        try:
            price = float(price_text) if price_text else 0.0
        except:
            messagebox.showerror("Error", "Price must be a number.")
            return

        room_number = str(self.next_room_id)
        self.next_room_id += 1

        new = {
            "id": int(room_number),
            "hotel": hotel,
            "room_number": room_number,
            "type": room_type,
            "capacity": capacity,
            "price": f"{price:.2f}"
        }
        self.rooms.append(new)
        self.reload_listbox()
        messagebox.showinfo("Added", f"Room {room_number} added.")

    # -----------------------------------
    # UPDATE
    # -----------------------------------
    def update_room(self):
        if self.current_index is None:
            messagebox.showinfo("Info", "Select a room first.")
            return

        hotel = self.hotel_combo.get()
        room_type = self.room_type_combo.get()
        capacity = self.capacity_combo.get()
        price_text = self.price_entry.get().strip()

        try:
            price = float(price_text) if price_text else 0.0
        except:
            messagebox.showerror("Error", "Invalid price.")
            return

        r = self.rooms[self.current_index]
        r.update({
            "hotel": hotel,
            "type": room_type,
            "capacity": capacity,
            "price": f"{price:.2f}"
        })

        self.reload_listbox()
        messagebox.showinfo("Updated", "Room updated.")

    # -----------------------------------
    # DELETE
    # -----------------------------------
    def delete_room(self):
        if self.current_index is None:
            messagebox.showinfo("Info", "Select a room first.")
            return

        r = self.rooms[self.current_index]
        if not messagebox.askyesno("Confirm", f"Delete room {r['room_number']}?"):
            return

        self.rooms.pop(self.current_index)
        self.reload_listbox()
        messagebox.showinfo("Deleted", "Room deleted.")

    # -----------------------------------
    # REVIEW ALL
    # -----------------------------------
    def review_all(self):
        win = tk.Toplevel(self)
        win.title("All Rooms")
        win.geometry("600x400")

        txt = tk.Text(win, font=("Arial", 11))
        txt.pack(fill="both", expand=True)

        for r in self.rooms:
            txt.insert(
                tk.END,
                f"Room: {r['room_number']}\n"
                f"Hotel: {r['hotel']}\n"
                f"Type: {r['type']}\n"
                f"Capacity: {r['capacity']}\n"
                f"Price: €{r['price']}\n"
                "----------------------\n"
            )
        txt.config(state="disabled")