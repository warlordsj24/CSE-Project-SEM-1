# CSE-Project-SEM-1

# Bus Seat Booking System (Python Tkinter)

This is a simple GUI-based Bus Seat Booking System made using Python and Tkinter.
It lets you book seats, cancel them, check statistics, and view all bookings.
All data is saved in a JSON file so it doesn’t get lost when the program closes.

---

## Features

- Clickable seat buttons (A1, A2, A3, …)
- Book a seat by entering name + phone number
- Cancel a booked seat
- Shows which seats are taken (red) and free (green)
- Currently selected seat turns yellow
- Statistics window (total seats, booked, free, % occupancy)
- View all bookings in a scrollable window
- Data saved to `data_bus.json`

---

## How to Run

1. Install Python 3 (if not installed)
2. Make sure Tkinter is installed (comes with Python)
3. Run the program:


4. The GUI will open and you can start booking seats.

---

## Files

- `bus_gui_messy.py` — main program  
- `data_bus.json` — automatically created data file  

---

## Requirements

- Python 3.8 or higher
- Tkinter (preinstalled with Python)
- JSON module (built in)

---

## Notes

- This is a simple student-level project.
- The code is intentionally a bit imperfect to resemble human-written logic.
- You can customize the number of rows/columns inside the code if needed.

---

## Future Improvements

- Add multiple buses
- Add seat pricing
- Add admin login
- Print tickets to PDF

