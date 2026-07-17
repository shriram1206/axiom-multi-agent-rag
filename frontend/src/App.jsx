import React, { useState } from 'react';
import './index.css';
import './App.css';
import ChatWindow from './components/ChatWindow';

function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  if (showDashboard) {
    return <ChatWindow onExit={() => setShowDashboard(false)} />;
  }

  return (
    <div className="landing-wrapper">
      <nav className="top-nav">
        <div className="nav-logo">
          <div className="logo-mark">A</div>
          <span>Axiom OS</span>
        </div>
        <div className="nav-links">
          <a href="#suite">The Suite</a>
          <a href="#manifesto">Manifesto</a>
          <a href="#pricing">Pricing</a>
        </div>
        <div className="nav-cta">
          <a href="#login" className="login-link">Log in</a>
          <button className="btn-solid" onClick={() => setShowDashboard(true)}>Get Access</button>
        </div>
      </nav>

      <main className="main-content">
        <section className="hero-center">
          <div className="pill-badge">
            <span className="sparkle">✦</span>
            <span>Axiom Core is now in Beta</span>
          </div>
          
          <h1 className="display-title">
            The software suite for <br />
            <span className="serif-highlight">uncompromising</span> teams.
          </h1>
          
          <p className="hero-description">
            We replaced 14 enterprise applications with one lightning-fast, 
            unified system. Stop wrestling with integrations. Start building.
          </p>
          
          <div className="action-row">
            <button className="btn-solid large" onClick={() => setShowDashboard(true)}>Deploy Axiom</button>
            <button className="btn-outline large">View Demo</button>
          </div>
        </section>

        <section className="dashboard-preview">
          <div className="mock-window">
            <div className="mock-header">
              <span className="dot red"></span>
              <span className="dot yellow"></span>
              <span className="dot green"></span>
            </div>
            <div className="mock-body">
              <div className="mock-sidebar">
                <div className="sidebar-line active"></div>
                <div className="sidebar-line"></div>
                <div className="sidebar-line"></div>
                <div className="sidebar-line"></div>
              </div>
              <div className="mock-main">
                <div className="mock-card header-card">
                  <div className="mock-text-block"></div>
                  <div className="mock-text-block short"></div>
                </div>
                <div className="mock-card split">
                   <div className="mock-card-inner">
                     <div className="mock-circle"></div>
                   </div>
                   <div className="mock-card-inner bar-chart">
                     <div className="bar b1"></div>
                     <div className="bar b2"></div>
                     <div className="bar b3"></div>
                     <div className="bar b4"></div>
                   </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
