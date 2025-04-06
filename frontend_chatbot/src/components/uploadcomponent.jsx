import React, { useState } from "react";
import { uploadFile } from "../services/api";

const UploadComponent = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (file) {
      try {
        await uploadFile(file);
        alert("File uploaded successfully!");
      } catch (error) {
        console.error("Error uploading file", error);
      }
    }
  };

  return (
    <div>
      <h2>Upload PDF</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadComponent;
