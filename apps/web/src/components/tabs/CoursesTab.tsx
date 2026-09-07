"use client";

import React, { useState, useEffect } from "react";
import { api, CourseItem, FreeExternalCourse } from "@/lib/api";
import CourseViewer from "@/components/courses/CourseViewer";

interface CoursesTabProps {
  initialGoal?: string;
  initialWeak?: string;
  initialEnrolled?: string[];
  onNavigateTab: (tabKey: string) => void;
}

export default function CoursesTab({
  initialGoal = "CBSE",
  initialWeak = "",
  initialEnrolled = [],
  onNavigateTab,
}: CoursesTabProps) {
  const [filterTrack, setFilterTrack] = useState<string>("All");
  const [goal, setGoal] = useState<string>(initialGoal);
  const [weak, setWeak] = useState<string>(initialWeak);
  const [studentClass, setStudentClass] = useState<string>("10");
  const [catalog, setCatalog] = useState<CourseItem[]>([]);
  const [recommendations, setRecommendations] = useState<CourseItem[]>([]);
  const [freeCourses, setFreeCourses] = useState<FreeExternalCourse[]>([]);
  const [enrolledList, setEnrolledList] = useState<string[]>(initialEnrolled);
  const [selectedCourseForStudy, setSelectedCourseForStudy] = useState<CourseItem | null>(null);
  const [previewCourse, setPreviewCourse] = useState<CourseItem | null>(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [enrollmentNotification, setEnrollmentNotification] = useState<string | null>(null);

  useEffect(() => {
    loadCourses();
  }, [filterTrack, goal]);

  const loadCourses = async () => {
    setIsLoading(true);
    try {
      const [cat, recs, profile, freeExt] = await Promise.all([
        api.getCatalog(filterTrack),
        api.getRecommendations(),
        api.getProfile().catch(() => null),
        api.getFreeExternalCourses().catch(() => []),
      ]);
      setCatalog(cat);
      setRecommendations(recs);
      setFreeCourses(freeExt);
      if (profile?.enrolled_courses) {
        setEnrolledList(profile.enrolled_courses);
      }
      if (profile?.klass) {
        setStudentClass(String(profile.klass));
      }
      if (profile?.goal) {
        setGoal(profile.goal);
      }
    } catch (e) {
      console.error("Failed to load courses:", e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnroll = async (course: CourseItem) => {
    try {
      await api.enrollCourse(course.title);
      setEnrolledList((prev) => (prev.includes(course.title) ? prev : [...prev, course.title]));
      setEnrollmentNotification(`🎉 Successfully enrolled in "${course.title}". You can study it anytime!`);
    } catch (e: any) {
      alert(`Enrollment failed: ${e.message}`);
    }
  };

  const handleUnenroll = async (courseTitle: string) => {
    const ok = window.confirm(`Remove "${courseTitle}" from your enrolled courses?`);
    if (!ok) return;

    try {
      await api.unenrollCourse(courseTitle);
      setEnrolledList((prev) => prev.filter((c) => c.toLowerCase().trim() !== courseTitle.toLowerCase().trim()));
      setEnrollmentNotification(`Course "${courseTitle}" has been removed from your enrolled curriculum.`);
      if (previewCourse && previewCourse.title.toLowerCase().trim() === courseTitle.toLowerCase().trim()) {
        setPreviewCourse(null);
      }
    } catch (e: any) {
      alert(`Failed to unenroll: ${e.message}`);
    }
  };

  const handleOpenCourse = async (course: CourseItem) => {
    try {
      if (course.modules && course.modules.length > 0) {
        setSelectedCourseForStudy(course);
        return;
      }
      const fullCourse = await api.getCourseDetail(course.id || course.title);
      setSelectedCourseForStudy(fullCourse);
    } catch {
      setSelectedCourseForStudy(course);
    }
  };

  const handlePreviewCourse = async (course: CourseItem) => {
    setIsPreviewLoading(true);
    setPreviewCourse(course);
    try {
      const fullCourse = await api.getCourseDetail(course.id || course.title);
      setPreviewCourse(fullCourse);
    } catch {
      setPreviewCourse(course);
    } finally {
      setIsPreviewLoading(false);
    }
  };

  // If student is currently viewing a specific course learning workspace
  if (selectedCourseForStudy) {
    return (
      <CourseViewer
        course={selectedCourseForStudy}
        onBack={() => setSelectedCourseForStudy(null)}
        onNavigateTab={onNavigateTab}
      />
    );
  }

  const filteredCatalog = catalog.filter((c) => {
    if (!weak.trim()) return true;
    const w = weak.toLowerCase();
    return (c.tag && c.tag.toLowerCase().includes(w)) || c.title.toLowerCase().includes(w);
  });

  return (
    <div id="panel-courses" className="card">
      {/* Header with personalization badge */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px", flexWrap: "wrap", gap: "8px" }}>
        <div>
          <h2 style={{ margin: 0, fontSize: "20px", fontWeight: 800, color: "var(--text-heading)" }}>
            Curriculum Courses & Verified Online Study
          </h2>
          <p style={{ margin: "3px 0 0 0", fontSize: "13px", color: "var(--muted)" }}>
            Explore course syllabi, preview topic overviews, and manage your active enrollments.
          </p>
        </div>
        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
          <span className="pill small" style={{ background: "rgba(56, 189, 248, 0.12)", color: "var(--accent)", fontWeight: 700, border: "1px solid rgba(56, 189, 248, 0.25)" }}>
            🎯 Target: {goal}
          </span>
          <span className="pill small" style={{ background: "rgba(16, 185, 129, 0.12)", color: "var(--ok)", fontWeight: 700, border: "1px solid rgba(16, 185, 129, 0.25)" }}>
            🎓 Class {studentClass}
          </span>
        </div>
      </div>

      {/* Notification Toast */}
      {enrollmentNotification && (
        <div
          style={{
            padding: "12px 16px",
            background: "rgba(16, 185, 129, 0.14)",
            border: "1px solid var(--ok)",
            borderRadius: "10px",
            color: "var(--ok)",
            marginBottom: "14px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span style={{ fontWeight: 600, fontSize: "13.5px" }}>{enrollmentNotification}</span>
          <button
            onClick={() => setEnrollmentNotification(null)}
            style={{ background: "none", border: "none", cursor: "pointer", fontWeight: 700, color: "var(--ok)", fontSize: "15px" }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Active Enrolled Courses Section */}
      {enrolledList.length > 0 && (
        <div style={{ marginBottom: "18px", padding: "14px 16px", background: "rgba(2, 132, 199, 0.08)", borderRadius: "12px", border: "1.5px solid rgba(2, 132, 199, 0.25)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px", flexWrap: "wrap", gap: "6px" }}>
            <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--accent)" }}>
              📚 Your Active Enrolled Courses ({enrolledList.length})
            </div>
            <span className="small note">Manage your learning path or remove courses you no longer need</span>
          </div>
          <div style={{ display: "grid", gap: "10px", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))" }}>
            {enrolledList.map((courseTitle, idx) => {
              const lowerTitle = courseTitle.toLowerCase();
              let matched = catalog.find((c) => c.title.toLowerCase() === lowerTitle);
              if (!matched) {
                matched = recommendations.find((c) => c.title.toLowerCase() === lowerTitle);
              }
              if (!matched) {
                matched = catalog.find((c) => {
                  const cTitle = c.title.toLowerCase();
                  return (c.tag && lowerTitle.includes(c.tag.toLowerCase())) ||
                         lowerTitle.split(" ").some((word) => word.length > 3 && cTitle.includes(word));
                });
              }

              const deducedTag = lowerTitle.includes("bio")
                ? "Biology"
                : lowerTitle.includes("chem")
                ? "Chemistry"
                : lowerTitle.includes("math")
                ? "Math"
                : lowerTitle.includes("aptitude")
                ? "General Aptitude"
                : lowerTitle.includes("ai") || lowerTitle.includes("data")
                ? "AI / Data Science"
                : "Physics";

              const courseToUse: CourseItem = matched || {
                id: `enrolled_${idx}`,
                title: courseTitle,
                tag: deducedTag,
                track: goal,
                hours: 6,
              };

              return (
                <div
                  key={idx}
                  className="card"
                  style={{
                    background: "var(--card)",
                    border: "1px solid var(--border)",
                    padding: "12px 14px",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderRadius: "10px",
                    boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
                    flexWrap: "wrap",
                    gap: "8px",
                  }}
                >
                  <div style={{ marginRight: "10px", flex: 1 }}>
                    <div style={{ fontWeight: 700, fontSize: "13.5px", color: "var(--text-heading)" }}>{courseTitle}</div>
                    <div style={{ display: "flex", gap: "6px", alignItems: "center", marginTop: "3px" }}>
                      <span className="small note" style={{ color: "#10b981", fontWeight: 700 }}>Enrolled & Active ✓</span>
                      <span className="small note">• {deducedTag}</span>
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
                    <button
                      className="btn small"
                      style={{ background: "var(--card-subtle)", color: "var(--text)", border: "1px solid var(--border)", whiteSpace: "nowrap" }}
                      onClick={() => handlePreviewCourse(courseToUse)}
                      title="Inspect course syllabus and details"
                    >
                      View 👁
                    </button>
                    <button
                      className="btn small"
                      onClick={() => handleOpenCourse(courseToUse)}
                      style={{ whiteSpace: "nowrap" }}
                    >
                      Start Learning ▶
                    </button>
                    <button
                      className="btn small"
                      onClick={() => handleUnenroll(courseTitle)}
                      title="Unenroll from this course"
                      style={{ background: "rgba(239, 68, 68, 0.14)", color: "var(--danger)", border: "1px solid rgba(239, 68, 68, 0.3)", whiteSpace: "nowrap" }}
                    >
                      Unenroll ✕
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Filter Row */}
      <div className="grid-3 row">
        <div>
          <label htmlFor="courseFilter">Filter by Curriculum Track</label>
          <select
            id="courseFilter"
            className="input"
            value={filterTrack}
            onChange={(e) => setFilterTrack(e.target.value)}
          >
            <option value="All">All Tracks (Universal)</option>
            {goal && !["JEE", "NEET", "CUET", "CBSE", "ICSE", "State Board", "CET"].includes(goal) && (
              <option value={goal}>{goal} (Your Goal)</option>
            )}
            <option value="JEE">JEE (Engineering)</option>
            <option value="NEET">NEET (Medical)</option>
            <option value="CUET">CUET Entrance</option>
            <option value="CBSE">CBSE Board</option>
            <option value="ICSE">ICSE / ISC</option>
            <option value="State Board">State Board</option>
            <option value="CET">State CET</option>
          </select>
        </div>
        <div>
          <label htmlFor="courseGoal">Target Exam Prep Aim</label>
          <input
            id="courseGoal"
            className="input"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="Enter target exam or discipline"
          />
        </div>
        <div>
          <label htmlFor="courseWeak">Filter by Subject / Weak Area</label>
          <input
            id="courseWeak"
            className="input"
            placeholder="Filter by subject or topic name..."
            value={weak}
            onChange={(e) => setWeak(e.target.value)}
          />
        </div>
      </div>

      {/* Available Curriculum Courses Grid */}
      <div style={{ marginTop: "16px", marginBottom: "8px", fontWeight: 800, fontSize: "15px", color: "var(--text-heading)" }}>
        📖 Interactive Curriculum Modules ({filteredCatalog.length})
      </div>
      <div id="courseGrid" className="grid-3 row" style={{ marginTop: "8px" }}>
        {filteredCatalog.map((c) => {
          const isEnrolled = enrolledList.includes(c.title);
          return (
            <div
              key={c.id}
              className="card"
              style={{
                background: "var(--card)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                border: "1px solid var(--border)",
              }}
            >
              <div>
                <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--text-heading)" }}>{c.title}</div>
                <div className="subtitle" style={{ marginTop: "3px" }}>
                  <span style={{ fontWeight: 700, color: "var(--accent)" }}>{c.tag}</span> • ~{c.hours} hrs • {c.track}
                </div>
                {c.is_weakness_remedy && (
                  <div style={{ marginTop: "6px" }}>
                    <span className="pill small" style={{ background: "rgba(239, 68, 68, 0.12)", color: "var(--danger)", border: "1px solid var(--danger)", fontSize: "11px", fontWeight: 700 }}>
                      🎯 Diagnosed Weak Area Remedy
                    </span>
                  </div>
                )}
                {c.description && (
                  <div className="small note" style={{ marginTop: "8px", fontSize: "12.5px", lineHeight: "1.45" }}>
                    {c.description}
                  </div>
                )}
              </div>
              <div className="right" style={{ marginTop: "14px", display: "flex", gap: "6px", justifyContent: "flex-end" }}>
                <button
                  className="btn small"
                  style={{ background: "var(--card-subtle)", color: "var(--text)", border: "1px solid var(--border)" }}
                  onClick={() => handlePreviewCourse(c)}
                  title="View course overview and syllabus breakdown"
                >
                  View Details 👁
                </button>
                {isEnrolled ? (
                  <button className="btn small" onClick={() => handleOpenCourse(c)}>
                    Start Learning ▶
                  </button>
                ) : (
                  <button className="btn small" onClick={() => handleEnroll(c)}>
                    Enroll Course
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* FREE ACCREDITED ONLINE COURSES SECTION */}
      {freeCourses.length > 0 && (
        <div style={{ marginTop: "24px", padding: "18px 20px", background: "var(--card-subtle)", borderRadius: "14px", border: "1.5px solid var(--border)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px", marginBottom: "14px" }}>
            <div>
              <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                <span style={{ fontSize: "20px" }}>🌐</span>
                <span style={{ fontWeight: 800, fontSize: "16px", color: "var(--text-heading)" }}>
                  Free Accredited Online Courses (100% Free Open Access)
                </span>
              </div>
              <p style={{ margin: "4px 0 0 0", fontSize: "13px", color: "var(--muted)" }}>
                Curated open-access university & government courses personalized for your {goal} preparation and Class {studentClass} syllabus.
              </p>
            </div>
            <span className="pill small" style={{ background: "var(--accent)", color: "#ffffff", fontWeight: 700, border: "none" }}>
              Verified Free Web Access ✓
            </span>
          </div>

          <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(auto-fill, minmax(310px, 1fr))" }}>
            {freeCourses.map((fc) => (
              <div
                key={fc.id}
                style={{
                  background: "var(--card)",
                  padding: "14px 16px",
                  borderRadius: "12px",
                  border: "1px solid var(--border)",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.04)",
                }}
              >
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                    <span
                      style={{
                        fontSize: "11px",
                        fontWeight: 800,
                        textTransform: "uppercase",
                        padding: "2px 8px",
                        borderRadius: "6px",
                        background: "rgba(14, 165, 233, 0.15)",
                        color: "var(--accent)",
                      }}
                    >
                      {fc.platform}
                    </span>
                    <span style={{ fontSize: "12px", fontWeight: 700, color: "#f59e0b" }}>
                      ★ {fc.rating}
                    </span>
                  </div>
                  <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--text-heading)", marginBottom: "4px" }}>
                    {fc.title}
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--muted)", marginBottom: "8px" }}>
                    Offered by: <strong>{fc.provider}</strong> • Duration: {fc.duration}
                  </div>
                  <div style={{ fontSize: "12.5px", color: "var(--text)", lineHeight: "1.45" }}>
                    {fc.description}
                  </div>
                </div>

                <div style={{ marginTop: "14px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span className="pill small" style={{ background: "rgba(16, 185, 129, 0.12)", color: "var(--ok)", border: "1px solid var(--ok)", fontSize: "11px", fontWeight: 700 }}>
                    {fc.badge}
                  </span>
                  <a
                    href={fc.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn small"
                    style={{
                      background: "var(--brand)",
                      color: "#ffffff",
                      textDecoration: "none",
                      display: "inline-block",
                    }}
                  >
                    Open Free Course ↗
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="hr" style={{ margin: "20px 0" }}></div>

      {/* Personalized Recommendations Section */}
      <div>
        <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)" }}>
          🎯 Adaptive Recommendations (Calibrated to Class {studentClass} + {goal} + Diagnostic Mastery)
        </div>
        <ul id="recommendedList" className="list" style={{ marginTop: "10px" }}>
          {recommendations.length > 0 ? (
            recommendations.map((r) => {
              const isEnrolled = enrolledList.includes(r.title);
              return (
                <li key={r.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 12px", flexWrap: "wrap", gap: "8px" }}>
                  <div>
                    <strong style={{ fontSize: "13.5px", color: "var(--text-heading)" }}>{r.title}</strong>
                    <div className="small note" style={{ color: "var(--accent)", fontWeight: 600, marginTop: "2px" }}>
                      {r.reason}
                    </div>
                  </div>
                  <div className="right" style={{ display: "flex", gap: "6px" }}>
                    <button
                      className="btn small"
                      style={{ background: "var(--card-subtle)", color: "var(--text)", border: "1px solid var(--border)" }}
                      onClick={() => handlePreviewCourse(r)}
                    >
                      View Details 👁
                    </button>
                    {isEnrolled ? (
                      <button className="btn small" onClick={() => handleOpenCourse(r)}>
                        Start Learning ▶
                      </button>
                    ) : (
                      <button className="btn small" onClick={() => handleEnroll(r)}>
                        Enroll Course
                      </button>
                    )}
                  </div>
                </li>
              );
            })
          ) : (
            <li className="small">No personalized recommendations yet. Complete a diagnostic test to calibrate.</li>
          )}
        </ul>
      </div>

      {/* ============================================================ */}
      {/* COURSE PREVIEW & OVERVIEW MODAL */}
      {/* ============================================================ */}
      {previewCourse && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(15, 23, 42, 0.65)",
            backdropFilter: "blur(4px)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
            padding: "20px",
          }}
          onClick={() => setPreviewCourse(null)}
        >
          <div
            className="card"
            style={{
              background: "var(--card)",
              maxWidth: "680px",
              width: "100%",
              maxHeight: "85vh",
              overflowY: "auto",
              boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)",
              borderRadius: "16px",
              padding: "24px",
              position: "relative",
              border: "1px solid var(--border)",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "14px" }}>
              <div>
                <div style={{ display: "flex", gap: "8px", alignItems: "center", marginBottom: "6px" }}>
                  <span className="badge small" style={{ color: "var(--accent)", borderColor: "var(--accent)", background: "rgba(2, 132, 199, 0.12)", fontWeight: 700 }}>
                    {previewCourse.tag}
                  </span>
                  <span className="badge small" style={{ color: "var(--brand)", borderColor: "var(--brand)", background: "rgba(99, 102, 241, 0.12)", fontWeight: 700 }}>
                    ~{previewCourse.hours} Hours
                  </span>
                  <span className="badge small" style={{ color: "var(--ok)", borderColor: "var(--ok)", background: "rgba(16, 185, 129, 0.12)", fontWeight: 700 }}>
                    Track: {previewCourse.track || goal}
                  </span>
                </div>
                <h2 style={{ margin: 0, fontSize: "20px", fontWeight: 800, color: "var(--text-heading)" }}>
                  {previewCourse.title}
                </h2>
              </div>
              <button
                onClick={() => setPreviewCourse(null)}
                style={{
                  background: "var(--card-subtle)",
                  border: "1px solid var(--border)",
                  borderRadius: "50%",
                  width: "32px",
                  height: "32px",
                  cursor: "pointer",
                  fontSize: "16px",
                  fontWeight: 700,
                  color: "var(--muted)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                ✕
              </button>
            </div>

            {/* Why prioritized indicator */}
            {previewCourse.reason && (
              <div
                style={{
                  padding: "10px 14px",
                  background: "rgba(2, 132, 199, 0.1)",
                  border: "1px solid rgba(2, 132, 199, 0.25)",
                  borderRadius: "10px",
                  color: "var(--accent)",
                  fontSize: "13px",
                  marginBottom: "14px",
                }}
              >
                💡 <strong>Why this fits you:</strong> {previewCourse.reason}
              </div>
            )}

            {/* Course Overview / Syllabus Description */}
            <div style={{ marginBottom: "16px" }}>
              <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--text-heading)", marginBottom: "6px" }}>
                Course Overview & Objectives
              </div>
              <p style={{ margin: 0, fontSize: "13.5px", lineHeight: "1.6", color: "var(--text)" }}>
                {previewCourse.description ||
                  `This comprehensive curriculum track is engineered to build complete conceptual mastery and application fluency in ${previewCourse.title}. Topics include foundational axioms, step-by-step mathematical/analytical derivations, worked problem sets, and interactive diagnostic drills.`}
              </p>
            </div>

            {/* Modules & Topics Covered */}
            <div style={{ marginBottom: "20px" }}>
              <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--text-heading)", marginBottom: "8px" }}>
                Syllabus Breakdown ({previewCourse.modules?.length || 4} Interactive Modules)
              </div>
              {previewCourse.modules && previewCourse.modules.length > 0 ? (
                <div style={{ display: "grid", gap: "8px" }}>
                  {previewCourse.modules.map((m, idx) => (
                    <div
                      key={m.id || idx}
                      style={{
                        padding: "10px 12px",
                        background: "var(--card-subtle)",
                        border: "1px solid var(--border)",
                        borderRadius: "8px",
                      }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <strong style={{ fontSize: "13.5px", color: "var(--text-heading)" }}>
                          Module {idx + 1}: {m.title}
                        </strong>
                        <span className="badge small">{m.duration || "45 mins"}</span>
                      </div>
                      <div className="small note" style={{ marginTop: "4px", lineHeight: "1.4" }}>
                        {m.summary}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ display: "grid", gap: "8px" }}>
                  <div style={{ padding: "10px 12px", background: "var(--card-subtle)", border: "1px solid var(--border)", borderRadius: "8px" }}>
                    <strong style={{ fontSize: "13px", color: "var(--text-heading)" }}>Module 1: Foundations & Core Axioms</strong>
                    <div className="small note" style={{ marginTop: "2px" }}>Deconstructs fundamental definitions, theorems, and prerequisites.</div>
                  </div>
                  <div style={{ padding: "10px 12px", background: "var(--card-subtle)", border: "1px solid var(--border)", borderRadius: "8px" }}>
                    <strong style={{ fontSize: "13px", color: "var(--text-heading)" }}>Module 2: Analytical Derivations & Worked Proofs</strong>
                    <div className="small note" style={{ marginTop: "2px" }}>Deep problem solving and standard test derivations.</div>
                  </div>
                  <div style={{ padding: "10px 12px", background: "var(--card-subtle)", border: "1px solid var(--border)", borderRadius: "8px" }}>
                    <strong style={{ fontSize: "13px", color: "var(--text-heading)" }}>Module 3: Advanced Numerical Drills</strong>
                    <div className="small note" style={{ marginTop: "2px" }}>Timed exam-level problems and misconception traps.</div>
                  </div>
                  <div style={{ padding: "10px 12px", background: "var(--card-subtle)", border: "1px solid var(--border)", borderRadius: "8px" }}>
                    <strong style={{ fontSize: "13px", color: "var(--text-heading)" }}>Module 4: Spaced Recall & Diagnostic Review</strong>
                    <div className="small note" style={{ marginTop: "2px" }}>Consolidation drill and self-evaluation post-mortem.</div>
                  </div>
                </div>
              )}
            </div>

            {/* Modal Actions */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: "12px", borderTop: "1px solid var(--border)" }}>
              <button
                className="btn small"
                style={{ background: "var(--card-subtle)", color: "var(--text)", border: "1px solid var(--border)" }}
                onClick={() => setPreviewCourse(null)}
              >
                Close Preview
              </button>

              <div style={{ display: "flex", gap: "8px" }}>
                {enrolledList.includes(previewCourse.title) ? (
                  <>
                    <button
                      className="btn small"
                      style={{ background: "rgba(239, 68, 68, 0.14)", color: "var(--danger)", border: "1px solid rgba(239, 68, 68, 0.3)" }}
                      onClick={() => handleUnenroll(previewCourse.title)}
                    >
                      Unenroll from Course ✕
                    </button>
                    <button
                      className="btn small"
                      style={{ background: "#4f46e5", color: "#ffffff", fontWeight: 700 }}
                      onClick={() => {
                        setPreviewCourse(null);
                        handleOpenCourse(previewCourse);
                      }}
                    >
                      Start Learning ▶
                    </button>
                  </>
                ) : (
                  <button
                    className="btn small"
                    style={{ background: "#0284c7", color: "#ffffff", fontWeight: 700 }}
                    onClick={async () => {
                      await handleEnroll(previewCourse);
                      setPreviewCourse(null);
                    }}
                  >
                    Enroll in this Course ✓
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
