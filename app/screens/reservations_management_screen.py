# app/screens/reservations_management_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import datetime

# optional tkcalendar
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
        self.bind("<Enter>", lambda e: self.config(bg="#f0f0f0"))
        self.bind("<Leave>", lambda e: self.config(bg="#ffffff"))


class ReservationsManagementScreen(tk.Frame):
    """
    Reservations Management screen (Inputs on right, list on left).
    - Address and payment_status are NOT inputs, but are shown in the list rows.
    - 'Delete Selected' button removed; 'Cancel Reservation' remains.
    """

    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.on_back = on_back

        # background (optional)
        self.configure(bg="white")
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "reservations_mg_screen.jpg"
        )
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path).resize((1200, 700))
                self.bg_image = ImageTk.PhotoImage(img)
                tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)
            except:
                pass

        # dummy reservations (address and payment_status included for table display)
        self.reservations = [
            {
                "id": 1001,
                "hotel_name": "StayFlow Beach Resort",
                "address": "123 Ocean Road, Nice, France",
                "room_type": "Deluxe Sea View",
                "guests": "2",
                "check_in": "2026-07-10",
                "check_out": "2026-07-14",
                "total_price": "624.00",
                "payment_status": "Not Paid"
            },
            {
                "id": 1002,
                "hotel_name": "Grand City Hotel",
                "address": "Beyoglu, Istanbul, Turkey",
                "room_type": "Standard Double",
                "guests": "3",
                "check_in": "2026-08-01",
                "check_out": "2026-08-05",
                "total_price": "420.00",
                "payment_status": "Paid"
            }
        ]
        self.next_id = max(r["id"] for r in self.reservations) + 1 if self.reservations else 1
        self.current_index = None

        # ------------ LISTBOX (same position as users screen) ------------
        self.listbox = tk.Listbox(self, width=53, height=18, font=("Arial", 12))
        self.listbox.place(x=150, y=180)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # ------------ FIND (just below listbox) ------------
        self.search_entry = tk.Entry(self, width=25, font=("Arial", 12))
        self.search_entry.place(x=150, y=480)
        ModernButton(self, text="Find by ID", width=14, command=self.find_by_id).place(x=350, y=480)

        # ------------ INPUTS (right side, coordinates match Users screen style) ------------
        # Reservation ID (readonly)
        self.res_id_var = tk.StringVar()
        self.res_id_entry = tk.Entry(self, textvariable=self.res_id_var, width=30, font=("Arial", 13), state="readonly")
        self.res_id_entry.place(x=790, y=180)

        # Hotel name
        self.hotel_entry = tk.Entry(self, width=30, font=("Arial", 13))
        self.hotel_entry.place(x=785, y=243)

        # Room type combobox
        self.room_type_combo = ttk.Combobox(self, values=["Single", "Double", "Twin", "Suite", "Deluxe", "Family"],
                                            state="readonly", width=27, font=("Arial", 12))
        self.room_type_combo.place(x=780, y=305)

        # Guests combobox
        self.guests_combo = ttk.Combobox(self, values=[str(i) for i in range(1, 11)], state="readonly", width=15, font=("Arial", 12))
        self.guests_combo.place(x=765, y=363)

        # Check-in / Check-out
        if DateEntry is not None:
            self.checkin_entry = DateEntry(self, width=18, font=("Arial", 11), date_pattern="yyyy-mm-dd")
            self.checkout_entry = DateEntry(self, width=18, font=("Arial", 11), date_pattern="yyyy-mm-dd")
        else:
            self.checkin_entry = tk.Entry(self, width=20, font=("Arial", 11))
            self.checkout_entry = tk.Entry(self, width=20, font=("Arial", 11))
        # place them a little below other inputs (align with Users layout spacing)
        self.checkin_entry.place(x=806, y=426)
        self.checkout_entry.place(x=812, y=480)

        # Total price
        self.total_price_entry = tk.Entry(self, width=18, font=("Arial", 12))
        self.total_price_entry.place(x=785, y=540)

        # ------------ Buttons (no Delete Selected) ------------
        ModernButton(self, text="Add Reservation", width=14, command=self.add_reservation).place(x=600, y=600)
        ModernButton(self, text="Update Selected", width=14, command=self.update_reservation).place(x=800, y=600)

        ModernButton(self, text="Cancel Reservation", width=16, command=self.cancel_reservation).place(x=1000, y=600)

        ModernButton(self, text="Review All", width=14, command=self.review_all).place(x=250, y=555)
        ModernButton(self, text="← Back", width=12, command=self.on_back).place(x=60, y=555)

        # load initial list
        self.reload_list()

    # ---------------- Helpers ----------------
    def reload_list(self):
        self.listbox.delete(0, tk.END)
        for r in self.reservations:
            # show address & payment_status in the row (even though they are not inputs)
            line = (
                f"{r['id']} • {r['hotel_name']} • {r.get('room_type','')} • "
                f"{r.get('guests','')}p • {r.get('check_in','')}→{r.get('check_out','')} • "
                f"{r.get('address','')} • €{r.get('total_price','0.00')} • {r.get('payment_status','Not Paid')}"
            )
            self.listbox.insert(tk.END, line)
        self.current_index = None
        self.clear_inputs()

    def clear_inputs(self):
        self.res_id_var.set("")
        self.hotel_entry.delete(0, tk.END)
        self.room_type_combo.set("")
        self.guests_combo.set("")
        if DateEntry is not None:
            try:
                today = datetime.date.today()
                self.checkin_entry.set_date(today)
                self.checkout_entry.set_date(today)
            except Exception:
                pass
        else:
            self.checkin_entry.delete(0, tk.END)
            self.checkout_entry.delete(0, tk.END)
        self.total_price_entry.delete(0, tk.END)

    # ---------------- Selection ----------------
    def on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.current_index = idx
        r = self.reservations[idx]
        self._fill_from_reservation(r)

    def _fill_from_reservation(self, r: dict):
        self.res_id_var.set(str(r["id"]))
        self.hotel_entry.delete(0, tk.END); self.hotel_entry.insert(0, r.get("hotel_name",""))
        self.room_type_combo.set(r.get("room_type", ""))
        self.guests_combo.set(r.get("guests", ""))
        if DateEntry is not None:
            try:
                self.checkin_entry.set_date(r.get("check_in"))
                self.checkout_entry.set_date(r.get("check_out"))
            except Exception:
                pass
        else:
            self.checkin_entry.delete(0, tk.END); self.checkin_entry.insert(0, r.get("check_in",""))
            self.checkout_entry.delete(0, tk.END); self.checkout_entry.insert(0, r.get("check_out",""))
        self.total_price_entry.delete(0, tk.END); self.total_price_entry.insert(0, r.get("total_price",""))

    # ---------------- Find by ID ----------------
    def find_by_id(self):
        q = self.search_entry.get().strip()
        if not q:
            messagebox.showinfo("Find", "Please enter reservation ID.")
            return
        if not q.isdigit():
            messagebox.showerror("Find", "Reservation ID must be numeric.")
            return
        rid = int(q)
        for i, r in enumerate(self.reservations):
            if r["id"] == rid:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(i)
                self.listbox.see(i)
                self.current_index = i
                self._fill_from_reservation(r)
                messagebox.showinfo("Found", f"Reservation {rid} loaded.")
                return
        messagebox.showwarning("Not found", "No reservation with that ID.")

    # ---------------- Add / Update ----------------
    def add_reservation(self):
        hotel = self.hotel_entry.get().strip()
        room_type = self.room_type_combo.get().strip()
        guests = self.guests_combo.get().strip()
        total_price = self.total_price_entry.get().strip()

        if DateEntry is not None:
            try:
                checkin = self.checkin_entry.get_date()
                checkout = self.checkout_entry.get_date()
            except Exception:
                messagebox.showerror("Error", "Invalid dates.")
                return
        else:
            checkin = self.checkin_entry.get().strip()
            checkout = self.checkout_entry.get().strip()

        if not hotel or not room_type or not guests or not total_price:
            messagebox.showerror("Error", "Hotel, room type, guests and total price are required.")
            return

        # try to reuse address from existing reservations for same hotel, otherwise blank
        addr = ""
        for r in self.reservations:
            if r.get("hotel_name","").lower() == hotel.lower() and r.get("address"):
                addr = r.get("address")
                break

        new = {
            "id": self.next_id,
            "hotel_name": hotel,
            "address": addr,
            "room_type": room_type,
            "guests": guests,
            "check_in": str(checkin) if not isinstance(checkin, datetime.date) else checkin.isoformat(),
            "check_out": str(checkout) if not isinstance(checkout, datetime.date) else checkout.isoformat(),
            "total_price": f"{float(total_price):.2f}",
            "payment_status": "Pending"  # default
        }
        self.reservations.append(new)
        self.next_id += 1
        self.reload_list()
        messagebox.showinfo("Added", f"Reservation created (ID {new['id']}).")

    def update_reservation(self):
        if self.current_index is None:
            messagebox.showinfo("Update", "Select a reservation first.")
            return
        r = self.reservations[self.current_index]
        r["hotel_name"] = self.hotel_entry.get().strip()
        r["room_type"] = self.room_type_combo.get().strip()
        r["guests"] = self.guests_combo.get().strip()
        if DateEntry is not None:
            try:
                r["check_in"] = self.checkin_entry.get_date().isoformat()
                r["check_out"] = self.checkout_entry.get_date().isoformat()
            except Exception:
                pass
        else:
            r["check_in"] = self.checkin_entry.get().strip()
            r["check_out"] = self.checkout_entry.get().strip()
        try:
            r["total_price"] = f"{float(self.total_price_entry.get().strip()):.2f}"
        except Exception:
            messagebox.showerror("Error", "Invalid price.")
            return
        # address remains whatever it was (no input)
        self.reload_list()
        messagebox.showinfo("Updated", "Reservation updated.")

    # ---------------- Cancel ----------------
    def cancel_reservation(self):
        if self.current_index is None:
            messagebox.showinfo("Cancel", "Select a reservation first.")
            return
        if not messagebox.askyesno("Cancel", "Are you sure you want to cancel this reservation?"):
            return
        r = self.reservations[self.current_index]
        r["payment_status"] = "Cancelled"
        self.reload_list()
        messagebox.showinfo("Cancelled", f"Reservation {r['id']} marked as Cancelled.")

    # ---------------- Review all ----------------
    def review_all(self):
        win = tk.Toplevel(self)
        win.title("All Reservations")
        win.geometry("800x500")
        txt = tk.Text(win, font=("Arial", 11))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        if not self.reservations:
            txt.insert(tk.END, "No reservations.")
        else:
            for r in self.reservations:
                txt.insert(
                    tk.END,
                    f"ID: {r['id']}\n"
                    f"Hotel: {r['hotel_name']}\n"
                    f"Address: {r.get('address','')}\n"
                    f"Room: {r['room_type']}\n"
                    f"Guests: {r['guests']}\n"
                    f"Check-in: {r['check_in']}\n"
                    f"Check-out: {r['check_out']}\n"
                    f"Price: €{r['total_price']}\n"
                    f"Payment status: {r['payment_status']}\n"
                    "---------------------------------\n"
                )
        txt.config(state="disabled")