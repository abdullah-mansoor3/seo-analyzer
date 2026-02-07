import React, { useState, useCallback } from 'react';
import Loader from './Loader';

// Lightweight markdown-to-HTML (handles headings, bold, lists, code, blockquotes)
function renderMarkdown(md) {
  if (!md) return '';
  let html = md
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul>${m}</ul>`)
    .replace(/\n{2,}/g, '</p><p>')
    .replace(/\n/g, '<br/>');
  return `<p>${html}</p>`;
}

export default function CrawlForm() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('ai');

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setResult(null);
    setError(null);
    setStep(0);

    // Simulate step progression while waiting for backend
    const stepTimer = setInterval(() => {
      setStep((s) => (s < 3 ? s + 1 : s));
    }, 3000);

    try {
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      clearInterval(stepTimer);
      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || 'Analysis failed');
      } else {
        setStep(4);
        setResult(data);
      }
    } catch (err) {
      clearInterval(stepTimer);
      setError(`Network error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [url]);

  const checks = result?.report?.rules_summary?.checks || [];
  const totalIssues = checks.reduce((n, c) => n + (c.issues?.length || 0), 0);
  const cleanPages = checks.filter((c) => !c.issues?.length).length;
  const aiMarkdown = result?.report?.ai_analysis || '';

  return (
    <>
      <form className="crawl-form" onSubmit={handleSubmit} aria-label="Analyze website">
        <input
          type="url"
          className="input"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          disabled={loading}
        />
        <button className="btn primary" type="submit" disabled={loading}>
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>
      </form>

      {loading && <Loader currentStep={step} />}

      {error && !loading && (
        <div className="error-card">
          <strong>Error</strong> — {error}
        </div>
      )}

      {result && !loading && (
        <div className="results-section">
          {/* Stats bar */}
          <div className="stats-bar">
            <div className="stat-card">
              <div className="stat-value">{result.pages_crawled}</div>
              <div className="stat-label">Pages Crawled</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{totalIssues}</div>
              <div className="stat-label">Issues Found</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{cleanPages}</div>
              <div className="stat-label">Clean Pages</div>
            </div>
          </div>

          {/* Tabs */}
          <div className="tabs">
            <button
              className={`tab-btn ${activeTab === 'ai' ? 'active' : ''}`}
              onClick={() => setActiveTab('ai')}
            >
              AI Analysis
            </button>
            <button
              className={`tab-btn ${activeTab === 'checks' ? 'active' : ''}`}
              onClick={() => setActiveTab('checks')}
            >
              Rule Checks ({checks.length})
            </button>
          </div>

          {/* AI tab */}
          {activeTab === 'ai' && (
            <div
              className="ai-analysis"
              dangerouslySetInnerHTML={{ __html: renderMarkdown(aiMarkdown) }}
            />
          )}

          {/* Rule checks tab */}
          {activeTab === 'checks' && (
            <div className="checks-list">
              {checks.map((check, i) => (
                <div className="check-card" key={i} style={{ animationDelay: `${i * .06}s` }}>
                  <div className="check-url">{check.page}</div>
                  {check.issues?.length ? (
                    <ul className="issue-list">
                      {check.issues.map((issue, j) => (
                        <li className="issue-item" key={j} style={{ animationDelay: `${(i * .06) + (j * .04)}s` }}>
                          {issue}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <div className="check-pass">✓ No issues found</div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </>
  );
}
