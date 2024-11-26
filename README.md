# ✈️ Airline Ticket Reservation System 📋

Welcome to the **Airline Ticket Reservation System** project! This project is a comprehensive implementation of a flight booking system using Python with a GUI designed in **CustomTkinter**. It also incorporates CSV files for data storage, using **Pandas** for data manipulation and retrieval. This README will guide you through the setup, features, and the technical aspects of the project. 

## 📑 Table of Contents
- [🎯 Project Overview](#-project-overview)
- [🛠️ Features](#️-features)
- [📋 Prerequisites](#-prerequisites)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📊 Analysis and Algorithms](#-analysis-and-algorithms)
  - [🔀 Dijkstra Algorithm for Flight Routes](#-dijkstra-algorithm-for-flight-routes)
- [📸 Screenshots](#-screenshots)
- [📜 License](#-license)
- [📞 Contact](#-contact)

## 🎯 Project Overview

This Airline Ticket Reservation System is designed to provide an intuitive GUI-based platform for users to search and book flights. It consists of several key functionalities including user registration, flight search, booking, and payment handling. The application aims to make the flight booking process efficient and user-friendly.

The system consists of:
- **User Sign In / Registration Page**
- **Admin Login for Flight Management**
- **Flight Search & Booking**
- **Seat Selection**
- **Passenger Information Form**
- **Payment Gateway Integration**
- **Booking History View**

Data is stored in CSV files, and operations like sorting by flight price (low to high/high to low) and filtering by flight duration are handled seamlessly with **Pandas**.

## 🛠️ Features

- 🌐 **User Authentication** (Registration & Login)
- 🔍 **Flight Search** with sorting and filtering
- 🛫 **Seat Selection** Interface
- 📑 **Passenger Information** Collection
- 💳 **Payment System** (Mock implementation)
- 📚 **View Booking History**
- 🛡️ **Admin Panel** for managing flights
- 📊 **Data Analysis** using CSV

## 📋 Prerequisites

Make sure you have the following installed:
- **Python 3.7+**
- Required Python libraries:
  ```python
  pip install customtkinter pandas tkcalendar
  ```
- CSV files for storing flight data and user information.

## 📦 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Airline_Reservation_system.git
   cd Airline_Reservation_system
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

## 🚀 Usage

### 1. User Registration
Sign up for a new account or log in using existing credentials. This allows users to access flight search, booking, and other features.

### 2. Admin Log In and Flight Management
Admins can log in with special credentials to manage the flight database. Admin capabilities include:
- **Add a Flight**: Input flight details to add a new flight to the system.
- **Delete a Flight**: Remove a flight from the database if it is no longer available.
- **Modify a Flight**: Update flight details such as schedule, price, or available seats.

### 3. Flight Search
Enter departure location, destination, travel date, and other necessary details to find available flights.

### 4. Booking
Choose a preferred flight, select seats, and enter passenger information to complete the reservation.

### 5. Payment
Complete the booking by proceeding through a mock payment interface. Review the booking summary and confirm payment.

### 6. View Bookings
Access and manage your booking history at any time. This section provides a summary of all past and current reservations.


## 📊 Analysis and Algorithms

![WhatsApp Image 2024-11-04 at 21 30 37_b81febb5](https://github.com/user-attachments/assets/703530fc-787b-4176-8f49-a757078fb77c)


### 🔀 Dijkstra Algorithm for Flight Routes

The system incorporates the **Dijkstra Algorithm** to calculate the shortest path between two airports in terms of travel time or cost. This algorithm is essential for:
- **Optimizing flight routes** for display.
- Allowing users to see the most efficient travel options based on their search criteria.
- Handling the underlying graph structure that represents interconnected airports and available flights.

Here's a brief explanation of the algorithm:

> **Dijkstra's Algorithm** is used to find the shortest path from a source node to all other nodes in a graph. It works by iteratively selecting the node with the smallest known distance, updating the distances to its neighbors, and marking it as "visited."

This functionality is key for providing users with accurate and optimized flight options, enhancing the overall user experience. Additionally, it helps to sort the available flights based on the **total travel time** efficiently.



## 📸 Screenshots

- Log In Page
  ![Login Page](https://github.com/user-attachments/assets/eb501db6-2165-4789-92d0-5ca037d0461f)

- Registration Page
  ![Registration Page](https://github.com/user-attachments/assets/433dca25-be27-4d58-ba5a-4a5d484365b7)

- Admin Log In and Operations
  ![Admin Login](https://github.com/user-attachments/assets/8d5d4fb0-4390-4d98-a094-5d94d7744704)
  ![Admin Page](https://github.com/user-attachments/assets/fbba5b26-a672-496e-b11c-d40f85fad561)
  ![Add New FLight](https://github.com/user-attachments/assets/3834845d-6a09-4f06-a0fc-e1a7b77cd2a5)
  ![Modify a Flight](https://github.com/user-attachments/assets/6f4b6183-56cf-4d51-b3db-6127953ce618)
  ![Delete Flight](https://github.com/user-attachments/assets/afe9acc4-307b-43ed-a267-be7917060d55)

- Flight Search
  ![Book a flight](https://github.com/user-attachments/assets/f3ecad79-462f-415b-9614-4f92a8152856)

- Flight Display
  ![Flight Details](https://github.com/user-attachments/assets/8b2da9df-474b-452f-9fdd-9a8e797ecb55)

- Seat Selection
  ![Seat Selection](https://github.com/user-attachments/assets/cb77f7f0-e3ec-4d6c-b0c0-f1eddae7f420)

- Passenger Credentials
  ![Pasenger Credentials](https://github.com/user-attachments/assets/2cad0760-4e10-441d-b108-c8314a37fdf0)

- Payment Page
  ![Payment Details](https://github.com/user-attachments/assets/be3663c7-823b-4042-bdb5-599962be1984)
  ![Payment Confirmation](https://github.com/user-attachments/assets/eec1ad71-7db5-438a-acfc-57bcd875095d)




## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms.

## 📞 Contact

For any inquiries or contributions, please reach out:

- 📧 Email: lithigesh@gmail.com
- 🔗 LinkedIn: [Your Profile](https://linkedin.com/in/lithigesh15)

---
