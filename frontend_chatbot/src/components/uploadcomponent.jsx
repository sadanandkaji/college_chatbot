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
        alert("Failed to upload file.");
      }
    } else {
      alert("Please select a file first.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Upload PDF</h2>

        <div className="space-y-4">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />

          <button
            onClick={handleUpload}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadComponent;
