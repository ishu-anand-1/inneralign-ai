import API from "./api";

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
