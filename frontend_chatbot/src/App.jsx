
import './App.css'
import { BrowserRouter,Route,Routes } from "react-router-dom"
import RegisterComponent from './components/Registercomponent'
import LoginComponent from './components/logincomponent'
import ChatComponent from './components/chatcomponent'
import UploadComponent from './components/uploadcomponent'
import LandingPage from "./components/Landingpage";






function App() {
  

  return <>
  <BrowserRouter>
    <Routes>
      <Route path="/register" element={<RegisterComponent></RegisterComponent> } />
      <Route path="/login" element={<LoginComponent ></LoginComponent> } />
      <Route path="/chat" element={<ChatComponent></ChatComponent>} />
      <Route path="/upload" element={<UploadComponent></UploadComponent> } />
      <Route path="/" element={<LandingPage />} />
      
     
   
    </Routes>
  </BrowserRouter>
  </>
  
}

export default App
