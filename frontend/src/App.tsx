import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar"
import Dashboard from "./pages/Dashboard";
import Notes from "./pages/Notes";
import Practice from "./pages/Practice";
import Performance from "./pages/Performance";
import Schedule from "./pages/Schedule";
import Flashcards from './pages/Flashcards';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/notes" element={<Notes />} />
        <Route path="/practice" element={<Practice />} />
        <Route path="/performance" element={<Performance />} />
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/flashcards" element={<Flashcards />} />
      </Routes>
    </Router>
  );
}

export default App;