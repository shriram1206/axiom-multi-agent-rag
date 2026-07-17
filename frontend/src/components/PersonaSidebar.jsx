import React from 'react';
import './PersonaSidebar.css';

export default function PersonaSidebar({ onPersonaClick }) {
  const personas = [
    { name: 'Maya', role: 'Marketing Lead', desc: 'Growth, budgets, brand.', color: '#FF6B35' },
    { name: 'Vibhishana', role: 'People Lead', desc: 'Hiring, remote policy.', color: '#00c853' },
    { name: 'Kubera', role: 'Finance Lead', desc: 'Runway, burn rate, spend.', color: '#2A1B5E' }
  ];

  return (
    <div className="sidebar-container">
      <div className="sidebar-header">
        <h2 className="sidebar-title">Executive Team</h2>
        <p className="sidebar-sub">Click to mention in chat</p>
      </div>
      
      <div className="persona-list">
        {personas.map(p => (
          <div 
            key={p.name} 
            className="persona-card"
            onClick={() => onPersonaClick(`@${p.name} `)}
          >
            <div className="persona-avatar" style={{ backgroundColor: p.color }}>
              {p.name.charAt(0)}
            </div>
            <div className="persona-info">
              <div className="persona-name-text">{p.name}</div>
              <div className="persona-role">{p.role}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
