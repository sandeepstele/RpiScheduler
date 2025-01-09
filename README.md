RPi Scheduler - README

Overview
RPi Scheduler is an open-source task and event scheduling application designed for managing events and tasks efficiently. It includes multiple features like event creation, event categorization, deadline tracking, and more. The app also integrates weather data for better user context and enables automated notifications via Google Home. The application is designed to run on a Raspberry Pi but can also be deployed on any platform with Python support.

Features
Event Scheduling: Add, modify, and delete events.
Task Completion: Mark events as completed.
Weather Integration: Displays the current weather for Chennai using OpenWeatherMap API.
Dashboard View: Events are displayed in an interactive, color-coded format.
Google Home Integration: Provides daily task summaries.
Canvas Mode (Task Display): Visual display of tasks with dynamic sorting and priority adjustments.
Technologies Used
Python 3.x
Flask Web Framework
SQLite Database
HTML5, CSS3
JavaScript for Dynamic Features
Google Assistant Integration (via API)
OpenWeatherMap API for weather data
Installation Instructions
1. Clone the Repository

git clone https://github.com/yourusername/rpi-scheduler.git

cd rpi-scheduler
2. Set Up Virtual Environment

python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt
4. Set Up Database

python setup.py
Configuration
Weather API Key: You’ll need to register at OpenWeatherMap to obtain an API key for weather data.
Add the key in config.py:
WEATHER_API_KEY = "your-api-key-here"
Google Home Integration:
To connect Google Assistant with your app, follow these Google Assistant integration guidelines.
Configure the task summaries to be sent daily at 9:00 AM.
Usage
Running the Application: After installing all dependencies and configuring your API keys, run the application with:
python run.py
Accessing the Web Interface: Open a browser and navigate to:
Admin Dashboard: http://localhost:5000/admin
Task Dashboard: http://localhost:5000/display
Canvas Mode:
The display.html page provides an interactive canvas-like display where you can view tasks categorized into Overdue, Today's Tasks, Tomorrow's Tasks, and Future Tasks.
Tasks are displayed side-by-side in their respective categories, with color-coded priority indicators (Urgent, Important, Not Urgent).
Tasks can be marked as completed and are visually crossed out.
A weather widget is included at the top of the page for context.
Contributing
Fork the Repository: Click the "Fork" button on GitHub to create a personal copy of the repository.
Clone Your Fork:
git clone https://github.com/yourusername/rpi-scheduler.git
Create a Branch:
git checkout -b feature-name
Make Changes & Commit: After making your changes, commit them with:
git add .
git commit -m "Add new feature"
Push Changes: Push your changes back to your forked repository:
git push origin feature-name
Create a Pull Request: Open a pull request to contribute your changes to the main repository.
License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Future Improvements
Mobile Optimization: Implement a responsive design for mobile screens.
User Authentication: Add user roles and login functionality to secure the application.
Advanced Sorting: Allow more complex sorting options such as filtering by categories or custom date ranges.
