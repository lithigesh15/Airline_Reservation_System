import os
import pandas as pd
import customtkinter as ctk
import tkinter.messagebox as tkmb

class DeleteFlightWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Delete Flight")
        self.window.geometry("400x300")
        self.window.configure(bg="#2A2D2E")
        
        # CSV file path
        self.csv_file = 'DSA_project_flight_reservation.csv'

        # Title Label
        title_label = ctk.CTkLabel(self.window, text="DELETE FLIGHT", text_color='cyan', font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Flight Number Entry
        flight_number_label = ctk.CTkLabel(self.window, text="Flight Number:", font=("Arial", 14))
        flight_number_label.pack(pady=(20, 5))
        self.flight_number_entry = ctk.CTkEntry(self.window, width=250, placeholder_text="Enter flight number to delete")
        self.flight_number_entry.pack(pady=5)

        # Delete Button
        delete_button = ctk.CTkButton(self.window, text="Delete", command=self.delete_flight, corner_radius=15)
        delete_button.pack(pady=20)

    def delete_flight(self):
        flight_number = self.flight_number_entry.get().strip()  # Strip whitespace

        # Check if the CSV file exists
        if not os.path.exists(self.csv_file):
            tkmb.showerror("Error", "Flight data file not found.")
            return

        # Load CSV file
        df = pd.read_csv(self.csv_file)

        # Verify that 'flightNumber' column exists
        if 'flightNumber' not in df.columns:
            tkmb.showerror("Error", "'flightNumber' column not found in file.")
            return

        # Check if flight exists in the CSV (convert both to strings for accurate comparison)
        df['flightNumber'] = df['flightNumber'].astype(str)
        if flight_number not in df['flightNumber'].values:
            tkmb.showwarning("Warning", f"Flight {flight_number} not found.")
            flight_number.delete(0, 'END')
            return

        # Remove the flight and save back to CSV
        df = df[df['flightNumber'] != flight_number]
        df.to_csv(self.csv_file, index=False)
        
        tkmb.showinfo("Success", f"Deleted Flight | ID: {flight_number}")
        # Close the window after deletion (optional)
        self.window.destroy()
