"use client";

import React, { useState, useEffect, useRef } from "react";
import { api } from "@/lib/api";

interface MessageItem {
  id?: string;
  role: "You" | "Mentor";
  text: string;
  pedagogical_state?: string;
  citations?: string[];
}

/**
 * Client-side fallback cleaner: transforms any leftover LaTeX or math tags
 * into clean, readable Unicode symbols and plain text.
 */
function cleanMathDisplay(text: string): string {
  if (!text) return "";
  let s = text;

  // Replace \frac{a}{b} with (a / b)
  s = s.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, "($1 / $2)");
  s = s.replace(/\\sqrt\{([^{}]+)\}/g, "√($1)");
  s = s.replace(/\\vec\{([^{}]+)\}/g, "$1");
  s = s.replace(/\\text\{([^{}]+)\}/g, "$1");

  // Symbols
  s = s.replace(/\\approx/g, "≈");
  s = s.replace(/\\pm/g, "±");
  s = s.replace(/\\cdot/g, " · ");
  s = s.replace(/\\times/g, " × ");
  s = s.replace(/\\leq/g, "≤");
  s = s.replace(/\\geq/g, "≥");
  s = s.replace(/\\neq/g, "≠");
  s = s.replace(/\\to|\\rightarrow/g, "→");
  s = s.replace(/\\implies/g, "=>");
  s = s.replace(/\\theta/g, "θ");
  s = s.replace(/\\lambda/g, "λ");
  s = s.replace(/\\pi/g, "π");
  s = s.replace(/\\Delta/g, "Δ");
  s = s.replace(/\\sum/g, "∑");
  s = s.replace(/\\int/g, "∫");
  s = s.replace(/\\infty/g, "∞");

  // Superscripts
  s = s.replace(/\^2\b|\^\{2\}/g, "²");
  s = s.replace(/\^3\b|\^\{3\}/g, "³");
  s = s.replace(/\^n\b|\^\{n\}/g, "ⁿ");

  // Strip math delimiters
  s = s.replace(/\$\$([\s\S]*?)\$\$/g, "$1");
  s = s.replace(/\$(.*?)\$/g, "$1");

  return s;
}

export default function MentorTab() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [isSending, setIsSending] = useState(false);
  const listEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversationHistory();
  }, []);

  useEffect(() => {
    listEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);

  const loadConversationHistory = async () => {
    try {
      const history = await api.getConversations();
      if (history && history.length > 0) {
        const formatted: MessageItem[] = [];
        history.forEach((h) => {
          formatted.push({ role: "You", text: h.user_message });
          formatted.push({
            role: "Mentor",
            text: cleanMathDisplay(h.tutor_reply),
            pedagogical_state: h.pedagogical_state,
          });
        });
        setMessages(formatted);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSend = async (overrideText?: string) => {
    const textToSend = (overrideText || input).trim();
    if (!textToSend) {
      alert("Type your question first");
      return;
    }

    setInput("");
    setMessages((prev) => [...prev, { role: "You", text: textToSend }]);
    setIsSending(true);

    try {
      const res = await api.sendTutorMessage(textToSend);
      setMessages((prev) => [
        ...prev,
        {
          role: "Mentor",
          text: cleanMathDisplay(res.content),
          pedagogical_state: res.pedagogical_state,
          citations: res.citations,
        },
      ]);
    } catch (e: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "Mentor",
          text: `I encountered an issue connecting to the reasoning service: ${e.message}. Please try asking again.`,
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const suggestionPrompts = [
    { label: "📐 Solve Quadratic", query: "solve x^2 - 5x + 6 = 0" },
    { label: "🚀 Kinematics Calculation", query: "A car has u = 10 m/s, a = 2 m/s², t = 5 s. What is final velocity and distance?" },
    { label: "⚡ Force & Newton's 2nd Law", query: "mass = 5 kg, acceleration = 4 m/s². What is the net force?" },
    { label: "📈 Find Derivative", query: "find derivative of 3x^2 + 5x" },
    { label: "🌿 How Photosynthesis Works", query: "Explain how photosynthesis works with chemical equations and light reactions" },
    { label: "🌈 Why is the Sky Blue?", query: "Why is the sky blue? Explain Rayleigh scattering" },
  ];

  return (
    <div id="panel-mentor" className="card" style={{ maxWidth: "1000px", margin: "0 auto" }}>
      <div style={{ display: "grid", gap: "14px" }}>
        {/* Header Title */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid var(--border)", paddingBottom: "10px" }}>
          <div>
            <h3 style={{ margin: 0, fontSize: "17px", fontWeight: 800, color: "var(--text-heading)" }}>
              🎓 Socratic AI Mentor & Equation Solver
            </h3>
            <span className="small note">
              Answers physics, chemistry, biology, and mathematics with exact values, step-by-step formulas, and clean Unicode symbols.
            </span>
          </div>
          <span className="badge small" style={{ color: "#10b981", borderColor: "#10b981", background: "rgba(16, 185, 129, 0.1)" }}>
            ● Online & Reasoning
          </span>
        </div>

        {/* Quick Suggestion Chips */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
          {suggestionPrompts.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSend(p.query)}
              disabled={isSending}
              style={{
                background: "var(--card-subtle)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
                padding: "5px 10px",
                fontSize: "12px",
                fontWeight: 600,
                color: "var(--text)",
                cursor: "pointer",
                transition: "all 0.15s ease",
              }}
              onMouseOver={(e) => (e.currentTarget.style.borderColor = "var(--brand)")}
              onMouseOut={(e) => (e.currentTarget.style.borderColor = "var(--border)")}
            >
              {p.label}
            </button>
          ))}
        </div>

        {/* Question Input */}
        <div>
          <label style={{ display: "block", marginBottom: "6px", fontWeight: 700, fontSize: "13.5px" }}>
            Ask Your Question or Equation:
          </label>
          <textarea
            id="mInput"
            className="input"
            rows={3}
            placeholder="Ask any question, derive formulas, or type equations to solve (e.g. 'solve 3x + 5 = 20', 'mass = 4 kg, velocity = 10 m/s', 'explain Newton's laws')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            style={{ width: "100%", padding: "10px 14px", fontSize: "14px", borderRadius: "10px", resize: "vertical" }}
          />
        </div>
        <div className="right" style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            className="btn"
            onClick={() => handleSend()}
            disabled={isSending || !input.trim()}
            style={{
              padding: "9px 24px",
              fontWeight: 700,
              background: "linear-gradient(135deg, #4f46e5 0%, #0284c7 100%)",
              border: "none",
            }}
          >
            {isSending ? "Reasoning & Solving..." : "🚀 Ask Mentor"}
          </button>
        </div>

        {/* Message Thread */}
        <ul id="mentorList" className="list" style={{ marginTop: "10px", maxHeight: "520px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "12px" }}>
          {messages.length === 0 && (
            <div style={{ textAlign: "center", padding: "40px 20px", color: "var(--muted)" }}>
              <div style={{ fontSize: "32px", marginBottom: "8px" }}>💡</div>
              <strong style={{ display: "block", fontSize: "15px", color: "var(--text-heading)", marginBottom: "4px" }}>
                Welcome to your AI Personal Teacher!
              </strong>
              <span className="small note">
                Ask any question, request step-by-step math derivations, or click one of the suggestion chips above to begin.
              </span>
            </div>
          )}

          {messages.map((m, idx) => (
            <li
              key={idx}
              style={{
                display: "block",
                background: m.role === "You" ? "var(--card-subtle)" : "var(--card)",
                border: "1px solid var(--border)",
                borderLeft: m.role === "Mentor" ? "4px solid var(--brand)" : "1px solid var(--border)",
                borderRadius: "10px",
                padding: "14px 18px",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontWeight: 800, fontSize: "14px", color: m.role === "Mentor" ? "var(--brand)" : "var(--text-heading)" }}>
                  {m.role === "Mentor" ? "🧑‍🏫 Mentor Mate" : "👤 You"}
                </span>
                {m.pedagogical_state && (
                  <span className="badge small" style={{ color: "var(--brand)", borderColor: "var(--brand)", fontSize: "11px" }}>
                    {m.pedagogical_state}
                  </span>
                )}
              </div>
              <div
                style={{
                  whiteSpace: "pre-wrap",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  color: "var(--text)",
                  fontFamily: "inherit",
                }}
              >
                {m.text}
              </div>
              {m.citations && m.citations.length > 0 && (
                <div className="small note" style={{ marginTop: "10px", paddingTop: "6px", borderTop: "1px dashed var(--border)", color: "var(--muted)", fontSize: "11.5px" }}>
                  📚 Grounded in: {m.citations.join(" • ")}
                </div>
              )}
            </li>
          ))}
          <div ref={listEndRef} />
        </ul>
      </div>
    </div>
  );
}

