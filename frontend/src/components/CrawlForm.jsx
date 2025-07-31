import React, { useState } from 'react';

function CrawlForm() {
  const [url, setUrl] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('Crawling...');

    try {
      const response = await fetch('http://localhost:8000/crawl', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(`✅ Crawling complete: ${data.message || 'Success'}`);
      } else {
        setMessage(`❌ Error: ${data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setMessage('❌ Network error: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="url"
        placeholder="Enter website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        required
        style={{ width: '300px', padding: '0.5rem', marginRight: '1rem' }}
      />
      <button type="submit">Analyze</button>
      <p style={{ marginTop: '1rem' }}>{message}</p>
    </form>
  );
}

export default CrawlForm;
