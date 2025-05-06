import React, { useState } from 'react';
import './App.css';
function App() {
  const [text, setText] = useState('');
  const [image, setImage] = useState(null);
  const [audio, setAudio] = useState(null);
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = new FormData();
    form.append('text', text);
    if (image) form.append('image', image);
    if (audio) form.append('audio', audio);
    const res = await fetch('http://localhost:8000/predict', { method: 'POST', body: form });
    const data = await res.json();
    setResponse(data.result);
  };

  return (
    <div className="App p-4">
      <h1 className="text-2xl mb-4">Phi-4 Multimodal Chat</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <textarea value={text} onChange={e => setText(e.target.value)} placeholder="Enter text prompt" className="border p-2 w-full" />
        <input type="file" accept="image/*" onChange={e => setImage(e.target.files[0])} />
        <input type="file" accept="audio/*" onChange={e => setAudio(e.target.files[0])} />
        <button type="submit" className="bg-blue-600 text-white p-2 rounded">Submit</button>
      </form>
      {response && (
        <div className="mt-4">
          <h2 className="text-xl">Response</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
export default App;