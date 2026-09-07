"use client";

import React, { useState, useEffect } from "react";
import { StudentProfile } from "@/lib/api";

interface SettingsTabProps {
  profile: StudentProfile | null;
  onSaveSettings: (updated: Partial<StudentProfile>) => Promise<void>;
  onLogout: () => void;
}

export default function SettingsTab({ profile, onSaveSettings, onLogout }: SettingsTabProps) {
  const quickActionsMaster = [
    { id: "upload", text: "Upload Marksheet & Notes OCR" },
    { id: "plan", text: "AI Personalized Schedule Planner" },
    { id: "test", text: "Adaptive Diagnostic Knowledge Test" },
    { id: "mark", text: "Mark Today Studied (Daily Streak)" },
    { id: "courses", text: "Explore Curriculum Courses" },
    { id: "mentor", text: "Ask AI Socratic Mentor" },
    { id: "performance", text: "Cognitive Analytics & Learning Twin" },
  ];

  const [darkMode, setDarkMode] = useState(false);
  const [dailyHours, setDailyHours] = useState(3.0);
  const [daysToExam, setDaysToExam] = useState(180);
  const [selectedActions, setSelectedActions] = useState<string[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [successToast, setSuccessToast] = useState<string | null>(null);

  useEffect(() => {
    // Check current dark mode from DOM or profile
    if (typeof document !== "undefined") {
      const isCurrentlyDark = document.documentElement.classList.contains("dark") ||
        document.body.classList.contains("dark") ||
        (profile?.dark_mode ?? false);
      setDarkMode(isCurrentlyDark);
    }

    if (profile) {
      setDailyHours(profile.daily_available_hours || 3.0);
      setDaysToExam(profile.days_to_exam || 180);
      setSelectedActions(
        profile.quick_actions && profile.quick_actions.length > 0
          ? profile.quick_actions
          : ["upload", "plan", "test", "mark", "mentor"]
      );
    }
  }, [profile]);

  const toggleDarkMode = (enabled: boolean) => {
    setDarkMode(enabled);
    if (typeof document !== "undefined") {
      // Remove any leftover CSS invert filter
      document.body.style.filter = "none";
      if (enabled) {
        document.documentElement.classList.add("dark");
        document.body.classList.add("dark");
        document.documentElement.setAttribute("data-theme", "dark");
      } else {
        document.documentElement.classList.remove("dark");
        document.body.classList.remove("dark");
        document.documentElement.setAttribute("data-theme", "light");
      }
    }
    if (typeof window !== "undefined") {
      localStorage.setItem("mentormate_dark_mode", enabled ? "true" : "false");
    }
  };

  const toggleAction = (id: string) => {
    setSelectedActions((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleSave = async () => {
    setIsSaving(true);
    setSuccessToast(null);
    try {
      await onSaveSettings({
        dark_mode: darkMode,
        daily_available_hours: Math.max(0.5, Math.min(18, Number(dailyHours) || 3.0)),
        days_to_exam: Math.max(1, Number(daysToExam) || 180),
        quick_actions: selectedActions,
      });
      setSuccessToast("Settings saved successfully ✅");
      setTimeout(() => setSuccessToast(null), 4000);
    } catch (e: any) {
      alert(`Failed to save settings: ${e.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div id="panel-settings" className="card" style={{ display: "grid", gap: "16px" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "8px" }}>
        <div>
          <h2 style={{ margin: 0, fontSize: "20px", fontWeight: 800, color: "var(--text-heading)" }}>
            ⚙️ Preferences & Study Settings
          </h2>
          <p style={{ margin: "3px 0 0 0", fontSize: "13px", color: "var(--muted)" }}>
            Customize your learning theme, daily study capacity, and dashboard shortcuts.
          </p>
        </div>
      </div>

      {successToast && (
        <div
          style={{
            padding: "10px 14px",
            background: "rgba(16, 185, 129, 0.14)",
            border: "1px solid var(--ok)",
            borderRadius: "8px",
            color: "var(--ok)",
            fontWeight: 600,
            fontSize: "13.5px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span>{successToast}</span>
          <button
            onClick={() => setSuccessToast(null)}
            style={{ background: "none", border: "none", cursor: "pointer", fontWeight: 700, color: "var(--ok)" }}
          >
            ✕
          </button>
        </div>
      )}

      {/* 1. Appearance / Theme */}
      <div className="card" style={{ background: "var(--card-subtle)", border: "1px solid var(--border)" }}>
        <div style={{ fontWeight: 800, fontSize: "15px", marginBottom: "8px", color: "var(--text-heading)" }}>
          🎨 Appearance & Visual Theme
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px", padding: "8px 0" }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: "14px", color: "var(--text)" }}>
              {darkMode ? "🌙 Dark Mode (Active)" : "☀️ Light Mode (Active)"}
            </div>
            <div className="note" style={{ marginTop: "2px" }}>
              High-contrast sleek dark theme engineered for comfortable low-light study sessions.
            </div>
          </div>
          <button
            type="button"
            className="btn small"
            onClick={() => toggleDarkMode(!darkMode)}
            style={{
              background: darkMode ? "var(--card)" : "var(--card-subtle)",
              color: darkMode ? "var(--accent)" : "var(--text)",
              border: "1.5px solid var(--border)",
              padding: "8px 14px",
              fontWeight: 700,
              fontSize: "13px",
            }}
          >
            {darkMode ? "Switch to Light ☀️" : "Switch to Dark 🌙"}
          </button>
        </div>
      </div>

      {/* 2. Study Pace & Capacity */}
      <div className="card" style={{ background: "var(--card-subtle)", border: "1px solid var(--border)" }}>
        <div style={{ fontWeight: 800, fontSize: "15px", marginBottom: "8px", color: "var(--text-heading)" }}>
          ⏱️ Study Target & Schedule Calibration
        </div>
        <div className="grid-2 row">
          <div>
            <label htmlFor="setHours">Daily Available Study Hours: {dailyHours}h</label>
            <input
              id="setHours"
              type="range"
              min="1"
              max="14"
              step="0.5"
              className="input"
              value={dailyHours}
              onChange={(e) => setDailyHours(Number(e.target.value))}
              style={{ cursor: "pointer" }}
            />
            <div className="note" style={{ marginTop: "4px" }}>
              The AI Daily Scheduler calibrates tasks to sum to this duration.
            </div>
          </div>

          <div>
            <label htmlFor="setDays">Days Remaining to Exam / Milestone</label>
            <input
              id="setDays"
              type="number"
              min="1"
              max="1000"
              className="input"
              value={daysToExam}
              onChange={(e) => setDaysToExam(Number(e.target.value))}
            />
            <div className="note" style={{ marginTop: "4px" }}>
              Used for pacing spaced retention intervals and mock revisions.
            </div>
          </div>
        </div>
      </div>

      {/* 3. Dashboard Shortcuts */}
      <div className="card" style={{ background: "var(--card-subtle)", border: "1px solid var(--border)" }}>
        <div style={{ fontWeight: 800, fontSize: "15px", marginBottom: "6px", color: "var(--text-heading)" }}>
          📌 Dashboard Quick Action Cards
        </div>
        <div className="note" style={{ marginBottom: "12px" }}>
          Choose which convenience shortcuts appear on your primary study dashboard:
        </div>
        <div style={{ display: "grid", gap: "8px", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}>
          {quickActionsMaster.map((qa) => {
            const isChecked = selectedActions.includes(qa.id);
            return (
              <label
                key={qa.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  cursor: "pointer",
                  padding: "8px 12px",
                  borderRadius: "8px",
                  background: isChecked ? "rgba(99, 102, 241, 0.08)" : "var(--card)",
                  border: isChecked ? "1px solid var(--brand)" : "1px solid var(--border)",
                  transition: "all 0.15s ease",
                }}
              >
                <input
                  type="checkbox"
                  checked={isChecked}
                  onChange={() => toggleAction(qa.id)}
                  style={{ width: "16px", height: "16px", cursor: "pointer" }}
                />
                <span style={{ fontSize: "13px", fontWeight: isChecked ? 700 : 500, color: "var(--text)" }}>
                  {qa.text}
                </span>
              </label>
            );
          })}
        </div>
      </div>

      {/* 4. Account Overview & Actions */}
      <div className="card" style={{ background: "var(--card-subtle)", border: "1px solid var(--border)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px" }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: "14px", color: "var(--text)" }}>
              Account: {profile?.name || "Student"} ({profile?.email || ""})
            </div>
            <div className="note" style={{ marginTop: "2px" }}>
              Target: <strong>{profile?.goal || "Academic Prep"}</strong> • Academic Level: <strong>Class {profile?.klass || "10"}</strong>
            </div>
          </div>
          <button
            type="button"
            className="btn secondary small"
            onClick={onLogout}
            style={{ color: "#ef4444", borderColor: "#fca5a5" }}
          >
            Sign Out
          </button>
        </div>
      </div>

      {/* Save Button */}
      <div className="right" style={{ marginTop: "8px" }}>
        <button
          className="btn"
          onClick={handleSave}
          disabled={isSaving}
          style={{ padding: "9px 22px", fontSize: "14px" }}
        >
          {isSaving ? "Saving..." : "Save Settings"}
        </button>
      </div>
    </div>
  );
}
