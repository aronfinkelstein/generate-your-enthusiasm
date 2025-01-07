import React, { useState } from "react";
import randomEntries from "../randomEntries.json";

function Home() {
  const [inputs, setInputs] = useState({
    variable1: "",
    variable2: "",
    variable3: "",
  });
  const [plot, setPlot] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      console.log("Sending data:", inputs);
      const response = await fetch("http://localhost:8000/generate-plot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputs),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setPlot(data.plot);
    } catch (error) {
      console.error("Error:", error);
      setError("Error generating plot. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const randomize = () => {
    const getRandomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];

    setInputs({
      variable1: getRandomItem(randomEntries.cameo_char),
      variable2: getRandomItem(randomEntries.new_loc),
      variable3: getRandomItem(randomEntries.new_event),
    });
  };

  return (
    <main className="container mx-auto px-4 py-8 min-h-screen">
      <div className="max-w-2xl mx-auto rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-6 text-yellow-400 tracking-tighter font-sans">
          Larry David is completely out of ideas and needs some help with new
          plots for the show. Help a poor old Jew out and give him some
          suggestions for new characters, events and locations.
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            { key: "variable1", label: "Cameo Character" },
            { key: "variable2", label: "New Location" },
            { key: "variable3", label: "Chosen Event" },
          ].map(({ key, label }) => (
            <div key={key} className="space-y-1">
              <label className="block font-sans text-sm font-medium text-white">
                {label}:
              </label>
              <input
                type="text"
                value={inputs[key]}
                onChange={(e) =>
                  setInputs((prev) => ({ ...prev, [key]: e.target.value }))
                }
                className="w-full font-mono p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}

          <div className="flex gap-4">
            <button
              type="button"
              onClick={randomize}
              className="flex-1 bg-green-600 font-sans text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:bg-green-400"
            >
              Randomize
            </button>

            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 bg-yellow-400 font-sans text-black py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-blue-400 relative"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white  mr-2"></div>
                  Generating Plot...
                </div>
              ) : (
                "Generate Plot"
              )}
            </button>
          </div>
        </form>

        {isLoading && (
          <div className="mt-6 p-4 bg-yellow-400 rounded-md">
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 yellow-400 border-blue-600"></div>
              <span className="text-gray-600">Generating your plot...</span>
            </div>
          </div>
        )}

        {!isLoading && error && (
          <div className="mt-4 text-red-600">{error}</div>
        )}

        {!isLoading && plot && (
          <div className="mt-6 p-4 bg-gray-50 font-mono rounded-md">{plot}</div>
        )}
      </div>
    </main>
  );
}

export default Home;
