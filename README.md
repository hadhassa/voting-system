🗳️ Voting System
A Comprehensive Dual-Platform Electronic Voting Solution
A feature-rich voting system available in both desktop (Tkinter) and web (Flask) versions. This application provides secure, user-friendly voting with real-time results, duplicate prevention, and comprehensive admin monitoring.

📋 Table of Contents
Overview

Key Features

Technical Stack

Project Structure

Installation Guide

Desktop Application

Web Application

How It Works

API Documentation

Database Schema

Security Features

Screenshots

Future Enhancements

Contributing

License

Author

🎯 Overview
The Voting System is a comprehensive electronic voting solution available in two variants:

🖥️ Desktop Version (Tkinter)
A standalone GUI application with fullscreen interface, ideal for local deployments in schools, colleges, or small organizations.

🌐 Web Version (Flask)
A modern web-based platform accessible from any device with a browser, featuring real-time updates and comprehensive admin dashboard.

Both versions share core functionality:

✅ One voter, one vote

✅ Age verification (18+)

✅ Real-time result tracking

✅ Winner/Tie detection

✅ Secure database storage

✨ Key Features
Core Features (Both Versions)
Feature	Description
🔐 Unique Code Voting	Each voter uses a personalized code
🛡️ Duplicate Prevention	Advanced validation to prevent multiple votes
👤 Age Validation	Automatic eligibility verification (18+)
🏆 Winner Detection	Identifies majority party and handles ties
💾 SQLite Integration	Reliable local database storage
📊 Result Analysis	Instant vote counting and display
Desktop Version Features
🖥️ Fullscreen immersive interface

🎨 Custom background image support

🎯 Intuitive party selection

📋 Immediate result display

🔄 Auto-initialization on start

Web Version Features
🌐 Accessible from any device

📱 Responsive design

⚡ Real-time AJAX updates

🖥️ Admin dashboard with complete vote history

🔄 Live result refreshing

📊 Detailed vote breakdown

🛠️ Technical Stack
Desktop Application
Component	Technology
GUI Framework	Tkinter
Image Processing	Pillow (PIL)
Database	SQLite3
Language	Python 3.x
Web Application
Component	Technology
Backend Framework	Flask
Frontend	HTML5, CSS3, JavaScript
API	RESTful JSON
Templating	Jinja2
Database	SQLite3
Language	Python 3.x
📁 Project Structure
text
voting-system/
│
├── 📁 desktop-app/                 # Tkinter Desktop Version
│   ├── 📄 votingsystem.py          # Main application file
│   ├── 🗄️ voting_system.db         # SQLite database
│   └── 🖼️ voting_bg.png            # Background image
│
├── 📁 web-app/                      # Flask Web Version
│   ├── 📄 app.py                    # Flask application
│   ├── 🗄️ voting.db                 # SQLite database
│   └── 📁 templates/                # HTML templates
│       ├── 📄 index.html            # Voting interface
│       └── 📄 admin.html            # Admin dashboard
│
├── 📄 README.md                     # Project documentation
├── 📄 LICENSE                       # MIT License
├── 📄 .gitignore                    # Git ignore file
├── 📄 requirements.txt              # Python dependencies
│
└── 📁 screenshots/                  # Application screenshots
    ├── desktop-interface.png
    ├── web-interface.png
    ├── admin-dashboard.png
    └── results-display.png
💻 Installation Guide
Prerequisites
Python 3.6 or higher

pip package manager

Modern web browser (for web version)

🖥️ Desktop Application
Step 1: Clone Repository
bash
git clone https://github.com/hadhassa/voting-system.git
cd voting-system/desktop-app
Step 2: Install Dependencies
bash
pip install pillow
Step 3: Verify Installation
bash
python -c "import PIL; print('Pillow installed successfully')"
Step 4: Run Application
bash
python votingsystem.py
Note: The application will launch in fullscreen mode.

🌐 Web Application
Step 1: Navigate to Web Directory
bash
cd web-app
Step 2: Install Dependencies
bash
pip install flask
Step 3: Run Application
bash
python app.py
Step 4: Access Application
Voting Interface: http://localhost:5000

Admin Dashboard: http://localhost:5000/admin

🔄 How It Works
Voting Process Flow
<img width="3279" height="5287" alt="deepseek_mermaid_20260616_46025a" src="https://github.com/user-attachments/assets/0fbefe23-bc8d-4404-a62f-95ceedce4cdf" />
Winner Determination Logic
Count Votes: Tally votes for each party

Find Maximum: Identify party with highest votes

Check Tie: If multiple parties have same highest votes

Declare Winner:

Single party: Winner announced

Multiple parties: Tie declared

Supported Parties
NOTA (None of the Above)

Party A

Party B

Party C

Party D

🌐 API Documentation (Web Version)
1. Home Page
text
GET /
Returns the voting interface with party selection.

2. Submit Vote
text
POST /vote
Content-Type: application/json

Request Body:
{
    "user_code": "ABC123",
    "age": 25,
    "party": "Party A"
}

Success Response (200):
{
    "status": "success",
    "message": "Vote cast successfully."
}

Error Responses:
400: {"status": "error", "message": "Error description"}
409: {"status": "error", "message": "This code has already voted."}
3. Get Results
text
GET /results

Response:
{
    "totals": {
        "NOTA": 5,
        "Party A": 12,
        "Party B": 8,
        "Party C": 3,
        "Party D": 7
    },
    "details": {
        "Party A": [
            {
                "user_code": "ABC123",
                "age": 25,
                "created_at": "2026-01-16T10:30:00"
            }
        ]
    },
    "total_votes": 35,
    "winner": {
        "parties": ["Party A"],
        "votes": 12,
        "is_tie": false
    }
}
4. Admin Dashboard
text
GET /admin
Returns admin interface with:

Complete vote history

Real-time vote tally by party

Winner determination with tie handling

Timestamp of each vote

📊 Database Schema
Desktop Version (voting_system.db)
Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY, AUTOINCREMENT	Unique record identifier
code	TEXT	UNIQUE, NOT NULL	Voter's unique identification
age	INTEGER	CHECK (age >= 18)	Voter's age
party	TEXT	NOT NULL	Selected political party
timestamp	DATETIME	DEFAULT CURRENT_TIMESTAMP	Vote timestamp
Web Version (voting.db)
Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY, AUTOINCREMENT	Unique record identifier
user_code	TEXT	UNIQUE, NOT NULL	Voter's unique identification
age	INTEGER	NOT NULL	Voter's age
party	TEXT	NOT NULL	Selected political party
created_at	TEXT	NOT NULL	ISO timestamp of vote
Database Indexes
sql
-- For faster lookups
CREATE INDEX idx_votes_code ON votes(user_code);
CREATE INDEX idx_votes_party ON votes(party);
CREATE INDEX idx_votes_created ON votes(created_at);
🔒 Security Features
Implemented Security Measures
Feature	Desktop Version	Web Version
Duplicate Prevention	✅ UNIQUE constraint	✅ UNIQUE constraint
Age Verification	✅ Server-side validation	✅ Server-side validation
Input Validation	✅ Type checking	✅ Type checking
Data Integrity	✅ ACID compliance	✅ ACID compliance
SQL Injection Prevention	✅ Parameterized queries	✅ Parameterized queries
Transaction Support	✅	✅
Error Handling	✅ Try-catch blocks	✅ Comprehensive responses
Security Best Practices
✅ No storage of sensitive personal information

✅ Local database with restricted access

✅ Input sanitization and validation

✅ Clear error messages without system exposure

✅ Unique code validation for unauthorized access prevention

🖼️ Screenshots
Desktop Application
Interface	Description
https://screenshots/desktop-interface.png	Fullscreen voting interface with background image
https://screenshots/desktop-results.png	Results display with vote counts
Web Application
Interface	Description
https://screenshots/web-interface.png	Responsive web voting interface
https://screenshots/admin-dashboard.png	Admin dashboard with vote history
(Note: Add your actual screenshots in the screenshots folder)

🚀 Future Enhancements
Short-term (Next Release)
User authentication system

Email notification for vote confirmation

Export results to CSV/PDF

Interactive charts for results

Multi-language support

Long-term (Future Releases)
Blockchain integration for vote verification

Biometric authentication

Real-time vote streaming

Mobile application (React Native)

Docker containerization

CI/CD pipeline setup

Cloud deployment (AWS/Azure)

Load balancing for high traffic

Advanced analytics dashboard

API rate limiting

Desktop Version Specific
Dark/Light theme toggle

Print results functionality

Export data to Excel

Voice input support

Accessibility features (screen reader)

Web Version Specific
OAuth integration (Google/Facebook login)

Two-factor authentication

CAPTCHA implementation

WebSocket for real-time updates

Progressive Web App (PWA)

🤝 Contributing
We welcome contributions! Please follow these steps:

Contribution Process
Fork the Repository

bash
# Click the Fork button on GitHub
Clone Your Fork

bash
git clone https://github.com/yourusername/voting-system.git
cd voting-system
Create a Feature Branch

bash
git checkout -b feature/AmazingFeature
Make Your Changes

Follow PEP 8 style guide

Write meaningful commit messages

Add comments for complex logic

Update documentation

Test Thoroughly

Run both applications

Test all endpoints

Verify database operations

Commit and Push

bash
git add .
git commit -m 'Add some AmazingFeature'
git push origin feature/AmazingFeature
Open a Pull Request

Provide clear description

Reference related issues

Include screenshots if applicable

Code Style Guidelines
Python: PEP 8

JavaScript: ESLint

HTML/CSS: W3C standards

Comments: Clear and descriptive

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

text
MIT License

Copyright (c) 2026 Hadhassa Chigurupati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
👨‍💻 Author
Hadhassa Chigurupati
Student | Developer | Technology Enthusiast

🐙 GitHub: @hadhassa

🔗 LinkedIn: Hadhassa Chigurupati

📧 Email: hadhassa@example.com

Project Links
📦 Repository: https://github.com/hadhassa/voting-system

🐛 Issue Tracker: https://github.com/hadhassa/voting-system/issues

🙏 Acknowledgments
Thanks to all contributors and testers

Special appreciation to the open-source community

Inspired by the need for secure digital voting systems

Built with ❤️ using Python and Flask

📚 Additional Resources
Documentation
Tkinter Documentation

Flask Documentation

SQLite Documentation

Pillow Documentation

Tutorials
Python GUI Programming with Tkinter

Flask Web Development Tutorial

SQLite with Python

📝 Version History
Version	Date	Changes
1.0.0	2024-01-15	Initial release - Desktop Tkinter version
2.0.0	2026-01-16	Complete rewrite - Flask web version added
2.1.0	2026-01-16	Admin dashboard and API endpoints
2.2.0	2026-01-16	Enhanced winner determination and tie handling
2.3.0	2026-01-16	Dual-platform support (Desktop + Web)
2.4.0	Current	Comprehensive documentation and security updates
💡 Quick Start
Desktop Version
bash
cd desktop-app
pip install pillow
python votingsystem.py
Web Version
bash
cd web-app
pip install flask
python app.py
# Open http://localhost:5000
📞 Support & Contact
For support, feature requests, or bug reports:

🐛 GitHub Issues: Create an issue

📧 Email: hadhassachigurupati@gmail.com

💬 Discussions: GitHub Discussions

⭐ Star the Project
If you found this project helpful, please consider giving it a ⭐ on GitHub!

Made with ❤️ by Hadhassa Chigurupati

