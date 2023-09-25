# Budgeting App

A simple budgeting application built using React, Flask, and MongoDB. The application allows users to create accounts and add financial information for better budgeting.

## Features

- Account creation with first name, last name, email, and username.
- Add financial details like retirement amount, savings, and checkings.
- Backend API built with Flask and MongoDB for data persistence.
  
## Technologies Used

- Frontend: React.js
- Backend: Flask, Python
- Database: MongoDB
- Containerization: Docker

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

### Clone the repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### Build and Run the Application

We use Docker Compose to manage and run the services. This will build the React frontend, Flask backend, and MongoDB database as separate services.

```bash
docker-compose up --build
```

After running the above command, you should have:

- React app running on `http://localhost:3000`
- Flask API running on `http://localhost:5000`
- MongoDB running on `localhost:27017`

### Note for MontereyOS Users

If you are using MontereyOS and encounter an error stating that port 5000 is already in use, this may be because the AirPlay feature uses this port. To resolve this, go into your computer's preferences to disable AirPlay, and the application should run as expected.

## Directory Structure

```
.
├── flask_api
│   ├── app
│   │   └── app.py
│   └── Dockerfile
├── budget-app-frontend
│   ├── src
│   │   └── App.js
│   └── Dockerfile
└── docker-compose.yml
```

### Frontend (React.js)

The frontend is built using React.js. Here are some important files and their descriptions:

- `App.js`: Main component where all routes and major logic reside.

### Backend (Flask)

The backend is built using Flask. Here are some important files and their descriptions:

- `app/app.py`: This is where the Flask app and routes are defined. Note that it resides inside an `app` directory within the `flask_api` folder.
- `models.py`: Contains the MongoDB models for storing data.

## Endpoints

### Flask API

#### `POST /add_account`

Creates a new user account.

#### `POST /add_financial_info`

Adds financial details of a particular user.

## Contributing

If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

MIT

---

Feel free to adjust as needed!