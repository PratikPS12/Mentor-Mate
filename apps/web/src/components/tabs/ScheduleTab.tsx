"use client";

import React, { useState, useEffect, useMemo } from "react";
import { api, StudyPlan, StudyPlanTask } from "@/lib/api";

interface ScheduleTabProps {
  initialDays?: number;
  initialHours?: number;
  initialSubjects?: string;
}

const PRESETS = [
  {
    label: "💻 CS & AI/ML",
    subs: "Data Structures & Algorithms, Linear Algebra, Python",
  },
  {
    label: "🚀 JEE (PCM)",
    subs: "Mathematics, Physics, Chemistry",
  },
  {
    label: "🧬 NEET (PCB)",
    subs: "Biology, Chemistry, Physics",
  },
  {
    label: "📐 Class 12 Boards",
    subs: "Mathematics, Physics, Chemistry, English",
  },
];

export default function ScheduleTab({
  initialDays = 180,
  initialHours = 3.0,
  initialSubjects = "Data Structures & Algorithms, Linear Algebra, Python",
}: ScheduleTabProps) {
  const [days, setDays] = useState(initialDays);
  const [hours, setHours] = useState(initialHours);
  const [subs, setSubs] = useState(initialSubjects);
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [viewMode, setViewMode] = useState<"timeline" | "timer" | "distribution">("timeline");
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  // Focus / Pomodoro Timer State
  const [activeTimerTask, setActiveTimerTask] = useState<StudyPlanTask | null>(null);
  const [timeLeftSeconds, setTimeLeftSeconds] = useState<number>(25 * 60);
  const [timerRunning, setTimerRunning] = useState<boolean>(false);

  // Custom Task Inline Form
  const [showAddCustom, setShowAddCustom] = useState<boolean>(false);
  const [customTitle, setCustomTitle] = useState<string>("");
  const [customSubject, setCustomSubject] = useState<string>("");
  const [customMinutes, setCustomMinutes] = useState<number>(30);

  const showToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(null), 3000);
  };

  // Timer Tick
  useEffect(() => {
    let interval: any = null;
    if (timerRunning && timeLeftSeconds > 0) {
      interval = setInterval(() => {
        setTimeLeftSeconds((prev) => prev - 1);
      }, 1000);
    } else if (timeLeftSeconds === 0 && timerRunning) {
      setTimerRunning(false);
      showToast("🎉 Block finished! Great work on this session.");
    }
    return () => clearInterval(interval);
  }, [timerRunning, timeLeftSeconds]);

  const handleStartFocus = (task: StudyPlanTask) => {
    setActiveTimerTask(task);
    setTimeLeftSeconds(task.duration_minutes * 60);
    setTimerRunning(true);
    setViewMode("timer");
    showToast(`⏱️ Started Focus Session: ${task.title}`);
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const generated = await api.generatePlan(days, hours, subs);
      setPlan(generated);
      showToast("✨ Adaptive schedule synthesized successfully!");
    } catch (e: any) {
      alert(`Failed to generate schedule: ${e.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleToggle = async (taskId: string, currentCompleted: boolean) => {
    if (!plan) return;
    try {
      await api.toggleTask(plan.id, taskId, !currentCompleted);
      setPlan({
        ...plan,
        tasks: plan.tasks.map((t) =>
          t.id === taskId ? { ...t, completed: !currentCompleted } : t
        ),
      });
      if (!currentCompleted) {
        showToast("✅ Task marked as completed!");
      }
    } catch (e: any) {
      console.error(e);
    }
  };

  const handleAddCustomTask = () => {
    if (!customTitle.trim()) return;
    if (!plan) return;
    const newTask: StudyPlanTask = {
      id: `task_custom_${Date.now().toString(36)}`,
      type: "custom",
      subject: customSubject.trim() || (plan.subjects[0] || "General"),
      title: customTitle.trim(),
      description: "Custom study or review session added manually.",
      duration_minutes: Number(customMinutes) || 30,
      completed: false,
      reason: "Self-directed student target.",
      category: "Custom Session",
      priority: "Medium",
      time_slot: "Flexible Slot",
      suggested_method: "Independent Practice",
    };
    setPlan({
      ...plan,
      tasks: [...plan.tasks, newTask],
    });
    setCustomTitle("");
    setShowAddCustom(false);
    showToast("➕ Custom study block added to today's plan!");
  };

  // Stats Calculations
  const stats = useMemo(() => {
    if (!plan || !plan.tasks.length) {
      return { total: 0, completed: 0, percent: 0, totalMinutes: 0 };
    }
    const total = plan.tasks.length;
    const completed = plan.tasks.filter((t) => t.completed).length;
    const totalMinutes = plan.tasks.reduce((sum, t) => sum + (t.duration_minutes || 0), 0);
    const percent = Math.round((completed / total) * 100);
    return { total, completed, percent, totalMinutes };
  }, [plan]);

  // Subject Breakdown for Distribution View
  const subjectDistribution = useMemo(() => {
    if (!plan || !plan.tasks.length) return [];
    const map: Record<string, number> = {};
    plan.tasks.forEach((t) => {
      const s = t.subject || "General";
      map[s] = (map[s] || 0) + (t.duration_minutes || 0);
    });
    const total = Object.values(map).reduce((a, b) => a + b, 0) || 1;
    return Object.entries(map).map(([sub, mins]) => ({
      subject: sub,
      minutes: mins,
      percentage: Math.round((mins / total) * 100),
    }));
  }, [plan]);

  // Copy Plan as Markdown
  const handleCopyMarkdown = () => {
    if (!plan) return;
    const text = [
      `# 📅 Mentor Mate Daily Study Schedule`,
      `Target Exam in: ${days} days | Daily Target: ${hours} hours (${stats.totalMinutes} mins)`,
      `Subjects: ${subs}`,
      ``,
      ...plan.tasks.map((t, idx) => {
        const check = t.completed ? "[x]" : "[ ]";
        const slot = t.time_slot ? ` (${t.time_slot})` : "";
        return `${idx + 1}. ${check} **${t.title}**${slot} — ${t.duration_minutes}m [${t.subject}]\n   *Description*: ${t.description}\n   *Why*: ${t.reason}\n`;
      }),
    ].join("\n");

    navigator.clipboard.writeText(text).then(() => {
      showToast("📋 Schedule copied to clipboard in markdown format!");
    });
  };

  // Export .ICS Calendar File
  const handleExportICS = () => {
    if (!plan) return;
    const now = new Date();
    const pad = (n: number) => (n < 10 ? "0" + n : "" + n);
    const formatDate = (d: Date) =>
      `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}T${pad(d.getHours())}${pad(d.getMinutes())}00Z`;

    let cursor = new Date();
    cursor.setHours(9, 0, 0, 0); // Start at 9am today

    let icsContent = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//Mentor Mate//Adaptive Study Planner//EN",
      "CALSCALE:GREGORIAN",
    ];

    plan.tasks.forEach((t, i) => {
      const start = new Date(cursor);
      const end = new Date(cursor.getTime() + t.duration_minutes * 60000);
      cursor = new Date(end.getTime() + 10 * 60000); // 10 min break

      icsContent.push(
        "BEGIN:VEVENT",
        `UID:mentormate-${Date.now()}-${i}@mentormate.ai`,
        `DTSTAMP:${formatDate(now)}`,
        `DTSTART:${formatDate(start)}`,
        `DTEND:${formatDate(end)}`,
        `SUMMARY:Mentor Mate: ${t.title} [${t.subject}]`,
        `DESCRIPTION:${t.description}\\n\\nPedagogical Reason: ${t.reason}`,
        "STATUS:CONFIRMED",
        "END:VEVENT"
      );
    });

    icsContent.push("END:VCALENDAR");

    const blob = new Blob([icsContent.join("\r\n")], { type: "text/calendar;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `MentorMate_StudySchedule_${now.toISOString().slice(0, 10)}.ics`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("📥 Calendar (.ics) file downloaded successfully!");
  };

  const formatTimer = (sec: number) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m < 10 ? "0" + m : m}:${s < 10 ? "0" + s : s}`;
  };

  const getCategoryBadgeStyle = (category?: string, type?: string) => {
    const c = (category || type || "").toLowerCase();
    if (c.includes("warm") || c.includes("recall")) {
      return { background: "rgba(245, 158, 11, 0.12)", color: "#f59e0b", border: "1px solid rgba(245, 158, 11, 0.3)" };
    }
    if (c.includes("deep") || c.includes("core")) {
      return { background: "rgba(99, 102, 241, 0.12)", color: "#6366f1", border: "1px solid rgba(99, 102, 241, 0.3)" };
    }
    if (c.includes("drill") || c.includes("practice") || c.includes("secondary")) {
      return { background: "rgba(14, 165, 233, 0.12)", color: "#0ea5e9", border: "1px solid rgba(14, 165, 233, 0.3)" };
    }
    if (c.includes("spaced") || c.includes("review") || c.includes("retrieval")) {
      return { background: "rgba(16, 185, 129, 0.12)", color: "#10b981", border: "1px solid rgba(16, 185, 129, 0.3)" };
    }
    return { background: "rgba(148, 163, 184, 0.12)", color: "var(--muted)", border: "1px solid var(--border)" };
  };

  return (
    <div id="panel-schedule" className="card" style={{ padding: "20px" }}>
      {/* Toast Notification Banner */}
      {toastMsg && (
        <div
          style={{
            position: "fixed",
            bottom: "24px",
            right: "24px",
            zIndex: 9999,
            background: "var(--card-elevated, #1f2b48)",
            color: "var(--text, #fff)",
            padding: "12px 20px",
            borderRadius: "12px",
            boxShadow: "0 10px 25px rgba(0,0,0,0.3)",
            border: "1px solid var(--accent, #38bdf8)",
            fontWeight: 600,
            fontSize: "14px",
            animation: "fadeIn 0.2s ease-in-out",
          }}
        >
          {toastMsg}
        </div>
      )}

      {/* Header & Preset Bar */}
      <div style={{ marginBottom: "16px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "12px" }}>
          <div>
            <h2 style={{ fontSize: "22px", fontWeight: 800, margin: "0 0 4px 0", color: "var(--text-heading)" }}>
              📅 Adaptive Daily Study Planner
            </h2>
            <p style={{ margin: 0, color: "var(--muted)", fontSize: "13px" }}>
              Constraint-optimized allocations matching your Ebbinghaus memory curve, diagnostic weaknesses, and exam horizon.
            </p>
          </div>

          {/* Quick Preset Buttons */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", alignItems: "center" }}>
            <span style={{ fontSize: "12px", fontWeight: 700, color: "var(--muted)", marginRight: "4px" }}>
              Presets:
            </span>
            {PRESETS.map((p) => (
              <button
                key={p.label}
                type="button"
                className="btn small"
                style={{
                  padding: "4px 10px",
                  fontSize: "12px",
                  borderRadius: "20px",
                  background: subs === p.subs ? "var(--brand, #4f46e5)" : "var(--card-subtle, #f1f5f9)",
                  color: subs === p.subs ? "#ffffff" : "var(--text)",
                  border: "1px solid var(--border)",
                  cursor: "pointer",
                }}
                onClick={() => setSubs(p.subs)}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* Input Parameters Row */}
        <div className="grid-3 row" style={{ marginTop: "16px", gap: "12px" }}>
          <div>
            <label style={{ fontSize: "13px", fontWeight: 700, display: "block", marginBottom: "4px" }}>
              ⏳ Days until exam
            </label>
            <input
              id="sDays"
              type="number"
              min="7"
              className="input"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              style={{ width: "100%", padding: "8px 12px", borderRadius: "8px" }}
            />
          </div>
          <div>
            <label style={{ fontSize: "13px", fontWeight: 700, display: "block", marginBottom: "4px" }}>
              ⏱️ Daily target hours
            </label>
            <input
              id="sHours"
              type="number"
              min="1"
              max="12"
              step="0.5"
              className="input"
              value={hours}
              onChange={(e) => setHours(Number(e.target.value))}
              style={{ width: "100%", padding: "8px 12px", borderRadius: "8px" }}
            />
          </div>
          <div>
            <label style={{ fontSize: "13px", fontWeight: 700, display: "block", marginBottom: "4px" }}>
              🎯 Target Subjects (comma separated)
            </label>
            <input
              id="sSubs"
              className="input"
              placeholder="e.g. Data Structures & Algorithms, Linear Algebra, Python"
              value={subs}
              onChange={(e) => setSubs(e.target.value)}
              style={{ width: "100%", padding: "8px 12px", borderRadius: "8px" }}
            />
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", marginTop: "12px", gap: "8px" }}>
          <button
            className="btn"
            onClick={handleGenerate}
            disabled={isGenerating}
            style={{
              background: "linear-gradient(135deg, var(--brand, #4f46e5), var(--accent, #0284c7))",
              color: "#fff",
              fontWeight: 700,
              padding: "10px 22px",
              borderRadius: "10px",
              border: "none",
              cursor: isGenerating ? "not-allowed" : "pointer",
              boxShadow: "0 4px 14px rgba(79, 70, 229, 0.35)",
            }}
          >
            {isGenerating ? "⚡ Synthesizing Adaptive Schedule..." : "✨ Generate Today's Optimized Plan"}
          </button>
        </div>
      </div>

      {/* Plan Dashboard */}
      {plan && (
        <div style={{ marginTop: "20px", borderTop: "1px solid var(--border)", paddingTop: "16px" }}>
          {/* Stats Bar & Progress */}
          <div
            style={{
              background: "var(--card-subtle, rgba(255, 255, 255, 0.04))",
              borderRadius: "14px",
              padding: "14px 18px",
              marginBottom: "16px",
              border: "1px solid var(--border)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <span style={{ fontSize: "16px", fontWeight: 800 }}>Daily Progress</span>
                <span
                  style={{
                    background: stats.percent === 100 ? "rgba(16, 185, 129, 0.15)" : "rgba(79, 70, 229, 0.15)",
                    color: stats.percent === 100 ? "#10b981" : "var(--brand)",
                    padding: "3px 10px",
                    borderRadius: "12px",
                    fontWeight: 800,
                    fontSize: "13px",
                  }}
                >
                  {stats.completed} of {stats.total} Tasks Completed ({stats.percent}%)
                </span>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span className="badge" style={{ color: "var(--accent)" }}>
                  ⏳ {days} days to exam
                </span>
                <span className="badge" style={{ color: "#10b981" }}>
                  ⏱️ {hours}h target ({stats.totalMinutes}m planned)
                </span>
              </div>
            </div>

            {/* Visual Animated Progress Bar */}
            <div
              style={{
                width: "100%",
                height: "8px",
                background: "var(--border, #e2e8f0)",
                borderRadius: "4px",
                overflow: "hidden",
                marginTop: "10px",
              }}
            >
              <div
                style={{
                  width: `${stats.percent}%`,
                  height: "100%",
                  background:
                    stats.percent === 100
                      ? "linear-gradient(90deg, #10b981, #34d399)"
                      : "linear-gradient(90deg, var(--brand, #4f46e5), var(--accent, #0284c7))",
                  borderRadius: "4px",
                  transition: "width 0.4s ease",
                }}
              />
            </div>
          </div>

          {/* View Mode Switcher & Quick Actions */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "16px",
              flexWrap: "wrap",
              gap: "10px",
            }}
          >
            {/* View Switcher Pills */}
            <div style={{ display: "flex", gap: "6px" }}>
              <button
                className="btn small"
                style={{
                  background: viewMode === "timeline" ? "var(--brand, #4f46e5)" : "transparent",
                  color: viewMode === "timeline" ? "#fff" : "var(--text)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  fontWeight: 700,
                  fontSize: "13px",
                  padding: "6px 14px",
                  cursor: "pointer",
                }}
                onClick={() => setViewMode("timeline")}
              >
                📋 Timeline View
              </button>
              <button
                className="btn small"
                style={{
                  background: viewMode === "timer" ? "var(--brand, #4f46e5)" : "transparent",
                  color: viewMode === "timer" ? "#fff" : "var(--text)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  fontWeight: 700,
                  fontSize: "13px",
                  padding: "6px 14px",
                  cursor: "pointer",
                }}
                onClick={() => setViewMode("timer")}
              >
                ⏱️ Focus Pomodoro Timer
              </button>
              <button
                className="btn small"
                style={{
                  background: viewMode === "distribution" ? "var(--brand, #4f46e5)" : "transparent",
                  color: viewMode === "distribution" ? "#fff" : "var(--text)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  fontWeight: 700,
                  fontSize: "13px",
                  padding: "6px 14px",
                  cursor: "pointer",
                }}
                onClick={() => setViewMode("distribution")}
              >
                📊 Subject Allocation
              </button>
            </div>

            {/* Utility Buttons */}
            <div style={{ display: "flex", gap: "8px" }}>
              <button
                className="btn small"
                style={{ borderRadius: "8px", padding: "6px 12px", fontSize: "12px", border: "1px solid var(--border)" }}
                onClick={handleCopyMarkdown}
                title="Copy schedule as formatted Markdown"
              >
                📋 Copy Schedule
              </button>
              <button
                className="btn small"
                style={{ borderRadius: "8px", padding: "6px 12px", fontSize: "12px", border: "1px solid var(--border)" }}
                onClick={handleExportICS}
                title="Download .ics file for Google Calendar or Apple Calendar"
              >
                📥 Export to Calendar (.ics)
              </button>
              <button
                className="btn small"
                style={{
                  borderRadius: "8px",
                  padding: "6px 12px",
                  fontSize: "12px",
                  border: "1px solid var(--accent)",
                  color: "var(--accent)",
                }}
                onClick={() => setShowAddCustom(!showAddCustom)}
              >
                ➕ Add Custom Block
              </button>
            </div>
          </div>

          {/* Inline Add Custom Task Form */}
          {showAddCustom && (
            <div
              style={{
                background: "var(--card-subtle, rgba(255, 255, 255, 0.05))",
                border: "1px dashed var(--accent, #38bdf8)",
                borderRadius: "12px",
                padding: "14px",
                marginBottom: "16px",
              }}
            >
              <h4 style={{ margin: "0 0 10px 0", fontSize: "14px", fontWeight: 700 }}>
                Add Custom Study or Break Session
              </h4>
              <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignItems: "center" }}>
                <input
                  className="input"
                  placeholder="Task title (e.g., LeetCode 2 Mediums or Math Mock Test)"
                  value={customTitle}
                  onChange={(e) => setCustomTitle(e.target.value)}
                  style={{ flex: 2, minWidth: "200px", padding: "8px 12px", borderRadius: "8px" }}
                />
                <input
                  className="input"
                  placeholder="Subject (e.g., Python / Calculus)"
                  value={customSubject}
                  onChange={(e) => setCustomSubject(e.target.value)}
                  style={{ flex: 1, minWidth: "140px", padding: "8px 12px", borderRadius: "8px" }}
                />
                <input
                  className="input"
                  type="number"
                  min="5"
                  max="180"
                  step="5"
                  value={customMinutes}
                  onChange={(e) => setCustomMinutes(Number(e.target.value))}
                  style={{ width: "90px", padding: "8px 12px", borderRadius: "8px" }}
                />
                <span style={{ fontSize: "12px", color: "var(--muted)" }}>mins</span>
                <button
                  className="btn"
                  onClick={handleAddCustomTask}
                  style={{
                    background: "var(--accent, #0284c7)",
                    color: "#fff",
                    fontWeight: 700,
                    padding: "8px 16px",
                    borderRadius: "8px",
                  }}
                >
                  Add Block
                </button>
                <button
                  className="btn small"
                  onClick={() => setShowAddCustom(false)}
                  style={{ border: "none", background: "transparent", color: "var(--muted)" }}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* VIEW 1: TIMELINE VIEW */}
          {viewMode === "timeline" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {plan.tasks.map((task, index) => {
                const badgeStyle = getCategoryBadgeStyle(task.category, task.type);
                return (
                  <div
                    key={task.id}
                    style={{
                      background: task.completed
                        ? "var(--card-subtle, rgba(255, 255, 255, 0.02))"
                        : "var(--card-elevated, #ffffff)",
                      border: task.completed
                        ? "1px solid rgba(16, 185, 129, 0.3)"
                        : "1px solid var(--border)",
                      borderRadius: "14px",
                      padding: "16px 20px",
                      boxShadow: task.completed ? "none" : "var(--shadow)",
                      opacity: task.completed ? 0.75 : 1.0,
                      transition: "all 0.2s ease",
                      position: "relative",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "flex-start", gap: "14px" }}>
                      {/* Checkbox */}
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => handleToggle(task.id, task.completed)}
                        style={{
                          cursor: "pointer",
                          width: "20px",
                          height: "20px",
                          marginTop: "3px",
                          accentColor: "#10b981",
                        }}
                        id={`chk_${task.id}`}
                      />

                      {/* Main Task Info */}
                      <div style={{ flex: 1 }}>
                        {/* Header Badges Row */}
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            flexWrap: "wrap",
                            marginBottom: "6px",
                          }}
                        >
                          {/* Chronological Time Slot */}
                          {task.time_slot && (
                            <span
                              style={{
                                fontSize: "12px",
                                fontWeight: 700,
                                background: "rgba(56, 189, 248, 0.12)",
                                color: "var(--accent, #0284c7)",
                                padding: "2px 8px",
                                borderRadius: "6px",
                                border: "1px solid rgba(56, 189, 248, 0.25)",
                              }}
                            >
                              🕒 {task.time_slot}
                            </span>
                          )}

                          {/* Category Badge */}
                          <span
                            style={{
                              fontSize: "12px",
                              fontWeight: 700,
                              padding: "2px 8px",
                              borderRadius: "6px",
                              ...badgeStyle,
                            }}
                          >
                            {task.category || task.type}
                          </span>

                          {/* Subject Pill */}
                          <span
                            style={{
                              fontSize: "12px",
                              fontWeight: 600,
                              background: "var(--card-subtle, #f1f5f9)",
                              color: "var(--text)",
                              padding: "2px 8px",
                              borderRadius: "6px",
                              border: "1px solid var(--border)",
                            }}
                          >
                            📚 {task.subject}
                          </span>

                          {/* Duration Badge */}
                          <span className="badge small" style={{ fontWeight: 700 }}>
                            ⏱️ {task.duration_minutes} mins
                          </span>

                          {/* Priority */}
                          {task.priority && (
                            <span
                              style={{
                                fontSize: "11px",
                                fontWeight: 800,
                                color: task.priority === "Essential" ? "#ef4444" : "#f59e0b",
                                textTransform: "uppercase",
                                letterSpacing: "0.5px",
                              }}
                            >
                              {task.priority}
                            </span>
                          )}
                        </div>

                        {/* Title */}
                        <label
                          htmlFor={`chk_${task.id}`}
                          style={{
                            display: "block",
                            fontSize: "16px",
                            fontWeight: 800,
                            color: "var(--text-heading)",
                            textDecoration: task.completed ? "line-through" : "none",
                            cursor: "pointer",
                            marginBottom: "6px",
                          }}
                        >
                          {index + 1}. {task.title}
                        </label>

                        {/* Actionable Description */}
                        <div style={{ fontSize: "14px", color: "var(--text)", lineHeight: 1.5, marginBottom: "8px" }}>
                          {task.description}
                        </div>

                        {/* Pedagogical Reason / Why */}
                        <div
                          style={{
                            fontSize: "12px",
                            background: "rgba(79, 70, 229, 0.05)",
                            color: "var(--muted)",
                            padding: "6px 12px",
                            borderRadius: "8px",
                            borderLeft: "3px solid var(--brand, #4f46e5)",
                            display: "flex",
                            alignItems: "center",
                            gap: "6px",
                          }}
                        >
                          <span>💡 <em>{task.reason}</em></span>
                          {task.suggested_method && (
                            <span style={{ marginLeft: "auto", fontWeight: 700, color: "var(--brand)" }}>
                              Strategy: {task.suggested_method}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Quick Action: Start Focus Timer */}
                      <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                        <button
                          className="btn small"
                          style={{
                            background: "var(--card-subtle, #f1f5f9)",
                            border: "1px solid var(--border)",
                            borderRadius: "8px",
                            fontSize: "12px",
                            padding: "6px 10px",
                            whiteSpace: "nowrap",
                            fontWeight: 700,
                          }}
                          onClick={() => handleStartFocus(task)}
                          title="Launch built-in focus timer for this block"
                        >
                          ⏱️ Focus
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* VIEW 2: BUILT-IN POMODORO / FOCUS TIMER VIEW */}
          {viewMode === "timer" && (
            <div
              style={{
                background: "var(--card-elevated, #131b2e)",
                borderRadius: "16px",
                padding: "32px 24px",
                textAlign: "center",
                border: "1px solid var(--border)",
                maxWidth: "600px",
                margin: "0 auto",
                boxShadow: "var(--shadow)",
              }}
            >
              <span
                style={{
                  fontSize: "12px",
                  fontWeight: 800,
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                  color: "var(--accent, #38bdf8)",
                }}
              >
                Deep Focus Session
              </span>

              <h3 style={{ fontSize: "20px", fontWeight: 800, margin: "8px 0 4px 0", color: "var(--text-heading)" }}>
                {activeTimerTask ? activeTimerTask.title : plan.tasks[0]?.title || "Study Block"}
              </h3>
              <p style={{ color: "var(--muted)", fontSize: "14px", margin: "0 0 24px 0" }}>
                {activeTimerTask ? activeTimerTask.subject : plan.tasks[0]?.subject} •{" "}
                {activeTimerTask ? activeTimerTask.time_slot : "Active Block"}
              </p>

              {/* Digital Countdown Timer Display */}
              <div
                style={{
                  fontSize: "64px",
                  fontWeight: 900,
                  fontFamily: "monospace",
                  letterSpacing: "4px",
                  color: timerRunning ? "var(--brand, #6366f1)" : "var(--text)",
                  margin: "12px 0 24px 0",
                  textShadow: timerRunning ? "0 0 20px rgba(99, 102, 241, 0.4)" : "none",
                }}
              >
                {formatTimer(timeLeftSeconds)}
              </div>

              {/* Timer Control Buttons */}
              <div style={{ display: "flex", justifyContent: "center", gap: "12px", flexWrap: "wrap" }}>
                <button
                  className="btn"
                  onClick={() => setTimerRunning(!timerRunning)}
                  style={{
                    background: timerRunning ? "#ef4444" : "var(--ok, #10b981)",
                    color: "#fff",
                    fontWeight: 800,
                    padding: "10px 28px",
                    borderRadius: "12px",
                    fontSize: "16px",
                    border: "none",
                    cursor: "pointer",
                  }}
                >
                  {timerRunning ? "⏸️ Pause Session" : "▶️ Start Focus"}
                </button>

                <button
                  className="btn"
                  onClick={() => {
                    setTimerRunning(false);
                    setTimeLeftSeconds((activeTimerTask?.duration_minutes || 25) * 60);
                  }}
                  style={{
                    background: "var(--card-subtle, #1a243d)",
                    color: "var(--text)",
                    border: "1px solid var(--border)",
                    fontWeight: 700,
                    borderRadius: "12px",
                    padding: "10px 18px",
                  }}
                >
                  🔄 Reset
                </button>

                <button
                  className="btn"
                  onClick={() => setTimeLeftSeconds((prev) => prev + 5 * 60)}
                  style={{
                    background: "var(--card-subtle, #1a243d)",
                    color: "var(--text)",
                    border: "1px solid var(--border)",
                    fontWeight: 700,
                    borderRadius: "12px",
                    padding: "10px 18px",
                  }}
                >
                  +5 Mins
                </button>

                {activeTimerTask && (
                  <button
                    className="btn"
                    onClick={() => {
                      handleToggle(activeTimerTask.id, false);
                      setTimerRunning(false);
                      showToast("🎉 Session marked completed!");
                    }}
                    style={{
                      background: "rgba(16, 185, 129, 0.2)",
                      color: "#10b981",
                      border: "1px solid #10b981",
                      fontWeight: 700,
                      borderRadius: "12px",
                      padding: "10px 18px",
                    }}
                  >
                    ✅ Complete Block
                  </button>
                )}
              </div>

              {/* Task Quick Selector */}
              <div style={{ marginTop: "28px", textAlign: "left", borderTop: "1px solid var(--border)", paddingTop: "16px" }}>
                <span style={{ fontSize: "12px", fontWeight: 700, color: "var(--muted)", display: "block", marginBottom: "8px" }}>
                  Switch Active Block:
                </span>
                <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                  {plan.tasks.map((t) => (
                    <button
                      key={t.id}
                      className="btn small"
                      onClick={() => handleStartFocus(t)}
                      style={{
                        background: activeTimerTask?.id === t.id ? "var(--brand, #4f46e5)" : "var(--card-subtle, #1a243d)",
                        color: activeTimerTask?.id === t.id ? "#fff" : "var(--text)",
                        border: "1px solid var(--border)",
                        borderRadius: "8px",
                        fontSize: "12px",
                        padding: "6px 12px",
                      }}
                    >
                      {t.subject}: {t.duration_minutes}m
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* VIEW 3: SUBJECT ALLOCATION / ROADMAP VIEW */}
          {viewMode === "distribution" && (
            <div
              style={{
                background: "var(--card-elevated, #131b2e)",
                borderRadius: "16px",
                padding: "24px",
                border: "1px solid var(--border)",
              }}
            >
              <h3 style={{ fontSize: "18px", fontWeight: 800, margin: "0 0 4px 0", color: "var(--text-heading)" }}>
                📊 Daily Subject Allocation & Time Balance
              </h3>
              <p style={{ color: "var(--muted)", fontSize: "13px", margin: "0 0 20px 0" }}>
                Balanced distribution prevents cognitive fatigue while keeping high-yield syllabus concepts in active recall.
              </p>

              <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                {subjectDistribution.map((item) => (
                  <div key={item.subject}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px", fontSize: "14px", fontWeight: 700 }}>
                      <span>📚 {item.subject}</span>
                      <span style={{ color: "var(--brand)" }}>
                        {item.minutes} mins ({item.percentage}%)
                      </span>
                    </div>
                    <div
                      style={{
                        width: "100%",
                        height: "10px",
                        background: "var(--border)",
                        borderRadius: "5px",
                        overflow: "hidden",
                      }}
                    >
                      <div
                        style={{
                          width: `${item.percentage}%`,
                          height: "100%",
                          background: "linear-gradient(90deg, var(--brand, #4f46e5), var(--accent, #0284c7))",
                          borderRadius: "5px",
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* 7-Day Spaced Repetition Progression Preview */}
              <div style={{ marginTop: "28px", borderTop: "1px solid var(--border)", paddingTop: "16px" }}>
                <h4 style={{ margin: "0 0 8px 0", fontSize: "15px", fontWeight: 800 }}>
                  📈 7-Day Adaptive Progression Model
                </h4>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: "10px", marginTop: "12px" }}>
                  {["Day 1 (Today)", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7 (Diagnostic)"].map((dayName, idx) => (
                    <div
                      key={dayName}
                      style={{
                        background: idx === 0 ? "rgba(79, 70, 229, 0.12)" : "var(--card-subtle, rgba(255, 255, 255, 0.03))",
                        border: idx === 0 ? "1px solid var(--brand)" : "1px solid var(--border)",
                        borderRadius: "10px",
                        padding: "10px",
                        textAlign: "center",
                      }}
                    >
                      <div style={{ fontSize: "12px", fontWeight: 800, color: idx === 0 ? "var(--brand)" : "var(--text)" }}>
                        {dayName}
                      </div>
                      <div style={{ fontSize: "11px", color: "var(--muted)", marginTop: "4px" }}>
                        {idx === 0
                          ? "Current Plan"
                          : idx === 6
                          ? "Full Diagnostic"
                          : idx % 2 === 0
                          ? "Spaced Review"
                          : "Deep Derivations"}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
