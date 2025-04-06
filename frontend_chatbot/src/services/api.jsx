import axios from "axios";

const API_URL = "http://localhost:8000"; // Replace with your backend URL

export const register = async (userData) => {
  const response = await axios.post(`${API_URL}/users/register`, userData);
  return response.data;
};

export const login = async (userData) => {
  const response = await axios.post(`${API_URL}/users/login`, userData);
  return response.data;
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_URL}/upload/upload`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

export const chatWithBot = async (query) => {
    const response = await axios.post(
      `${API_URL}/chat/`,
      { question: query },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  };
  
  
  
