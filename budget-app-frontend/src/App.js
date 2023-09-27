import React, { useState } from "react";
import {
  BrowserRouter as Router,
  useNavigate,
  useLocation,
  Link,
  Route,
  Routes,
} from "react-router-dom";
import "./App.css";
import useAccountAccess from "./useAccountAccess";
import useInputChange from "./useInputChange";
import useSubmitFinancialData from "./useSubmitFinancialData"; // Import the new hook

const AccountForm = ({ onSubmit }) => {
  const [formData, handleInputChange] = useInputChange({
    first_name: "",
    last_name: "",
    user_name: "",
    password: "",
  });

  const [usernameError, setUsernameError] = useState(null); // <-- Step 1: New state for error message

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const result = await onSubmit(formData); // get the returned value or error object
      if (result === 200) {
        setUsernameError("Username already exists");
      } else {
        setUsernameError(null);
      }
    } catch (error) {
      console.log(error);
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
          name="password"
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
  const [loginData, handleInputChange] = useInputChange({
    user_name: "",
    password: "",
  });

  const [loginError, setError] = useState({
    wrongusername: null,
    wrongpassword: null,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await onSubmit(loginData); // get the returned value or error object
      if (result === 201) {
        setError({ wrongusername: "Username does not exist" });
      } else if (result === 202) {
        setError({ wrongpassword: "Password supplied is incorrect" });
      } else {
        setError({ wrongusername: null, wrongpassword: null });
      }
    } catch (error) {
      console.log(error);
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
            className={loginError.password ? "input-error" : ""} // <-- change the class conditionally
          />
          {loginError.wrongpassword && (
            <span className="error-text">{loginError.wrongpassword}</span>
          )}{" "}
        </div>
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

const FinancialForm = ({ accountInfo }) => {
  const location = useLocation();

  const [financialData, handleInputChange] = useInputChange({
    retirement_amount: "",
    savings: "",
    checkings: "",
    account_id: accountInfo.account_id,
  });

  const handleSubmitFinancialData = useSubmitFinancialData(); // Use the new hook

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await handleSubmitFinancialData(financialData); // Use the function from the hook
      console.log(data);
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

const DisplayFinances = ({ accountInfo }) => {
  return (
    <div>
      {accountInfo}
    </div>
  );
};
const NavigationLinks = ({ location }) => (
  <>
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
  </>
);

const AppRoutes = ({ handleCreateAccount, handleLogin, accountInfo }) => (
  <Routes>
    <Route path="/" element={<AccountForm onSubmit={handleCreateAccount} />} />
    <Route path="/login" element={<LoginForm onSubmit={handleLogin} />} />
    <Route
      path="/financial-form"
      element={<FinancialForm accountInfo={accountInfo} />}
    />
    <Route
      path="/homepage"
      element={<DisplayFinances accountInfo={accountInfo} />}
    />
  </Routes>
);

const AppContent = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [accountInfo, handleCreateAccount, handleLogin] =
    useAccountAccess(navigate);

  return (
    <div className="app-container">
      <h1 className="app-title">Budgeting App</h1>

      <AppRoutes
        handleCreateAccount={handleCreateAccount}
        handleLogin={handleLogin}
        accountInfo={accountInfo}
      />

      <NavigationLinks location={location} />
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
