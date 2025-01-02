import { useState } from "react";

export function PlotForm({ onSubmit }) {
  const [inputs, setInputs] = useState({
    cameo_char: "",
    new_loc: "",
    new_event: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(inputs);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {["Cameo Character", "New Location", "New Event"].map((variable) => (
        <div key={variable}>
          <label
            htmlFor={variable}
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            {variable.charAt(0).toUpperCase() + variable.slice(1)}:
          </label>
          <input
            id={variable}
            name={variable}
            value={inputs[variable]}
            onChange={handleInputChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm 
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder={`Enter ${variable}`}
          />
        </div>
      ))}

      <button
        type="submit"
        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white 
                 font-medium rounded-md focus:outline-none focus:ring-2 
                 focus:ring-blue-500 focus:ring-offset-2"
      >
        Generate Plot
      </button>
    </form>
  );
}
