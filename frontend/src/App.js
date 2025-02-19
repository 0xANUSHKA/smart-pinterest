import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text_query: searchQuery,
          top_k: 5
        }),
      });
      const data = await response.json();
      setResults(data.matches);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Pinterest</h1>
      </header>

      <main>
        <section className="upload-section">
          <h2>Upload Image</h2>
          <form onSubmit={handleUpload}>
            <input
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              accept="image/*"
            />
            <button type="submit" disabled={!selectedFile || loading}>
              Upload
            </button>
          </form>
        </section>

        <section className="search-section">
          <h2>Search Images</h2>
          <form onSubmit={handleSearch}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search images..."
            />
            <button type="submit" disabled={!searchQuery || loading}>
              Search
            </button>
          </form>
        </section>

        <section className="results-section">
          {results.length > 0 && (
            <div className="results-grid">
              {results.map((result) => (
                <div key={result.id} className="result-card">
                  <h3>{result.id}</h3>
                  <p>Similarity: {(result.score * 100).toFixed(2)}%</p>
                  {result.metadata.tags && (
                    <p>Tags: {result.metadata.tags.join(', ')}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App; 