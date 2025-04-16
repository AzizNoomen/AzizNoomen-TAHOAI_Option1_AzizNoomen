import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [text, setText] = useState('');
  const [fileName, setFileName] = useState('');
  const [response, setResponse] = useState<{ label: string; confidence: number } | null>(null);
  const [showModal, setShowModal] = useState(false);

  const fileInputRef = React.useRef<HTMLInputElement | null>(null);

  // Handle text file input
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Only allow text files
    if (file.type !== 'text/plain') {
      alert('Only .txt files are allowed.');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      // Set the content of the text file to the text state
      setText(reader.result as string);
      setFileName(file.name);
    };
    reader.readAsText(file);  // Read the file content as text
  };

  // Handle the form submission
  const handleSubmit = async () => {
    if (!text.trim()) {
      alert('Please enter some text or upload a file.');
      return;
    }

    try {
      // Send the text (either from textarea or file) to the backend
      const res = await axios.post('http://localhost:8000/api/classify', null, {
        params: {
          text: text,
        },
      });

      setResponse(res.data);
      setShowModal(true);  // Show the modal when response is available
      console.log('response', res.data);

      // Reset the text and file input after submission
      setText('');
      setFileName('');
      
      // Reset the file input itself
      if (fileInputRef.current) {
        fileInputRef.current.value = ''; // This clears the file input
      }
    } catch (error) {
      alert('Error sending text to backend.');
      console.error(error);
    }
  };

  // Close the modal
  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div className="app-container">
      <h2>Document Classifier</h2>

      <textarea
        rows={10}
        className="text-area"
        placeholder="Enter your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="file-upload">
        <input
          type="file"
          accept=".txt"
          onChange={handleFileChange}
          ref={fileInputRef} // Reference to the file input
        />
        {fileName && <p className="file-info">📄 Loaded: <strong>{fileName}</strong></p>}
      </div>

      <button className="submit-btn" onClick={handleSubmit}>
        Submit
      </button>

      {/* Modal (Popup) */}
      {showModal && response && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Result</h3>
            <p><strong>Label:</strong> {response.label}</p>
            <p><strong>Confidence:</strong> {(response.confidence * 100).toFixed(2)}%</p>
            <button className="close-btn" onClick={closeModal}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
