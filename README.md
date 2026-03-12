🗳️ Voting System (Python + Tkinter + SQLite)

A GUI-based Voting System developed using Python, Tkinter, and SQLite.
This application allows users to cast votes using a unique code, verifies voter eligibility based on age, prevents duplicate voting, and displays the majority and minority voting results.

📌 Project Description

This project demonstrates a secure and user-friendly electronic voting system.
The application uses a graphical interface (Tkinter) for user interaction and SQLite database for storing voting data.

It ensures:

Each voter can vote only once

Only users 18 years or older can vote

Votes are stored securely

Results display vote counts, majority, and minority parties

🚀 Features

🖥️ User-friendly GUI interface

🗳️ Voting using unique user codes

🔐 Duplicate vote prevention

👤 Age validation (18+)

💾 SQLite database integration

📊 Automatic vote counting

🏆 Majority and minority party identification

🖼️ Fullscreen interface with background image

🛠️ Technologies Used

Python

Tkinter (GUI)

SQLite Database

Pillow (PIL) for images

📂 Project Structure
voting-system/
│
├── votingsystem.py        # Main Python voting application
├── voting_system.db       # SQLite database
├── voting_bg.png          # Background image for GUI
├── memorygame.html        # Additional project file
├── hotelbooking.java      # Additional project file
└── README.md              # Project documentation
⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/hadhassa/voting-system.git
2️⃣ Navigate to Project Folder
cd voting-system
3️⃣ Install Required Library
pip install pillow
▶️ Run the Application
python votingsystem.py

The application will launch in fullscreen voting interface.

📊 How the System Works

User enters a unique code

User enters their age

User selects a political party

System checks:

Age eligibility (must be 18+)

Whether the user already voted

If valid, the vote is stored in SQLite database

Results page displays:

Total votes per party

Majority party

Minority party

🔒 Security Features

Unique user code validation

Duplicate voting prevention

Database-level unique constraints

Input validation for age and selections

📷 Future Improvements

Admin login for result access

Vote result graphs

Online voting system

Voter authentication system

Improved UI design

👨‍💻 Author

Hadhassa Chigurupati

GitHub:
https://github.com/hadhassa
