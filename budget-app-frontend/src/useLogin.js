// useCreateAccount.js
import axios from 'axios';
import { useState } from 'react';

export const useLogin = (navigate) => {
  const [accountInfo, setLogin] = useState(null);

  const handleLogin = async (formData) => {
    try {
        console.log("Attempting API POST", formData);
        const response = await axios.post(
          login,
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

  return [accountInfo, handleCreateAccount];
};


const handleLogin = async (formData) => {
    try {
      console.log("Attempting API POST", formData);
      const response = await axios.post(
        login,
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