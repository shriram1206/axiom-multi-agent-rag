import React from 'react';
import ReactMarkdown from 'react-markdown';
import './MessageBubble.css';

export default function MessageBubble({ role, content, persona }) {
  const isUser = role === 'user';
  
  // Assign colors based on persona
  let headerClass = 'persona-header default';
  if (!isUser) {
    if (persona === 'Maya') headerClass = 'persona-header maya';
    if (persona === 'Vibhishana') headerClass = 'persona-header vibhishana';
    if (persona === 'Kubera') headerClass = 'persona-header kubera';
  }

  return (
    <div className={`message-wrapper ${isUser ? 'user-wrapper' : 'ai-wrapper'}`}>
      <div className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`}>
        {!isUser && (
          <div className={headerClass}>
            <span className="persona-name">{persona}</span>
          </div>
        )}
        <div className="message-content markdown-body">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
