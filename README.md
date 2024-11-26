![Screenshot 2024-11-26 203304](https://github.com/user-attachments/assets/a7e30ac9-378f-46ac-b64f-1d0099e5010a)![image](https://github.com/user-attachments/assets/6ebea9fb-30e7-46cd-a188-96050323fc23)# ✈️ Airline Ticket Reservation System 📋

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
   git clone https://github.com/yourusername/AirlineTicketReservationSystem.git
   cd AirlineTicketReservationSystem
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

1. **User Registration** - Sign up or log in using existing credentials.
2. **Flight Search** - Enter departure, destination, date, and other details to find available flights.
3. **Booking** - Choose a flight, select seats, and enter passenger details.
4. **Payment** - Complete the booking via the mock payment interface.
5. **View Bookings** - Access your booking history anytime.

## 📊 Analysis and Algorithms

### 🔀 Dijkstra Algorithm for Flight Routes

The system incorporates the **Dijkstra Algorithm** to calculate the shortest path between two airports in terms of travel time or cost. This algorithm is essential for:
- **Optimizing flight routes** for display.
- Allowing users to see the most efficient travel options based on their search criteria.
- Handling the underlying graph structure that represents interconnected airports and available flights.

Here's a brief explanation of the algorithm:

> **Dijkstra's Algorithm** is used to find the shortest path from a source node to all other nodes in a graph. It works by iteratively selecting the node with the smallest known distance, updating the distances to its neighbors, and marking it as "visited."

This functionality is key for providing users with accurate and optimized flight options, enhancing the overall user experience. Additionally, it helps to sort the available flights based on the **total travel time** efficiently.



## 📸 Screenshots

- **Log In Page**
  ![Screenshot 2024-11-26 203138](https://github.com/user-attachments/assets/19ff6866-af79-4b4e-81b6-20840e9247b9)
- **Registration Form**
  ![Screenshot 2024-11-26 203200](https://github.com/user-attachments/assets/49547025-6f51-4c7c-946d-a40c3d300a7a)
- **Admin Log in and Admin Operations Page**
![Screenshot 2024-11-26 203724](https://github.com/user-attachments/assets/7463fbf7-ecf7-415f-a627-d7de5df428f8)
![Screenshot 2024-11-26 203700](https://github.com/user-attachments/assets/fdc8c6cb-22d6-4f84-8a50-fd9d8c0a92ef)
![Screenshot 2024-11-26 203648](https://github.com/user-attachments/assets/4e8881c6-315f-4d26-bc4e-ff8cee07bbb6)
![Screenshot 2024-11-26 203638](https://github.com/user-attachments/assets/239d58b1-9cd7-4ecd-afb4-5583cb750f28)
![Screenshot 2024-11-26 203148](https://github.com/user-attachments/assets/23b7fa9c-1b54-429d-bdeb-2a80d088315a)
- **Flight Search Page**
  ![Screenshot 2024-11-26 203216](https://github.com/user-attachments/assets/1d3fd900-daf6-482a-bf1b-655c81662bb0)
- **Flight Display**
 ![Screenshot 2024-11-26 203251](https://github.com/user-attachments/assets/df8be392-9609-4cf2-8b9b-76907a965240)
- **Seat Selection**
  ![Screenshot 2024-11-26 203304](https://github.com/user-attachments/assets/94f260ab-e467-4c19-a73e-61767ff14836)
- **Passenger Credentials**
![Screenshot 2024-11-26 203317](https://github.com/user-attachments/assets/18ae50b5-9dc3-400b-9581-af462ada23e8)
- **Payment Page**
  ![Screenshot 2024-11-26 203328](https://github.com/user-attachments/assets/9d9a9d71-d3a4-4e09-9885-f460b21c55fd)
![Screenshot 2024-11-26 203401](https://github.com/user-attachments/assets/8089d484-9a8a-45e5-a211-ca023c02a691)


## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms.

## 📞 Contact

For any inquiries or contributions, please reach out:

- 📧 Email: lithigesh@gmail.com
- 🔗 LinkedIn: [Your Profile](https://linkedin.com/in/lithigesh15)

---
