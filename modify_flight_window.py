# modify_flight_window.py

import customtkinter as ctk
import tkinter.messagebox as tkmb
import os
import pandas as pd

class ModifyFlightWindow:
    def __init__(self, parent, csv_file="DSA_project_flight_reservation.csv"):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("ADMIN - MODIFY FLIGHT DETAILS")
        self.window.geometry("600x700")
        self.window.configure(bg="#2A2D2E")
        self.csv_file = csv_file  # Path to the CSV file

        # Title Label
        title_label = ctk.CTkLabel(self.window, text="MODIFY FLIGHT DETAILS", text_color='cyan', font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Frame to hold all the entry fields
        entry_frame = ctk.CTkFrame(self.window, width=550, height=650, corner_radius=10)
        entry_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Template function to add each field with old and new values
        def add_entry_row(label_text, old_placeholder, new_placeholder):
            label = ctk.CTkLabel(entry_frame, text=label_text, font=("Arial", 14))
            label.pack(anchor="w", padx=20, pady=(15, 5))
            
            row_frame = ctk.CTkFrame(entry_frame, fg_color="#2A2D2E")
            row_frame.pack(pady=5)
            
            # Old Entry
            old_entry = ctk.CTkEntry(row_frame, width=200, placeholder_text=old_placeholder)
            old_entry.pack(side="left", padx=(0, 10))

            # Arrow Label
            arrow_label = ctk.CTkLabel(row_frame, text="→", font=("Arial", 14), text_color="white")
            arrow_label.pack(side="left")

            # New Entry
            new_entry = ctk.CTkEntry(row_frame, width=200, placeholder_text=new_placeholder)
            new_entry.pack(side="left", padx=(10, 0))
            
            return old_entry, new_entry

        # Adding the rows with old and new entries
        self.flight_number_old, self.flight_number_new = add_entry_row("Flight Number:", "Old flight number", "New flight number")
        self.origin_old, self.origin_new = add_entry_row("Origin:", "Old origin", "New origin")
        self.destination_old, self.destination_new = add_entry_row("Destination:", "Old destination", "New destination")
        self.days_old, self.days_new = add_entry_row("Active Days:", "Old days", "New days")
        self.departure_time_old, self.departure_time_new = add_entry_row("Scheduled Departure Time:", "Old time", "New time")
        self.arrival_time_old, self.arrival_time_new = add_entry_row("Scheduled Arrival Time:", "Old time", "New time")

        # Submit Button
        submit_button = ctk.CTkButton(entry_frame, text="Submit", command=self.submit, corner_radius=15)
        submit_button.pack(pady=20)

    def submit(self):
        # Get old and new data from entries
        old_data = [
            self.flight_number_old.get(),
            self.origin_old.get(),
            self.destination_old.get(),
            self.departure_time_old.get(),
            self.arrival_time_old.get(),
            self.days_old.get()
        ]

        new_data = [
            self.flight_number_new.get(),
            self.origin_new.get(),
            self.destination_new.get(),
            self.departure_time_new.get(),
            self.arrival_time_new.get(),
            self.days_new.get()
        ]

        # Load the CSV file and check if the old data exists
        if os.path.exists(self.csv_file):
            df = pd.read_csv(self.csv_file)
            # Check if there's a row matching all old values
            condition = (
                (df["flightNumber"] == old_data[0]) &
                (df["origin"] == old_data[1]) &
                (df["destination"] == old_data[2]) &
                (df["scheduledDepartureTime"] == old_data[3]) &
                (df["scheduledArrivalTime"] == old_data[4]) &
                (df["dayOfWeek"] == old_data[5])
            )

            if condition.any():
                # Apply modifications
                df.loc[condition, :] = new_data
                df.to_csv(self.csv_file, index=False)
                tkmb.showinfo("Success", "Flight details modified successfully!")
            else:
                tkmb.showerror("Error", "Old flight details do not match any records.")
        else:
            tkmb.showerror("Error", "Flight data file does not exist.")

        # Print to console for verification
        print("Old Data:", old_data)
        print("New Data:", new_data)
