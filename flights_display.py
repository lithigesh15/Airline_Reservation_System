import customtkinter as ctk
import pandas as pd
import numpy as np
import heapq
from datetime import datetime, timedelta
import random
import tkinter as tk
import os
from tkinter import messagebox

class FlightDisplayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        self.title("Flight Display")
        self.geometry("900x610")
        self.configure(bg="#f8f9fa")  # Light background for modern look


        self.selected_seats = []

        self.final_flight_booking = ["", "", "", "", "", "","","","", "", "", "" ,"","","",""]
        #self.final_flight_booking = np.array(["acco", "depar", "arr", "date", "way", "flight no","path","depart_time","arr_time", "duration", "price", "seat" ])

        # Center the main window
        self.center_window()

        # Set up main frame
        self.setup_main_frame()

        # Flight data can be fetched from a database or API
        self.flight_data = self.get_flight_data()

        self.connecting_flights = self.find_top_connecting_flights()

        # Dynamically create the flight rows
        self.display_flights(self.flight_data,"Direct FLights")

        self.display_flights(self.connecting_flights,"Connecting Flights")

        # Start the main loop
        self.mainloop()

        print(self.final_flight_booking)

    def center_window(self):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position x and y
        x = (screen_width // 2) - (900 // 2)  # 900 is the width of the window
        y = (screen_height // 2) - (600 // 2)  # 600 is the height of the window

        # Set the position of the window
        self.geometry(f"+{x}+{y}")

    def setup_main_frame(self):
        # Create main frame that holds the content
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")  # White background for content
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Add sorting and filtering bar
        self.setup_sort_filter_bar()

        # Add header for the page
        self.setup_header()

        # Create a scrollable frame for displaying flights
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#e9ecef")
        self.scrollable_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        # Add IST indication at the bottom
        self.ist_label = ctk.CTkLabel(self.main_frame, text="All times are in Indian Standard Time (IST)", 
                                       font=("Arial", 10), text_color="#6c757d")  # Grey color for the IST note
        self.ist_label.pack(side="bottom", pady=(5, 0))

    def setup_sort_filter_bar(self):
        # Create a bar for sorting and filtering
        sort_filter_frame = ctk.CTkFrame(self.main_frame, fg_color="#f1f3f4")  # Light color for the bar
        sort_filter_frame.pack(fill="x", padx=10, pady=10)

        # Sorting dropdown
        sort_label = ctk.CTkLabel(sort_filter_frame, text="Sort by:", font=("Arial", 14))
        sort_label.pack(side="left", padx=10)

        sort_options = ["Price (Low to High)", "Price (High to Low)", "Duration", "Departure Time"]
        self.sort_dropdown = ctk.CTkOptionMenu(sort_filter_frame, values=sort_options)
        self.sort_dropdown.pack(side="left", padx=10)

        # Apply Button
        apply_button = ctk.CTkButton(sort_filter_frame, text="Apply", command=self.apply_sort_filter, fg_color="#007bff")
        apply_button.pack(side="right", padx=10)

    def setup_header(self):
        # Create a label for the source, destination, and date selection
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#f1f3f4")
        header_frame.pack(fill="x", padx=10, pady=10)

        src_label = ctk.CTkLabel(header_frame, text="", font=("Arial", 16, "bold"))
        src_label.pack(side="left", padx=10)

        arrow_label = ctk.CTkLabel(header_frame, text="", font=("Arial", 16))
        arrow_label.pack(side="left", padx=5)

        dest_label = ctk.CTkLabel(header_frame, text="", font=("Arial", 16, "bold"))
        dest_label.pack(side="left", padx=5)

        date_label = ctk.CTkLabel(header_frame, text="Thu, 17 Oct 24", font=("Arial", 14))
        date_label.pack(side="right", padx=10)

    def display_flights(self, flights,header):
        # Add a header row for flight details
        self.create_flight_header(self.scrollable_frame,header)

        # Dynamically add rows for each flight
        for flight in flights:
            self.create_flight_row(self.scrollable_frame, flight)

    def create_flight_header(self, parent_frame,header):
        # Header row with titles for each column
        # Create the "Direct Flight" header
        
        direct_flight_header = ctk.CTkLabel(parent_frame, text=header, font=("Arial", 14, "bold"), fg_color="#d1e7dd", corner_radius=10)
        direct_flight_header.pack(fill="x", pady=(10, 0))

        # Create the header row with labels
        header_row = ctk.CTkFrame(parent_frame, fg_color="#d1e7dd", corner_radius=10)
        header_row.pack(fill="x", pady=5)

        labels = ["Flight", "  Departure", " Arrival", "    Duration", "     Economy", "  Business", "First Class", "View More"]
        for label in labels:
            header_label = ctk.CTkLabel(header_row, text=label, font=("Arial", 12, "bold"), padx=5)
            header_label.pack(side="left", padx=20, pady=10)


    def create_flight_row(self, parent_frame, flight):
        # Create a row for each flight
        flight_row = ctk.CTkFrame(parent_frame, fg_color="#fdfdfe", corner_radius=10, border_width=1, border_color="#ced4da")
        flight_row.pack(fill="x", pady=5)

        # Set proper grid alignment for the flight details
        for i in range(8):
            flight_row.grid_columnconfigure(i, weight=1, uniform="flight_col")  # Ensures all columns get equal weight

        # Flight number, departure time, arrival time, and duration
        flight_no_label = ctk.CTkLabel(flight_row, text=f"{flight['flight_no']}", font=("Arial", 14), padx=10)
        flight_no_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        departure_label = ctk.CTkLabel(flight_row, text=f"{flight['departure_time']}", font=("Arial", 14), padx=10)
        departure_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        arrival_label = ctk.CTkLabel(flight_row, text=f"{flight['arrival_time']}", font=("Arial", 14), padx=10)
        arrival_label.grid(row=0, column=2, padx=5, pady=10, sticky="w")

        duration_label = ctk.CTkLabel(flight_row, text=f"{flight['duration']}", font=("Arial", 14), padx=10)
        duration_label.grid(row=0, column=3, padx=5, pady=10, sticky="w")

        # Economy, Business, and First Class prices as buttons
        economy_button = ctk.CTkButton(flight_row, text=f"INR {flight['price_economy']}", font=("Arial", 14), command=lambda: self.book_flight(flight, "Economy"), fg_color="#007bff")
        economy_button.grid(row=0, column=4, padx=5, pady=10, sticky="ew")  # Ensure buttons stretch to fill space horizontally

        business_button = ctk.CTkButton(flight_row, text=f"INR {flight['price_business']}", font=("Arial", 14), command=lambda: self.book_flight(flight, "Business"), fg_color="#007bff")
        business_button.grid(row=0, column=5, padx=5, pady=10, sticky="ew")

        first_class_button = ctk.CTkButton(flight_row, text=f"INR {flight['price_first_class']}", font=("Arial", 14), command=lambda: self.book_flight(flight, "First Class"), fg_color="#007bff")
        first_class_button.grid(row=0, column=6, padx=5, pady=10, sticky="ew")

        # View More button to open detailed flight window with green color
        view_more_button = ctk.CTkButton(flight_row, text="View More", font=("Arial", 14), command=lambda: self.show_loading_screen_view_more(flight), fg_color="#28a745")  # Green color for the button       
        view_more_button.grid(row=0, column=7, padx=5, pady=10, sticky="ew")

    def get_flight_data(self):

        # Load the flight details CSV
        flight_details_path = 'DSA_project_flight_reservation.csv'
        flight_data = pd.read_csv(flight_details_path)

        def parse_time(time_str):
            """Convert a time string in 'HH:MM' format to a datetime object."""
            return datetime.strptime(time_str, '%H:%M')

        def calculate_duration(departure_time, arrival_time):
            """Calculate duration between departure and arrival, handling overnight flights."""
            dep_time = parse_time(departure_time)
            arr_time = parse_time(arrival_time)
            
            # If arrival is earlier than departure, assume the flight lands the next day
            if arr_time < dep_time:
                arr_time += timedelta(days=1)
                
            # Calculate the duration as a timedelta object
            duration = arr_time - dep_time
            return duration

        def format_duration(duration):
            """Format a timedelta duration into HH:MM."""
            total_minutes = int(duration.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours:02}:{minutes:02}"

        # Create a flight graph as an adjacency list
        flight_graph = {}
        flight_data_list = []

        for _, row in flight_data.iterrows():
            flight_no = str(row['flightNumber'])
            departure_time = row['scheduledDepartureTime']
            arrival_time = row['scheduledArrivalTime']
            origin = row['origin']
            destination = row['destination']
            
            # Calculate duration with proper handling for overnight flights
            duration = calculate_duration(departure_time, arrival_time)
            formatted_duration = format_duration(duration)  # Convert to HH:MM format for display

            flight_data_list.append({
                "flight_no": flight_no,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "origin": origin,
                "destination": destination,
                "duration": formatted_duration  # Use formatted duration for display
            })
            
            # Store duration in minutes for internal calculations, formatted only for display
            duration_minutes = int(duration.total_seconds() // 60)
            if origin not in flight_graph:
                flight_graph[origin] = []
            flight_graph[origin].append((destination, duration_minutes, flight_no))

        # Function to fix a random price based on flight duration
        def fix_price_based_on_duration(duration):
            """Fix prices for economy, business, and first class based on duration."""
            # Example pricing strategy
            if duration < 60:
                return {
                    "economy": random.randint(1000, 1500),
                    "business": random.randint(2000, 3000),
                    "first_class": random.randint(4000, 6000)
                }
            elif duration < 120:
                return {
                    "economy": random.randint(1500, 2500),
                    "business": random.randint(3000, 4500),
                    "first_class": random.randint(6000, 8000)
                }
            else:
                return {
                    "economy": random.randint(2500, 3500),
                    "business": random.randint(4500, 6000),
                    "first_class": random.randint(8000, 10000)
                }

        # Dijkstra's algorithm to find all flights from departure city
        def dijkstra_all_flights(departure):
            """Find all flights from the departure city."""
            # Priority queue to hold (duration, current_city, path)
            pq = [(0, departure, [])]
            visited = set()
            all_flights = []

            while pq:
                total_duration, current_city, path = heapq.heappop(pq)

                if current_city in visited:
                    continue
                    
                visited.add(current_city)
                path = path + [current_city]

                # Record flights from the current city
                for neighbor, duration, flight_no in flight_graph.get(current_city, []):
                    if neighbor not in visited:
                        # Collect flight details
                        for flight in flight_data_list:
                            if flight['flight_no'] == flight_no:
                                all_flights.append({
                                    "flight_no": flight['flight_no'],
                                    "departure_time": flight['departure_time'],
                                    "arrival_time": flight['arrival_time'],
                                    "duration": total_duration + duration,  # Include the duration to neighbor
                                    "origin": current_city,
                                    "destination": neighbor
                                })
                        heapq.heappush(pq, (total_duration + duration, neighbor, path))

            return all_flights

        # Load the CSV containing booking details and extract the last row
        file_path = 'user_input.csv'  # Path to the booking details CSV
        data = pd.read_csv(file_path)
        booking_details = data.iloc[-1].values

        departure = booking_details[1]

        self.final_flight_booking[1] = str(booking_details[1])  # "Departure"
        self.final_flight_booking[2] = str(booking_details[2])  # "Arrival"
        self.final_flight_booking[3] = str(booking_details[8])  # "date" as string
        self.final_flight_booking[4] = str(booking_details[9])  # return date
        self.final_flight_booking[12] = str(booking_details[0])  # user id
        self.final_flight_booking[13] = str(booking_details[3]) # adult
        self.final_flight_booking[14] = str(booking_details[4]) # child
        self.final_flight_booking[15] = str(booking_details[5]) # infant


        # Find all flights from the departure city

        all_flights = dijkstra_all_flights(departure)

        # Sort and select the top 20 flights based on their duration
        top_flights = sorted(all_flights, key=lambda x: x['duration'])[:20]

        # Prepare final flight details in the desired format
        flight_data = []
        for flight in top_flights:
            duration_str = str(timedelta(minutes=flight['duration']))
            price = fix_price_based_on_duration(flight['duration'])  # Get price based on duration
            flight_data.append({
                "flight_no": flight['flight_no'],
                "departure_time": flight['departure_time'],
                "arrival_time": flight['arrival_time'],
                "duration": duration_str,
                "price_economy": price['economy'],
                "price_business": price['business'],
                "price_first_class": price['first_class']
            })

        return flight_data

    def apply_sort_filter(self):
        # Show loading screen
        self.show_loading_screen()

        # Get the selected sorting option
        self.selected_option = self.sort_dropdown.get()

        # Sort direct flights based on the selected option
        self.sorted_direct_flights = self.sort_flights(self.flight_data, self.selected_option)

        # Sort connecting flights based on the selected option
        self.sorted_connecting_flights = self.sort_flights(self.connecting_flights, self.selected_option)

        # Update the display with sorted flights
        self.display_flights(self.sorted_direct_flights, header="Sorted Direct Flights")
        self.display_flights(self.sorted_connecting_flights, header="Sorted Connecting Flights")

    def sort_flights(self, flights, selected_option):
        # Define sorting logic based on selected option
        if selected_option == "Price (Low to High)":
            sorted_flights = sorted(flights, key=lambda x: x['price_economy'])
        elif selected_option == "Price (High to Low)":
            sorted_flights = sorted(flights, key=lambda x: x['price_economy'], reverse=True)
        elif selected_option == "Duration":
            sorted_flights = sorted(flights, key=lambda x: x['duration'])
        elif selected_option == "Departure Time":
            sorted_flights = sorted(flights, key=lambda x: x['departure_time'])
        else:
            # Default to no sorting if option doesn't match
            sorted_flights = flights

        return sorted_flights

    def show_loading_screen(self):
        # Hide the main application window
        self.withdraw()  # Hides the main window

        # Create the splash screen window
        splash_root = ctk.CTk()
        splash_root.geometry("400x200")
        splash_root.title("Loading...")

        # Center the splash screen
        splash_x = (self.winfo_screenwidth() // 2) - (400 // 2)
        splash_y = (self.winfo_screenheight() // 2) - (200 // 2)
        splash_root.geometry(f"+{splash_x}+{splash_y}")

        # Add a label to the splash screen
        splash_label = ctk.CTkLabel(splash_root, text="Sorting the Flights", font=("Arial", 16))
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
                self.perform_sort_filter()  # Perform sorting/filtering logic after loading is complete

        # Start updating the progress after 100ms
        splash_root.after(100, update_progress)
        splash_root.mainloop()

    def perform_sort_filter(self):
        # Clear existing flights from display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Re-display sorted/filtered flights (this is where you would apply sorting/filtering logic)
        self.display_flights(self.flight_data,"Direct Flights")

        self.display_flights(self.connecting_flights,"Connecting Flights")

        # Show the main window again after loading is complete
        self.deiconify()

    def show_flight_details(self, flight):
        # Create a new window for flight details
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Flight Details - {flight['flight_no']}")
        details_window.geometry("900x600")  # Fixed size
        details_window.resizable(False, False)  # Disable resizing to prevent fullscreen

        # Center the details window
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        details_window.geometry(f"+{x}+{y}")

        # Flight details header with larger font and a separator line
        flight_info = f"Flight No: {flight['flight_no']}\n" \
                    f"Departure: {flight['departure_time']}\n" \
                    f"Arrival: {flight['arrival_time']}\n" \
                    f"Duration: {flight['duration']}"
        
        # Display path if available
        if 'path' in flight:
            path_info = " ➔ ".join(flight['path'])
            flight_info += f"\nConnecting Path: {path_info}"

        flight_info_label = ctk.CTkLabel(
            details_window, text=flight_info, font=("Arial", 18, "bold"), justify="center", 
            text_color="#2D3A45"  # Dark grey color for text
        )
        flight_info_label.pack(pady=(10, 5))

        # Main frame containing all elements
        main_frame = ctk.CTkFrame(details_window, width=860, height=500)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Back button at the top-right corner
        close_button = ctk.CTkButton(
            main_frame, text="Back", command=lambda: self.back_view_more(details_window),
            fg_color="#FF0000", text_color="white", font=("Arial", 14, "bold")
        )
        close_button.grid(row=8, column=1, sticky="ne", padx=(0, 10), pady=(10, 0))

        # Section header with icons and spacing for classes
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="ew")

        economy_label = ctk.CTkLabel(header_frame, text="✈️ Economy", font=("Arial", 14, "bold"), text_color="#2D3A45")
        economy_label.grid(row=0, column=0, padx=50)

        business_label = ctk.CTkLabel(header_frame, text="💼 Business", font=("Arial", 14, "bold"), text_color="#2D3A45")
        business_label.grid(row=0, column=1, padx=50)

        first_class_label = ctk.CTkLabel(header_frame, text="🛋️ First Class", font=("Arial", 14, "bold"), text_color="#2D3A45")
        first_class_label.grid(row=0, column=2, padx=50)

        # Price details
        prices_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        prices_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        economy_price_label = ctk.CTkLabel(prices_frame, text=f"INR {flight['price_economy']}", font=("Arial", 12), text_color="#545E6F")
        economy_price_label.grid(row=0, column=0, padx=50)

        business_price_label = ctk.CTkLabel(prices_frame, text=f"INR {flight['price_business']}", font=("Arial", 12), text_color="#545E6F")
        business_price_label.grid(row=0, column=1, padx=50)

        first_class_price_label = ctk.CTkLabel(prices_frame, text=f"INR {flight['price_first_class']}", font=("Arial", 12), text_color="#545E6F")
        first_class_price_label.grid(row=0, column=2, padx=50)

        # Baggage details
        baggage_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        baggage_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        economy_baggage_label = ctk.CTkLabel(baggage_frame, text="🧳 Baggage: 40kg", font=("Arial", 12), text_color="#545E6F")
        economy_baggage_label.grid(row=0, column=0, padx=50)

        business_baggage_label = ctk.CTkLabel(baggage_frame, text="🧳 Baggage: 50kg", font=("Arial", 12), text_color="#545E6F")
        business_baggage_label.grid(row=0, column=1, padx=50)

        first_class_baggage_label = ctk.CTkLabel(baggage_frame, text="🧳 Baggage: 60kg", font=("Arial", 12), text_color="#545E6F")
        first_class_baggage_label.grid(row=0, column=2, padx=50)

        # Seat selection and lounge access
        seat_selection_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        seat_selection_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        seat_selection_label = ctk.CTkLabel(seat_selection_frame, text="🪑 Seat Selection: Complimentary", font=("Arial", 12), text_color="#545E6F")
        seat_selection_label.grid(row=0, column=0, padx=50)

        lounge_label = ctk.CTkLabel(seat_selection_frame, text="🛋️ Lounge Access: Available", font=("Arial", 12), text_color="#545E6F")
        lounge_label.grid(row=0, column=1, padx=50)

        # Add hover effect for the Back button
        close_button.bind("<Enter>", lambda e: close_button.configure(fg_color="#CC0000"))
        close_button.bind("<Leave>", lambda e: close_button.configure(fg_color="#FF0000"))

    def back_view_more(self, details_window):
        # Close the details window and show the main window again
        details_window.destroy()
        self.deiconify()  # Show the main flight display window


    def show_loading_screen_view_more(self, flight):
        # Hide the main application window
        self.withdraw()  # Hides the main window

        # Create the splash screen window
        splash_root = ctk.CTk()
        splash_root.geometry("400x100")
        splash_root.title("Loading...")
        splash_root.resizable(0,0)

        # Center the splash screen
        splash_x = (self.winfo_screenwidth() // 2) - (400 // 2)
        splash_y = (self.winfo_screenheight() // 2) - (200 // 2)
        splash_root.geometry(f"+{splash_x}+{splash_y}")

        # Add a label to the splash screen
        splash_label = ctk.CTkLabel(splash_root, text="Loading", font=("Arial", 16))
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
                self.show_flight_details(flight)  # Perform sorting/filtering logic after loading is complete

        # Start updating the progress after 100ms
        splash_root.after(100, update_progress)
        splash_root.mainloop()

    def seat_selection_app(self):
    # Create a Toplevel window instead of Tk root to avoid blocking
        seat_window = tk.Toplevel(self)
        seat_window.title("Seat Selection")
        seat_window.geometry("800x800")

        # Create a frame for the seat grid
        seat_frame = tk.Frame(seat_window)
        seat_frame.pack(pady=20)

        # Initialize seat selection (8 rows, 6 columns)
        seats = [[0] * 6 for _ in range(8)]  # 8 rows, 6 columns
        buttons = []

        # Row labels
        row_labels = [chr(65 + i) for i in range(8)]  # A, B, C, D, E, F, G, H

        # Create column labels
        for col in range(6):
            label = tk.Label(seat_frame, text=str(col + 1), font=('Arial', 12, 'bold'))
            label.grid(row=0, column=col + 1 + (1 if col >= 3 else 0), padx=5, pady=5)

        # Function to toggle seat selection
        def toggle_seat(row, col):
            if seats[row][col] == 0:  # Available
                seats[row][col] = 1  # Mark as selected
                buttons[row][col].config(text="Selected", bg="green")
            else:  # Selected
                seats[row][col] = 0  # Mark as available
                buttons[row][col].config(text="Available", bg="SystemButtonFace")

        # Create seat buttons with row labels
        for row in range(8):
            row_buttons = []
            for col in range(6):
                button = tk.Button(seat_frame, text="Available", width=10, height=3,
                                command=lambda r=row, c=col: toggle_seat(r, c))
                button.grid(row=row + 1, column=col + 1 + (1 if col >= 3 else 0), padx=5, pady=5)
                row_buttons.append(button)
            buttons.append(row_buttons)

            # Row label
            label = tk.Label(seat_frame, text=row_labels[row], font=('Arial', 12, 'bold'))
            label.grid(row=row + 1, column=0)

        # Confirmation button
        def confirm_selection():
            
            for r in range(8):
                for c in range(6):
                    if seats[r][c] == 1:
                        seat_label = f"{row_labels[r]}{c + 1}"
                        self.selected_seats.append(seat_label)

            if self.selected_seats:
                self.final_flight_booking[11] = str(self.selected_seats)
                messagebox.showinfo("Selected Seats", f"You have selected: {', '.join(self.selected_seats)}")
            else:
                messagebox.showinfo("No Selection", "No seats selected.")

            seat_window.destroy()  # Close seat selection window when done

        confirm_button = tk.Button(seat_window, text="Confirm Selection", command=confirm_selection)
        confirm_button.pack(pady=20)


    def book_flight(self, flight, class_type):
        self.withdraw()  # Hide main window
        self.seat_selection_app()  # Call seat selection

        # Create booking window after seat selection window
        booking_window = ctk.CTkToplevel(self)
        booking_window.title("Book Flight")
        booking_window.geometry("700x450")
        booking_window.minsize(700, 450)
        booking_window.configure(bg="white")

        # Convert class_type to lowercase and construct the price key
        class_type = class_type.lower()
        price_key = f"price_{class_type}"

        # Retrieve the price
        price = flight.get(price_key, None)  # Get the price or None if key doesn't exist
        
        self.final_flight_booking[5] = str(flight['flight_no'])  # "flight_no"
        self.final_flight_booking[6] = str(flight['path']) if 'path' in flight else None  # "path"
        self.final_flight_booking[7] = str(flight['departure_time'])  # "departure_time"
        self.final_flight_booking[8] = str(flight['arrival_time'])  # "arrival_time"
        self.final_flight_booking[9] = str(flight['duration'])  # "duration"
        self.final_flight_booking[10] = str(price)  # "price"

        def go_back():
            booking_window.destroy()
            self.deiconify()  # Show the main window again

        # Header section
        header_frame = ctk.CTkFrame(booking_window, bg_color="lightblue")
        header_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(header_frame, text="Flight Booking", font=("Arial", 24, "bold"), text_color="black").pack(pady=5)

        ctk.CTkLabel(booking_window, text="Passenger Details", font=("Arial", 18, "bold"), bg_color="white").pack(pady=10)

        self.passenger_frame = ctk.CTkFrame(booking_window, bg_color="white")
        self.passenger_frame.pack(pady=10, fill="both", expand=True, padx=10)

        self.passenger_entries = []

        self.create_passenger_input(1)

        # Back button to return to previous window
        back_button = ctk.CTkButton(booking_window, text="Back",
                                    command=go_back,
                                    fg_color="lightcoral", hover_color="red", corner_radius=8)
        back_button.pack(side="left", padx=20, pady=20)

        # Next button to go to the next window
        next_button = ctk.CTkButton(booking_window, text="Next",
                                    command=lambda: self.show_passenger_windows(booking_window, flight, class_type),
                                    fg_color="lightgreen", hover_color="green", corner_radius=8)
        next_button.pack(side="right", padx=20, pady=20)


    def create_passenger_input(self, passenger_number):
        passenger_frame = ctk.CTkFrame(self.passenger_frame, bg_color="white")
        passenger_frame.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(passenger_frame, text=f"Passenger {passenger_number} Name:", font=("Arial", 12)).pack(side="top", anchor="w")
        name_entry = ctk.CTkEntry(passenger_frame, width=250)
        name_entry.pack(pady=5)

        ctk.CTkLabel(passenger_frame, text=f"Passenger {passenger_number} Phone:", font=("Arial", 12)).pack(side="top", anchor="w")
        phone_entry = ctk.CTkEntry(passenger_frame, width=250)
        phone_entry.pack(pady=5)

        ctk.CTkLabel(passenger_frame, text=f"Passenger {passenger_number} Email:", font=("Arial", 12)).pack(side="top", anchor="w")
        email_entry = ctk.CTkEntry(passenger_frame, width=250)
        email_entry.pack(pady=5)

        # Store the entry widgets for the passenger
        self.passenger_entries.append((name_entry, phone_entry, email_entry))

    def show_passenger_windows(self, booking_window, flight, class_type):
        # Gather passenger data before closing the booking window
        passenger_data = []
        for passenger_info in self.passenger_entries:
            name_entry, phone_entry, email_entry = passenger_info
            passenger_data.append({
                "name": name_entry.get(),
                "phone": phone_entry.get(),
                "email": email_entry.get(),
            })

        # Close the booking window after gathering data

        self.show_passenger_confirmation(passenger_data,booking_window)


    def save_booking_to_csv(self):
        filename = "booking_info.csv"
        
        # Ensure that self.final_flight_booking exists and is a list
        if not hasattr(self, 'final_flight_booking') or not isinstance(self.final_flight_booking, list):
            print("Error: 'final_flight_booking' is missing or is not a list.")
            return

        # Define headers for each element in the list
        headers = ["Account No", "Departure", "Arrival", "departure_date", "retrun_date", "flight no", "path", "depart_time", "arr_time", "duration", "price", "seat","user id", "adult","child", "infant"]

        # Create a DataFrame with one row from the list
        df = pd.DataFrame([self.final_flight_booking], columns=headers)

        # Debugging: Print the DataFrame to check its structure before saving
        print("Data to be saved:\n", df)

        # Check if the file exists
        if os.path.isfile(filename):
            # Append the new data without writing the header
            df.to_csv(filename, mode='a', header=False, index=False)
            print(f"Data appended to {filename}.")
        else:
            # Write data with the header if the file is new
            df.to_csv(filename, mode='w', header=True, index=False)
            print(f"{filename} created and data written with header.")



    def show_passenger_confirmation(self, passenger_data, booking_window):
        booking_window.withdraw()
        passenger_window = ctk.CTkToplevel(self)
        passenger_window.title("Confirm Booking Details")
        passenger_window.geometry("600x400")
        passenger_window.minsize(600, 400)
        passenger_window.configure(bg="white")

        def go_back():
            passenger_window.destroy()
            booking_window.deiconify()

        ctk.CTkLabel(passenger_window, text="Confirm Booking Details", font=("Arial", 24, "bold"), bg_color="white").pack(pady=10)

        for passenger_info in passenger_data:
            ctk.CTkLabel(passenger_window, text=f"Name: {passenger_info['name']}", font=("Arial", 14), bg_color="white").pack(pady=5)
            ctk.CTkLabel(passenger_window, text=f"Phone: {passenger_info['phone']}", font=("Arial", 14), bg_color="white").pack(pady=5)
            ctk.CTkLabel(passenger_window, text=f"Email: {passenger_info['email']}", font=("Arial", 14), bg_color="white").pack(pady=5)
            ctk.CTkLabel(passenger_window, text="", bg_color="white").pack()

        back_button = ctk.CTkButton(passenger_window, text="Back", command=go_back, 
                                    fg_color="lightcoral", hover_color="red", corner_radius=8)
        back_button.pack(pady=20)

        confirm_button = ctk.CTkButton(passenger_window, text="Confirm",
                                        command=lambda: self.show_payment_window(passenger_window),
                                        fg_color="lightgreen", hover_color="green", corner_radius=8)
        confirm_button.pack(pady=5)

    def show_payment_window(self,passenger_window):
        passenger_window.withdraw()
        # Create the payment window
        payment_window = ctk.CTkToplevel(self)
        payment_window.title("Payment Window")
        payment_window.geometry("700x450")  # Increased size for better layout
        payment_window.minsize(700, 450)  # Set minimum size
        payment_window.configure(bg="white")  # Light background

        def go_back():
            payment_window.destroy()
            passenger_window.deiconify()

        ctk.CTkLabel(payment_window, text="Payment Details", font=("Arial", 24, "bold"), bg_color="white").pack(pady=20)

        # Frame for payment input fields
        payment_frame = ctk.CTkFrame(payment_window, bg_color="white")
        payment_frame.pack(pady=10)

        # Account Number
        ctk.CTkLabel(payment_frame, text="Account Number:", font=("Arial", 14), bg_color="white").pack(pady=5)
        account_entry = ctk.CTkEntry(payment_frame, width=300)
        account_entry.pack(pady=5)

        # PAN Card Details
        ctk.CTkLabel(payment_frame, text="Aadhar Card Details:", font=("Arial", 14), bg_color="white").pack(pady=5)
        pan_entry = ctk.CTkEntry(payment_frame, width=300)
        pan_entry.pack(pady=5)

        # Account Password
        ctk.CTkLabel(payment_frame, text="Account Password:", font=("Arial", 14), bg_color="white").pack(pady=5)
        password_entry = ctk.CTkEntry(payment_frame, width=300, show="*")  # Hide password
        password_entry.pack(pady=5)

        # Back button to return to booking window
        back_button = ctk.CTkButton(payment_window, text="Back", command=go_back, 
                                    fg_color="lightcoral", hover_color="red", corner_radius=8)
        back_button.pack(side="left", padx=20, pady=20)

        # Payment button
        pay_button = ctk.CTkButton(payment_window, text="Pay",
                            command=lambda: self.process_payment(
                                account_entry.get(), 
                                pan_entry.get(), 
                                password_entry.get(),
                                payment_window  # Pass the payment window to close it later
                            ),
                            fg_color="lightgreen", hover_color="green", corner_radius=8)
        
        pay_button.pack(side="right", padx=20, pady=20)

    def process_payment(self, account_number, pan_card, password,payment_window):
        self.final_flight_booking[0] = str(account_number)
        # Simulate payment processing
        print(f"Processing payment...\nAccount: {account_number}\nAadhar: {pan_card}\nPassword: {password}")
        
        # Simulate a successful payment process
        payment_success = True  # Change this based on real payment logic

        if payment_success:
            self.payment_loading_screen(account_number,payment_window)
        else:
            print("Payment failed!")
            # You can add error handling here if needed

    def payment_loading_screen(self,account_number,payment_window):
        payment_window.withdraw()

        # Create the splash screen window
        splash_root = ctk.CTk()
        splash_root.geometry("400x100")
        splash_root.title("Loading...")

        # Center the splash screen
        splash_x = (self.winfo_screenwidth() // 2) - (400 // 2)
        splash_y = (self.winfo_screenheight() // 2) - (200 // 2)
        splash_root.geometry(f"+{splash_x}+{splash_y}")

        # Add a label to the splash screen
        splash_label = ctk.CTkLabel(splash_root, text="Processing.....", font=("Arial", 16))
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
                self.show_payment_confirmation_csv(account_number)

        # Start updating the progress after 100ms
        splash_root.after(100, update_progress)
        splash_root.mainloop()

    def show_payment_confirmation_csv(self,account_number):
        
        
        
        self.save_booking_to_csv()
        self.show_payment_confirmation(account_number)


    def show_payment_confirmation(self,account_number):
        # Create a payment confirmation window
        confirmation_window = ctk.CTkToplevel(self)
        confirmation_window.title("Payment Confirmation")
        confirmation_window.geometry("600x300")  # Size for confirmation window
        confirmation_window.minsize(600, 300)  # Set minimum size
        confirmation_window.configure(bg="white")  # Light background

        ctk.CTkLabel(confirmation_window, text="Payment Successful!", font=("Arial", 24, "bold"), bg_color="white").pack(pady=20)

        ctk.CTkLabel(confirmation_window, text="Thank you for your payment.", font=("Arial", 16), bg_color="white").pack(pady=10)

        # Optionally, show account details or any other relevant info
        ctk.CTkLabel(confirmation_window, text=f"Account Number: {account_number}", font=("Arial", 14), bg_color="white").pack(pady=5)
        ctk.CTkLabel(confirmation_window, text="Your transaction has been completed successfully.", font=("Arial", 14), bg_color="white").pack(pady=5)

        # Button to close the confirmation window
        close_button = ctk.CTkButton(confirmation_window, text="Close", command=confirmation_window.destroy, fg_color="lightcoral", hover_color="red", corner_radius=8)

        close_button.pack(pady=20)

    def find_top_connecting_flights(self):
        # Paths to the CSV files
        flight_details_path = 'DSA_project_flight_reservation.csv'  # Path to flight details
        user_input_path = 'user_input.csv'  # Path to user booking details

        # Load the flight details CSV
        flight_data = pd.read_csv(flight_details_path)

        def calculate_flight_duration(departure_time, arrival_time):
            # Assuming departure_time and arrival_time are in 'HH:MM' format.
            time_format = "%H:%M"
            
            # Convert the time strings to datetime objects
            departure_dt = datetime.strptime(departure_time, time_format)
            arrival_dt = datetime.strptime(arrival_time, time_format)
            
            # Calculate the difference in time
            duration = arrival_dt - departure_dt
            
            # Handle cases where arrival time is past midnight
            if duration.days < 0:
                duration += timedelta(days=1)
            
            # Calculate the duration in minutes
            duration_minutes = duration.seconds // 60
            return duration_minutes

        
        # Create a flight graph as an adjacency list
        flight_graph = {}
        flight_data_list = []

        for _, row in flight_data.iterrows():
            flight_no = str(row['flightNumber'])
            departure_time = row['scheduledDepartureTime']
            arrival_time = row['scheduledArrivalTime']
            origin = row['origin']
            destination = row['destination']

            duration = calculate_flight_duration(departure_time, arrival_time)

            flight_data_list.append({
                "flight_no": flight_no,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "origin": origin,
                "destination": destination,
                "duration": duration
            })

            # Add to the graph
            if origin not in flight_graph:
                flight_graph[origin] = []
            flight_graph[origin].append((destination, duration, flight_no))

        # Function to fix a random price based on flight duration
        def fix_price_based_on_duration(duration):
            """Fix prices for economy, business, and first class based on duration."""
            if duration < 60:
                return {
                    "economy": random.randint(1000, 1500),
                    "business": random.randint(2000, 3000),
                    "first_class": random.randint(4000, 6000)
                }
            elif duration < 120:
                return {
                    "economy": random.randint(1500, 2500),
                    "business": random.randint(3000, 4500),
                    "first_class": random.randint(6000, 8000)
                }
            else:
                return {
                    "economy": random.randint(2500, 3500),
                    "business": random.randint(4500, 6000),
                    "first_class": random.randint(8000, 10000)
                }

        # Dijkstra's algorithm to find all connecting flights
        def dijkstra_connecting_flights(departure, arrival):
            """Find all connecting flights from the departure city to the arrival city."""
            pq = [(0, departure, [])]  # (total_duration, current_city, path)
            visited = set()
            all_flights = []
            connecting_flight_paths = []  # Array to store only the paths

            while pq:
                total_duration, current_city, path = heapq.heappop(pq)

                if current_city in visited:
                    continue

                visited.add(current_city)
                path = path + [current_city]

                # Explore flights from the current city
                for neighbor, duration, flight_no in flight_graph.get(current_city, []):
                    if neighbor not in path:  # Ensure not to revisit a city in the current path
                        new_duration = total_duration + duration

                        # If we reach the arrival city with at least one connection, record the flight details
                        if neighbor == arrival and len(path) > 1:  # Ensure there is a connection
                            all_flights.append({
                                "path": path + [neighbor],  # Full path taken
                                "total_duration": new_duration,
                                "flight_no": flight_no
                            })
                            connecting_flight_paths.append(path + [neighbor])  # Store only the path

                        # Push the next flight to the priority queue
                        heapq.heappush(pq, (new_duration, neighbor, path))

            return all_flights, connecting_flight_paths

        # Load the CSV containing booking details and extract the last row
        data = pd.read_csv(user_input_path)
        booking_details = data.iloc[-1].values

        departure = booking_details[1]
        arrival = booking_details[2]

        # Find all connecting flights
        connecting_flights, connecting_flight_paths = dijkstra_connecting_flights(departure, arrival)

        # Sort and select the top 10 connecting flights based on their total duration
        top_connecting_flights = sorted(connecting_flights, key=lambda x: x['total_duration'])[:10]

        # Prepare final flight details in the desired format
        final_flight_data_with_paths = []
        for i, flight in enumerate(top_connecting_flights):
            total_duration_str = str(timedelta(minutes=flight['total_duration']))
            price = fix_price_based_on_duration(flight['total_duration'])  # Get price based on total duration
            final_flight_data_with_paths.append({
                "flight_no": flight['flight_no'],
                "path": flight['path'],
                "departure_time": flight_data_list[0]['departure_time'],  # Assume first departure for simplicity
                "arrival_time": flight_data_list[0]['arrival_time'],  # Assume first arrival for simplicity
                "duration": total_duration_str,
                "price_economy": price['economy'],
                "price_business": price['business'],
                "price_first_class": price['first_class']
            })
            

        # Return both final flight data and paths for further use if needed
        return final_flight_data_with_paths



#FlightDisplayApp()