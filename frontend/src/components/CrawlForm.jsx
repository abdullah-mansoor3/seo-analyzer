import React, { useState } from 'react';
import Loader from './Loader';

export default function CrawlForm() {
  const [url, setUrl] = useState('');
  const [status, setStatus] = useState({ loading: false, message: null, ok: null, data: null });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;
    setStatus({ loading: true, message: 'Crawling…', ok: null, data: null });

    try {
      const response = await fetch('http://localhost:8000/crawl', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      if (response.ok) {
        setStatus({ loading: false, message: 'Crawl complete', ok: true, data });
      } else {
        setStatus({ loading: false, message: data.detail || 'Crawl failed', ok: false, data });
      }
    } catch (err) {
      setStatus({ loading: false, message: `Network error: ${err.message}`, ok: false, data: null });
    }
  };

  return (
    <div className="card glass-card">
      <form className="crawl-form" onSubmit={handleSubmit} aria-label="Crawl website form">
        <label htmlFor="url" className="visually-hidden">Website URL</label>
        <input
          id="url"
          name="url"
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          className="input"
          aria-required="true"
        />

        <button className={`btn primary ${status.loading ? 'loading' : ''}`} type="submit" disabled={status.loading}>
          {status.loading ? <span className="btn-spinner" aria-hidden /> : 'Analyze'}
        </button>
      </form>

      <div className="status-area">
        {status.loading && (
          <div className="status-row">
            <Loader size={32} />
            <div className="status-text">Analyzing <strong>{url || 'website'}</strong> — this can take a few seconds</div>
          </div>
        )}

        {!status.loading && status.message && (
          <div className={`result ${status.ok ? 'ok' : 'error'}`}>
            <div className="result-header">
              <strong>{status.ok ? 'Success' : 'Error'}</strong>
              <span className="result-message"> — {status.message}</span>
            </div>

            {status.data && (
              <pre className="result-body" aria-live="polite">{JSON.stringify(status.data, null, 2)}</pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
