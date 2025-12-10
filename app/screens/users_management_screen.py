# app/screens/users_management_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
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


class UsersManagementScreen(tk.Frame):
    """
    Users Management (No scrollbar version)
    """

    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.on_back = on_back

        # BACKGROUND (optional)
        self.configure(bg="white")
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "users_mg_screenn.jpg"
        )
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path).resize((1200, 700))
                self.bg_image = ImageTk.PhotoImage(img)
                tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)
            except:
                pass

        # Dummy users
        self.users = [
            {"id": 1, "fname": "Ali", "lname": "Yılmaz", "email": "ali@mail.com", "dob": "1999", "role": "User"},
            {"id": 2, "fname": "Ayşe", "lname": "Demir", "email": "ayse@mail.com", "dob": "1998", "role": "Admin"},
            {"id": 3, "fname": "Sude", "lname": "Kaya", "email": "sude@mail.com", "dob": "2000", "role": "User"},
        ]
        self.next_id = max(u["id"] for u in self.users) + 1
        self.current_index = None

        # ------------ LISTBOX (NO SCROLLBAR) ------------
        self.user_listbox = tk.Listbox(self, width=53, height=18, font=("Arial", 12))
        self.user_listbox.place(x=150, y=180)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_select)

        # -------- FIND USER (just below listbox) --------
        self.search_entry = tk.Entry(self, width=25, font=("Arial", 12))
        self.search_entry.place(x=150, y=480)

        ModernButton(self, text="Find User", width=14, command=self.find_user)\
            .place(x=350, y=480)

        # ------------ INPUTS (right) ------------
        self.fn_entry = tk.Entry(self, width=30, font=("Arial", 13))
        self.fn_entry.place(x=760, y=190)

        self.ln_entry = tk.Entry(self, width=30, font=("Arial", 13))
        self.ln_entry.place(x=760, y=248)

        self.email_entry = tk.Entry(self, width=30, font=("Arial", 13))
        self.email_entry.place(x=760, y=320)

        self.dob_entry = tk.Entry(self, width=30, font=("Arial", 13))
        self.dob_entry.place(x=760, y=380)

        self.role_combo = ttk.Combobox(
            self, values=["User", "Admin"], state="readonly", width=27, font=("Arial", 12)
        )
        self.role_combo.place(x=750, y=445)

        # ------------ BUTTONS ------------
        ModernButton(self, text="Add User", width=14, command=self.add_user)\
            .place(x=600, y=540)

        ModernButton(self, text="Update Selected", width=14, command=self.update_user)\
            .place(x=800, y=540)

        ModernButton(self, text="Delete Selected", width=14, command=self.delete_user)\
            .place(x=1000, y=540)

        ModernButton(self, text="Review All", width=14, command=self.review_all)\
            .place(x=250, y=555)

        ModernButton(self, text="← Back", width=12, command=self.on_back)\
            .place(x=60, y=555)

        self.reload_listbox()

    # ------------ Listbox reload ------------
    def reload_listbox(self):
        self.user_listbox.delete(0, tk.END)
        for u in self.users:
            self.user_listbox.insert(
                tk.END,
                f"{u['id']} • {u['fname']} {u['lname']} • {u['email']} • {u['role']}"
            )
        self.current_index = None
        self.clear_inputs()

    # ------------ Clear inputs ------------
    def clear_inputs(self):
        self.fn_entry.delete(0, tk.END)
        self.ln_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.role_combo.set("")

    # ------------ Select user ------------
    def on_select(self, event):
        sel = self.user_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.current_index = idx
        u = self.users[idx]

        self.fn_entry.delete(0, tk.END)
        self.fn_entry.insert(0, u["fname"])

        self.ln_entry.delete(0, tk.END)
        self.ln_entry.insert(0, u["lname"])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, u["email"])

        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, u["dob"])

        self.role_combo.set(u["role"])

    # ------------ Add user ------------
    def add_user(self):
        fname = self.fn_entry.get().strip()
        lname = self.ln_entry.get().strip()
        email = self.email_entry.get().strip()
        dob = self.dob_entry.get().strip()
        role = self.role_combo.get().strip()

        if not fname or not lname or not email or not role:
            messagebox.showerror("Error", "Please fill required fields.")
            return

        self.users.append({
            "id": self.next_id,
            "fname": fname,
            "lname": lname,
            "email": email,
            "dob": dob,
            "role": role
        })
        self.next_id += 1

        self.reload_listbox()
        messagebox.showinfo("Added", "User added successfully.")

    # ------------ Update user ------------
    def update_user(self):
        if self.current_index is None:
            messagebox.showinfo("Info", "Select a user first.")
            return

        fname = self.fn_entry.get().strip()
        lname = self.ln_entry.get().strip()
        email = self.email_entry.get().strip()
        dob = self.dob_entry.get().strip()
        role = self.role_combo.get().strip()

        if not fname or not lname or not email or not role:
            messagebox.showerror("Error", "Required fields missing.")
            return

        u = self.users[self.current_index]
        u.update({"fname": fname, "lname": lname, "email": email, "dob": dob, "role": role})

        self.reload_listbox()
        messagebox.showinfo("Updated", "User updated.")

    # ------------ Delete user ------------
    def delete_user(self):
        if self.current_index is None:
            messagebox.showinfo("Info", "Select a user first.")
            return

        u = self.users[self.current_index]
        if not messagebox.askyesno("Confirm", f"Delete {u['fname']} {u['lname']}?"):
            return

        self.users.pop(self.current_index)
        self.reload_listbox()
        messagebox.showinfo("Deleted", "User removed.")

    # ------------ Find user ------------
    def find_user(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showinfo("Info", "Enter a name to search.")
            return

        for i, u in enumerate(self.users):
            full = f"{u['fname']} {u['lname']}".lower()
            if keyword in full:
                self.user_listbox.selection_clear(0, tk.END)
                self.user_listbox.selection_set(i)
                self.user_listbox.see(i)
                self.on_select(None)
                return

        messagebox.showinfo("Not found", "No matching user.")

    # ------------ Review all ------------
    def review_all(self):
        win = tk.Toplevel(self)
        win.title("All Users")
        win.geometry("600x400")

        txt = tk.Text(win, font=("Arial", 11))
        txt.pack(fill="both", expand=True)

        for u in self.users:
            txt.insert(
                tk.END,
                f"ID: {u['id']}\n"
                f"Name: {u['fname']} {u['lname']}\n"
                f"Email: {u['email']}\n"
                f"DOB: {u['dob']}\n"
                f"Role: {u['role']}\n"
                "----------------------\n"
            )
        txt.config(state="disabled")