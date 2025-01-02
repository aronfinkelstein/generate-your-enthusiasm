import React from "react";

function Contact() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4 text-yellow-400">Contact Us</h2>
        <p className="text-white font-mono mb-4">
          Have suggestions or feedback? Email me at: <br />
          <a
            href="mailto:contact@generateyourenthusiasm.com"
            className="text-yellow-400 hover:underline"
          >
            finkelstein.aron@gmail.com
          </a>
        </p>
      </div>
      <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4 text-yellow-400">GitHub</h2>
        <p className="text-white font-mono mb-4">
          Check out the project: <br />
          <a href="githublink" className="text-yellow-400 hover:underline">
            https://github.com/aronfinkelstein/generate-your-enthusiasm.git
          </a>
        </p>
      </div>
    </div>
  );
}

export default Contact;
