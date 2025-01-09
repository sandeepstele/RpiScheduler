# RPi Scheduler

## Overview  
**RPi Scheduler** is an open-source task and event scheduling application designed for efficient event and task management. It includes features like event creation, event categorization, deadline tracking, and more. The app integrates weather data for better user context and enables automated notifications via Google Home.  

While primarily designed to run on a Raspberry Pi, it can also be deployed on any platform with Python support.

---

## Features  

- **Event Scheduling**: Add, modify, and delete events.  
- **Task Completion**: Mark events as completed.  
- **Weather Integration**: Displays the current weather for Chennai using the OpenWeatherMap API.  
- **Dashboard View**: Interactive, color-coded event display.  
- **Google Home Integration**: Provides daily task summaries.  
- **Canvas Mode (Task Display)**: Visual display of tasks with dynamic sorting and priority adjustments.  

---

## Technologies Used  

- **Python 3.x**  
- **Flask Web Framework**  
- **SQLite Database**  
- **HTML5, CSS3, JavaScript** (for dynamic features)  
- **Google Assistant Integration** (via API)  
- **OpenWeatherMap API** (for weather data)  

---

## Installation Instructions  

### 1. Clone the Repository  

```bash
git clone https://github.com/yourusername/rpi-scheduler.git
cd rpi-scheduler
