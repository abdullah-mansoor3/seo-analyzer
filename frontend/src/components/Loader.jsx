import React from 'react';

export default function Loader({ size = 48 }) {
  const s = Math.max(16, size);
  return (
    <div className="loader" style={{ width: s, height: s }} aria-hidden="true">
      <svg viewBox="0 0 50 50" className="spinner">
        <circle className="path" cx="25" cy="25" r="20" fill="none" strokeWidth="4" />
      </svg>
    </div>
  );
}