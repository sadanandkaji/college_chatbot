import React, { useState } from "react";
import { chatWithBot } from "../services/api";

const ChatComponent = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleChat = async () => {
    try {
      const data = await chatWithBot(query); // Only pass the raw string here
      setResponse(data.response);
    } catch (error) {
      console.error("Error chatting", error.response?.data || error.message);
    }
  };
  

  return (
    <div>
      <h2>Ask a Question</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask me anything"
      />
      <button onClick={handleChat}>Send</button>
      {response && <p>{response}</p>}
    </div>
  );
};

export default ChatComponent;
