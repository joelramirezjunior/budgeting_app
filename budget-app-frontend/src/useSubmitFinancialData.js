import axios from "axios";

const useSubmitFinancialData = () => {
  const handleSubmitFinancialData = async (financialData) => {
    try {
      const response = await axios.post('/your-api-endpoint', financialData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error while sending financial data:", error);
      throw error;
    }
  };

  return handleSubmitFinancialData;
};

export default useSubmitFinancialData;
