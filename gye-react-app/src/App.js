import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Contact from "./pages/Contact";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-800">
        <header className="bg-gray-800 p-4 flex items-center justify-start gap-4">
          <h1 className="text-6xl font-bold text-yellow-400 tracking-tighter font-sans">
            Generate Your Enthusiasm
          </h1>
          <img src="/Larry Head.png" alt="Larry silhouette" className="h-12" />
          <nav className="ml-auto">
            <ul className="flex space-x-4">
              <li>
                <Link
                  to="/"
                  className="text-2xl font-bold text-yellow-400 tracking-tighter font-sans hover:text-white"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  to="/about"
                  className="text-2xl font-bold text-yellow-400 tracking-tighter font-sans hover:text-white"
                >
                  About
                </Link>
              </li>
              <li>
                <Link
                  to="/contact"
                  className="text-2xl font-bold text-yellow-400 tracking-tighter font-sans hover:text-white"
                >
                  Contact
                </Link>
              </li>
            </ul>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
