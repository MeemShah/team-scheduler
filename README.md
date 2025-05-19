# Team Schedule Manager

## Project Description

Team Schedule Manager is a web-based application designed to help teams efficiently track and manage their schedules. It enables users to create teams, assign members, and set an initial working date from which schedules are calculated, working days in week. 

The system automatically determines which team is scheduled to work on any given day. In addition to daily tracking, users can view a complete weekly schedule and search for team assignments based on specific dates, ensuring streamlined coordination and planning.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [Contributing](#contributing)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MeemShah/team-scheduler.git
   cd team-schedule-manager
   ```

2. **Backend Setup (Python + FastAPI)**
   - Create a virtual environment and activate it
     ```bash
     python -m .venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```
   - Install dependencies
     ```bash
     pip install -r requirements.txt
     ```

3. **Database Setup (PostgreSQL)**
   - Make sure PostgreSQL is running.
   - Put your credentials in .env file 
   - Create a new database `team-scheduler` 
   - go to `repository/db` and uncomment the 15'th line Once for migration.

              #self._initialize_schema()

4. **Frontend Setup**
   - Static files (HTML, CSS, JS) are located in the `static/` directory.
   - Open `index.html` in a browser or serve via a static file server.

5. **Run the server**
   ```bash
   uvicorn src.main:app --reload
   ```

## Usage

- Access the web app at `http://localhost:8000/index.html`.
- Features include:
  - Creating new teams
  - Adding team members
  - Setting an initial start date
  - Viewing the current weekly schedule
  - Highlighting which team is working on a specific day

## Credits

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL

Developed by Mostofa Meem

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a Pull Request
