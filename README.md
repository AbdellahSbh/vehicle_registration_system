# vehicle_registration_system

This project is a comprehensive automated traffic management system that digitizes vehicle registration, monitors traffic violations, analyzes traffic flow, and prioritizes emergency vehicles.

## Project Overview

The vehicle_registration_system is designed for a city's traffic department to digitize its operations with the following core functionality:

- Vehicle registration with details like number plate, owner's name, and vehicle type
- License plate recognition to monitor vehicles at major city junctions
- Traffic violation monitoring and automated fine issuance
- Traffic flow analysis and congestion management
- Emergency vehicle prioritization and route clearing
- PostgreSQL database for data storage

## Software Dependencies

### Docker & Git
* Docker https://www.docker.com/
* Git https://git-scm.com/downloads

### Backend (Django)
* Python 3.11 or higher
* Django 4.x or higher
* `psycopg2` (PostgreSQL adapter for Python)
* OpenCV for license plate recognition
* Django REST framework for API endpoints

### Database (PostgreSQL)
* PostgreSQL 13.x or higher

## Setup Instructions

### Step 1: Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/AbdellahSbh/vehicle_registration_system.git
cd vehicle_registration_system
```

### Step 2: Build and Start the Containers
Run the following command to build and start all Docker containers:

```bash
docker-compose up -d --build
```

### Step 3: Run Migrations
Once the containers are up and running, enter the backend Django container:

```bash
docker-compose exec backend_django bash
```

Inside the container, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Access the Frontend
Open your browser and visit:

```
http://0.0.0.0:8000
```

### Step 5: Stop the Containers
To stop and remove the running containers:

```bash
docker-compose down
```

Your PostgreSQL data will persist between runs.

## Docker Compose Services

* **db** – PostgreSQL database
* **backend_django** – Django backend

## Project Structure

```
vehicle_registration_system/
│
├── registration/                           #Django backend
├── vehicleregistration/                    #Django backend
├── requirements.txt                        #Docker
├── docker-compose.yml                      #Docker
├── Dockerfile                              #Docker
└── README.md                               #This file
```

## Features

1. Register a Vehicle
- Allows you to enter a new vehicle into the system.

2. Log License Plate
- Lets you manually log or scan a vehicle’s license plate.

3. View Registered Vehicles
- Displays a list of all vehicles that have been registered.

4. View License Plate Logs
- Shows records of all logged license plates, including time and possibly location.

5. Start Vehicle Simulation
- Starts a simulation to vehicle movement.

6. View Junction Traffic
- Displays traffic data or statistics for specific intersections.

7. Log Vehicle Violation
- Allows entry of traffic violations committed by vehicles.

8. Admin Panel
- Opens the administrative dashboard for system management or settings.

9. Login
- Button to log into the system.

