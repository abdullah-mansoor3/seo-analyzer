import React from 'react';
import CrawlForm from '../components/CrawlForm';

export default function Home() {
  return (
    <main className="app-shell">
      <header className="site-header">
        <div className="brand">
          <div className="logo-mark" aria-hidden />
          <div>
            <h1 className="brand-title">SEO Analyzer</h1>
            <p className="brand-sub">Crawl, extract metadata, get rule-based & RAG suggestions</p>
          </div>
        </div>
      </header>

      <section className="hero">
        <div className="hero-inner glass-card">
          <h2 className="hero-title">Analyze any website for SEO opportunities</h2>
          <p className="hero-sub">Enter a URL and get metadata extraction, SEO suggestions and actionable tips.</p>
          <CrawlForm />
        </div>
      </section>

      <footer className="site-footer">
        <small>© {new Date().getFullYear()} SEO Analyzer — Built for clear, actionable SEO insights</small>
      </footer>
    </main>
  );
}
