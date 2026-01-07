import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const analyzeImage = (formData) =>
  API.post("/analyze", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
