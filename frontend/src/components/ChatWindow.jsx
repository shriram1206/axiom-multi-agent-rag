import React, { useState, useRef, useEffect } from 'react';
import PersonaSidebar from './PersonaSidebar';
import MessageBubble from './MessageBubble';
import { sendMessage } from '../api';
import './ChatWindow.css';

export default function ChatWindow({ onExit }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Welcome to the Axiom executive dashboard. Tag @Maya, @Vibhishana, or @Kubera to begin.', persona: 'System' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // A unique session ID per browser load to utilize our new backend logic
  const [sessionId] = useState(() => 'sess_' + Math.random().toString(36).substr(2, 9));

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage, persona: 'You' }]);
    setInput('');
    setIsLoading(true);

    const data = await sendMessage(userMessage, sessionId);
    
    setMessages(prev => [...prev, { role: 'assistant', content: data.response, persona: data.persona }]);
    setIsLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const insertMention = (mention) => {
    setInput(prev => prev + mention);
    // Auto-focus the input after clicking a sidebar persona
    const inputEl = document.querySelector('.chat-input');
    if (inputEl) inputEl.focus();
  };

  return (
    <div className="chat-layout">
      <PersonaSidebar onPersonaClick={insertMention} />
      
      <div className="chat-main">
        <header className="chat-header">
          <div className="header-brand">Axiom OS <span className="beta-tag">BETA</span></div>
          <button className="btn-exit" onClick={onExit}>Exit Dashboard</button>
        </header>

        <div className="messages-container">
          {messages.map((msg, idx) => (
            <MessageBubble 
              key={idx}
              role={msg.role}
              content={msg.content}
              persona={msg.persona}
            />
          ))}
          {isLoading && (
            <div className="loading-indicator">
              <span className="dot"></span><span className="dot"></span><span className="dot"></span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-box">
            <textarea
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message your team... (e.g. '@Kubera what is our Q3 budget?')"
              rows={1}
            />
            <button 
              className="send-button" 
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </div>
          <div className="input-footer">Axiom OS Internal Tooling. Strictly Confidential.</div>
        </div>
      </div>
    </div>
  );
}
