"use client";

import React, { useState, useEffect } from "react";
import { api, AIGuidanceResponse } from "@/lib/api";

interface GuidanceTabProps {
  initialGoal?: string;
  initialWeak?: string;
  initialKlass?: string;
  initialHours?: number;
}

export default function GuidanceTab({
  initialGoal = "AI/ML",
  initialWeak = "",
  initialKlass = "Degree",
  initialHours = 3.5,
}: GuidanceTabProps) {
  const [goal, setGoal] = useState<string>(initialGoal);
  const [klass, setKlass] = useState<string>(initialKlass);
  const [hours, setHours] = useState<number>(initialHours);
  const [weak, setWeak] = useState<string>(initialWeak);
  const [subjects, setSubjects] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [guidanceData, setGuidanceData] = useState<AIGuidanceResponse["guidance"] | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (initialGoal) setGoal(initialGoal);
    if (initialWeak) setWeak(initialWeak);
    if (initialKlass) setKlass(initialKlass);
    if (initialHours) setHours(initialHours);
  }, [initialGoal, initialWeak, initialKlass, initialHours]);

  const handleGenerate = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const weakList = weak
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      const subList = subjects
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      const res = await api.generateGuidance({
        goal: goal.trim() || "Academic Preparation",
        klass: klass || "Degree",
        daily_hours: Number(hours) || 3.0,
        weak_areas: weakList,
        subjects: subList.length > 0 ? subList : undefined,
      });

      if (res && res.guidance) {
        setGuidanceData(res.guidance);
      }
    } catch (e: any) {
      console.error("Failed to generate AI guidance:", e);
      setErrorMessage(e.message || "Failed to contact AI guidance engine.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div id="panel-guidance" className="card" style={{ display: "grid", gap: "16px" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "8px" }}>
        <div>
          <h2 style={{ margin: 0, fontSize: "20px", fontWeight: 800, color: "var(--text-heading)" }}>
            🧠 AI Academic Guidance & Strategic Roadmap
          </h2>
          <p style={{ margin: "4px 0 0 0", fontSize: "13px", color: "var(--muted)" }}>
            Generated dynamically by AI LLM based on your exact weak areas, daily schedule, and target educational goal.
          </p>
        </div>
        <span
          className="pill small"
          style={{ background: "rgba(99, 102, 241, 0.12)", color: "var(--brand)", fontWeight: 700, border: "1px solid var(--brand)" }}
        >
          Powered by GPT-4o Intelligence
        </span>
      </div>

      {/* Dynamic Input Form */}
      <div className="card" style={{ background: "var(--card-subtle)", border: "1px solid var(--border)" }}>
        <div className="grid-3 row">
          <div>
            <label htmlFor="gGoal">Target Exam / Educational Goal</label>
            <input
              id="gGoal"
              className="input"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Enter target exam or educational goal"
            />
          </div>

          <div>
            <label htmlFor="gClass">Academic Tier / Level</label>
            <select
              id="gClass"
              className="input"
              value={klass}
              onChange={(e) => setKlass(e.target.value)}
            >
              <option value="10">Class 10</option>
              <option value="11">Class 11</option>
              <option value="12">Class 12</option>
              <option value="Degree">College Undergraduate / Degree</option>
            </select>
          </div>

          <div>
            <label htmlFor="gHours">Available Study Hours / Day ({hours}h)</label>
            <input
              id="gHours"
              type="range"
              min="1"
              max="14"
              step="0.5"
              className="input"
              value={hours}
              onChange={(e) => setHours(Number(e.target.value))}
              style={{ cursor: "pointer" }}
            />
          </div>

          <div style={{ gridColumn: "1/-1", display: "grid", gap: "10px", gridTemplateColumns: "repeat(2, minmax(0, 1fr))" }}>
            <div>
              <label htmlFor="gWeak">Weak Areas & Pain Points (Comma separated)</label>
              <input
                id="gWeak"
                className="input"
                placeholder="Enter weak areas separated by commas"
                value={weak}
                onChange={(e) => setWeak(e.target.value)}
              />
              <div className="small note" style={{ fontSize: "11px", marginTop: "2px" }}>
                The AI will design specific tactical remediation for each topic listed.
              </div>
            </div>

            <div>
              <label htmlFor="gSubjects">Focus Subjects / Sub-fields (Optional)</label>
              <input
                id="gSubjects"
                className="input"
                placeholder="Enter focus subjects separated by commas"
                value={subjects}
                onChange={(e) => setSubjects(e.target.value)}
              />
              <div className="small note" style={{ fontSize: "11px", marginTop: "2px" }}>
                Leave empty to automatically prioritize your weak areas and goal curriculum.
              </div>
            </div>
          </div>
        </div>

        <div className="right" style={{ marginTop: "12px" }}>
          <button
            className="btn"
            onClick={handleGenerate}
            disabled={isLoading}
            style={{
              background: "linear-gradient(135deg, #4f46e5 0%, #0284c7 100%)",
              color: "#ffffff",
              fontWeight: 700,
              padding: "9px 20px",
              boxShadow: "0 2px 6px rgba(79, 70, 229, 0.25)",
            }}
          >
            {isLoading ? "Synthesizing AI Guidance..." : "Generate AI Academic Guidance ⚡"}
          </button>
        </div>
      </div>

      {/* Error Banner */}
      {errorMessage && (
        <div style={{ padding: "12px 16px", background: "rgba(239, 68, 68, 0.14)", border: "1px solid var(--danger)", borderRadius: "10px", color: "var(--danger)" }}>
          ⚠️ {errorMessage}
        </div>
      )}

      {/* Loading Skeleton */}
      {isLoading && (
        <div style={{ textAlign: "center", padding: "36px 20px", background: "rgba(99, 102, 241, 0.08)", borderRadius: "12px", border: "1.5px dashed var(--brand)" }}>
          <div style={{ fontSize: "28px", animation: "spin 2s linear infinite" }}>⚙️</div>
          <div style={{ fontWeight: 800, fontSize: "16px", color: "var(--brand)", marginTop: "10px" }}>
            Analyzing Your Weak Areas & Goal With AI LLM...
          </div>
          <p style={{ fontSize: "13px", color: "var(--muted)", margin: "4px 0 0 0" }}>
            Constructing diagnostic remedies, weekly time allocations, and milestone targets specifically for {goal}.
          </p>
        </div>
      )}

      {/* Results View */}
      {guidanceData && !isLoading && (
        <div style={{ display: "grid", gap: "16px" }}>
          {/* 1. Executive Master Strategy */}
          <div
            className="card"
            style={{
              background: "linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(14, 165, 233, 0.1) 100%)",
              border: "1.5px solid var(--border)",
              padding: "18px 20px",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
              <span style={{ fontSize: "22px" }}>🎯</span>
              <div style={{ fontWeight: 800, fontSize: "16px", color: "var(--text-heading)" }}>
                AI Executive Strategy for {goal} ({klass === "Degree" ? "Undergraduate" : `Class ${klass}`})
              </div>
            </div>
            <p style={{ margin: 0, fontSize: "14px", lineHeight: "1.6", color: "var(--text)" }}>
              {guidanceData.executive_strategy}
            </p>
          </div>

          {/* 2. Weak Area Action Plan */}
          {guidanceData.weak_area_action_plan && guidanceData.weak_area_action_plan.length > 0 && (
            <div>
              <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)", marginBottom: "8px" }}>
                🔍 Targeted Remediation for Input Weak Areas ({guidanceData.weak_area_action_plan.length})
              </div>
              <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))" }}>
                {guidanceData.weak_area_action_plan.map((item, idx) => (
                  <div
                    key={idx}
                    className="card"
                    style={{
                      background: "var(--card)",
                      border: "1px solid var(--border)",
                      padding: "14px 16px",
                      borderLeft: "4px solid var(--danger)",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                      <span style={{ fontWeight: 800, fontSize: "14px", color: "var(--danger)" }}>
                        {item.weak_area}
                      </span>
                      <span className="pill small" style={{ background: "rgba(239, 68, 68, 0.12)", color: "var(--danger)", border: "1px solid var(--danger)" }}>
                        Weak Area Priority
                      </span>
                    </div>

                    <div style={{ fontSize: "13px", color: "var(--text-heading)", marginTop: "6px" }}>
                      <strong>Tactical Remedy:</strong>
                      <div style={{ color: "var(--text)", marginTop: "2px", lineHeight: "1.4" }}>
                        {item.tactical_remedy}
                      </div>
                    </div>

                    <div style={{ fontSize: "13px", color: "var(--text-heading)", marginTop: "8px" }}>
                      <strong>Recommended Practice:</strong>
                      <div style={{ color: "var(--accent)", marginTop: "2px", lineHeight: "1.4", fontWeight: 600 }}>
                        {item.recommended_practice}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 3. Subject Time Allocation & Weekly Hours */}
          {guidanceData.subject_time_allocation && guidanceData.subject_time_allocation.length > 0 && (
            <div className="card" style={{ background: "var(--card)", border: "1px solid var(--border)" }}>
              <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)", marginBottom: "10px" }}>
                ⏱️ Weekly Study Time Allocation ({hours}h/day = {roundVal(hours * 7)} hrs/week)
              </div>
              <div style={{ display: "grid", gap: "10px" }}>
                {guidanceData.subject_time_allocation.map((alloc, idx) => (
                  <div key={idx}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", fontWeight: 600, marginBottom: "4px" }}>
                      <span style={{ color: "var(--text)" }}>{alloc.subject}</span>
                      <span style={{ color: "var(--accent)" }}>
                        {alloc.percentage}% • {alloc.weekly_hours} hrs/week
                      </span>
                    </div>
                    <div style={{ width: "100%", height: "8px", background: "var(--border)", borderRadius: "4px", overflow: "hidden" }}>
                      <div
                        style={{
                          width: `${Math.min(100, alloc.percentage)}%`,
                          height: "100%",
                          background: idx === 0 ? "var(--brand)" : idx === 1 ? "var(--accent)" : "var(--ok)",
                          borderRadius: "4px",
                          transition: "width 0.4s ease",
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 4. Milestone Timeline & Pitfalls */}
          <div className="grid-2 row">
            {guidanceData.milestone_timeline && guidanceData.milestone_timeline.length > 0 && (
              <div className="card" style={{ background: "var(--card-subtle)", border: "1px solid var(--border)" }}>
                <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--text-heading)", marginBottom: "8px" }}>
                  🚩 Milestone Roadmap
                </div>
                <div style={{ display: "grid", gap: "8px" }}>
                  {guidanceData.milestone_timeline.map((m, i) => (
                    <div key={i} style={{ padding: "8px 10px", background: "var(--card)", borderRadius: "8px", border: "1px solid var(--border)" }}>
                      <div style={{ fontWeight: 700, fontSize: "13px", color: "var(--accent)" }}>
                        {m.phase}: {m.milestone}
                      </div>
                      <div className="small note" style={{ marginTop: "2px" }}>{m.action}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {guidanceData.pitfalls_to_avoid && guidanceData.pitfalls_to_avoid.length > 0 && (
              <div className="card" style={{ background: "rgba(239, 68, 68, 0.08)", border: "1px solid rgba(239, 68, 68, 0.25)" }}>
                <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--danger)", marginBottom: "8px" }}>
                  ⚠️ Critical Pitfalls to Avoid
                </div>
                <ul style={{ margin: 0, paddingLeft: "18px", fontSize: "13px", color: "var(--danger)", display: "grid", gap: "6px" }}>
                  {guidanceData.pitfalls_to_avoid.map((pitfall, i) => (
                    <li key={i}>{pitfall}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Initial state placeholder */}
      {!guidanceData && !isLoading && (
        <div style={{ textAlign: "center", padding: "32px 20px", background: "var(--card-subtle)", borderRadius: "12px", border: "1px dashed var(--border)" }}>
          <div style={{ fontSize: "28px" }}>📋</div>
          <div style={{ fontWeight: 700, fontSize: "15px", color: "var(--text-heading)", marginTop: "8px" }}>
            Ready to Generate Your Personalized Study Guidance
          </div>
          <div className="small note" style={{ maxWidth: "480px", margin: "4px auto 14px auto" }}>
            Verify your target goal, class level, and any weak areas above, then click &quot;Generate AI Academic Guidance&quot; to synthesize an adaptive roadmap.
          </div>
          <button
            className="btn small"
            onClick={handleGenerate}
            style={{ background: "var(--brand)", color: "#ffffff", fontWeight: 700 }}
          >
            Generate Now ▶
          </button>
        </div>
      )}
    </div>
  );
}

function roundVal(num: number): number {
  return Math.round(num * 10) / 10;
}
