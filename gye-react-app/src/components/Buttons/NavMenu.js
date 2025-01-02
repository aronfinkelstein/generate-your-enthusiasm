import React from "react";

const NavMenu = () => {
  return (
    <div className="relative group">
      <button className="p-2 text-yellow-400 hover:bg-gray-700 rounded-md">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
      <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
        <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100">
          Home
        </a>
        <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100">
          About
        </a>
        <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100">
          Contact
        </a>
      </div>
    </div>
  );
};

export default NavMenu;
