"use client";

import React, { useState, useEffect } from "react";
import { api, StudentProfile, DashboardSummary, StudyMaterialItem, StudyMaterialUploadResponse } from "@/lib/api";

interface DashboardTabProps {
  profile: StudentProfile | null;
  streakDays: number;
  onMarkStudied: () => void;
  onNavigateTab: (tabKey: string) => void;
  isMarking: boolean;
}

export default function DashboardTab({
  profile,
  streakDays,
  onMarkStudied,
  onNavigateTab,
  isMarking,
}: DashboardTabProps) {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Study Material OCR & AI Guidance State
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [materialTitle, setMaterialTitle] = useState("");
  const [materialSubject, setMaterialSubject] = useState("Math");
  const [isUploadingMaterial, setIsUploadingMaterial] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [activeAnalysis, setActiveAnalysis] = useState<StudyMaterialUploadResponse | StudyMaterialItem | null>(null);
  const [materialsList, setMaterialsList] = useState<StudyMaterialItem[]>([]);
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [quizSubmitted, setQuizSubmitted] = useState<Record<number, boolean>>({});

  useEffect(() => {
    loadDashboard();
    loadStudyMaterials();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await api.getDashboardSummary();
      setSummary(data);
    } catch (e) {
      console.error("Dashboard summary load failed:", e);
    } finally {
      setIsLoading(false);
    }
  };

  const loadStudyMaterials = async () => {
    try {
      const res = await api.getStudyMaterials();
      if (res && res.materials) {
        setMaterialsList(res.materials);
        if (res.materials.length > 0 && !activeAnalysis) {
          setActiveAnalysis(res.materials[0]);
        }
      }
    } catch (e) {
      console.error("Failed to load study materials:", e);
    }
  };

  const handleMaterialFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setSelectedFile(file);
    if (file && !materialTitle) {
      const base = file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
      setMaterialTitle(base);
    }
  };

  const handleUploadMaterialSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      alert("Please select a study material or notes file (PDF, PNG, JPG, TXT, MD).");
      return;
    }

    setIsUploadingMaterial(true);
    setUploadStatus("Extracting content with OCR & analyzing curriculum concepts with AI...");
    try {
      const res = await api.uploadStudyMaterial(
        selectedFile,
        materialTitle.trim() || undefined,
        materialSubject
      );
      setActiveAnalysis(res);
      setSelectedFile(null);
      setMaterialTitle("");
      setQuizAnswers({});
      setQuizSubmitted({});
      await loadStudyMaterials();
      await loadDashboard();
      setUploadStatus(null);
    } catch (err: any) {
      setUploadStatus(null);
      alert(`Study material OCR analysis failed: ${err.message}`);
    } finally {
      setIsUploadingMaterial(false);
    }
  };

  const handleAnswerOption = (questionIdx: number, optionIdx: number) => {
    setQuizAnswers((prev) => ({ ...prev, [questionIdx]: optionIdx }));
    setQuizSubmitted((prev) => ({ ...prev, [questionIdx]: true }));
  };

  const handleGeneratePlanFromMaterial = async (subject: string) => {
    try {
      await api.generatePlan(90, 3.5, subject || "Core Curriculum");
      onNavigateTab("schedule");
    } catch (e: any) {
      alert(`Could not generate plan: ${e.message}`);
    }
  };

  const quickActionsMaster = [
    { id: "upload", text: "Upload Marksheet & Calibrate", fn: () => onNavigateTab("uploads") },
    { id: "plan", text: "Generate Personalized Plan", fn: () => onNavigateTab("schedule") },
    { id: "test", text: "Start Adaptive Diagnostic Test", fn: () => onNavigateTab("test") },
    { id: "mark", text: "Mark Today Studied", fn: onMarkStudied },
    { id: "courses", text: "Explore Curriculum Courses", fn: () => onNavigateTab("courses") },
    { id: "mentor", text: "Ask AI Pedagogical Mentor", fn: () => onNavigateTab("mentor") },
    { id: "performance", text: "View Cognitive Analytics", fn: () => onNavigateTab("performance") },
  ];

  const enabledActions = profile?.quick_actions && profile.quick_actions.length > 0
    ? quickActionsMaster.filter((q) => profile.quick_actions.includes(q.id))
    : quickActionsMaster.slice(0, 4);

  const streakPercent = Math.min(100, Math.round((streakDays / 7) * 100));
  const enrolledCourses = summary?.enrolled_courses || profile?.enrolled_courses || [];
  const todayFocus = summary?.today_focus;
  const recentEval = summary?.recent_assessment;
  const revisions = summary?.upcoming_revision || [];

  return (
    <div style={{ display: "grid", gap: "14px" }}>
      {/* Top 2-Column: Streak & Quick Actions */}
      <div id="panel-dashboard" className="card grid-2">
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontWeight: 800 }}>Streak</div>
              <div className="subtitle">Days studied this week</div>
            </div>
            <div className="pill" id="streakPill">
              {streakDays} 🔥
            </div>
          </div>
          <div className="hr"></div>
          <div className="progress">
            <div id="streakBar" style={{ width: `${streakPercent}%` }}></div>
          </div>
          <div className="right" style={{ marginTop: "8px" }}>
            <button className="btn small" onClick={onMarkStudied} disabled={isMarking}>
              {isMarking ? "Marking..." : "Mark Today Studied"}
            </button>
          </div>

          {/* Daily Schedule & Revision Queue Section */}
          <div style={{ marginTop: "18px", paddingTop: "14px", borderTop: "1px solid #e2e8f0" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
              <div style={{ fontWeight: 800, fontSize: "14px", display: "flex", alignItems: "center", gap: "6px" }}>
                <span>📅</span>
                <span>Today&apos;s Schedule &amp; Revision</span>
              </div>
              <button
                className="btn small secondary"
                style={{ fontSize: "11.5px", padding: "3px 8px" }}
                onClick={() => onNavigateTab("schedule")}
              >
                Planner →
              </button>
            </div>

            {/* If revisions are due */}
            {revisions && revisions.length > 0 ? (
              <div style={{ display: "grid", gap: "8px" }}>
                {revisions.slice(0, 2).map((rev, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: "#f8fafc",
                      border: "1px solid #e2e8f0",
                      borderRadius: "10px",
                      padding: "10px 12px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 700, fontSize: "13px", color: "var(--text-heading)" }}>{rev.title}</div>
                      <div className="small note" style={{ marginTop: "2px" }}>
                        {rev.subject} • Retention: <strong style={{ color: rev.retention_percent < 50 ? "var(--danger)" : "var(--accent)" }}>{rev.retention_percent}%</strong>
                      </div>
                    </div>
                    <button
                      className="btn small"
                      style={{ padding: "4px 10px", fontSize: "12px" }}
                      onClick={() => onNavigateTab("test")}
                    >
                      Revise ▶
                    </button>
                  </div>
                ))}
              </div>
            ) : summary?.current_plan?.tasks && summary.current_plan.tasks.some((t) => !t.completed) ? (
              /* If study plan tasks exist */
              <div style={{ display: "grid", gap: "8px" }}>
                {summary.current_plan.tasks
                  .filter((t) => !t.completed)
                  .slice(0, 2)
                  .map((task, idx) => (
                    <div
                      key={idx}
                      style={{
                        background: "var(--card-subtle)",
                        border: "1px solid var(--border)",
                        borderRadius: "10px",
                        padding: "10px 12px",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: 700, fontSize: "13px", color: "var(--text-heading)" }}>{task.title}</div>
                        <div className="small note" style={{ marginTop: "2px" }}>
                          {task.subject} • {task.duration_minutes} mins
                        </div>
                      </div>
                      <button
                        className="btn small secondary"
                        style={{ padding: "4px 10px", fontSize: "12px" }}
                        onClick={() => onNavigateTab("schedule")}
                      >
                        Start ▶
                      </button>
                    </div>
                  ))}
              </div>
            ) : (
              /* If neither exist yet (clean, inviting prompt that balances height) */
              <div
                style={{
                  background: "rgba(99, 102, 241, 0.04)",
                  border: "1px dashed rgba(99, 102, 241, 0.22)",
                  borderRadius: "10px",
                  padding: "12px 14px",
                }}
              >
                <div style={{ fontSize: "12.5px", color: "var(--muted)", lineHeight: "1.5", marginBottom: "10px" }}>
                  Active revision queue and daily schedule adjust automatically as you complete study modules.
                </div>
                <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                  <button
                    className="btn small"
                    onClick={() => onNavigateTab("schedule")}
                    style={{ fontSize: "12px", padding: "5px 10px" }}
                  >
                    Open Daily Schedule ▶
                  </button>
                  <button
                    className="btn small secondary"
                    onClick={() => onNavigateTab("test")}
                    style={{ fontSize: "12px", padding: "5px 10px" }}
                  >
                    Start Quick Test ▶
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ fontWeight: 800 }}>Quick Actions</div>
            <div className="small note">Personalized Shortcuts</div>
          </div>
          <div className="hr"></div>
          <ul className="list" id="quickActionsList">
            {enabledActions.map((action) => (
              <li key={action.id}>
                <span>{action.text}</span>
                <button className="btn small" onClick={action.fn}>
                  Go
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Dynamic Evidence-Driven Today's Focus Card */}
      {todayFocus && (
        <div
          className="card"
          style={{
            background: "linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(14, 165, 233, 0.1) 100%)",
            border: "1.5px solid var(--border)",
            padding: "18px 20px"
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px" }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ fontSize: "20px" }}>🎯</span>
                <span style={{ fontWeight: 800, fontSize: "16px", color: "var(--text-heading)" }}>
                  Today&apos;s Priority Focus: {todayFocus.title}
                </span>
                <span
                  style={{
                    fontSize: "11px",
                    fontWeight: 700,
                    padding: "2px 8px",
                    borderRadius: "999px",
                    background: todayFocus.has_evidence ? "rgba(239, 68, 68, 0.15)" : "rgba(100, 116, 139, 0.15)",
                    color: todayFocus.has_evidence ? "var(--danger)" : "var(--muted)"
                  }}
                >
                  {todayFocus.subject} • {todayFocus.has_evidence ? `Mastery: ${todayFocus.mastery_percent}%` : "Calibration Needed"}
                </span>
                {todayFocus.basis_source && (
                  <span
                    style={{
                      fontSize: "11px",
                      fontWeight: 700,
                      padding: "2px 8px",
                      borderRadius: "999px",
                      background: "rgba(56, 189, 248, 0.14)",
                      color: "var(--accent)",
                      border: "1px solid rgba(56, 189, 248, 0.3)"
                    }}
                  >
                    Source: {todayFocus.basis_source}
                  </span>
                )}
              </div>
              <div style={{ marginTop: "8px", fontSize: "13.5px", color: "var(--text)", lineHeight: "1.5" }}>
                <strong>Why this is prioritized:</strong> {todayFocus.why}
              </div>
              <div style={{ marginTop: "4px", fontSize: "13px", color: "var(--accent)", fontWeight: 600 }}>
                💡 <strong>Recommended Action:</strong> {todayFocus.next_action}
              </div>
            </div>

            <div style={{ display: "flex", gap: "8px" }}>
              <button
                className="btn small"
                style={{ background: "#4f46e5", color: "#ffffff", fontWeight: 700 }}
                onClick={() => onNavigateTab(todayFocus.has_evidence ? "mentor" : "test")}
              >
                {todayFocus.has_evidence ? "Ask Socratic Mentor ▶" : "Start Diagnostic ▶"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/* 📑 STUDY MATERIAL & NOTES AI OCR & PERSONALIZED GUIDANCE CARD */}
      {/* ============================================================ */}
      <div className="card" style={{ background: "var(--card)", border: "1.5px solid var(--border)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ fontSize: "20px" }}>📑</span>
              <span style={{ fontWeight: 800, fontSize: "16px", color: "var(--text-heading)" }}>
                Upload Study Material & Notes (AI OCR & Document Intelligence)
              </span>
              <span className="pill small" style={{ background: "rgba(2, 132, 199, 0.12)", color: "var(--accent)", fontWeight: 700 }}>
                Live OCR Enabled
              </span>
            </div>
            <div className="subtitle" style={{ marginTop: "4px" }}>
              Upload your handwritten lecture notes, PDF textbook chapters, or question sheets. AI OCR extracts formulas, concepts, and synthesizes your personalized study guidance, custom diagnostic quiz, and course modules.
            </div>
          </div>
          {materialsList.length > 0 && (
            <span className="pill small" style={{ background: "var(--card-subtle)", color: "var(--muted)" }}>
              {materialsList.length} Material{materialsList.length > 1 ? "s" : ""} Indexed
            </span>
          )}
        </div>

        <div className="hr"></div>

        {/* Upload Form */}
        <form onSubmit={handleUploadMaterialSubmit} style={{ display: "grid", gap: "12px" }}>
          <div style={{ display: "grid", gap: "10px", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))" }}>
            <div>
              <label htmlFor="materialFile" style={{ fontSize: "12.5px", fontWeight: 600 }}>
                Select Notes / Material File (PDF, Image, or Text)
              </label>
              <input
                id="materialFile"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.webp,.txt,.md"
                onChange={handleMaterialFileChange}
                className="input"
                style={{ padding: "7px 10px" }}
              />
            </div>

            <div>
              <label htmlFor="materialTitle" style={{ fontSize: "12.5px", fontWeight: 600 }}>
                Document / Chapter Title (Optional)
              </label>
              <input
                id="materialTitle"
                type="text"
                placeholder="Enter document title or chapter name"
                value={materialTitle}
                onChange={(e) => setMaterialTitle(e.target.value)}
                className="input"
              />
            </div>

            <div>
              <label htmlFor="materialSubject" style={{ fontSize: "12.5px", fontWeight: 600 }}>
                Academic Subject
              </label>
              <select
                id="materialSubject"
                value={materialSubject}
                onChange={(e) => setMaterialSubject(e.target.value)}
                className="input"
              >
                <option value="Math">Mathematics / Quantitative</option>
                <option value="Physics">Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Biology">Biology / Pre-Med</option>
                <option value="Computer Science">Computer Science & DSA</option>
                <option value="Engineering Mathematics">Engineering Mathematics</option>
                <option value="General">General / Other Track</option>
              </select>
            </div>
          </div>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
            <div style={{ fontSize: "12px", color: "#64748b" }}>
              Supported: PDF documents, JPG/PNG camera snaps of handwritten notes, and TXT/MD files.
            </div>
            <button
              type="submit"
              className="btn"
              disabled={isUploadingMaterial || !selectedFile}
              style={{ fontWeight: 700, padding: "8px 18px", fontSize: "13.5px" }}
            >
              {isUploadingMaterial ? "Analyzing with AI OCR..." : "⚡ Analyze Notes & Generate Personalized Guidance"}
            </button>
          </div>

          {uploadStatus && (
            <div style={{ padding: "10px 14px", borderRadius: "8px", background: "rgba(56, 189, 248, 0.12)", border: "1px solid rgba(56, 189, 248, 0.25)", fontSize: "13px", color: "var(--accent)", display: "flex", alignItems: "center", gap: "8px" }}>
              <span>🔄</span>
              <span>{uploadStatus}</span>
            </div>
          )}
        </form>

        {/* Previous Materials Selector Tabs (if multiple) */}
        {materialsList.length > 1 && (
          <div style={{ marginTop: "14px", display: "flex", alignItems: "center", gap: "6px", overflowX: "auto", paddingBottom: "4px" }}>
            <span style={{ fontSize: "11.5px", fontWeight: 700, color: "var(--muted)", whiteSpace: "nowrap" }}>
              Your Uploaded Materials:
            </span>
            {materialsList.map((m, idx) => {
              const isCurrent = (activeAnalysis as any)?.material_id === (m as any).id || activeAnalysis?.title === m.title;
              return (
                <button
                  key={m.id || idx}
                  type="button"
                  onClick={() => {
                    setActiveAnalysis(m);
                    setQuizAnswers({});
                    setQuizSubmitted({});
                  }}
                  style={{
                    fontSize: "11.5px",
                    padding: "4px 10px",
                    borderRadius: "14px",
                    border: isCurrent ? "1.5px solid var(--accent)" : "1px solid var(--border)",
                    background: isCurrent ? "rgba(56, 189, 248, 0.16)" : "var(--card-subtle)",
                    color: isCurrent ? "var(--accent)" : "var(--muted)",
                    fontWeight: isCurrent ? 700 : 500,
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                  }}
                >
                  {m.title} ({m.subject})
                </button>
              );
            })}
          </div>
        )}

        {/* Display Active AI Analysis & Guidance Card */}
        {activeAnalysis && activeAnalysis.analysis && (
          <div
            style={{
              marginTop: "16px",
              padding: "16px",
              borderRadius: "12px",
              background: "var(--card-subtle)",
              border: "1.5px solid var(--border)"
            }}
          >
            {/* Analysis Header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px" }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
                  <span style={{ fontSize: "17px", fontWeight: 800, color: "var(--text-heading)" }}>
                    {activeAnalysis.title}
                  </span>
                  <span className="pill small" style={{ background: "rgba(99, 102, 241, 0.12)", color: "var(--brand)", fontWeight: 700 }}>
                    {activeAnalysis.subject}
                  </span>
                  {activeAnalysis.ocr_engine && (
                    <span className="pill small" style={{ background: "rgba(16, 185, 129, 0.12)", color: "var(--ok)" }}>
                      Engine: {activeAnalysis.ocr_engine}
                    </span>
                  )}
                  {activeAnalysis.word_count ? (
                    <span style={{ fontSize: "11.5px", color: "var(--muted)" }}>
                      • {activeAnalysis.word_count} words analyzed
                    </span>
                  ) : null}
                </div>
                <div style={{ marginTop: "6px", fontSize: "13px", color: "var(--text)", lineHeight: "1.5" }}>
                  {activeAnalysis.analysis.summary}
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                <button
                  className="btn small"
                  style={{ background: "var(--accent)", color: "#ffffff", fontWeight: 700 }}
                  onClick={() => handleGeneratePlanFromMaterial(activeAnalysis.subject)}
                  title="Generate adaptive study schedule based on these notes"
                >
                  📅 Generate Study Plan ▶
                </button>
                <button
                  className="btn small secondary"
                  onClick={() => onNavigateTab("mentor")}
                  title="Discuss concepts from these notes with Socratic Mentor"
                >
                  🤖 Ask Mentor About Notes
                </button>
                <button
                  className="btn small secondary"
                  onClick={() => onNavigateTab("courses")}
                  title="Open auto-generated course module"
                >
                  📖 View Course Module
                </button>
              </div>
            </div>

            {/* Extracted Key Concepts & Formulas Grid */}
            <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", marginTop: "14px" }}>
              {/* Concepts */}
              {activeAnalysis.analysis.key_concepts && activeAnalysis.analysis.key_concepts.length > 0 && (
                <div style={{ background: "var(--card)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border)" }}>
                  <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--muted)", marginBottom: "8px" }}>
                    🧠 Key Concepts Extracted from Notes:
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                    {activeAnalysis.analysis.key_concepts.map((concept, idx) => (
                      <span
                        key={idx}
                        style={{
                          fontSize: "11.5px",
                          padding: "3px 8px",
                          borderRadius: "6px",
                          background: "var(--card-subtle)",
                          color: "var(--text)",
                          border: "1px solid var(--border)",
                          fontWeight: 600,
                        }}
                      >
                        {concept}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Formulas & Governing Rules */}
              {activeAnalysis.analysis.key_formulas && activeAnalysis.analysis.key_formulas.length > 0 && (
                <div style={{ background: "var(--card)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border)" }}>
                  <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--muted)", marginBottom: "8px" }}>
                    📐 Extracted Formulas & Governing Equations:
                  </div>
                  <div style={{ display: "grid", gap: "6px" }}>
                    {activeAnalysis.analysis.key_formulas.map((formula, idx) => (
                      <div
                        key={idx}
                        style={{
                          fontSize: "12px",
                          fontFamily: "monospace",
                          background: "var(--card-subtle)",
                          padding: "4px 8px",
                          borderRadius: "4px",
                          borderLeft: "3px solid var(--accent)",
                          color: "var(--text-heading)",
                        }}
                      >
                        {formula}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Personalized Guidance & Monitoring Directive */}
            {activeAnalysis.analysis.study_recommendation && (
              <div
                style={{
                  marginTop: "12px",
                  padding: "10px 14px",
                  borderRadius: "8px",
                  background: "rgba(16, 185, 129, 0.12)",
                  border: "1px solid var(--ok)",
                  fontSize: "13px",
                  color: "var(--ok)",
                  lineHeight: "1.45",
                }}
              >
                <strong>💡 Personalized Study Guidance:</strong> {activeAnalysis.analysis.study_recommendation}
                {activeAnalysis.analysis.estimated_study_minutes ? (
                  <span style={{ marginLeft: "8px", fontWeight: 700 }}>
                    (Est. Target Duration: {activeAnalysis.analysis.estimated_study_minutes} mins)
                  </span>
                ) : null}
              </div>
            )}

            {/* AI Generated Practice Diagnostic Quiz derived from notes */}
            {activeAnalysis.analysis.generated_questions && activeAnalysis.analysis.generated_questions.length > 0 && (
              <div style={{ marginTop: "14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                  <div style={{ fontSize: "13px", fontWeight: 700, color: "var(--text-heading)" }}>
                    ✍️ AI Diagnostic Practice Drill (Generated Directly from Your Uploaded Notes)
                  </div>
                  <span style={{ fontSize: "11.5px", color: "var(--muted)" }}>
                    Click an option to test your understanding
                  </span>
                </div>

                <div style={{ display: "grid", gap: "10px" }}>
                  {activeAnalysis.analysis.generated_questions.map((q, qIdx) => {
                    const answered = quizSubmitted[qIdx];
                    const selected = quizAnswers[qIdx];
                    return (
                      <div
                        key={qIdx}
                        style={{
                          background: "var(--card)",
                          padding: "12px",
                          borderRadius: "8px",
                          border: "1px solid var(--border)",
                        }}
                      >
                        <div style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-heading)", marginBottom: "8px" }}>
                          Q{qIdx + 1}. {q.question}
                        </div>
                        <div style={{ display: "grid", gap: "6px" }}>
                          {q.options.map((opt, optIdx) => {
                            const isChosen = selected === optIdx;
                            const isCorrectOpt = optIdx === q.correct_index;
                            let btnBg = "var(--card-subtle)";
                            let btnBorder = "var(--border)";
                            let btnColor = "var(--text)";

                            if (answered) {
                              if (isCorrectOpt) {
                                btnBg = "rgba(16, 185, 129, 0.15)";
                                btnBorder = "var(--ok)";
                                btnColor = "var(--ok)";
                              } else if (isChosen && !isCorrectOpt) {
                                btnBg = "rgba(239, 68, 68, 0.15)";
                                btnBorder = "var(--danger)";
                                btnColor = "var(--danger)";
                              }
                            }

                            return (
                              <button
                                key={optIdx}
                                type="button"
                                onClick={() => handleAnswerOption(qIdx, optIdx)}
                                style={{
                                  textAlign: "left",
                                  padding: "8px 12px",
                                  borderRadius: "6px",
                                  border: `1px solid ${btnBorder}`,
                                  background: btnBg,
                                  color: btnColor,
                                  fontSize: "12.5px",
                                  cursor: "pointer",
                                  fontWeight: isChosen ? 700 : 400,
                                  display: "flex",
                                  alignItems: "center",
                                  gap: "8px",
                                  transition: "all 0.15s ease",
                                }}
                              >
                                <span style={{ fontWeight: 700, fontSize: "11px", color: "var(--muted)" }}>
                                  {String.fromCharCode(65 + optIdx)}.
                                </span>
                                <span>{opt}</span>
                                {answered && isCorrectOpt && <span style={{ marginLeft: "auto", color: "var(--ok)", fontWeight: 700 }}>✓ Correct</span>}
                                {answered && isChosen && !isCorrectOpt && <span style={{ marginLeft: "auto", color: "var(--danger)", fontWeight: 700 }}>✗ Incorrect</span>}
                              </button>
                            );
                          })}
                        </div>
                        {answered && (
                          <div
                            style={{
                              marginTop: "8px",
                              padding: "8px 10px",
                              borderRadius: "6px",
                              background: "var(--card-subtle)",
                              fontSize: "12px",
                              color: "var(--text)",
                              borderLeft: "3px solid var(--brand)",
                            }}
                          >
                            <strong style={{ color: "var(--text-heading)" }}>Explanation:</strong> {q.explanation}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Spaced Revision & Recent Diagnostic Section (2-Column) */}
      <div className="grid-2">
        {/* Card 1: Spaced Revision Queue */}
        <div className="card" style={{ background: "var(--card)", border: "1px solid var(--border)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontWeight: 800, fontSize: "14px", color: "var(--text-heading)" }}>
                ⏳ Spaced Revision Queue (Ebbinghaus Decay)
              </div>
              <div className="subtitle">Concepts approaching memory retention threshold (≤75%)</div>
            </div>
            <span className="pill small" style={{ background: revisions.length > 0 ? "rgba(245, 158, 11, 0.12)" : "rgba(16, 185, 129, 0.12)", color: revisions.length > 0 ? "var(--warn)" : "var(--ok)", fontWeight: 700 }}>
              {revisions.length} Due
            </span>
          </div>
          <div className="hr"></div>

          {revisions.length > 0 ? (
            <ul className="list" style={{ marginTop: "6px" }}>
              {revisions.map((rev) => (
                <li key={rev.concept_id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 10px" }}>
                  <div>
                    <strong style={{ fontSize: "13px", color: "var(--text-heading)" }}>{rev.title}</strong>
                    <div className="small note" style={{ color: "var(--warn)" }}>
                      Estimated Retention: {rev.retention_percent}% • Due: {rev.next_review || "Today"}
                    </div>
                  </div>
                  <button className="btn small" onClick={() => onNavigateTab("test")}>
                    Revise 🔄
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div style={{ padding: "16px", textAlign: "center", color: "var(--muted)", fontSize: "13px" }}>
              ✓ All reviewed concepts currently maintain strong memory stability ($R(t) &gt; 0.75$).
            </div>
          )}
        </div>

        {/* Card 2: Recent Diagnostic & Latent Ability Preview */}
        <div className="card" style={{ background: "var(--card)", border: "1px solid var(--border)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontWeight: 800, fontSize: "14px", color: "var(--text-heading)" }}>
                📊 Calibrated Ability & Diagnostic Trajectory
              </div>
              <div className="subtitle">Item Response Theory (IRT $\theta$) & exam readiness</div>
            </div>
            {recentEval && (
              <span className="pill small" style={{ background: "rgba(99, 102, 241, 0.12)", color: "var(--brand)", fontWeight: 700 }}>
                {recentEval.performance_tier}
              </span>
            )}
          </div>
          <div className="hr"></div>

          {recentEval ? (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "13px", color: "var(--muted)" }}>Last Test Score:</span>
                <strong style={{ fontSize: "14px", color: "var(--text-heading)" }}>{recentEval.score} ({recentEval.percentage}%)</strong>
              </div>
              {recentEval.irt_ability && (
                <>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                    <span style={{ fontSize: "13px", color: "var(--muted)" }}>Latent Ability ($\theta$):</span>
                    <strong style={{ fontSize: "14px", color: "var(--brand)" }}>
                      {recentEval.irt_ability.theta > 0 ? `+${recentEval.irt_ability.theta}` : recentEval.irt_ability.theta} (SE: ±{recentEval.irt_ability.standard_error})
                    </strong>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                    <span style={{ fontSize: "13px", color: "var(--muted)" }}>Proficiency Band:</span>
                    <span style={{ fontSize: "12.5px", fontWeight: 700, color: "var(--ok)" }}>
                      {recentEval.irt_ability.proficiency_band}
                    </span>
                  </div>
                </>
              )}
              <div className="right">
                <button className="btn small secondary" onClick={() => onNavigateTab("performance")}>
                  Full Analytics →
                </button>
              </div>
            </div>
          ) : (
            <div style={{ padding: "16px", textAlign: "center", color: "var(--muted)", fontSize: "13px" }}>
              <p style={{ margin: "0 0 10px 0" }}>Take your first adaptive diagnostic to compute your latent ability index.</p>
              <button className="btn small" onClick={() => onNavigateTab("test")}>
                Start Diagnostic Test ▶
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Enrolled Courses Section on Dashboard */}
      {enrolledCourses.length > 0 && (
        <div className="card" style={{ background: "var(--card)", border: "1px solid var(--border)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <div>
              <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)" }}>
                📚 Your Enrolled Courses ({enrolledCourses.length})
              </div>
              <div className="subtitle">Active learning modules linked to your student model</div>
            </div>
            <button className="btn small secondary" onClick={() => onNavigateTab("courses")}>
              Browse All Courses →
            </button>
          </div>
          <div className="hr"></div>
          <div style={{ display: "grid", gap: "10px", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))" }}>
            {enrolledCourses.map((courseTitle, idx) => (
              <div
                key={idx}
                style={{
                  background: "var(--card-subtle)",
                  padding: "12px",
                  borderRadius: "10px",
                  border: "1px solid var(--border)",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div>
                  <div style={{ fontWeight: 700, fontSize: "13.5px", color: "var(--text-heading)" }}>{courseTitle}</div>
                  <div className="small note" style={{ color: "var(--ok)", fontWeight: 600 }}>
                    In Progress • Active
                  </div>
                </div>
                <button className="btn small" onClick={() => onNavigateTab("courses")}>
                  Continue ▶
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
