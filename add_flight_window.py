import os
import pandas as pd
import customtkinter as ctk
import tkinter.messagebox as tkmb


class AddFlightWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Add Flight")
        self.window.geometry("500x735")
        self.window.configure(bg="#2A2D2E")
        
        # CSV file path
        self.csv_file = 'DSA_project_flight_reservation.csv'

        # Title Label
        title_label = ctk.CTkLabel(self.window, text="ADD NEW FLIGHT", text_color='cyan', font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Frame to hold all the entry fields
        entry_frame = ctk.CTkFrame(self.window, width=350, height=400, corner_radius=10)
        entry_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Flight Number
        flight_number_label = ctk.CTkLabel(entry_frame, text="Flight Number:", font=("Arial", 14))
        flight_number_label.pack(pady=(20, 5))
        self.flight_number_entry = ctk.CTkEntry(entry_frame, width=250, placeholder_text="Enter flight number")
        self.flight_number_entry.pack(pady=5)

        # Origin
        origin_label = ctk.CTkLabel(entry_frame, text="Origin:", font=("Arial", 14))
        origin_label.pack(pady=(20, 5))
        self.origin_entry = ctk.CTkEntry(entry_frame, width=250, placeholder_text="Enter origin")
        self.origin_entry.pack(pady=5)

        # Destination
        destination_label = ctk.CTkLabel(entry_frame, text="Destination:", font=("Arial", 14))
        destination_label.pack(pady=(20, 5))
        self.destination_entry = ctk.CTkEntry(entry_frame, width=250, placeholder_text="Enter destination")
        self.destination_entry.pack(pady=5)

        # Scheduled Departure Time
        departure_time_label = ctk.CTkLabel(entry_frame, text="Scheduled Departure Time:", font=("Arial", 14))
        departure_time_label.pack(pady=(20, 5))

        # Frame for departure time (HH:MM format)
        departure_time_frame = ctk.CTkFrame(entry_frame, fg_color="#2A2D2E")
        departure_time_frame.pack(pady=5)

        self.departure_hour_entry = ctk.CTkEntry(departure_time_frame, width=50, placeholder_text="HH")
        self.departure_hour_entry.pack(side="left", padx=(0, 2))
        
        colon_label1 = ctk.CTkLabel(departure_time_frame, text=":", font=("Arial", 14), text_color="white")
        colon_label1.pack(side="left")
        
        self.departure_minute_entry = ctk.CTkEntry(departure_time_frame, width=50, placeholder_text="MM")
        self.departure_minute_entry.pack(side="left", padx=(2, 0))

        # Scheduled Arrival Time
        arrival_time_label = ctk.CTkLabel(entry_frame, text="Scheduled Arrival Time:", font=("Arial", 14))
        arrival_time_label.pack(pady=(20, 5))

        # Frame for arrival time (HH:MM format)
        arrival_time_frame = ctk.CTkFrame(entry_frame, fg_color="#2A2D2E")
        arrival_time_frame.pack(pady=5)

        self.arrival_hour_entry = ctk.CTkEntry(arrival_time_frame, width=50, placeholder_text="HH")
        self.arrival_hour_entry.pack(side="left", padx=(0, 2))
        
        colon_label2 = ctk.CTkLabel(arrival_time_frame, text=":", font=("Arial", 14), text_color="white")
        colon_label2.pack(side="left")
        
        self.arrival_minute_entry = ctk.CTkEntry(arrival_time_frame, width=50, placeholder_text="MM")
        self.arrival_minute_entry.pack(side="left", padx=(2, 0))

        # Days of the Week (Active Days)
        days_label = ctk.CTkLabel(entry_frame, text="Day of the Week (Active Days):", font=("Arial", 14))
        days_label.pack(pady=(20, 5))
        self.days_entry = ctk.CTkEntry(entry_frame, width=250, placeholder_text="Enter active days (e.g., Monday, Tuesday)")
        self.days_entry.pack(pady=5)

        # Submit Button
        submit_button = ctk.CTkButton(entry_frame, text="Submit", command=self.submit, corner_radius=15)
        submit_button.pack(pady=20)

    def submit(self):
        # Retrieve data from the entries and store in a 1D array
        data_array = [
            self.flight_number_entry.get(),                # Flight Number
            "XYZ",                                         # Airline
            self.origin_entry.get(),                       # Origin
            self.destination_entry.get(),                  # Destination
            self.days_entry.get(),                         # Active Days
            f"{self.departure_hour_entry.get()}:{self.departure_minute_entry.get()}",  # Scheduled Departure Time
            f"{self.arrival_hour_entry.get()}:{self.arrival_minute_entry.get()}",      # Scheduled Arrival Time
            "0","0"                                       # validFrom, validTo
        ]

        # Check if CSV file exists and write or append data
        if not os.path.exists(self.csv_file):
            # Create the CSV file with headers if it doesn't exist
            df = pd.DataFrame([data_array], columns=["flightNumber", "origin", "destination",  "dayOfWeek", "scheduledDepartureTime", "scheduledArrivalTime"])
            df.to_csv(self.csv_file, index=False)
        else:
            # Append to the existing file without headers
            df = pd.DataFrame([data_array])
            df.to_csv(self.csv_file, mode='a', header=False, index=False)

        # Print the array to the console (for verification)
        print("Flight Data Array:", data_array)

        tkmb.showinfo("Success", f"Added Flight | ID:{self.flight_number_entry.get()}")
        # Close the window after submission (optional)
        self.window.destroy()
