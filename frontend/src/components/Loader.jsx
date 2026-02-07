import React from 'react';

const STEPS = ['Crawling pages', 'Running SEO checks', 'Building embeddings', 'AI analysis'];

export default function Loader({ currentStep = 0 }) {
  return (
    <div className="loader-wrapper">
      <div className="orbit-loader">
        <div className="ring" />
        <div className="ring" />
        <div className="ring" />
      </div>
      <p className="loader-text">Analyzing your website…</p>
      <div className="progress-steps">
        {STEPS.map((label, i) => (
          <span
            key={label}
            className={`step-pill ${i < currentStep ? 'done' : i === currentStep ? 'active' : ''}`}
          >
            {i < currentStep ? '✓ ' : ''}{label}
          </span>
        ))}
      </div>
    </div>
  );
}