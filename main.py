
import customtkinter as ctk
import tkinter.messagebox as tkmb
from typing import Union, Callable
from tkcalendar import DateEntry
import tkinter as tk
import pandas as pd
import numpy as np
from tkinter import ttk, Scrollbar, Canvas
import os

#custom libraries
import flights_display
from add_flight_window import AddFlightWindow
from modify_flight_window import ModifyFlightWindow
from delete_flight_window import DeleteFlightWindow

# Setting the appearance and color themes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FloatSpinbox(ctk.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: Union[int, float] = 1, max_value: int = 9, command: Callable = None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs) #initialising CTk Frame

        self.step_size = step_size
        self.command = command
        self.value = 1  # default value
        self.max_value = max_value  # maximum value
        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                             command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, justify="center")
        self.entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.entry.insert(0, self.value)

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        

    def add_button_callback(self):
        if self.value < self.max_value:
            self.value += self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, str(int(self.value)))

    def subtract_button_callback(self):
        if self.value > 0:
            self.value -= self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, str(int(self.value)))

    def get(self) -> int:
        return int(self.entry.get())

    def set(self, value: int):
        self.value = value
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))

class AirlineManagementSystem:
    def __init__(self, csv_file='user_credentials.csv', csv_file_ip='user_input.csv', csv_file_admin='admin_credentials.csv'):
        self.app = ctk.CTk()
        self.app.geometry("720x620")
        self.app.title("AIRLINE RESERVATION SYSTEM")
        self.app.resizable(0, 0)

        # Variables to store selected passengers
        self.num_adults = 1
        self.num_children = 0
        self.num_infants = 0

        self.user=""

        self.num_adults_ow = 1
        self.num_children_ow = 0
        self.num_infants_ow = 0

        self.csv_file = csv_file  # Initialize self.csv_file here
        self.csv_file_ip = csv_file_ip #Initialize self.csv_file_ip here

        self.csv_file_admin = csv_file_admin #Initialize self.csv_file_admin

        self.dashboard = None
        
        # Ensure the CSV file exists
        if not os.path.exists(self.csv_file):
            # Create a new CSV file with columns for username and password
            df = pd.DataFrame(columns=['username', 'password', 'Name', 'Age'])
            df.to_csv(self.csv_file, index=False)

        # Ensure the CSV file exists
        if not os.path.exists(self.csv_file_ip):
            # Create a new CSV file with columns for username and password
            df = pd.DataFrame(columns=['Username','Departure', 'Arrival', 'Adults', 'Children', 'Infants', 'TicketClass', 'Departure_Date', 'Arrival_Date', "Trip-Type"])
            df.to_csv(self.csv_file_ip, index=False)   
            
        self.booking_details = np.array(["", "", "", 1, 0, 0, "Economy", "", "", "one-way"])

        self.flag=0
 
        self.build_main_screen()
        self.app.mainloop()

    #ADMIN LOGIN
    def open_admin_login(self):
        self.app.withdraw()
        # Create a new Toplevel window for the admin login screen
        self.admin_window = ctk.CTkToplevel(self.app)
        self.admin_window.geometry("720x620")  # Set the size of the new window
        self.admin_window.title("Airline Reservation System")
        
        # Build the admin login screen within this new window
        self.build_admin_login_screen()

    def build_admin_login_screen(self):

        def go_to_login_screen():
            self.admin_window.destroy()
            self.app.deiconify()

        # Title Label for Admin Login Page
        label = ctk.CTkLabel(self.admin_window, text="AIRLINE RESERVATION SYSTEM", text_color='white', font=("Arial", 24, "bold"))
        label.pack(pady=30)

        # Admin Login Frame
        frame = ctk.CTkFrame(master=self.admin_window, width=400, height=500, corner_radius=15)
        frame.pack(fill="both", pady=20, padx=50)

        # Login Label
        admin_login_label = ctk.CTkLabel(frame, text="ADMIN LOGIN", text_color='cyan', font=("Arial", 24, "bold"))
        admin_login_label.pack(pady=30)

        # Username Label and Entry
        label_admin_username = ctk.CTkLabel(frame, text="Admin Username", font=("Arial", 16))
        label_admin_username.pack(pady=(20, 5))

        self.admin_user_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter admin username", width=300)
        self.admin_user_entry.pack(pady=5, padx=10)

        # Password Label and Entry
        label_admin_password = ctk.CTkLabel(frame, text="Password", font=("Arial", 16))
        label_admin_password.pack(pady=(20, 5))

        self.admin_pass_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter admin password", show="*", width=300)
        self.admin_pass_entry.pack(pady=12, padx=10)

        # Login Button
        admin_login_button = ctk.CTkButton(master=frame, text='Admin Login', command=self.admin_login, corner_radius=25, width=150)
        admin_login_button.pack(pady=(20, 10))

        # Back Button to close the admin login window
        back_button = ctk.CTkButton(master=frame, text='Back', command=go_to_login_screen, corner_radius=25, width=150)
        back_button.pack(pady=(10, 20))


    def admin_login(self):
        # Get the entered credentials
        admin_username = self.admin_user_entry.get()
        admin_password = self.admin_pass_entry.get()

        # Check if the admin credentials CSV exists
        if not os.path.exists(self.csv_file_admin):
            tkmb.showerror("Error", "Admin credentials file not found.")
            return
        
        # Read the CSV file using pandas, with headers for username, password, Name, and Age
        df = pd.read_csv(self.csv_file_admin)

        # Check if the entered credentials match any entry in the DataFrame
        user_row = df[(df['username'] == admin_username) & (df['password'] == admin_password)]
        
        if not user_row.empty:
            # Successful login
            tkmb.showinfo("Success", "Login successful!")
            self.admin_login_success()
        else:
            # Incorrect credentials
            tkmb.showerror("Login Failed", "Incorrect username or password. Please try again.")
            self.reset_admin_login_fields()

    def reset_admin_login_fields(self):
        self.admin_user_entry.delete(0, 'end')
        self.admin_pass_entry.delete(0, 'end')


    def admin_login_success(self):
        #Resetting admin login fields and minimizing admin login window
        self.reset_admin_login_fields()
        self.admin_window.withdraw()
        # Create a new window for the admin dashboard
        self.admin_dashboard = ctk.CTkToplevel(self.app)
        self.admin_dashboard.title("Admin Dashboard")
        self.admin_dashboard.geometry("720x620")
        
        # Configure the layout
        self.admin_dashboard.grid_rowconfigure(0, weight=1)
        self.admin_dashboard.grid_rowconfigure(1, weight=1)
        self.admin_dashboard.grid_rowconfigure(2, weight=1)
        self.admin_dashboard.grid_rowconfigure(3, weight=1)
        self.admin_dashboard.grid_columnconfigure(0, weight=1)

        # Frame to hold the dashboard content
        admin_dashboard_frame = ctk.CTkFrame(self.admin_dashboard, width=600, height=500, corner_radius=15)
        admin_dashboard_frame.pack(pady=40, padx=60, fill="both", expand=True)

        # Admin Dashboard Title Label at the top center
        dashboard_label = ctk.CTkLabel(admin_dashboard_frame, text="ADMIN DASHBOARD", text_color='cyan', font=("Arial", 24, "bold"))
        dashboard_label.pack(pady=(30, 10))

        # Button Frame to center the buttons
        admin_button_frame = ctk.CTkFrame(admin_dashboard_frame, fg_color="transparent")
        admin_button_frame.pack(pady=60)

        # Buttons for different admin functionalities
        # Add "ADD FLIGHT" button
        add_flight_button = ctk.CTkButton(admin_button_frame, text="ADD FLIGHT", width=500, height=80, command=self.add_flight, corner_radius=15, font=("Arial", 20, "bold"))
        add_flight_button.pack(pady=10, fill="x", padx=40)

        # Add "MODIFY FLIGHT" button
        modify_flight_button = ctk.CTkButton(admin_button_frame, text="MODIFY FLIGHT", width=500, height=80, command=self.modify_flight, corner_radius=7, font=("Arial", 20, "bold"))
        modify_flight_button.pack(pady=10, fill="x", padx=40)

        # Add "DELETE FLIGHT" button
        delete_flight_button = ctk.CTkButton(admin_button_frame, text="DELETE FLIGHT", width=500, height=80, command=self.delete_flight, corner_radius=15, font=("Arial", 20, "bold"))
        delete_flight_button.pack(pady=10, fill="x", padx=40)

        # Logout Button at the top-right corner of the window (outside frame)
        admin_dashboard_logout_button = ctk.CTkButton(self.admin_dashboard, text="LOGOUT", command=self.admin_dashboard_logout, width=80, fg_color="red", hover_color="dark red")
        admin_dashboard_logout_button.place(x=580, y=9)

    def admin_dashboard_logout(self):
        # Close the admin window and go back to the admin login page
        self.admin_dashboard.destroy()
        self.admin_window.deiconify()

    # Placeholder functions for add, modify, and delete actions
    def add_flight(self):
        AddFlightWindow(self.admin_dashboard)

    def modify_flight(self):
        ModifyFlightWindow(self.admin_dashboard)

    def delete_flight(self):
        DeleteFlightWindow(self.admin_dashboard)



    #REGISTER / SIGNUP WINDOW
    def open_register_window(self):
        self.app.withdraw()
        register_window = ctk.CTkToplevel(self.app)
        register_window.title("Airline Reservation System - Register")
        register_window.geometry("720x600")
        register_window.resizable(0, 0)

        def go_back():
            register_window.destroy()
            self.app.deiconify()

        # Main frame for the content
        main_frame = ctk.CTkFrame(register_window, fg_color="#262626")
        main_frame.pack(pady=20, padx=40, fill='both', expand=True)

        # Header with Title
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(pady=(10, 20))

        header_label = ctk.CTkLabel(header_frame, text="Register", font=("Helvetica", 26, "bold"), text_color="#00CED1")
        header_label.pack(pady=(10, 20))

        # Personal Info Section (horizontal layout)
        form_frame = ctk.CTkFrame(main_frame, fg_color="#333333", corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill='x')

        # Full Name Field
        full_name_label = ctk.CTkLabel(form_frame, text="Full Name", font=("Arial", 14), text_color="#FFFFFF")
        full_name_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        full_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your full name")
        full_name_entry.grid(row=0, column=2, padx=10, pady=10)

        # Age Field
        age_label = ctk.CTkLabel(form_frame, text="Age", font=("Arial", 14), text_color="#FFFFFF")
        age_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        age_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your age")
        age_entry.grid(row=1, column=2, padx=10, pady=10)


        # Username Field
        username_label = ctk.CTkLabel(form_frame, text="Username", font=("Arial", 14), text_color="#FFFFFF")
        username_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        username_entry = ctk.CTkEntry(form_frame, placeholder_text="Choose a username")
        username_entry.grid(row=2, column=2, padx=10, pady=10)

        # Password Field
        password_label = ctk.CTkLabel(form_frame, text="Password", font=("Arial", 14), text_color="#FFFFFF")
        password_label.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter a password", show="*")
        password_entry.grid(row=3, column=2, padx=10, pady=10)

        # Confirm Password Field
        confirm_password_label = ctk.CTkLabel(form_frame, text="Confirm Password", font=("Arial", 14),
                                              text_color="#FFFFFF")
        confirm_password_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        confirm_password_entry = ctk.CTkEntry(form_frame, placeholder_text="Re-enter password", show="*")
        confirm_password_entry.grid(row=4, column=2, padx=10, pady=10)

        # Submit Button
        submit_button = ctk.CTkButton(main_frame, text="Register", fg_color="#00CED1", hover_color="#20B2AA",
                                      text_color="white", font=("Arial", 16, "bold"),
                                      command=lambda: self.signup(register_window,username_entry  ,  password_entry, confirm_password_entry, age_entry,full_name_entry))
        submit_button.pack(pady=30)

        back_button = ctk.CTkButton(register_window, text="Back", text_color="#00CED1", font=("Arial", 18), 
                                    fg_color="#262626", hover_color="lightgray", cursor="hand2", 
                                    command=go_back)
        back_button.place(x=540, y=19)

    def signup(self, register_window, new_user_entry, new_user_pass, new_user_pass_re, new_user_age, new_user_name):
        new_username = new_user_entry.get()
        new_password = new_user_pass.get()
        re_password = new_user_pass_re.get()
        age = new_user_age.get()
        name = new_user_name.get()
        # Check if the username already exists

        if not new_username or not new_password:
            tkmb.showerror(title="Error", message="Please fill in all fields")
        elif len(new_password)<8:
            tkmb.showerror(title="Error", message="Password must be 8 characters long")
        elif new_password != re_password:
            tkmb.showerror(title="Error", message="Passwords do not match")
        elif int(age)<18:
            tkmb.showerror(title="Error", message="Age must be minimum 18")
        elif self._check_username_exists(new_username):
            tkmb.showerror(title="Error", message="Username already exsists")
        else:
            # Append new user credentials to the CSV file
            new_user = pd.DataFrame({'username': [new_username], 'password': [new_password], 'name': [name], 'age': [age]})
            new_user.to_csv(self.csv_file, mode='a', header=False, index=False)
            tkmb.showinfo(title="Registration Successful", message=f"User '{new_username}' registered successfully")
            self.reset_login_fields()
            register_window.destroy()
            self.app.deiconify()



    #MAIN SCREEN
    def build_main_screen(self):
        label = ctk.CTkLabel(self.app, text="AIRLINE RESERVATION SYSTEM", text_color='white', font=("Arial", 24, "bold"))
        label.pack(pady=30)

        frame = ctk.CTkFrame(master=self.app, width=400, height=500, corner_radius=15)
        frame.pack(fill="both", pady=20, padx=50)

        # LOGIN
        login_label = ctk.CTkLabel(frame, text="LOGIN", text_color='cyan', font=("Arial", 24, "bold"))
        login_label.pack(pady=30)

        label_username = ctk.CTkLabel(frame, text="Username", font=("Arial", 16))
        label_username.pack(pady=(20, 5))

        self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter your username", width=300)
        self.user_entry.pack(pady=5, padx=10)

        label_password = ctk.CTkLabel(frame, text="Password", font=("Arial", 16))
        label_password.pack(pady=(20, 5))

        self.user_pass = ctk.CTkEntry(master=frame, placeholder_text="Enter your password", show="*", width=300)
        self.user_pass.pack(pady=12, padx=10)


        login_button = ctk.CTkButton(master=frame, text='Login', command=self.login, corner_radius=25, width=150)
        login_button.pack(pady=(20, 10))

        register_button = ctk.CTkButton(master=frame, text='Register', command=self.open_register_window, corner_radius=25, width=150)
        register_button.pack(pady=(10, 20))

        # Button to open Admin Login Screen
        admin_login_button = ctk.CTkButton(self.app, text="Admin Login", command=self.open_admin_login)
        admin_login_button.pack(pady=20)



    #LOGIN VERIFICATION
    def login(self):
        username = self.user_entry.get()
        password = self.user_pass.get()

        # Verify the credentials
        if self._verify_credentials(username, password):
            tkmb.showinfo(title="Login Successful", message="You have logged in successfully")
            self.booking_details[0] = username
            self.user = username
            self.app.withdraw()
            self.open_dashboard()
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username and Password")

    def _check_username_exists(self, username):
        df = pd.read_csv(self.csv_file)
        return username in df['username'].values

    def _verify_credentials(self, username, password):
        df = pd.read_csv(self.csv_file)
        user = df[df['username'] == username]
        #print(f"User fetched: {user}")  # Debugging: Print the fetched user data
        #if not user.empty:
            #print(f"Stored password: {user['password'].values[0]}")  # Debugging: Print the stored password
        return not user.empty and user['password'].values[0] == password
    
    def reset_login_fields(self):
        self.user_entry.delete(0, 'end')
        self.user_pass.delete(0, 'end')



    #FLIGHT SEARCH DASHBOARD
    def open_dashboard(self):
        self.dashboard = ctk.CTk()
        self.dashboard.title("AIRLINES")
        self.dashboard.geometry("900x650")
        self.dashboard.resizable(0, 0)

        def logout():
            self.dashboard.destroy()
            self.app.deiconify()
            self.reset_login_fields()
            self.num_adults=1
            self.num_infant=0
            self.num_children=0 

        tab_view = ctk.CTkTabview(master=self.dashboard, width=800, height=600, corner_radius=10)
        tab_view.pack(pady=20, padx=20)

        # Create two tabs
        tab_view.add("One-Way")
        tab_view.add("Round-Trip")

        # Load the CSV file at the beginning or in the relevant function
        file_path = 'booking_info.csv'
        booking_data = pd.read_csv(file_path)


        def open_booking_window(dashboard):
            dashboard.withdraw()  # Hide the dashboard window


            booking_window = ctk.CTkToplevel(dashboard)
            booking_window.title("Booking")
            booking_window.geometry("500x500")
            #booking_window.resizable(0, 0)

            # Filter the data based on user ID
            matched_data = booking_data[booking_data['user id'] == self.user]

            if not matched_data.empty:
                # Create a canvas for scrollable content
                canvas = Canvas(booking_window, bg="#1c1c1c")  # Dark background
                scroll_y = Scrollbar(booking_window, orient="vertical", command=canvas.yview)
                scrollable_frame = ctk.CTkFrame(canvas, fg_color="#1c1c1c")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scroll_y.set)

                # Display all booking details in styled frames
                for i, (index, row) in enumerate(matched_data.iterrows()):
                    bg_color = "#2b2b2b" if i % 2 == 0 else "#3e3e3e"  # Alternating background colors
                    booking_frame = ctk.CTkFrame(
                        scrollable_frame, corner_radius=15, fg_color=bg_color, border_width=1, border_color="#555"
                    )
                    booking_frame.pack(pady=15, padx=15, fill="both", expand=True)

                    # Title with improved styling
                    booking_title = ctk.CTkLabel(
                        booking_frame, text=f"Booking {i + 1}", font=("Arial", 18, "bold"), text_color="#00bfff"
                    )
                    booking_title.pack(pady=(10, 5), anchor="center")

                    # Display each detail with updated styling
                    for col, value in row.items():
                        detail_text = f"{col.replace('_', ' ').title()}: {value if pd.notna(value) else 'N/A'}"
                        detail_label = ctk.CTkLabel(
                            booking_frame, text=detail_text, font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left"
                        )
                        detail_label.pack(anchor="w", padx=15, pady=2)

                canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                scroll_y.pack(side="right", fill="y")
            else:
                no_data_label = ctk.CTkLabel(
                    booking_window, text="No data found for this user.",
                    font=("Arial", 16, "bold"), text_color="#ff0000"
                )
                no_data_label.pack(pady=20)

            # Enhanced Back button
            back_button = ctk.CTkButton(
                booking_window, text="Back", text_color="#ffffff", font=("Arial", 14, "bold"),
                fg_color="#ff3333", hover_color="#cc0000", cursor="hand2",
                command=lambda: (booking_window.withdraw(), dashboard.deiconify())
            )
            back_button.pack(pady=10, side="bottom")



        # Logout button
        logout_button = ctk.CTkButton(self.dashboard, text="Logout", text_color="cyan", font=("Arial", 17), 
                                    fg_color="red", hover_color="dark red", cursor="hand2", 
                                    command=logout)
        logout_button.place(x=880, y=10, anchor="ne")

        booking_button = ctk.CTkButton(self.dashboard, text="Bookings", text_color="cyan", font=("Arial", 17), 
                                    fg_color="transparent", hover_color="cyan", cursor="hand2", 
                                    command=lambda: open_booking_window(self.dashboard))
        booking_button.place(x=170, y=10, anchor="ne")

        df = pd.read_csv(r"DSA_project_flight_reservation.csv") 
        df.dropna(subset=['origin','destination'])       
        data_dep = df['origin'].unique()
        data_arr = df['destination'].unique()

        # Add widgets on both tabs (similar content)
        self.add_flight_search_widgets_ow(tab_view.tab("One-Way"), data_dep, data_arr)
        self.add_flight_search_widgets(tab_view.tab("Round-Trip"), data_dep, data_arr)

        self.dashboard.mainloop()

    def add_flight_search_widgets(self, tab, data_dep, data_arr):
        # Function to update and show the Listbox for departure
        def update_search_departure(event):
            search_term = departure_entry.get().lower()

            # Clear the Listbox to display new matches
            departure_listbox.delete(0, tk.END)

            if search_term:
                matches = [item for item in data_dep if search_term in item.lower()]

                if matches:
                    # Show Listbox below the entry
                    departure_listbox.place(x=departure_entry.winfo_x(),
                                            y=departure_entry.winfo_y() + departure_entry.winfo_height())
                    departure_listbox.lift()
                    for item in matches:
                        departure_listbox.insert(tk.END, item)
                else:
                    departure_listbox.place_forget()
            else:
                departure_listbox.place_forget()

        # Function to update and show the Listbox for arrival
        def update_search_arrival(event):
            search_term = arrival_entry.get().lower()

            # Clear the Listbox to display new matches
            arrival_listbox.delete(0, tk.END)

            if search_term:
                matches = [item for item in data_arr if search_term in item.lower()]

                if matches:
                    # Show Listbox below the entry
                    arrival_listbox.place(x=arrival_entry.winfo_x(),
                                        y=arrival_entry.winfo_y() + arrival_entry.winfo_height())
                    arrival_listbox.lift()
                    for item in matches:
                        arrival_listbox.insert(tk.END, item)
                else:
                    arrival_listbox.place_forget()
            else:
                arrival_listbox.place_forget()

        # Hide Listbox for departure
        def hide_listbox_departure(event):
            if event.widget != departure_listbox and event.widget != departure_entry:
                departure_listbox.place_forget()

        # Hide Listbox for arrival
        def hide_listbox_arrival(event):
            if event.widget != arrival_listbox and event.widget != arrival_entry:
                arrival_listbox.place_forget()

        # Handle selection from departure Listbox
        def on_listbox_select_departure(event):
            selection = departure_listbox.curselection()
            if selection:
                selected_item = departure_listbox.get(selection[0])
                self.booking_details[1]=selected_item
                departure_entry.delete(0, tk.END)
                departure_entry.insert(0, selected_item)
                departure_listbox.place_forget()

        # Handle selection from arrival Listbox
        def on_listbox_select_arrival(event):
            selection = arrival_listbox.curselection()
            if selection:
                selected_item = arrival_listbox.get(selection[0])
                if self.booking_details[1] == selected_item:
                    tkmb.showerror(title="Invalid Entry", message="Same departure and arrival entry")
                self.booking_details[2]=selected_item
                arrival_entry.delete(0, tk.END)
                arrival_entry.insert(0, selected_item)
                arrival_listbox.place_forget()

        # Dashboard Label
        booking_label = ctk.CTkLabel(tab, text="Book a Flight", font=("Arial", 36, "bold"), text_color='cyan')
        booking_label.grid(row=0, column=0, columnspan=6, pady=(30, 20), sticky="ew")

        # Flight frame
        flight_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color='#343638')
        flight_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=20, sticky="ew")

        # Departure entry and Listbox
        departure_label = ctk.CTkLabel(flight_frame, text="Departure Airport", font=("Arial", 16), text_color='white')
        departure_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        departure_entry = ctk.CTkEntry(flight_frame, placeholder_text="Departure airport", width=250)
        departure_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        departure_entry.bind("<KeyRelease>", update_search_departure)

        departure_listbox = tk.Listbox(flight_frame, height=5, width=40)
        departure_listbox.place_forget()
        flight_frame.bind("<Button-1>", hide_listbox_departure)
        departure_entry.bind("<FocusOut>", hide_listbox_departure)
        departure_listbox.bind("<<ListboxSelect>>", on_listbox_select_departure)

        # Arrival entry and Listbox
        arrival_label = ctk.CTkLabel(flight_frame, text="Arrival Airport", font=("Arial", 16), text_color='white')
        arrival_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        arrival_entry = ctk.CTkEntry(flight_frame, placeholder_text="Arrival airport", width=250)
        arrival_entry.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        arrival_entry.bind("<KeyRelease>", update_search_arrival)

        arrival_listbox = tk.Listbox(flight_frame, height=5, width=40)
        arrival_listbox.place_forget()
        flight_frame.bind("<Button-1>", hide_listbox_arrival)
        arrival_entry.bind("<FocusOut>", hide_listbox_arrival)
        arrival_listbox.bind("<<ListboxSelect>>", on_listbox_select_arrival)

        depart_label = ctk.CTkLabel(flight_frame, text="Departing", font=("Arial", 16), text_color='white')
        depart_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        # DateEntry style to match the rest of the theme
        style = tk.ttk.Style()
        style.theme_use('clam')
        style.configure('my.DateEntry', fieldbackground='#343638', background='#343638', foreground='white',
                        arrowcolor='cyan')

        return_label = ctk.CTkLabel(flight_frame, text="Returning", font=("Arial", 16), text_color='white')
        return_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")


        self.depart_date = DateEntry(flight_frame, width=18, style='my.DateEntry', background='#343638', foreground='white',
                                 borderwidth=2, date_pattern='y-mm-dd')
        self.depart_date.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.return_date = DateEntry(flight_frame, width=18, style='my.DateEntry', background='#343638', foreground='white',
                                    borderwidth=2, date_pattern='y-mm-dd')
        self.return_date.grid(row=2, column=3, padx=10, pady=10, sticky="ew")

        self.class_dropdown = ctk.CTkOptionMenu(flight_frame, values=["Economy", "Business", "First Class"],
                                                fg_color='#565B5E')
        self.class_dropdown.grid(row=3, column=3, padx=10, pady=10, sticky="ew")

        passengers_label = ctk.CTkLabel(flight_frame, text="Passengers", font=("Arial", 16), text_color='white')
        passengers_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        passengers_button = ctk.CTkButton(flight_frame, text="Select Passengers", command=self.open_passenger_menu,
                                          corner_radius=25, fg_color='#565B5E', hover_color='#728089', width=250)
        passengers_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        class_label = ctk.CTkLabel(flight_frame, text="Class", font=("Arial", 16), text_color='white')
        class_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        # Adding a separator for visual separation
        separator = ctk.CTkLabel(flight_frame, text="", height=2, width=700, fg_color='white')
        separator.grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")

        search_button = ctk.CTkButton(flight_frame, text="Search Flights", command=self.round_trip_info,
                                      corner_radius=25,
                                      width=400, height=40, fg_color="#4caf50", hover_color="#45a049")
        search_button.grid(row=5, column=0, columnspan=4, pady=20)

    def add_flight_search_widgets_ow(self, tab, data_dep, data_arr):
        # Function to update and show the Listbox for departure
        def update_search_departure(event):
            search_term = departure_entry.get().lower()

            # Clear the Listbox to display new matches
            departure_listbox.delete(0, tk.END)

            if search_term:
                matches = [item for item in data_dep if search_term in item.lower()]

                if matches:
                    # Show Listbox below the entry
                    departure_listbox.place(x=departure_entry.winfo_x(),
                                            y=departure_entry.winfo_y() + departure_entry.winfo_height())
                    departure_listbox.lift()
                    for item in matches:
                        departure_listbox.insert(tk.END, item)
                else:
                    departure_listbox.place_forget()
            else:
                departure_listbox.place_forget()

        # Function to update and show the Listbox for arrival
        def update_search_arrival(event):
            search_term = arrival_entry.get().lower()

            # Clear the Listbox to display new matches
            arrival_listbox.delete(0, tk.END)

            if search_term:
                matches = [item for item in data_arr if search_term in item.lower()]

                if matches:
                    # Show Listbox below the entry
                    arrival_listbox.place(x=arrival_entry.winfo_x(),
                                        y=arrival_entry.winfo_y() + arrival_entry.winfo_height())
                    arrival_listbox.lift()
                    for item in matches:
                        arrival_listbox.insert(tk.END, item)
                else:
                    arrival_listbox.place_forget()
            else:
                arrival_listbox.place_forget()

        # Hide Listbox for departure
        def hide_listbox_departure(event):
            if event.widget != departure_listbox and event.widget != departure_entry:
                departure_listbox.place_forget()

        # Hide Listbox for arrival
        def hide_listbox_arrival(event):
            if event.widget != arrival_listbox and event.widget != arrival_entry:
                arrival_listbox.place_forget()

        # Handle selection from departure Listbox
        def on_listbox_select_departure(event):
            selection = departure_listbox.curselection()
            if selection:
                selected_item = departure_listbox.get(selection[0])
                self.booking_details[1]=selected_item
                departure_entry.delete(0, tk.END)
                departure_entry.insert(0, selected_item)
                departure_listbox.place_forget()

        # Handle selection from arrival Listbox
        def on_listbox_select_arrival(event):
            selection = arrival_listbox.curselection()
            if selection:
                selected_item = arrival_listbox.get(selection[0])
                if self.booking_details[1] == selected_item:
                    tkmb.showerror(title="Invalid Entry", message="Same departure and arrival entry")
                self.booking_details[2]=selected_item
                arrival_entry.delete(0, tk.END)
                arrival_entry.insert(0, selected_item)
                arrival_listbox.place_forget()

        # Dashboard Label
        booking_label = ctk.CTkLabel(tab, text="Book a Flight", font=("Arial", 36, "bold"), text_color='cyan')
        booking_label.grid(row=0, column=0, columnspan=6, pady=(30, 20), sticky="ew")

        # Flight frame
        flight_frame = ctk.CTkFrame(tab, corner_radius=10, fg_color='#343638')
        flight_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=20, sticky="ew")

        # Departure entry and Listbox
        departure_label = ctk.CTkLabel(flight_frame, text="Departure Airport", font=("Arial", 16), text_color='white')
        departure_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        departure_entry = ctk.CTkEntry(flight_frame, placeholder_text="Departure airport", width=250)
        departure_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        departure_entry.bind("<KeyRelease>", update_search_departure)

        departure_listbox = tk.Listbox(flight_frame, height=5, width=40)
        departure_listbox.place_forget()
        flight_frame.bind("<Button-1>", hide_listbox_departure)
        departure_entry.bind("<FocusOut>", hide_listbox_departure)
        departure_listbox.bind("<<ListboxSelect>>", on_listbox_select_departure)

        # Arrival entry and Listbox
        arrival_label = ctk.CTkLabel(flight_frame, text="Arrival Airport", font=("Arial", 16), text_color='white')
        arrival_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        arrival_entry = ctk.CTkEntry(flight_frame, placeholder_text="Arrival airport", width=250)
        arrival_entry.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        arrival_entry.bind("<KeyRelease>", update_search_arrival)

        arrival_listbox = tk.Listbox(flight_frame, height=5, width=40)
        arrival_listbox.place_forget()
        flight_frame.bind("<Button-1>", hide_listbox_arrival)
        arrival_entry.bind("<FocusOut>", hide_listbox_arrival)
        arrival_listbox.bind("<<ListboxSelect>>", on_listbox_select_arrival)

        depart_label = ctk.CTkLabel(flight_frame, text="Departing", font=("Arial", 16), text_color='white')
        depart_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        # DateEntry style to match the rest of the theme
        style = tk.ttk.Style()
        style.theme_use('clam')
        style.configure('my.DateEntry', fieldbackground='#343638', background='#343638', foreground='white',
                        arrowcolor='cyan')

        self.depart_date_ow = DateEntry(flight_frame, width=18, style='my.DateEntry', background='#343638', foreground='white',
                                 borderwidth=2, date_pattern='y-mm-dd')
        self.depart_date_ow.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.class_dropdown_ow = ctk.CTkOptionMenu(flight_frame, values=["Economy", "Business", "First Class"],
                                                fg_color='#565B5E')
        self.class_dropdown_ow.grid(row=3, column=3, padx=10, pady=10, sticky="ew")

        passengers_label = ctk.CTkLabel(flight_frame, text="Passengers", font=("Arial", 16), text_color='white')
        passengers_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        passengers_button = ctk.CTkButton(flight_frame, text="Select Passengers", command=self.open_passenger_menu_ow,
                                          corner_radius=25, fg_color='#565B5E', hover_color='#728089', width=250)
        passengers_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        class_label = ctk.CTkLabel(flight_frame, text="Class", font=("Arial", 16), text_color='white')
        class_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        # Adding a separator for visual separation
        separator = ctk.CTkLabel(flight_frame, text="", height=2, width=700, fg_color='white')
        separator.grid(row=4, column=0, columnspan=4, pady=10, sticky="ew")

        search_button = ctk.CTkButton(flight_frame, text="Search Flights", command=self.one_way_info,
                                      corner_radius=25,
                                      width=400, height=40, fg_color="#4caf50", hover_color="#45a049")
        search_button.grid(row=5, column=0, columnspan=4, pady=20)

    def dashboard_entry_ow(self):
        # Access the values using the class attributes
        self.dept_data = self.depart_date_ow.get()
        self.class_selction = self.class_dropdown_ow.get() 

        # Update booking details for departure date and class selection
        self.booking_details[7] = self.dept_data
        self.booking_details[6] = self.class_selction  # Save class selection

    def dashboard_entry(self):
        # Access the values using the class attributes
        self.dept_data = self.depart_date.get()
        self.class_selction = self.class_dropdown.get()
        # Update booking details for departure date and class selection
        self.booking_details[7] = self.dept_data
        self.booking_details[6] = self.class_selction  # Save class selection
        
        if self.flag == 2:  # Only for round-trip
            self.ret_date = self.return_date.get()
            self.booking_details[8] = self.ret_date

    def open_passenger_menu(self):
        """Open the passenger selection window."""
        passenger_window = ctk.CTkToplevel(self.app)
        passenger_window.title("Select Passengers")
        passenger_window.geometry("450x400")
        passenger_window.resizable(0, 0)

        frame = ctk.CTkFrame(passenger_window)
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        label = ctk.CTkLabel(frame, text="Select Number of Passengers", font=("Arial", 16), text_color='cyan')
        label.pack(pady=10)

        adult_label = ctk.CTkLabel(frame, text="Adults")
        adult_label.pack(pady=(10, 5))
        self.adult_spinbox = FloatSpinbox(frame)
        self.adult_spinbox.set(self.num_adults)
        self.adult_spinbox.pack()

        child_label = ctk.CTkLabel(frame, text="Children")
        child_label.pack(pady=(10, 5))
        self.child_spinbox = FloatSpinbox(frame)
        self.child_spinbox.set(self.num_children)
        self.child_spinbox.pack()

        infant_label = ctk.CTkLabel(frame, text="Infants")
        infant_label.pack(pady=(10, 5))
        self.infant_spinbox = FloatSpinbox(frame)
        self.infant_spinbox.set(self.num_infants)
        self.infant_spinbox.pack()

        confirm_button = ctk.CTkButton(frame, text="Confirm",command=lambda: self.confirm_passenger_selection(passenger_window),corner_radius=25)
        confirm_button.pack(pady=20)

    def open_passenger_menu_ow(self):
        """Open the passenger selection window."""
        passenger_window = ctk.CTkToplevel(self.app)
        passenger_window.title("Select Passengers")
        passenger_window.geometry("450x400")
        passenger_window.resizable(0, 0)

        frame = ctk.CTkFrame(passenger_window)
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        label = ctk.CTkLabel(frame, text="Select Number of Passengers", font=("Arial", 16), text_color='cyan')
        label.pack(pady=10)

        adult_label = ctk.CTkLabel(frame, text="Adults")
        adult_label.pack(pady=(10, 5))
        self.adult_spinbox = FloatSpinbox(frame)
        self.adult_spinbox.set(self.num_adults_ow)
        self.adult_spinbox.pack()


        child_label = ctk.CTkLabel(frame, text="Children")
        child_label.pack(pady=(10, 5))
        self.child_spinbox = FloatSpinbox(frame)
        self.child_spinbox.set(self.num_children_ow)
        self.child_spinbox.pack()

        infant_label = ctk.CTkLabel(frame, text="Infants")
        infant_label.pack(pady=(10, 5))
        self.infant_spinbox = FloatSpinbox(frame)
        self.infant_spinbox.set(self.num_infants_ow)
        self.infant_spinbox.pack()


        confirm_button = ctk.CTkButton(frame, text="Confirm",command=lambda: self.confirm_passenger_selection_ow(passenger_window),corner_radius=25)
        confirm_button.pack(pady=20)

    def confirm_passenger_selection(self, window):
        """Store the selected number of passengers."""
        self.num_adults = self.adult_spinbox.get()
        self.num_children = self.child_spinbox.get()
        self.num_infants = self.infant_spinbox.get()
        self.booking_details[3] = self.num_adults
        self.booking_details[4] = self.num_children 
        self.booking_details[5] = self.num_infants
        window.destroy()

    def confirm_passenger_selection_ow(self, window):
        """Store the selected number of passengers."""
        self.num_adults_ow = self.adult_spinbox.get()
        self.num_children_ow = self.child_spinbox.get()
        self.num_infants_ow = self.infant_spinbox.get()
        self.booking_details[3] = self.num_adults_ow 
        self.booking_details[4] = self.num_children_ow
        self.booking_details[5] = self.num_infants_ow
        window.destroy()

    def one_way_info(self): 
        self.flag=1
        self.booking_details[9] = 'one-way'
        self.dashboard_entry_ow()
        self.search_flights()

    def round_trip_info(self):
        self.flag=2
        self.booking_details[9] = 'round-trip'
        self.dashboard_entry()
        self.search_flights()
    

    def search_flights(self):
        # Initialize validation flag
        is_valid = True

        # Validate if departure and arrival fields are filled
        if self.booking_details[1] == '' or self.booking_details[2] == '':
            tkmb.showerror(title="Error", message="Both Departure and Arrival fields must be filled!")
            is_valid = False

        # Validate number of infants cannot exceed number of adults
        if self.booking_details[3] < self.booking_details[5]:
            tkmb.showerror(title="Error", message="Number of Infants cannot exceed number of Adults!")
            is_valid = False

        # If all validations pass
        if is_valid:
            # Display search information
            passenger_info = f"{self.booking_details[3]} Adults, {self.booking_details[4]} Children, {self.booking_details[5]} Infants"
            tkmb.showinfo(title="Search", message=f"Searching for flights...\nPassengers: {passenger_info}")
            
            # Reset passenger information after search
            self.num_adults = 1
            self.num_infants = 0
            self.num_children = 0 

            # Save booking data to CSV
            new_user = pd.DataFrame({
                'Username'       :  [self.booking_details[0]],
                'Departure'      :  [self.booking_details[1]],
                'Arrival'        :  [self.booking_details[2]],
                'Adults'         :  [self.booking_details[3]],
                'Children'       :  [self.booking_details[4]],
                'Infants'        :  [self.booking_details[5]],
                'TicketClass'    :  [self.booking_details[6]],
                'Departure_Date' :  [self.booking_details[7]],
                'Arrival_Date'   :  [self.booking_details[8]],
                'Trip-Type'      :  [self.booking_details[9]]
            })
            new_user.to_csv(self.csv_file_ip, mode='a', header=False, index=False)

            self.loading()
    
    def loading(self):
        self.dashboard.withdraw()

        # Create the splash screen window
        splash_root = ctk.CTk()
        splash_root.geometry("400x200")
        splash_root.title("Loading...")

        # Add a label to the splash screen
        splash_label = ctk.CTkLabel(splash_root, text="Searching for Flights", font=("Arial", 16))
        splash_label.pack(pady=10)

        # Add a progress bar to the splash screen
        progress = ctk.CTkProgressBar(splash_root, orientation="horizontal", width=300)
        progress.set(0)
        progress.pack(pady=20)

        # Update function using 'after' to avoid blocking the main loop
        def update_progress(value=0):
            progress.set(value / 100)
            if value < 100:
                splash_root.after(30, update_progress, value + 1)  # Increment progress
            else:
                splash_root.destroy()  # Close the splash screen
                flights_display.FlightDisplayApp()  # Open the main application window
                self.dashboard.deiconify()

        # Start updating the progress after 100ms
        splash_root.after(100, update_progress)
        splash_root.mainloop()

# Start the application
AirlineManagementSystem()
