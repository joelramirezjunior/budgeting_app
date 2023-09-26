import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom"; // Import Link from react-router-dom
import {
  BrowserRouter as Router,
  Route,
  useNavigate,
  useLocation,
} from "react-router-dom";
import { Routes } from "react-router-dom";
import "./App.css";

const AccountForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    user_name: "",
    password: "",
  });

  const [usernameError, setUsernameError] = useState(null); // <-- Step 1: New state for error message

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await onSubmit(formData); // get the returned value or error object
    if (result === null) {
      setUsernameError("Username already exists");
    } else if (result instanceof Error) {
      // handle other types of errors
    } else {
      setUsernameError(null);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleInputChange}
          placeholder="First Name"
        />
      </div>
      <div>
        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleInputChange}
          placeholder="Last Name"
        />
      </div>
      <div>
        <div className="input-container">
          <input
            type="text"
            name="user_name"
            value={formData.user_name}
            onChange={handleInputChange}
            placeholder="Username"
            className={usernameError ? "input-error" : ""} // <-- change the class conditionally
          />
          {usernameError && <span className="error-text">{usernameError}</span>}{" "}
        </div>
      </div>
      <div>
        <input
          type="password"
          name="pasword"
          value={formData.password}
          onChange={handleInputChange}
          placeholder="Password"
        />
      </div>
      <button type="submit">Create Account</button>
    </form>
  );
};

const LoginForm = ({ onSubmit }) => {
  const [loginData, setLoginData] = useState({
    user_name: "",
    password: "",
  });

  const [loginError, setError] = useState({
    wrongusername: null,
    wrongpassword: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLoginData({
      ...loginData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await onSubmit(formData); // get the returned value or error object
    if (result === 201) {
      setError({ wrongusername: "Username does not exist" });
    } else if (result == 202) {
      setError({ wrongpassword: "Password supplied is incorrect" });
    } else if (result instanceof Error) {
      console.log(result);
    } else {
      setError(null);
      setPasswordError(null);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <div className="input-container">
          <input
            type="text"
            name="user_name"
            value={loginData.user_name}
            onChange={handleInputChange}
            placeholder="Username"
            className={loginError.wrongusername ? "input-error" : ""} // <-- change the class conditionally
          />
          {loginError.wrongusername && (
            <span className="error-text">{loginError.wrongusername}</span>
          )}{" "}
        </div>
      </div>

      <div>
        <div className="input-container">
          <input
            type="password"
            name="password"
            value={loginData.password}
            onChange={handleInputChange}
            placeholder="Password"
            className={loginError.wrongusername ? "input-error" : ""} // <-- change the class conditionally
          />
          {loginError.wrongusername && (
            <span className="error-text">{loginError.wrongusername}</span>
          )}{" "}
        </div>
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

const FinancialForm = () => {
  const location = useLocation();

  const email = location.state?.email || ""; // extract email from state

  const [financialData, setFinancialData] = useState({
    retirement_amount: "",
    savings: "",
    checkings: "",
    email: email, // set email in financialData
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFinancialData({
      ...financialData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Submit to your API endpoint
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/add_financial_info",
        financialData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error while sending financial data:", error);
    }
  };

  return (
    <form className="financeInfo" onSubmit={handleSubmit}>
      <div>
        <label>Retirement Amount</label>
        <input
          type="number"
          name="retirement_amount"
          value={financialData.retirement_amount}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label>Savings</label>
        <input
          type="number"
          name="savings"
          value={financialData.savings}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label>Checkings</label>
        <input
          type="number"
          name="checkings"
          value={financialData.checkings}
          onChange={handleInputChange}
        />
      </div>
      <button type="submit">Submit Financial Info</button>
    </form>
  );
};

const homepage = () => {




  
}
const AppContent = () => {
  const [accountInfo, setAccountInfo] = useState(null);

  const navigate = useNavigate();
  const location = useLocation(); // Import this from 'react-router-dom'

  const handleCreateAccount = async (formData) => {
    try {
      console.log("Attempting API POST", formData);
      const response = await axios.post(
        "http://127.0.0.1:5000/add_account",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response);
      if (response && response.status === 200) {
        return null; // return a special value indicating failure
      }

      setAccountInfo(response.data);
      navigate("/financial-form", { state: { email: formData.email } });
      return response; // indicate success
    } catch (error) {
      console.error("Error while sending data: ", error);
      return error; // return the error object
    }
  };

  const handleLogin = async (formData) => {
    try {
      console.log("Attempting API POST", formData);
      const response = await axios.post(
        "http://127.0.0.1:5000/login",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response);
      if (response && response.status != 200) {
        return response.status;
      }

      setAccountInfo(response.data);
      navigate("/homepage", { state: { user_id: response.user_id } });
      return response; // indicate success
    } catch (error) {
      console.error("Error while sending data: ", error);
      return error; // return the error object
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Budgeting App</h1>

      <Routes>
        <Route
          path="/"
          element={<AccountForm onSubmit={handleCreateAccount} />}
        />
        <Route path="/login" element={<LoginForm onSubmit={handleLogin} />} />
        <Route path="/financial-form" element={<FinancialForm />} />
        <Route path="/homepage" element={<DisplayFinances />} />
      </Routes>

      {location.pathname === "/login" && (
        <div className="navigation">
          <Link to="/">Need to create an account?</Link>
        </div>
      )}

      {location.pathname === "/" && (
        <div className="navigation">
          <Link to="/login">Already have an account?</Link>
        </div>
      )}
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
