import React from "react";
import "./App.css";
import { ChatInterface } from "./components/Chat";

/**
 * Main App Component
 *
 * Integrates the chat interface with the main application structure.
 * Provides the foundation for future multi-agent system integration.
 *
 * Requirements addressed:
 * - 4.3: Connect frontend to backend API endpoints
 * - 5.3: Maintain clear separation between layers
 */
function App() {
  return (
    <div className="App">
      <main className="app-main">
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
