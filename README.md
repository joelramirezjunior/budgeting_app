# Budgeting App

##### note very barebones Readme -- will be updated as I work on this and get it functional. 
## Introduction

Welcome to the Budgeting App, a full-stack application built with React and Flask. This app helps users create an account and manage their finances.

## Features

- User Account creation
- Adding financial information like Retirement Amount, Savings, and Checking Account balance

## Getting Started

### Prerequisites

- Node.js
- Python 3.x
- MongoDB

### Setup

1. **Clone the repository**
    ```
    git clone https://github.com/your-repo-link
    ```

2. **Navigate to the frontend directory and install npm packages**
    ```
    cd frontend
    npm install
    ```

3. **Navigate to the backend directory and install Python packages**
    ```
    cd ../backend
    pip install -r requirements.txt
    ```

4. **Start MongoDB**

    Make sure MongoDB is running locally. If not, you can start it with:
    ```
    mongod
    ```

### Running the App

1. **Frontend**

    Navigate to the frontend directory and start the React app:
    ```
    cd frontend
    npm start
    ```
    The app will be available at `http://localhost:3000`.

2. **Backend**

    Navigate to the backend directory and start the Flask app:
    ```
    cd ../backend
    python app.py
    ```
    The backend API will be available at `http://localhost:8000`.

## File Structure

### Frontend (`/frontend`)

- `App.jsx`: The entry point of the React application.
- `AccountForm.jsx`: Component for account creation.
- `FinancialForm.jsx`: Component for entering financial details.
- `AccountInfo.jsx`: (Optional) Component for displaying account information.

### Backend (`/backend`)

- `app.py`: The entry point for the Flask application.
- `routes.py`: Contains all the route handlers.

## Code Overview

### Frontend

We use React hooks and Axios for API calls. For instance, in `AppContent`:

```jsx
const handleSubmit = async (formData) => {
  const response = await axios.post('http://127.0.0.1:5000/add_account', formData, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
};
```

### Backend

We use Flask and PyMongo for the backend. For example, in `add_account`:

```python
@app.route('/add_account', methods=['POST', 'OPTIONS'])
def add_account():
    json_data = request.get_json()
    accounts = mongo.db.accounts
    account_id = accounts.insert_one(data).inserted_id
```

## API Endpoints

### note: more to come eventually...just started writting this last night...or so.

- POST `/add_account`: Adds a new account.
- POST `/add_financial_info`: Adds financial information for an account.

## Security

Sensitive information like names and emails are hashed before storing in the MongoDB database.

## Contributing

Pull requests are welcome.

## License

This project is licensed under the MIT License.

---

Happy coding! Feel free to reach out for any questions or issues.