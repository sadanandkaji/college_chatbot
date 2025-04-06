import React, { useState } from "react";
import { BrowserRouter ,Routes, Route  } from "react-router-dom";
import RegisterComponent from "./components/Registercomponent";
import LoginComponent from "./components/logincomponent";
import ChatComponent from "./components/chatcomponent";
import UploadComponent from "./components/uploadcomponent";


function App() {

  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route path="/register" element={<RegisterComponent></RegisterComponent>} ></Route>
        <Route path="/login" element={<LoginComponent></LoginComponent>} ></Route>
        <Route path="/chat" element={<ChatComponent></ChatComponent>} ></Route>
        <Route path="/upload" element={<UploadComponent></UploadComponent>} ></Route>
      </Routes>
      </BrowserRouter>
    </div>

  );
}

export default App;
