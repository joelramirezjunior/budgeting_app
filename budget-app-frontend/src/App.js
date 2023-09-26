import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';  // Import Link from react-router-dom
import { BrowserRouter as Router, Route, useNavigate, useLocation } from 'react-router-dom';
import { Routes} from 'react-router-dom';
import './App.css'; 

const AccountForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    user_name: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
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
        <input
          type="text"
          name="user_name"
          value={formData.user_name}
          onChange={handleInputChange}
          placeholder="Username"
        />
      </div>
      <div>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          placeholder="Email"
        />
      </div>
      <button type="submit">Create Account</button>
    </form>
  );
};

const LoginForm = () => {
  const [loginData, setLoginData] = useState({
    user_name: '',
    password: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLoginData({
      ...loginData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle the login logic here, possibly making an API call.
    console.log("Attempting to login with data:", loginData);
  };

  return (
    
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="text"
          name="user_name"
          value={loginData.user_name}
          onChange={handleInputChange}
          placeholder="Username"
        />
      </div>
      <div>
        <input
          type="password"
          name="password"
          value={loginData.password}
          onChange={handleInputChange}
          placeholder="Password"
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};


const FinancialForm = () => {
  const location = useLocation();

  const email = location.state?.email || ""; // extract email from state
  
  const [financialData, setFinancialData] = useState({
    retirement_amount: '',
    savings: '',
    checkings: '',
    email: email // set email in financialData
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
      const response = await axios.post('http://127.0.0.1:5000/add_financial_info', financialData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log(response.data);
    } catch (error) {
      console.error("Error while sending financial data:", error);
    }
  };

  return (
    <form className="financeInfo" onSubmit={handleSubmit}>
      <div >
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

const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};


const AppContent = () => {
  const [accountInfo, setAccountInfo] = useState(null);
  
  const navigate = useNavigate();
  const location = useLocation();  // Import this from 'react-router-dom'

  const handleCreateAccount = async (formData) => {
    try {
      console.log("Attempting API POST", formData);
      const response = await axios.post('http://127.0.0.1:5000/add_account', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setAccountInfo(response.data);
      navigate("/financial-form", { state: { email: formData.email } });
    } catch (error) {
      console.error("Error while sending data:", error);
    }
  };
  

  return (
    <div className="app-container">
      <h1 className="app-title">Budgeting App</h1>
      

      <Routes>
        <Route path="/" element={<AccountForm onSubmit={handleCreateAccount} />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/financial-form" element={<FinancialForm />} />
      </Routes>
      
      {(location.pathname === '/login') && (
        <div className="navigation">
          <Link to="/">Need to create an account?</Link>
        </div>
      )}

      {(location.pathname === '/') && (
        <div className="navigation">
          <Link to="/login">Already have an account?</Link>
        </div>
      )}

    </div>
  );
};

export default App;
