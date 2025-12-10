# app/screens/countryandcity_management_screen.py
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


class CountryAndCityManagementScreen(tk.Frame):
    def __init__(self, master, on_back, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.on_back = on_back

        # SAFE BACKGROUND LOAD
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "images",
            "cac_mng_screen.jpg"
        )
        bg_label = None
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((1200, 700))
                self.bg_image = ImageTk.PhotoImage(img)
                bg_label = tk.Label(self, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("DEBUG: countryandcity image load failed:", e)

        if not bg_label:
            self.configure(bg="white")
        else:
            bg_label.lower()

        # Dummy data
        self.countries = ["Turkey", "France", "Spain"]
        self.cities_by_country = {
            "Turkey": ["Istanbul", "Ankara", "Izmir"],
            "France": ["Paris", "Nice", "Lyon"],
            "Spain": ["Madrid", "Barcelona", "Seville"]
        }


        # Countries listbox
        self.country_listbox = tk.Listbox(self, width=30, height=15, font=("Arial", 11))
        self.country_listbox.place(relx=0.25, rely=0.34, anchor="n")
        self.country_listbox.bind("<<ListboxSelect>>", self.on_country_selected)

        # Country entry + buttons
        self.country_entry = tk.Entry(self, width=25, font=("Arial", 11))
        self.country_entry.place(relx=0.25, rely=0.72, anchor="n")
        ModernButton(self, text="Add Country", width=14, command=self.add_country).place(relx=0.12, rely=0.80, anchor="n")
        ModernButton(self, text="Update Selected", width=14, command=self.update_country).place(relx=0.26, rely=0.80, anchor="n")
        ModernButton(self, text="Delete Selected", width=14, command=self.delete_country).place(relx=0.40, rely=0.80, anchor="n")

        # Cities listbox

        self.city_listbox = tk.Listbox(self, width=40, height=15, font=("Arial", 11))
        self.city_listbox.place(relx=0.70, rely=0.34, anchor="n")

        tk.Label(self, text="Country for new city:", font=("Arial", 10)).place(relx=0.62, rely=0.66, anchor="w")
        self.country_combo_for_city = ttk.Combobox(self, values=self.countries, state="readonly", width=22)
        self.country_combo_for_city.place(relx=0.62, rely=0.70, anchor="w")

        self.city_entry = tk.Entry(self, width=28, font=("Arial", 11))
        self.city_entry.place(relx=0.62, rely=0.74, anchor="w")
        ModernButton(self, text="Add City", width=14, command=self.add_city).place(relx=0.58, rely=0.82, anchor="w")
        ModernButton(self, text="Update Selected", width=14, command=self.update_city).place(relx=0.72, rely=0.82, anchor="w")
        ModernButton(self, text="Delete Selected", width=14, command=self.delete_city).place(relx=0.86, rely=0.82, anchor="w")

        # back
        ModernButton(self, text="← Back", width=10, command=self.on_back).place(relx=0.08, rely=0.92, anchor="w")

        # load lists
        self.reload_country_listbox()
        self.select_first_country_if_any()

    # ---------------------------
    # Helper methods (complete)
    # ---------------------------
    def reload_country_listbox(self):
        self.country_listbox.delete(0, tk.END)
        for c in sorted(self.countries):
            self.country_listbox.insert(tk.END, c)
        # update combo values for city creation
        self.country_combo_for_city["values"] = sorted(self.countries)

    def reload_city_listbox(self, country_name):
        self.city_listbox.delete(0, tk.END)
        if not country_name:
            return
        cities = self.cities_by_country.get(country_name, [])
        for city in cities:
            self.city_listbox.insert(tk.END, city)

    def select_first_country_if_any(self):
        if self.countries:
            # select first item in listbox
            self.country_listbox.selection_set(0)
            self.country_listbox.event_generate("<<ListboxSelect>>")

    def get_selected_country(self):
        sel = self.country_listbox.curselection()
        if not sel:
            return None
        return self.country_listbox.get(sel[0])

    def get_selected_city(self):
        sel = self.city_listbox.curselection()
        if not sel:
            return None
        return self.city_listbox.get(sel[0])

    # ---------------------------
    # Country operations
    # ---------------------------
    def add_country(self):
        name = self.country_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Country name cannot be empty.")
            return
        if name in self.countries:
            messagebox.showwarning("Warning", "This country already exists.")
            return
        self.countries.append(name)
        self.cities_by_country.setdefault(name, [])
        self.reload_country_listbox()
        self.country_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Country '{name}' added.")

    def update_country(self):
        sel_country = self.get_selected_country()
        if not sel_country:
            messagebox.showinfo("Update", "Please select a country to update.")
            return
        new_name = self.country_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "New country name cannot be empty.")
            return
        if new_name != sel_country and new_name in self.countries:
            messagebox.showwarning("Warning", "Another country with this name already exists.")
            return
        cities = self.cities_by_country.pop(sel_country, [])
        self.countries.remove(sel_country)
        self.countries.append(new_name)
        self.cities_by_country[new_name] = cities
        self.reload_country_listbox()
        idx = sorted(self.countries).index(new_name)
        self.country_listbox.selection_clear(0, tk.END)
        self.country_listbox.selection_set(idx)
        self.country_listbox.see(idx)
        self.country_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Country renamed to '{new_name}'.")

    def delete_country(self):
        sel_country = self.get_selected_country()
        if not sel_country:
            messagebox.showinfo("Delete", "Please select a country to delete.")
            return
        cities = self.cities_by_country.get(sel_country, [])
        if cities:
            ok = messagebox.askyesno(
                "Confirm delete",
                f"Country '{sel_country}' has {len(cities)} city(ies). Delete country and all its cities?"
            )
            if not ok:
                return
        else:
            ok = messagebox.askyesno("Confirm delete", f"Are you sure you want to delete country '{sel_country}'?")
            if not ok:
                return
        if sel_country in self.countries:
            self.countries.remove(sel_country)
        self.cities_by_country.pop(sel_country, None)
        self.reload_country_listbox()
        self.city_listbox.delete(0, tk.END)
        messagebox.showinfo("Deleted", f"Country '{sel_country}' and its cities deleted (if any).")

    # ---------------------------
    # City operations
    # ---------------------------
    def add_city(self):
        country_for_city = self.country_combo_for_city.get().strip()
        if not country_for_city:
            messagebox.showerror("Error", "Select a country for the new city.")
            return
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "City name cannot be empty.")
            return
        cities = self.cities_by_country.setdefault(country_for_city, [])
        if city_name in cities:
            messagebox.showwarning("Warning", "This city already exists in the selected country.")
            return
        cities.append(city_name)
        self.reload_city_listbox(country_for_city)
        self.city_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"City '{city_name}' added to '{country_for_city}'.")

    def update_city(self):
        sel_country = self.get_selected_country()
        if not sel_country:
            messagebox.showinfo("Update", "Select a country first.")
            return
        sel_city = self.get_selected_city()
        if not sel_city:
            messagebox.showinfo("Update", "Select a city to update.")
            return
        new_name = self.city_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "New city name cannot be empty.")
            return
        cities = self.cities_by_country.get(sel_country, [])
        if new_name != sel_city and new_name in cities:
            messagebox.showwarning("Warning", "Another city with this name already exists in this country.")
            return
        idx = cities.index(sel_city)
        cities[idx] = new_name
        self.reload_city_listbox(sel_country)
        idx2 = cities.index(new_name)
        self.city_listbox.selection_clear(0, tk.END)
        self.city_listbox.selection_set(idx2)
        self.city_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"City renamed to '{new_name}'.")

    def delete_city(self):
        sel_country = self.get_selected_country()
        if not sel_country:
            messagebox.showinfo("Delete", "Select the country first.")
            return
        sel_city = self.get_selected_city()
        if not sel_city:
            messagebox.showinfo("Delete", "Select a city to delete.")
            return
        ok = messagebox.askyesno("Confirm delete", f"Delete city '{sel_city}' from '{sel_country}'?")
        if not ok:
            return
        cities = self.cities_by_country.get(sel_country, [])
        if sel_city in cities:
            cities.remove(sel_city)
        self.reload_city_listbox(sel_country)
        messagebox.showinfo("Deleted", f"City '{sel_city}' deleted from '{sel_country}'.")

    # ---------------------------
    # Events
    # ---------------------------
    def on_country_selected(self, event=None):
        sel_country = self.get_selected_country()
        if sel_country:
            # reload cities for the selected country
            self.reload_city_listbox(sel_country)
            # prefill combo for city creation
            self.country_combo_for_city.set(sel_country)
        else:
            self.city_listbox.delete(0, tk.END)
            self.country_combo_for_city.set("")