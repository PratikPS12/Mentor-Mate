"use client";

import React, { useState } from "react";
import LoginCard from "@/components/auth/LoginCard";

interface LandingPageProps {
  onLoginSuccess: () => void;
  onContinueToApp?: () => void;
  isAuthenticated?: boolean;
}

export default function LandingPage({
  onLoginSuccess,
  onContinueToApp,
  isAuthenticated = false,
}: LandingPageProps) {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authInitialMode, setAuthInitialMode] = useState<"register" | "login">("register");
  const [activePreviewTab, setActivePreviewTab] = useState<
    "onboarding" | "ocr" | "diagnostic" | "planner" | "tutor"
  >("onboarding");

  const openAuth = (mode: "register" | "login") => {
    setAuthInitialMode(mode);
    setShowAuthModal(true);
  };

  const closeAuth = () => {
    setShowAuthModal(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "radial-gradient(1200px 800px at 50% -10%, rgba(99, 102, 241, 0.12), transparent 70%), radial-gradient(800px 600px at 90% 40%, rgba(2, 132, 199, 0.08), transparent 60%), #090d16",
        color: "#f8fafc",
        fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, sans-serif",
        position: "relative",
        overflowX: "hidden",
      }}
    >
      {/* Background Subtle Grid Effect */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />

      {/* ================= NAVIGATION BAR ================= */}
      <nav
        style={{
          position: "sticky",
          top: 0,
          zIndex: 40,
          backdropFilter: "blur(16px)",
          WebkitBackdropFilter: "blur(16px)",
          backgroundColor: "rgba(9, 13, 22, 0.82)",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
          padding: "16px 24px",
        }}
      >
        <div
          style={{
            maxWidth: "1200px",
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          {/* Logo & Brand */}
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <div
              style={{
                width: "40px",
                height: "40px",
                borderRadius: "12px",
                background: "linear-gradient(135deg, #6366f1 0%, #0284c7 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: 900,
                fontSize: "20px",
                color: "#ffffff",
                boxShadow: "0 0 20px rgba(99, 102, 241, 0.4)",
              }}
            >
              M
            </div>
            <div>
              <div style={{ fontWeight: 900, fontSize: "19px", letterSpacing: "-0.5px", display: "flex", alignItems: "center", gap: "8px" }}>
                <span>Mentor Mate</span>
                <span
                  style={{
                    fontSize: "11px",
                    fontWeight: 700,
                    textTransform: "uppercase",
                    letterSpacing: "0.8px",
                    padding: "2px 8px",
                    borderRadius: "999px",
                    background: "rgba(99, 102, 241, 0.2)",
                    color: "#a5b4fc",
                    border: "1px solid rgba(99, 102, 241, 0.35)",
                  }}
                >
                  AI Learning Twin
                </span>
              </div>
            </div>
          </div>

          {/* Quick Nav Links (Desktop) */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "24px",
              fontSize: "14px",
              fontWeight: 600,
              color: "#94a3b8",
            }}
          >
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              style={{ color: "inherit", textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#94a3b8")}
            >
              Home
            </a>
            <a
              href="#philosophy"
              style={{ color: "inherit", textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#94a3b8")}
            >
              Why Mentor Mate
            </a>
            <a
              href="#showcase"
              style={{ color: "inherit", textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#94a3b8")}
            >
              How It Works
            </a>
            <a
              href="#engines"
              style={{ color: "inherit", textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#94a3b8")}
            >
              Core AI Engines
            </a>
          </div>

          {/* Actions */}
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            {isAuthenticated ? (
              <button
                onClick={onContinueToApp}
                style={{
                  padding: "9px 20px",
                  borderRadius: "10px",
                  background: "linear-gradient(135deg, #6366f1 0%, #0284c7 100%)",
                  color: "#ffffff",
                  fontWeight: 700,
                  fontSize: "14px",
                  border: "none",
                  cursor: "pointer",
                  boxShadow: "0 0 16px rgba(99, 102, 241, 0.35)",
                }}
              >
                Go to Study Dashboard →
              </button>
            ) : (
              <>
                <button
                  onClick={() => openAuth("login")}
                  style={{
                    padding: "9px 18px",
                    borderRadius: "10px",
                    background: "rgba(255, 255, 255, 0.05)",
                    border: "1px solid rgba(255, 255, 255, 0.12)",
                    color: "#f1f5f9",
                    fontWeight: 700,
                    fontSize: "13.5px",
                    cursor: "pointer",
                    transition: "all 0.15s ease",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(255, 255, 255, 0.1)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)")}
                >
                  Sign In
                </button>
                <button
                  onClick={() => openAuth("register")}
                  style={{
                    padding: "9px 20px",
                    borderRadius: "10px",
                    background: "linear-gradient(135deg, #6366f1 0%, #0284c7 100%)",
                    color: "#ffffff",
                    fontWeight: 800,
                    fontSize: "13.5px",
                    border: "none",
                    cursor: "pointer",
                    boxShadow: "0 4px 16px rgba(99, 102, 241, 0.4)",
                    transition: "transform 0.15s ease",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-1px)")}
                  onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
                >
                  Get Started Free →
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* ================= HERO SECTION ================= */}
      <section
        style={{
          position: "relative",
          zIndex: 10,
          maxWidth: "1100px",
          margin: "0 auto",
          padding: "80px 24px 60px 24px",
          textAlign: "center",
        }}
      >
        {/* Ethos Tag */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "8px",
            padding: "8px 18px",
            borderRadius: "999px",
            background: "rgba(99, 102, 241, 0.1)",
            border: "1px solid rgba(99, 102, 241, 0.28)",
            color: "#a5b4fc",
            fontSize: "12.5px",
            fontWeight: 800,
            textTransform: "uppercase",
            letterSpacing: "1px",
            marginBottom: "24px",
          }}
        >
          <span>✨ Pure Academic Intelligence</span>
          <span style={{ opacity: 0.4 }}>•</span>
          <span>Zero Fake Testimonials</span>
          <span style={{ opacity: 0.4 }}>•</span>
          <span>Zero Hardcoded Tests</span>
        </div>

        {/* Primary Soul Headline */}
        <h1
          style={{
            fontSize: "clamp(34px, 5.5vw, 62px)",
            fontWeight: 900,
            lineHeight: 1.15,
            letterSpacing: "-1.5px",
            margin: "0 auto 20px auto",
            maxWidth: "920px",
            background: "linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          The AI Academic Learning Twin That Adapts Strictly to{" "}
          <span
            style={{
              background: "linear-gradient(135deg, #818cf8 0%, #38bdf8 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Your Real Data
          </span>
          .
        </h1>

        {/* Candid Subheadline */}
        <p
          style={{
            fontSize: "clamp(16px, 2vw, 19px)",
            lineHeight: 1.6,
            color: "#94a3b8",
            maxWidth: "760px",
            margin: "0 auto 36px auto",
            fontWeight: 400,
          }}
        >
          No pre-fabricated static packages. No memorized question banks. Mentor Mate ingests your exact school or college level, target exam goal, and handwritten class notes—dynamically generating personalized study calendars, real-time Bayesian cognitive diagnostics, and step-by-step Socratic guidance.
        </p>

        {/* CTAs */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "16px",
            marginBottom: "48px",
          }}
        >
          <button
            onClick={() => (isAuthenticated && onContinueToApp ? onContinueToApp() : openAuth("register"))}
            style={{
              padding: "16px 36px",
              borderRadius: "14px",
              background: "linear-gradient(135deg, #6366f1 0%, #0284c7 100%)",
              color: "#ffffff",
              fontSize: "16px",
              fontWeight: 800,
              border: "none",
              cursor: "pointer",
              boxShadow: "0 10px 30px rgba(99, 102, 241, 0.45)",
              display: "flex",
              alignItems: "center",
              gap: "10px",
              transition: "transform 0.15s ease",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-2px)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
          >
            <span>{isAuthenticated ? "Enter Your Study Dashboard" : "Start Your Personalized Onboarding"}</span>
            <span style={{ fontSize: "18px" }}>→</span>
          </button>

          <a
            href="#showcase"
            style={{
              padding: "15px 30px",
              borderRadius: "14px",
              background: "rgba(255, 255, 255, 0.04)",
              border: "1px solid rgba(255, 255, 255, 0.14)",
              color: "#e2e8f0",
              fontSize: "15px",
              fontWeight: 700,
              textDecoration: "none",
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              transition: "all 0.15s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "rgba(255, 255, 255, 0.08)";
              e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.25)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "rgba(255, 255, 255, 0.04)";
              e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.14)";
            }}
          >
            <span>Explore Adaptive System</span>
            <span>↓</span>
          </a>
        </div>

        {/* Authentic Pillars Ribbon (Zero fake vanity metrics) */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "14px",
            maxWidth: "960px",
            margin: "0 auto",
          }}
        >
          {[
            { label: "100% Student Data-Driven", desc: "No generic demo profiles" },
            { label: "AI LLM Diagnostic Tests", desc: "Zero hardcoded question banks" },
            { label: "Notes Vision OCR", desc: "Parses handwritten photos & PDFs" },
            { label: "Bayesian Knowledge Tracing", desc: "Models your true cognitive mastery" },
          ].map((item, idx) => (
            <div
              key={idx}
              style={{
                background: "rgba(255, 255, 255, 0.03)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "12px",
                padding: "16px 14px",
                textAlign: "center",
              }}
            >
              <div style={{ color: "#38bdf8", fontWeight: 800, fontSize: "14.5px" }}>{item.label}</div>
              <div style={{ color: "#64748b", fontSize: "12px", marginTop: "4px" }}>{item.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ================= SECTION 2: THE PHILOSOPHY (WHY MENTOR MATE IS DIFFERENT) ================= */}
      <section
        id="philosophy"
        style={{
          position: "relative",
          zIndex: 10,
          maxWidth: "1100px",
          margin: "0 auto",
          padding: "70px 24px",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "44px" }}>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 800,
              textTransform: "uppercase",
              letterSpacing: "1.2px",
              color: "#818cf8",
              marginBottom: "8px",
            }}
          >
            Core Philosophy
          </div>
          <h2 style={{ fontSize: "clamp(26px, 3.5vw, 40px)", fontWeight: 900, letterSpacing: "-0.8px", color: "#ffffff" }}>
            EdTech Built on Truth, Not Marketing Hype.
          </h2>
          <p style={{ color: "#94a3b8", fontSize: "16px", maxWidth: "680px", margin: "10px auto 0 auto" }}>
            Why does nearly every learning platform feel identical? Because they force you into prefabricated boxes. Here is how Mentor Mate is built differently:
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "20px",
          }}
        >
          {/* Traditional Edtech Box */}
          <div
            style={{
              background: "rgba(239, 68, 68, 0.03)",
              border: "1px solid rgba(239, 68, 68, 0.2)",
              borderRadius: "18px",
              padding: "28px",
              position: "relative",
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "4px 12px",
                borderRadius: "6px",
                background: "rgba(239, 68, 68, 0.15)",
                color: "#f87171",
                fontSize: "12px",
                fontWeight: 800,
                textTransform: "uppercase",
                marginBottom: "16px",
              }}
            >
              The Traditional Platform Pattern
            </div>
            <h3 style={{ fontSize: "20px", fontWeight: 800, color: "#fca5a5", marginBottom: "14px" }}>
              Pre-Packaged, Rigid &amp; Synthetic
            </h3>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: "12px", fontSize: "14px", color: "#cbd5e1" }}>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#ef4444", fontWeight: 900 }}>✕</span>
                <span><strong>Fake Testimonials:</strong> Manufactured student quotes and fabricated 5-star ratings to manufacture trust.</span>
              </li>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#ef4444", fontWeight: 900 }}>✕</span>
                <span><strong>Hardcoded Test Banks:</strong> Static multiple-choice sets that everyone memorizes; no adaptation to your class notes.</span>
              </li>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#ef4444", fontWeight: 900 }}>✕</span>
                <span><strong>Rigid Fixed Goals:</strong> Forced to choose from 3 predefined exams; zero support for specific goals like GATE, Placements, or College Core.</span>
              </li>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#ef4444", fontWeight: 900 }}>✕</span>
                <span><strong>Disconnected Notes:</strong> Your handwritten notebooks and college PDFs stay ignored in binders while you watch generic videos.</span>
              </li>
            </ul>
          </div>

          {/* Mentor Mate Solution Box */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(99, 102, 241, 0.1) 0%, rgba(2, 132, 199, 0.05) 100%)",
              border: "1px solid rgba(99, 102, 241, 0.4)",
              borderRadius: "18px",
              padding: "28px",
              position: "relative",
              boxShadow: "0 12px 40px rgba(99, 102, 241, 0.15)",
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "4px 12px",
                borderRadius: "6px",
                background: "rgba(99, 102, 241, 0.25)",
                color: "#c7d2fe",
                fontSize: "12px",
                fontWeight: 800,
                textTransform: "uppercase",
                marginBottom: "16px",
              }}
            >
              The Mentor Mate Philosophy
            </div>
            <h3 style={{ fontSize: "20px", fontWeight: 800, color: "#ffffff", marginBottom: "14px" }}>
              Student-Driven, Dynamic &amp; Authentic
            </h3>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: "12px", fontSize: "14px", color: "#f1f5f9" }}>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#10b981", fontWeight: 900 }}>✓</span>
                <span><strong>Zero Fake Data:</strong> Pure honesty. Everything on your dashboard reflects your actual uploads, tests, and schedule.</span>
              </li>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#10b981", fontWeight: 900 }}>✓</span>
                <span><strong>Dynamic AI LLM Question Generation:</strong> Real-time questions crafted on the fly for your level, topic, and uploaded notes.</span>
              </li>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#10b981", fontWeight: 900 }}>✓</span>
                <span><strong>Arbitrary Goal Freedom:</strong> Type any exact target exam—from Class 10 Boards to GATE CS 2027 or Software Placements.</span>
              </li>
              <li style={{ display: "flex", gap: "10px", alignItems: "flex-start" }}>
                <span style={{ color: "#10b981", fontWeight: 900 }}>✓</span>
                <span><strong>Vision OCR Notes Intelligence:</strong> Snaps of your handwritten pages automatically turn into formula sheets, summaries, and drills.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* ================= SECTION 3: LIVE ARCHITECTURE SHOWCASE (INTERACTIVE) ================= */}
      <section
        id="showcase"
        style={{
          position: "relative",
          zIndex: 10,
          maxWidth: "1150px",
          margin: "0 auto",
          padding: "70px 24px",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "36px" }}>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 800,
              textTransform: "uppercase",
              letterSpacing: "1.2px",
              color: "#38bdf8",
              marginBottom: "8px",
            }}
          >
            Interactive Platform Architecture
          </div>
          <h2 style={{ fontSize: "clamp(26px, 3.5vw, 40px)", fontWeight: 900, letterSpacing: "-0.8px", color: "#ffffff" }}>
            See How Every Engine Powers Your Journey
          </h2>
          <p style={{ color: "#94a3b8", fontSize: "16px", maxWidth: "680px", margin: "10px auto 0 auto" }}>
            Click through the core engines below to see how Mentor Mate works in practice:
          </p>
        </div>

        {/* Tab Buttons */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            flexWrap: "wrap",
            gap: "10px",
            marginBottom: "30px",
          }}
        >
          {[
            { id: "onboarding", label: "1. Interconnected Onboarding", badge: "Smart Goals" },
            { id: "ocr", label: "2. Notes Vision OCR", badge: "Document AI" },
            { id: "diagnostic", label: "3. AI LLM Diagnostics", badge: "Zero Hardcoding" },
            { id: "planner", label: "4. Adaptive Spaced Planner", badge: "Cognitive Decay" },
            { id: "tutor", label: "5. Socratic AI Mentor", badge: "Guided Intuition" },
          ].map((tab) => {
            const isActive = activePreviewTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActivePreviewTab(tab.id as any)}
                style={{
                  padding: "10px 18px",
                  borderRadius: "12px",
                  background: isActive ? "linear-gradient(135deg, #6366f1 0%, #0284c7 100%)" : "rgba(255, 255, 255, 0.04)",
                  border: isActive ? "1px solid #818cf8" : "1px solid rgba(255, 255, 255, 0.08)",
                  color: isActive ? "#ffffff" : "#94a3b8",
                  fontWeight: 700,
                  fontSize: "13.5px",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  boxShadow: isActive ? "0 4px 16px rgba(99, 102, 241, 0.3)" : "none",
                  transition: "all 0.15s ease",
                }}
              >
                <span>{tab.label}</span>
                <span
                  style={{
                    fontSize: "10px",
                    padding: "2px 6px",
                    borderRadius: "999px",
                    background: isActive ? "rgba(255, 255, 255, 0.25)" : "rgba(255, 255, 255, 0.06)",
                    color: isActive ? "#ffffff" : "#64748b",
                  }}
                >
                  {tab.badge}
                </span>
              </button>
            );
          })}
        </div>

        {/* Active Tab Preview Display Card */}
        <div
          style={{
            background: "rgba(15, 23, 42, 0.75)",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            borderRadius: "20px",
            padding: "36px",
            boxShadow: "0 20px 50px rgba(0, 0, 0, 0.4)",
            backdropFilter: "blur(20px)",
          }}
        >
          {activePreviewTab === "onboarding" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "24px" }}>
                <div>
                  <span className="pill" style={{ background: "rgba(99, 102, 241, 0.15)", color: "#a5b4fc", border: "1px solid rgba(99, 102, 241, 0.3)" }}>
                    Feature 01 • Academic Level &amp; Exam Goal Interconnection
                  </span>
                  <h3 style={{ fontSize: "24px", fontWeight: 800, marginTop: "12px", color: "#ffffff" }}>
                    The Portal Adapts to You From the Very First Screen
                  </h3>
                </div>
                <div style={{ color: "#38bdf8", fontWeight: 700, fontSize: "14px" }}>
                  Class 10, 11, 12 or College Undergrad
                </div>
              </div>

              <p style={{ color: "#cbd5e1", fontSize: "15px", lineHeight: 1.6, marginBottom: "24px" }}>
                Select your class level, and the system intelligently recalibrates its suggested target exams. If you select College Undergraduate, you are presented with GATE, Software Engineering Placements, Data Science &amp; AI, and CAT. Want to prepare for something completely custom? Simply type your custom goal (e.g. <em>GATE CS 2027</em> or <em>Full-Stack Placements</em>), and the entire curriculum, course catalog, and syllabus engine adjusts instantly.
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "14px" }}>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#818cf8", fontSize: "13.5px" }}>Class 10 Smart Scope</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    10th CBSE/ICSE Boards, State Boards, NTSE &amp; Olympiad, Foundation JEE/NEET.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#38bdf8", fontSize: "13.5px" }}>Class 11 &amp; 12 Smart Scope</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    JEE Main/Advanced, NEET Medical, MHT-CET, CUET, 12th Senior Secondary Boards.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#10b981", fontSize: "13.5px" }}>Undergraduate &amp; Arbitrary</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    GATE CS/ECE, Software Placements &amp; DSA, CAT, GRE, University Core, or any custom target.
                  </div>
                </div>
              </div>
            </div>
          )}

          {activePreviewTab === "ocr" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "24px" }}>
                <div>
                  <span className="pill" style={{ background: "rgba(14, 165, 233, 0.15)", color: "#38bdf8", border: "1px solid rgba(14, 165, 233, 0.3)" }}>
                    Feature 02 • Real Document &amp; Handwritten Notes OCR
                  </span>
                  <h3 style={{ fontSize: "24px", fontWeight: 800, marginTop: "12px", color: "#ffffff" }}>
                    Turn Handwritten Photos &amp; PDFs Into Interactive Intelligence
                  </h3>
                </div>
                <div style={{ color: "#a5b4fc", fontWeight: 700, fontSize: "14px" }}>
                  Multimodal Vision AI
                </div>
              </div>

              <p style={{ color: "#cbd5e1", fontSize: "15px", lineHeight: 1.6, marginBottom: "24px" }}>
                Upload photographs of your actual handwritten class notes, textbook summaries, or lecture slide PDFs directly on your dashboard. Mentor Mate’s OCR extraction engine reads your handwritten content, compiles an executive summary, isolates critical formulas and theorems, and generates an instant diagnostic drill based specifically on what you wrote.
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "14px" }}>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#38bdf8", fontSize: "13.5px" }}>Formula &amp; Relation Extraction</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Mathematically isolates governing equations and symbols from your handwritten sheets.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#818cf8", fontSize: "13.5px" }}>Instant Note Practice Drills</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Generates 2–4 targeted multiple-choice check questions directly from your notes content.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#10b981", fontSize: "13.5px" }}>Socratic Notes Grounding</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Your AI Mentor references your actual uploaded material during conversational tutoring.
                  </div>
                </div>
              </div>
            </div>
          )}

          {activePreviewTab === "diagnostic" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "24px" }}>
                <div>
                  <span className="pill" style={{ background: "rgba(16, 185, 129, 0.15)", color: "#34d399", border: "1px solid rgba(16, 185, 129, 0.3)" }}>
                    Feature 03 • Zero Hardcoding Dynamic Diagnostic Tests
                  </span>
                  <h3 style={{ fontSize: "24px", fontWeight: 800, marginTop: "12px", color: "#ffffff" }}>
                    AI LLM Dynamic Questions &amp; Bayesian Knowledge Tracing
                  </h3>
                </div>
                <div style={{ color: "#34d399", fontWeight: 700, fontSize: "14px" }}>
                  BKT &amp; IRT Latent Ability
                </div>
              </div>

              <p style={{ color: "#cbd5e1", fontSize: "15px", lineHeight: 1.6, marginBottom: "24px" }}>
                Instead of serving static, pre-written questions that every student has already seen, Mentor Mate’s AI LLM synthesizes fresh, rigorous multiple-choice questions on demand. The engine verifies what you have actually studied on the platform. If you haven’t studied on the platform yet, it invites you to type any topic from your school or college classes, then diagnoses misconceptions and updates your Bayesian mastery in real time.
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "14px" }}>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#34d399", fontSize: "13.5px" }}>Cognitive Error Diagnosis</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Distinguishes calculation slips from fundamental conceptual fallacies and formula misapplications.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#38bdf8", fontSize: "13.5px" }}>Definitive Sequential Review</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Complete question-by-question breakdown showing correct derivations and remedial pathways.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#818cf8", fontSize: "13.5px" }}>Continuous BKT Update</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Real-time posterior mastery estimation without hardcoded score thresholds.
                  </div>
                </div>
              </div>
            </div>
          )}

          {activePreviewTab === "planner" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "24px" }}>
                <div>
                  <span className="pill" style={{ background: "rgba(245, 158, 11, 0.15)", color: "#fbbf24", border: "1px solid rgba(245, 158, 11, 0.3)" }}>
                    Feature 04 • Adaptive Spaced Retention Planner
                  </span>
                  <h3 style={{ fontSize: "24px", fontWeight: 800, marginTop: "12px", color: "#ffffff" }}>
                    Ebbinghaus Spaced Schedules Tailored to Your Clock
                  </h3>
                </div>
                <div style={{ color: "#fbbf24", fontWeight: 700, fontSize: "14px" }}>
                  Half-Life Decay Modeling
                </div>
              </div>

              <p style={{ color: "#cbd5e1", fontSize: "15px", lineHeight: 1.6, marginBottom: "24px" }}>
                A generic timetable that assumes everyone has 6 hours a day is useless. Mentor Mate calculates your exact days remaining until your target exam and your daily available hours, balancing core concept acquisition, revision intervals, and practice problem sets to minimize cognitive overload.
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "14px" }}>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#fbbf24", fontSize: "13.5px" }}>Days-to-Exam Calibration</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Whether you have 45 days of intense sprint or 300 days of steady mastery.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#38bdf8", fontSize: "13.5px" }}>Daily Study Hours Budgeting</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Allocate 1.5, 3.0, or 5.0 hours daily with task completion state and streak tracking.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#34d399", fontSize: "13.5px" }}>Memory Half-Life Refresh</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Surfaces weak topics right before their projected retention drops below threshold.
                  </div>
                </div>
              </div>
            </div>
          )}

          {activePreviewTab === "tutor" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "24px" }}>
                <div>
                  <span className="pill" style={{ background: "rgba(168, 85, 247, 0.15)", color: "#c084fc", border: "1px solid rgba(168, 85, 247, 0.3)" }}>
                    Feature 05 • 24/7 Socratic AI Academic Mentor
                  </span>
                  <h3 style={{ fontSize: "24px", fontWeight: 800, marginTop: "12px", color: "#ffffff" }}>
                    Guided Problem-Solving That Builds Real Intuition
                  </h3>
                </div>
                <div style={{ color: "#c084fc", fontWeight: 700, fontSize: "14px" }}>
                  Non-Spoonfeeding Pedagogy
                </div>
              </div>

              <p style={{ color: "#cbd5e1", fontSize: "15px", lineHeight: 1.6, marginBottom: "24px" }}>
                Most AI tutors immediately spit out final answers, robbing you of the cognitive leap required to master a topic. Mentor Mate acts as a true Socratic mentor: asking guiding questions, highlighting relevant formulas, and helping you derive the breakthrough on your own.
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "14px" }}>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#c084fc", fontSize: "13.5px" }}>Socratic Scaffolding</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Breaks complex multi-step physics, math, and coding problems into intuitive sub-steps.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#38bdf8", fontSize: "13.5px" }}>Syllabus &amp; Exam Grounding</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    Strictly contextualizes answers to your class syllabus and exam format benchmarks.
                  </div>
                </div>
                <div style={{ background: "rgba(255, 255, 255, 0.04)", padding: "16px", borderRadius: "12px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
                  <div style={{ fontWeight: 800, color: "#34d399", fontSize: "13.5px" }}>Zero Hallucination Focus</div>
                  <div style={{ color: "#94a3b8", fontSize: "12.5px", marginTop: "6px" }}>
                    References verified curricula and your uploaded materials for reliable academic rigor.
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ================= SECTION 4: THE FIVE SCIENTIFIC ENGINES ================= */}
      <section
        id="engines"
        style={{
          position: "relative",
          zIndex: 10,
          maxWidth: "1150px",
          margin: "0 auto",
          padding: "70px 24px",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 800,
              textTransform: "uppercase",
              letterSpacing: "1.2px",
              color: "#a5b4fc",
              marginBottom: "8px",
            }}
          >
            Technical Underpinnings
          </div>
          <h2 style={{ fontSize: "clamp(26px, 3.5vw, 40px)", fontWeight: 900, letterSpacing: "-0.8px", color: "#ffffff" }}>
            The Scientific Engines Powering Mentor Mate
          </h2>
          <p style={{ color: "#94a3b8", fontSize: "16px", maxWidth: "680px", margin: "10px auto 0 auto" }}>
            No black boxes. Here are the core mathematical and pedagogical systems running beneath every feature:
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "20px",
          }}
        >
          {[
            {
              title: "1. Dynamic Goal & Curriculum Engine",
              tag: "Interconnected Taxonomy",
              desc: "Maps any arbitrary academic goal or class level into structured subject domains, prerequisite trees, and core syllabus topics without rigid hardcoded limits.",
              color: "#6366f1",
            },
            {
              title: "2. Multimodal OCR & Vision Pipeline",
              tag: "Computer Vision + LLM",
              desc: "Extracts textual, tabular, and mathematical equations from camera snaps of handwritten notes, class slides, and textbooks for deep semantic synthesis.",
              color: "#0284c7",
            },
            {
              title: "3. Bayesian Knowledge Tracing (BKT)",
              tag: "Probabilistic Modeling",
              desc: "Calculates posterior concept mastery P(L_t) using slips, guesses, and learning transitions, ensuring true skill depth is measured accurately.",
              color: "#10b981",
            },
            {
              title: "4. Item Response Theory (IRT) Engine",
              tag: "Latent Ability (θ) Estimation",
              desc: "Calibrates question difficulty (b) and discrimination (a) to assess your true latent ability parameter independently of raw percentage scores.",
              color: "#f59e0b",
            },
            {
              title: "5. Ebbinghaus Memory Retention Engine",
              tag: "Spaced Repetition Decay",
              desc: "Models individual memory strength and exponential half-life forgetting curves, scheduling targeted reviews right when memory begins to fade.",
              color: "#ec4899",
            },
            {
              title: "6. Cognitive Misconception Classifier",
              tag: "Error Root-Cause Analysis",
              desc: "Analyzes distractors and response latency to distinguish careless slips from deep conceptual gaps, recommending targeted remedial video modules.",
              color: "#8b5cf6",
            },
          ].map((engine, idx) => (
            <div
              key={idx}
              style={{
                background: "rgba(255, 255, 255, 0.03)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "16px",
                padding: "24px",
                transition: "all 0.2s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = "rgba(99, 102, 241, 0.35)";
                e.currentTarget.style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.08)";
                e.currentTarget.style.transform = "translateY(0)";
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <span
                  style={{
                    fontSize: "11px",
                    fontWeight: 800,
                    textTransform: "uppercase",
                    letterSpacing: "0.8px",
                    padding: "3px 8px",
                    borderRadius: "6px",
                    background: `${engine.color}1a`,
                    color: engine.color,
                    border: `1px solid ${engine.color}33`,
                  }}
                >
                  {engine.tag}
                </span>
              </div>
              <h3 style={{ fontSize: "18px", fontWeight: 800, color: "#ffffff", marginBottom: "8px" }}>
                {engine.title}
              </h3>
              <p style={{ color: "#94a3b8", fontSize: "14px", lineHeight: 1.5, margin: 0 }}>
                {engine.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ================= SECTION 5: FINAL CALL TO ACTION ================= */}
      <section
        style={{
          position: "relative",
          zIndex: 10,
          maxWidth: "960px",
          margin: "40px auto 90px auto",
          padding: "0 24px",
        }}
      >
        <div
          style={{
            background: "linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(2, 132, 199, 0.15) 100%)",
            border: "1px solid rgba(99, 102, 241, 0.35)",
            borderRadius: "24px",
            padding: "50px 30px",
            textAlign: "center",
            boxShadow: "0 20px 60px rgba(0, 0, 0, 0.5)",
          }}
        >
          <h2 style={{ fontSize: "clamp(28px, 4vw, 44px)", fontWeight: 900, color: "#ffffff", letterSpacing: "-1px", marginBottom: "16px" }}>
            Ready for an Academic Companion That Truly Adapts to You?
          </h2>
          <p style={{ color: "#cbd5e1", fontSize: "16.5px", maxWidth: "620px", margin: "0 auto 30px auto", lineHeight: 1.6 }}>
            Set your current class level and target goal. Experience authentic, student-centered learning with zero fluff and complete transparency.
          </p>
          <button
            onClick={() => (isAuthenticated && onContinueToApp ? onContinueToApp() : openAuth("register"))}
            style={{
              padding: "16px 40px",
              borderRadius: "14px",
              background: "linear-gradient(135deg, #6366f1 0%, #0284c7 100%)",
              color: "#ffffff",
              fontSize: "16.5px",
              fontWeight: 800,
              border: "none",
              cursor: "pointer",
              boxShadow: "0 8px 30px rgba(99, 102, 241, 0.4)",
              transition: "transform 0.15s ease",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-2px)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
          >
            {isAuthenticated ? "Launch Your Study Dashboard →" : "Begin Your Personalized Onboarding →"}
          </button>
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer
        style={{
          borderTop: "1px solid rgba(255, 255, 255, 0.08)",
          padding: "36px 24px",
          background: "#060911",
          position: "relative",
          zIndex: 10,
        }}
      >
        <div
          style={{
            maxWidth: "1200px",
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "20px",
          }}
        >
          <div>
            <div style={{ fontWeight: 800, fontSize: "16px", color: "#f8fafc" }}>
              Mentor Mate
            </div>
            <div style={{ color: "#64748b", fontSize: "13px", marginTop: "4px" }}>
              The student-driven AI academic learning twin. Zero fake data • 100% personalized.
            </div>
          </div>

          <div style={{ display: "flex", gap: "24px", fontSize: "13px", color: "#94a3b8" }}>
            <span>Supports Class 10</span>
            <span>Class 11 &amp; 12</span>
            <span>College Undergraduate</span>
            <span>Custom Goals</span>
          </div>
        </div>
      </footer>

      {/* ================= ONBOARDING / LOGIN MODAL ================= */}
      {showAuthModal && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            zIndex: 100,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "rgba(0, 0, 0, 0.75)",
            backdropFilter: "blur(10px)",
            padding: "20px",
            animation: "fadeIn 0.2s ease-out",
          }}
          onClick={(e) => {
            if (e.target === e.currentTarget) closeAuth();
          }}
        >
          <div
            className="no-scrollbar"
            style={{
              position: "relative",
              width: "100%",
              maxWidth: "520px",
              maxHeight: "96vh",
              overflowY: "auto",
              borderRadius: "20px",
              boxShadow: "0 25px 60px rgba(0, 0, 0, 0.6)",
              scrollbarWidth: "none",
              msOverflowStyle: "none",
            }}
          >
            {/* Close Button */}
            <button
              onClick={closeAuth}
              style={{
                position: "absolute",
                top: "14px",
                right: "14px",
                zIndex: 10,
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                background: "#ffffff",
                border: "1px solid #cbd5e1",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
                fontWeight: 700,
                color: "#475569",
                boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
              }}
              aria-label="Close"
              title="Close"
            >
              ✕
            </button>

            {/* Smart Onboarding Card */}
            <LoginCard
              initialMode={authInitialMode}
              onLoginSuccess={() => {
                closeAuth();
                onLoginSuccess();
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
