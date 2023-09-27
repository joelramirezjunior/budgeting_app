// useAccountAccess.js
import axios from 'axios';
import { useState } from 'react';
import API_URLS from "./constants.js"


export const useAccountAccess = (navigate) => {
  const [accountInfo, setAccountInfo] = useState(null);

  const handleCreateAccount = async (formData) => {
    try {
        console.log("Attempting API POST", formData);
        const response = await axios.post(
          API_URLS.addAccount,
          formData,
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response);
        if (response && response.status !== 400) {
          return response.status;
        }
        setAccountInfo(response.data);
        navigate("/financial-form", { state: { email: formData.email } });

    } catch (error) {
        console.error("Error while sending data: ", error);
        return error; // return the error object
      }
  };

  const handleLogin = async (formData) => {
    try {
        console.log("Attempting API POST", formData);
        const response = await axios.post(
          API_URLS.login,
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
      } catch (error) {
        console.error("Error while sending data: ", error);
        return error; 
      }
  };

  return [accountInfo, handleCreateAccount, handleLogin];
};

export default useAccountAccess;
