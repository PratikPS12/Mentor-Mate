"use client";

import React, { useState, useEffect } from "react";
import { api, StudentProfile } from "@/lib/api";
import LoginCard from "@/components/auth/LoginCard";
import DashboardTab from "@/components/tabs/DashboardTab";
import ProfileTab from "@/components/tabs/ProfileTab";
import MarksheetTab from "@/components/tabs/MarksheetTab";
import GuidanceTab from "@/components/tabs/GuidanceTab";
import ScheduleTab from "@/components/tabs/ScheduleTab";
import TestTab from "@/components/tabs/TestTab";
import CoursesTab from "@/components/tabs/CoursesTab";
import PerformanceTab from "@/components/tabs/PerformanceTab";
import MentorTab from "@/components/tabs/MentorTab";
import AboutTab from "@/components/tabs/AboutTab";
import SettingsTab from "@/components/tabs/SettingsTab";
import LandingPage from "@/components/landing/LandingPage";

const TABS = [
  { id: "dashboard", label: "🏠 Dashboard" },
  { id: "profile", label: "🧑‍💼 Profile" },
  { id: "uploads", label: "📄 Marksheet" },
  { id: "guidance", label: "🎯 Guidance" },
  { id: "schedule", label: "📅 Schedule" },
  { id: "test", label: "📝 Test" },
  { id: "courses", label: "📚 Courses" },
  { id: "performance", label: "📊 Performance" },
  { id: "mentor", label: "💬 Ask Mentor" },
  { id: "about", label: "ℹ About Us" },
  { id: "settings", label: "⚙ Settings" },
];

export default function MentorMateApp() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [streakDays, setStreakDays] = useState(0);
  const [isMarking, setIsMarking] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [viewingLandingPage, setViewingLandingPage] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    checkAuthAndHydrate();
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("mentormate_dark_mode");
      if (saved !== null) {
        const dark = saved === "true";
        setIsDarkMode(dark);
        applyTheme(dark);
      }
    }
  }, []);

  useEffect(() => {
    if (profile && profile.dark_mode !== undefined) {
      if (typeof window !== "undefined" && localStorage.getItem("mentormate_dark_mode") === null) {
        setIsDarkMode(profile.dark_mode);
        applyTheme(profile.dark_mode);
      }
    }
  }, [profile?.dark_mode]);

  const applyTheme = (dark: boolean) => {
    if (typeof document !== "undefined") {
      document.body.style.filter = "none";
      if (dark) {
        document.documentElement.classList.add("dark");
        document.body.classList.add("dark");
        document.documentElement.setAttribute("data-theme", "dark");
      } else {
        document.documentElement.classList.remove("dark");
        document.body.classList.remove("dark");
        document.documentElement.setAttribute("data-theme", "light");
      }
    }
  };

  const toggleTheme = () => {
    const next = !isDarkMode;
    setIsDarkMode(next);
    applyTheme(next);
    if (typeof window !== "undefined") {
      localStorage.setItem("mentormate_dark_mode", next ? "true" : "false");
    }
    if (profile) {
      handleSaveProfile({ dark_mode: next });
    }
  };

  const checkAuthAndHydrate = async () => {
    setIsLoading(true);
    try {
      const me = await api.getMe();
      if (me && me.profile) {
        setIsAuthenticated(true);
        setProfile(me.profile);
        const att = await api.getAttendance();
        setStreakDays(att.streak?.streak_days || 0);
      } else {
        setIsAuthenticated(false);
      }
    } catch {
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshProfileSilently = async () => {
    try {
      const me = await api.getMe();
      if (me && me.profile) {
        setProfile(me.profile);
        const att = await api.getAttendance();
        setStreakDays(att.streak?.streak_days || 0);
      }
    } catch {
      // Ignore background refresh errors
    }
  };

  const handleMarkStudied = async () => {
    setIsMarking(true);
    try {
      const res = await api.markTodayStudied();
      setStreakDays(res.streak_days);
      alert("Marked studied for today in Mentor Mate database ✅");
    } catch (e: any) {
      alert(`Error recording attendance: ${e.message}`);
    } finally {
      setIsMarking(false);
    }
  };

  const handleSaveProfile = async (updated: Partial<StudentProfile>) => {
    if (updated.dark_mode !== undefined) {
      setIsDarkMode(updated.dark_mode);
      applyTheme(updated.dark_mode);
    }
    const res = await api.updateProfile(updated);
    setProfile(res.profile);
  };

  const handleLogout = () => {
    api.clearToken();
    setIsAuthenticated(false);
    setProfile(null);
  };

  const openTab = (tabId: string) => {
    setActiveTab(tabId);
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  if (isLoading) {
    return (
      <div className="container" style={{ textAlign: "center", padding: "60px 20px" }}>
        <div className="pill">Mentor Mate • Initializing...</div>
      </div>
    );
  }

  if (!isAuthenticated || viewingLandingPage) {
    return (
      <LandingPage
        onLoginSuccess={checkAuthAndHydrate}
        isAuthenticated={isAuthenticated}
        onContinueToApp={() => setViewingLandingPage(false)}
      />
    );
  }

  return (
    <div className="container">
      <div id="app">
        {/* Header */}
        <div className="glass header">
          <div>
            <div id="greet" className="title">
              Hi, {profile?.name || "Student"} 👋
            </div>
            <div id="subg" className="subtitle">
              Your study dashboard
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            <span className="badge" id="badgeClass">
              Class {profile?.klass || "—"}
            </span>
            <span className="badge" id="badgeGoal">
              Goal: {profile?.goal || "—"}
            </span>
            <button
              type="button"
              className="btn small secondary"
              onClick={toggleTheme}
              title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
              style={{ fontSize: "14px", padding: "6px 10px" }}
            >
              {isDarkMode ? "☀️ Light" : "🌙 Dark"}
            </button>
            <button
              className="btn small secondary"
              onClick={() => setViewingLandingPage(true)}
              title="Go to Home Page"
            >
              🏠 Home
            </button>
            <button className="btn small" onClick={() => openTab("schedule")}>
              Start Study ▶
            </button>
          </div>
        </div>

          {/* Navigation Tabs */}
          <div className="glass panel" style={{ padding: "10px" }}>
            <div className="tabs" id="tabs">
              {TABS.map((tab) => (
                <div
                  key={tab.id}
                  id={`tab-${tab.id}`}
                  className={`tab ${activeTab === tab.id ? "active" : ""}`}
                  onClick={() => openTab(tab.id)}
                >
                  {tab.label}
                </div>
              ))}
            </div>
          </div>

          {/* Panels */}
          <div id="panels" className="panel">
            {activeTab === "dashboard" && (
              <DashboardTab
                profile={profile}
                streakDays={streakDays}
                onMarkStudied={handleMarkStudied}
                onNavigateTab={openTab}
                isMarking={isMarking}
              />
            )}

            {activeTab === "profile" && (
              <ProfileTab
                profile={profile}
                onSaveProfile={handleSaveProfile}
              />
            )}

            {activeTab === "uploads" && (
              <MarksheetTab
                profile={profile}
                onMarksheetVerified={checkAuthAndHydrate}
              />
            )}

            {activeTab === "guidance" && (
              <GuidanceTab
                initialGoal={profile?.goal}
                initialWeak={profile?.weak_areas?.join(", ")}
                initialKlass={profile?.klass}
                initialHours={profile?.daily_available_hours}
              />
            )}

            {activeTab === "schedule" && (
              <ScheduleTab
                initialDays={profile?.days_to_exam || 180}
                initialHours={profile?.daily_available_hours || 3.0}
                initialSubjects={
                  profile?.weak_areas && profile.weak_areas.length > 0
                    ? profile.weak_areas.join(", ")
                    : profile?.enrolled_courses && profile.enrolled_courses.length > 0
                    ? profile.enrolled_courses.join(", ")
                    : profile?.verified_marks && profile.verified_marks.length > 0
                    ? profile.verified_marks.map((m) => m.subject).join(", ")
                    : profile?.goal
                    ? `${profile.goal} Core Foundations`
                    : "Mathematics, Physics, Chemistry"
                }
              />
            )}

            {activeTab === "test" && (
              <TestTab
                onAssessmentCompleted={refreshProfileSilently}
                onNavigateTab={openTab}
              />
            )}

            {activeTab === "courses" && (
              <CoursesTab
                initialGoal={profile?.goal}
                initialWeak={profile?.weak_areas?.join(", ")}
                initialEnrolled={profile?.enrolled_courses}
                onNavigateTab={openTab}
              />
            )}

            {activeTab === "performance" && (
              <PerformanceTab />
            )}

            {activeTab === "mentor" && (
              <MentorTab />
            )}

            {activeTab === "about" && (
              <AboutTab />
            )}

            {activeTab === "settings" && (
              <SettingsTab
                profile={profile}
                onSaveSettings={handleSaveProfile}
                onLogout={handleLogout}
              />
            )}
          </div>
        </div>
    </div>
  );
}
