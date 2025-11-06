import React, { useState, useRef, useEffect } from "react";
import "./ChatInterface.css";

/**
 * ChatInterface Component
 *
 * A foundational chat interface component designed for future agent integration.
 * Provides message input, display area, and basic state management.
 *
 * Requirements addressed:
 * - 4.1: Chat interface component with message input and display
 * - 4.2: Render in web browser and accept user text input
 * - 4.4: Display messages when user types (even without processing)
 */
const ChatInterface = () => {
  // State for managing messages and input
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Welcome to the Agentic Platform! This chat interface is ready for future agent integration.",
      sender: "system",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Refs for DOM manipulation
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages are added
  const scrollToBottom = () => {
    if (
      messagesEndRef.current &&
      typeof messagesEndRef.current.scrollIntoView === "function"
    ) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle message sending
  const handleSendMessage = () => {
    const trimmedInput = inputValue.trim();

    if (!trimmedInput) {
      return;
    }

    // Create new user message
    const userMessage = {
      id: Date.now(),
      text: trimmedInput,
      sender: "user",
      timestamp: new Date(),
    };

    // Add user message to state
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue("");
    setIsLoading(true);

    // Simulate processing delay and echo response
    // This will be replaced with actual agent integration in the future
    setTimeout(() => {
      const echoMessage = {
        id: Date.now() + 1,
        text: `Echo: ${trimmedInput} (Agent integration coming soon!)`,
        sender: "system",
        timestamp: new Date(),
      };

      setMessages((prevMessages) => [...prevMessages, echoMessage]);
      setIsLoading(false);
    }, 1000);
  };

  // Handle input changes
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Format timestamp for display
  const formatTimestamp = (timestamp) => {
    return timestamp.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Agentic Platform Chat</h2>
        <div className="chat-status">
          <span className="status-indicator ready"></span>
          Ready for Agent Integration
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              <div className="message-timestamp">
                {formatTimestamp(message.timestamp)}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message system loading">
            <div className="message-content">
              <div className="message-text">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            className="chat-input"
            rows="1"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
            aria-label="Send message"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22,2 15,22 11,13 2,9"></polygon>
            </svg>
          </button>
        </div>

        <div className="chat-input-footer">
          <small>
            This interface is ready for future integration with orchestrator,
            SQL query, API, and RAG document agents.
          </small>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
