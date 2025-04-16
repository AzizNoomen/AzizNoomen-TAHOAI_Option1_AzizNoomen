import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [text, setText] = useState('');
  const [fileName, setFileName] = useState('');
  const [response, setResponse] = useState<{ label: string; confidence: number } | null>(null);
  const [showModal, setShowModal] = useState(false);  // State to manage modal visibility

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type !== 'text/plain') {
      alert('Only .txt files are allowed.');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setText(reader.result as string);
      setFileName(file.name);
    };
    reader.readAsText(file);
  };

  const handleSubmit = async () => {
    if (!text.trim()) {
      alert('Please enter some text or upload a file.');
      return;
    }

    try {
      console.log("request", text);
      const res = await axios.post('http://localhost:8000/api/classify', null, {
        params: {
          text: text,
        },
      });

      setResponse(res.data);
      setShowModal(true);  // Show the modal when response is available
      console.log("response", res.data);
    } catch (error) {
      alert('Error sending text to backend.');
      console.error(error);
    }
  };

  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div style={{ padding: '2rem', maxWidth: 600, margin: 'auto', fontFamily: 'Arial' }}>
      <h2>Document Classifier</h2>

      <textarea
        rows={10}
        style={{ width: '100%', marginBottom: '1rem' }}
        placeholder="Enter your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <input
        type="file"
        accept=".txt"
        onChange={handleFileChange}
        style={{ marginBottom: '1rem' }}
      />

      {fileName && <p>📄 Loaded: <strong>{fileName}</strong></p>}

      <button onClick={handleSubmit} style={{ padding: '0.5rem 1rem', marginBottom: '1rem' }}>
        Submit
      </button>

      {/* Modal (Popup) */}
      {showModal && response && (
        <div style={{
          position: 'fixed',
          top: '0',
          left: '0',
          right: '0',
          bottom: '0',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 9999,
        }}>
          <div style={{
            backgroundColor: 'white',
            padding: '2rem',
            borderRadius: '8px',
            textAlign: 'center',
            width: '400px',
          }}>
            <h3>Result</h3>
            <p><strong>Label:</strong> {response.label}</p>
            <p><strong>Confidence:</strong> {(response.confidence * 100).toFixed(2)}%</p>
            <button onClick={closeModal} style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
