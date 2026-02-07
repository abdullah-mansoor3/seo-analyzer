import React from 'react';
import CrawlForm from '../components/CrawlForm';

export default function Home() {
  return (
    <main className="app-shell">
      <header className="site-header">
        <div className="logo-mark" aria-hidden />
        <div>
          <h1 className="brand-title">SEO Analyzer</h1>
          <p className="brand-sub">AI-powered crawl → analyse → improve</p>
        </div>
      </header>

      <section className="hero">
        <div className="hero-inner">
          <h2 className="hero-title">Uncover SEO opportunities in seconds</h2>
          <p className="hero-sub">
            Enter any URL — we'll crawl the site, run rule-based checks, and use AI to give you
            prioritised, actionable fixes.
          </p>
          <CrawlForm />
        </div>
      </section>

      <footer className="site-footer">
        © {new Date().getFullYear()} SEO Analyzer — Built for clear, actionable SEO insights
      </footer>
    </main>
  );
}
