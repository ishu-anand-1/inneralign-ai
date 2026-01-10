import API from "./api";
import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 60000,
});
export const analyzeHandwriting = async (imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await API.post("/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};
