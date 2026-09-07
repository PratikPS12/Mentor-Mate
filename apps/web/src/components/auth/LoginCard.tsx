"use client";

import React, { useState, useEffect } from "react";
import { api } from "@/lib/api";

const EyeIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

const EyeOffIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
    <line x1="1" y1="1" x2="23" y2="23" />
  </svg>
);

interface LoginCardProps {
  onLoginSuccess: () => void;
  initialMode?: "register" | "login";
}

export default function LoginCard({ onLoginSuccess, initialMode = "login" }: LoginCardProps) {
  const [authMode, setAuthMode] = useState<"register" | "login">(initialMode);

  useEffect(() => {
    if (initialMode) {
      setAuthMode(initialMode);
    }
  }, [initialMode]);
  
  // Registration Form State
  const [regName, setRegName] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regKlass, setRegKlass] = useState("10");
  const [regGoal, setRegGoal] = useState("10th Boards (CBSE)");
  const [regSchool, setRegSchool] = useState("");

  // Helper for smart goals based on class
  const getGoalSuggestionsForKlass = (k: string) => {
    if (k === "10") {
      return [
        "10th Boards (CBSE)",
        "10th Boards (ICSE)",
        "State Board (10th)",
        "NTSE & Olympiad",
        "Foundation (JEE/NEET)",
      ];
    }
    if (k === "11" || k === "12") {
      return [
        "JEE (Main & Advanced)",
        "NEET Medical",
        "MHT-CET / State CET",
        "CUET Entrance",
        "12th Senior Secondary Boards",
      ];
    }
    // Undergraduate / Degree
    return [
      "GATE (Engineering)",
      "Software Engineering & Placements",
      "Data Science & AI",
      "CAT (IIM / MBA)",
      "GRE / Higher Studies",
      "University Semester Core",
    ];
  };

  const handleKlassChange = (newKlass: string) => {
    setRegKlass(newKlass);
    const suggestions = getGoalSuggestionsForKlass(newKlass);
    setRegGoal(suggestions[0]);
  };

  // Login Form State
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);

  // Show / Hide Password Toggles
  const [showRegPassword, setShowRegPassword] = useState(false);
  const [showLoginPassword, setShowLoginPassword] = useState(false);

  // Status & Feedback
  const [statusMessage, setStatusMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusMessage(null);

    if (!regName.trim()) {
      setStatusMessage({ type: "error", text: "Please enter your full name." });
      return;
    }
    if (!regEmail.trim()) {
      setStatusMessage({ type: "error", text: "Please enter a valid email address." });
      return;
    }
    if (!regPassword || regPassword.length < 6) {
      setStatusMessage({ type: "error", text: "Password must be at least 6 characters long." });
      return;
    }

    setIsSubmitting(true);
    try {
      await api.register({
        name: regName.trim(),
        email: regEmail.trim().toLowerCase(),
        password: regPassword,
        klass: regKlass,
        goal: regGoal,
      });

      // Update school if provided
      if (regSchool.trim()) {
        try {
          await api.updateProfile({ school: regSchool.trim() });
        } catch {
          // Non-blocking
        }
      }

      // Automatically prepopulate login form and transition as requested
      setLoginEmail(regEmail.trim().toLowerCase());
      setLoginPassword(regPassword);
      setAuthMode("login");
      setStatusMessage({
        type: "success",
        text: `🎉 Account successfully created for ${regName}! Please sign in once with your credentials to launch your learning twin.`,
      });
    } catch (err: any) {
      setStatusMessage({
        type: "error",
        text: err.message || "Registration failed. Please check your details and try again.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusMessage(null);

    if (!loginEmail.trim()) {
      setStatusMessage({ type: "error", text: "Please enter your registered email." });
      return;
    }
    if (!loginPassword) {
      setStatusMessage({ type: "error", text: "Please enter your password." });
      return;
    }

    setIsSubmitting(true);
    try {
      await api.login({
        email: loginEmail.trim().toLowerCase(),
        password: loginPassword,
      });
      onLoginSuccess();
    } catch (err: any) {
      setStatusMessage({
        type: "error",
        text: err.message || "Invalid email or password. Please try again or create an account.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "10px auto", padding: "0 10px" }}>
      {/* Brand & App Identity Header */}
      <div style={{ textAlign: "center", marginBottom: "14px" }}>
        <div style={{ display: "inline-flex", alignItems: "center", gap: "8px", padding: "6px 14px", borderRadius: "999px", background: "rgba(2, 132, 199, 0.15)", border: "1px solid rgba(2, 132, 199, 0.3)", marginBottom: "10px" }}>
          <span style={{ fontSize: "16px" }}>🎓</span>
          <span style={{ fontWeight: 800, fontSize: "13px", color: "#38bdf8" }}>MENTOR MATE</span>
          <span style={{ fontSize: "11px", color: "#94a3b8" }}>• Adaptive Learning Platform</span>
        </div>
        <h1 style={{ margin: "0 0 6px 0", fontSize: "26px", fontWeight: 800, color: "#f8fafc", letterSpacing: "-0.5px" }}>
          {authMode === "register" ? "Create Your Student Account" : "Sign In to Your Dashboard"}
        </h1>
        <p style={{ margin: 0, fontSize: "14px", color: "#cbd5e1" }}>
          {authMode === "register"
            ? "Register first to calibrate your adaptive student model and knowledge tracing."
            : "Welcome back! Enter your credentials to continue your personalized study plan."}
        </p>
      </div>

      {/* Main Elevated Authentication Card */}
      <div className="card" style={{ padding: "20px 22px", borderRadius: "16px", boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)", border: "1px solid #e2e8f0" }}>

        {/* Status Notification Alert */}
        {statusMessage && (
          <div
            style={{
              padding: "10px 12px",
              borderRadius: "10px",
              marginBottom: "14px",
              fontSize: "13px",
              lineHeight: "1.4",
              background: statusMessage.type === "success" ? "rgba(16, 185, 129, 0.1)" : "rgba(239, 68, 68, 0.1)",
              border: `1px solid ${statusMessage.type === "success" ? "#10b981" : "#ef4444"}`,
              color: statusMessage.type === "success" ? "#065f46" : "#991b1b",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <span>{statusMessage.type === "success" ? "✓" : "⚠"}</span>
            <span>{statusMessage.text}</span>
          </div>
        )}

        {/* ================= REGISTER VIEW ================= */}
        {authMode === "register" ? (
          <form onSubmit={handleRegisterSubmit} style={{ display: "grid", gap: "11px" }}>
            <div>
              <label htmlFor="regName">Student Full Name</label>
              <input
                id="regName"
                className="input"
                placeholder="Enter student full name"
                value={regName}
                onChange={(e) => setRegName(e.target.value)}
                required
              />
            </div>

            <div style={{ display: "grid", gap: "10px", gridTemplateColumns: "1fr 1fr" }}>
              <div>
                <label htmlFor="regKlass">Academic Level</label>
                <select
                  id="regKlass"
                  className="input"
                  value={regKlass}
                  onChange={(e) => handleKlassChange(e.target.value)}
                >
                  <option value="10">Class 10 (10th Boards)</option>
                  <option value="11">Class 11 (Senior Secondary)</option>
                  <option value="12">Class 12 (Board & Entrances)</option>
                  <option value="Degree">Undergraduate (Degree)</option>
                </select>
              </div>

              <div>
                <label htmlFor="regGoal">Target Exam or Educational Goal</label>
                <input
                  id="regGoal"
                  className="input"
                  placeholder="e.g. JEE, NEET, Boards, GATE..."
                  value={regGoal}
                  onChange={(e) => setRegGoal(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Smart Interconnected Exam Suggestions Chips */}
            <div style={{ background: "#f8fafc", padding: "8px 10px", borderRadius: "8px", border: "1px solid #e2e8f0" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                <span style={{ fontSize: "11.5px", fontWeight: 700, color: "#475569" }}>
                  🎯 Recommended for {regKlass === "Degree" ? "Undergraduate / Degree" : `Class ${regKlass}`}:
                </span>
                <span style={{ fontSize: "10.5px", color: "#64748b" }}>Click chip to select or type custom</span>
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {getGoalSuggestionsForKlass(regKlass).map((suggestion) => {
                  const isSelected = regGoal.toLowerCase().trim() === suggestion.toLowerCase().trim();
                  return (
                    <button
                      key={suggestion}
                      type="button"
                      onClick={() => setRegGoal(suggestion)}
                      style={{
                        fontSize: "11.5px",
                        padding: "3px 9px",
                        borderRadius: "14px",
                        border: isSelected ? "1.5px solid #0284c7" : "1px solid #cbd5e1",
                        background: isSelected ? "#e0f2fe" : "#ffffff",
                        color: isSelected ? "#0369a1" : "#334155",
                        fontWeight: isSelected ? 700 : 500,
                        cursor: "pointer",
                        transition: "all 0.15s ease",
                      }}
                    >
                      {isSelected ? "✓ " : ""}{suggestion}
                    </button>
                  );
                })}
              </div>
            </div>

            <div>
              <label htmlFor="regEmail">Parent / Student Email Address</label>
              <input
                id="regEmail"
                type="email"
                className="input"
                placeholder="Enter email address"
                value={regEmail}
                onChange={(e) => setRegEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label htmlFor="regPassword">Create Account Password</label>
              <div style={{ position: "relative" }}>
                <input
                  id="regPassword"
                  type={showRegPassword ? "text" : "password"}
                  className="input"
                  style={{ paddingRight: "40px" }}
                  placeholder="Minimum 6 characters"
                  value={regPassword}
                  onChange={(e) => setRegPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowRegPassword(!showRegPassword)}
                  style={{
                    position: "absolute",
                    right: "10px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "transparent",
                    border: "none",
                    cursor: "pointer",
                    color: "#64748b",
                    padding: "4px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                  aria-label={showRegPassword ? "Hide password" : "Show password"}
                  title={showRegPassword ? "Hide password" : "Show password"}
                >
                  {showRegPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="regSchool">School / College / Institution (Optional)</label>
              <input
                id="regSchool"
                className="input"
                placeholder="Enter school, college, or institute name"
                value={regSchool}
                onChange={(e) => setRegSchool(e.target.value)}
              />
            </div>

            <div style={{ marginTop: "6px" }}>
              <button
                type="submit"
                className="btn"
                disabled={isSubmitting}
                style={{ width: "100%", padding: "11px 20px", fontSize: "14.5px" }}
              >
                {isSubmitting ? "Registering..." : "Create Student Account →"}
              </button>
            </div>

            <div className="hr"></div>

            <div style={{ textAlign: "center", fontSize: "13px", color: "#64748b" }}>
              Already registered?{" "}
              <button
                type="button"
                onClick={() => { setAuthMode("login"); setStatusMessage(null); }}
                style={{ background: "none", border: "none", color: "#0284c7", fontWeight: 700, cursor: "pointer", textDecoration: "underline" }}
              >
                Sign in to your account here
              </button>
            </div>
          </form>
        ) : (
          /* ================= SIGN IN VIEW ================= */
          <form onSubmit={handleLoginSubmit} style={{ display: "grid", gap: "14px" }}>
            <div>
              <label htmlFor="loginEmail">Registered Email</label>
              <input
                id="loginEmail"
                type="email"
                className="input"
                placeholder="Enter registered email address"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <label htmlFor="loginPassword">Password</label>
                <span
                  className="small note"
                  style={{ color: "#0284c7", cursor: "pointer" }}
                  onClick={() => alert("Please contact your school administrator or re-register if you forgot your credentials.")}
                >
                  Forgot?
                </span>
              </div>
              <div style={{ position: "relative" }}>
                <input
                  id="loginPassword"
                  type={showLoginPassword ? "text" : "password"}
                  className="input"
                  style={{ paddingRight: "40px" }}
                  placeholder="Enter your password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowLoginPassword(!showLoginPassword)}
                  style={{
                    position: "absolute",
                    right: "10px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "transparent",
                    border: "none",
                    cursor: "pointer",
                    color: "#64748b",
                    padding: "4px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                  aria-label={showLoginPassword ? "Hide password" : "Show password"}
                  title={showLoginPassword ? "Hide password" : "Show password"}
                >
                  {showLoginPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </div>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <input
                type="checkbox"
                id="rememberMe"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                style={{ cursor: "pointer" }}
              />
              <label htmlFor="rememberMe" style={{ margin: 0, fontSize: "13px", cursor: "pointer" }}>
                Keep me signed in on this device
              </label>
            </div>

            <div style={{ marginTop: "6px" }}>
              <button
                type="submit"
                className="btn"
                disabled={isSubmitting}
                style={{ width: "100%", padding: "11px 24px", fontSize: "14.5px" }}
              >
                {isSubmitting ? "Authenticating..." : "Sign In to Student Account →"}
              </button>
            </div>

            <div className="hr"></div>

            <div style={{ textAlign: "center", fontSize: "13px", color: "#64748b" }}>
              Need an account?{" "}
              <button
                type="button"
                onClick={() => { setAuthMode("register"); setStatusMessage(null); }}
                style={{ background: "none", border: "none", color: "#0284c7", fontWeight: 700, cursor: "pointer", textDecoration: "underline" }}
              >
                Register as a new student here
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
