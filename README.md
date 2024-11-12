# Event Addis

Event Addis is an event management application that helps users in Addis Ababa discover, create, and manage events. It provides features for event discovery, creation, booking, and user management, all through a user-friendly interface.

## Key Features

- **Event Discovery**: Search events by category, location, or date.
- **Event Creation**: Host events by providing event details, date, time, location, and ticket options.
- **User Authentication**: Register and log in to create/manage events or register for events.
- **Location-Based Search**: Find events around specific locations in Addis Ababa.
- **Admin Dashboard**: Allows admins to manage events and users.

## Installation and Setup

### Prerequisites

- **Python 3.8+**
- **Flask** (for backend)
- **Node.js** (for frontend if separate)
- **MySQL/PostgreSQL**
- **Nginx** (for deployment)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Event-Addis.git
   cd Event-Addis
2. **Backend Installation**

**Set up a virtual environment and install dependencies:**

   Copy code
   ```bash
   
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   python3 -m api.v1.app

