import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const analyzeHandwriting = async (imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile);

  const res = await API.post("/analyze", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};
