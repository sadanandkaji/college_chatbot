import React from "react";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-white text-gray-800 px-6">
      <div className="max-w-xl text-center space-y-6">
        <h1 className="text-4xl font-bold text-blue-700">Welcome to RAG Chatbot</h1>
        <p className="text-lg">Interact with an AI chatbot trained on your uploaded files.</p>

        <div className="space-y-3">
          <button
            onClick={() => navigate("/login")}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/register")}
            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700"
          >
            Register
          </button>
          <button
            onClick={() => navigate("/upload")}
            className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700"
          >
            Upload Files (Update Model)
          </button>
          <button
            onClick={() => navigate("/chat")}
            className="w-full bg-gray-800 text-white py-2 rounded-lg hover:bg-gray-900"
          >
            Go to Chat
          </button>
        </div>

        <p className="mt-4 text-sm text-red-500">
          Don’t have an account? Please register first.
        </p>
      </div>
    </div>
  );
}
