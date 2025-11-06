import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders chat interface", () => {
  render(<App />);
  const chatHeader = screen.getByText(/Agentic Platform Chat/i);
  expect(chatHeader).toBeInTheDocument();
});

test("renders welcome message", () => {
  render(<App />);
  const welcomeMessage = screen.getByText(/Welcome to the Agentic Platform/i);
  expect(welcomeMessage).toBeInTheDocument();
});
