import React, { useEffect, useState, useRef } from "react";
import { chatWithBot, getAllMessages } from "../services/api";

export default function ChatComponent() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const bottomRef = useRef(null);

  // Load previous messages on mount
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const allMessages = await getAllMessages();
        setMessages(allMessages.reverse()); // Show oldest to newest
      } catch (error) {
        console.error("Failed to load messages", error);
      }
    };
    fetchMessages();
  }, []);

  // Auto-scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleChat = async () => {
    if (!query.trim()) return;
    try {
      const data = await chatWithBot(query);
      const newMessage = {
        question: query,
        answer: data.response,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, newMessage]);
      setQuery("");
    } catch (error) {
      console.error("Error chatting", error.response?.data || error.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 px-4">
      <div className="bg-white rounded-2xl shadow-lg w-full max-w-2xl flex flex-col h-[80vh] overflow-hidden">
        <div className="bg-blue-600 text-white px-6 py-4 text-xl font-semibold rounded-t-2xl">
          CollegeBot 💬
        </div>

        {/* Message List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.map((msg, index) => (
            <div key={index}>
              {/* User message */}
              <div className="flex justify-end items-end gap-2">
                <div className="bg-blue-500 text-white px-4 py-2 rounded-2xl max-w-[70%]">
                  <p>{msg.question}</p>
                  <p className="text-xs text-right mt-1 opacity-75">
                    {msg.timestamp || ""}
                  </p>
                </div>
                <img
                  src="https://api.dicebear.com/7.x/initials/svg?seed=U"
                  alt="User"
                  className="w-8 h-8 rounded-full"
                />
              </div>

              {/* Bot reply */}
              <div className="flex justify-start items-end gap-2 mt-2">
                <img
                  src="https://api.dicebear.com/7.x/bottts/svg?seed=Bot"
                  alt="Bot"
                  className="w-8 h-8 rounded-full"
                />
                <div className="bg-gray-200 text-gray-900 px-4 py-2 rounded-2xl max-w-[70%]">
                  <p>{msg.answer}</p>
                  <p className="text-xs text-right mt-1 opacity-60">
                    {msg.timestamp || ""}
                  </p>
                </div>
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {/* Chat Input */}
        <div className="flex p-4 border-t gap-2 bg-white">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyDown={(e) => e.key === "Enter" && handleChat()}
          />
          <button
            onClick={handleChat}
            className="bg-blue-600 text-white px-5 py-2 rounded-full hover:bg-blue-700 transition duration-200"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
