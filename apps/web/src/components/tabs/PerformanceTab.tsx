"use client";

import React, { useEffect, useRef, useState } from "react";
import { api, PerformanceSummary } from "@/lib/api";

declare global {
  interface Window {
    Chart: any;
  }
}

export default function PerformanceTab() {
  const chartWeekRef = useRef<HTMLCanvasElement>(null);
  const chartMonthRef = useRef<HTMLCanvasElement>(null);
  const chartYearRef = useRef<HTMLCanvasElement>(null);

  const chartWeekInst = useRef<any>(null);
  const chartMonthInst = useRef<any>(null);
  const chartYearInst = useRef<any>(null);

  const [summary, setSummary] = useState<PerformanceSummary | null>(null);
  const [attendanceLogs, setAttendanceLogs] = useState<Array<{ date: string; studied: boolean }>>([]);

  useEffect(() => {
    loadPerformance();
  }, []);

  const loadPerformance = async () => {
    try {
      const [perfData, attData] = await Promise.all([
        api.getPerformanceSummary(),
        api.getAttendance(),
      ]);
      setSummary(perfData);
      setAttendanceLogs(attData.history || []);
      renderCharts(perfData.charts);
    } catch (e) {
      console.error("Failed to load performance data:", e);
    }
  };

  const renderCharts = (chartsData: any) => {
    if (typeof window === "undefined" || !window.Chart) return;

    // Destroy existing instances
    if (chartWeekInst.current) chartWeekInst.current.destroy();
    if (chartMonthInst.current) chartMonthInst.current.destroy();
    if (chartYearInst.current) chartYearInst.current.destroy();

    // 1. Weekly Line Chart
    if (chartWeekRef.current) {
      chartWeekInst.current = new window.Chart(chartWeekRef.current, {
        type: "line",
        data: {
          labels: chartsData.labels_day || ["D1", "D2", "D3", "D4", "D5", "D6", "D7"],
          datasets: [
            {
              label: "% score",
              data: chartsData.by_day || [0, 0, 0, 0, 0, 0, 0],
              borderColor: "#4f46e5",
              backgroundColor: "rgba(79, 70, 229, 0.08)",
              fill: true,
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, max: 100 } },
        },
      });
    }

    // 2. Monthly Bar Chart
    if (chartMonthRef.current) {
      chartMonthInst.current = new window.Chart(chartMonthRef.current, {
        type: "bar",
        data: {
          labels: ["W1", "W2", "W3", "W4"],
          datasets: [
            {
              label: "Avg %",
              data: chartsData.weekly_avg || [0, 0, 0, 0],
              backgroundColor: "rgba(2, 132, 199, 0.2)",
              borderColor: "#0284c7",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, max: 100 } },
        },
      });
    }

    // 3. Yearly Line Chart
    if (chartYearRef.current) {
      chartYearInst.current = new window.Chart(chartYearRef.current, {
        type: "line",
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          datasets: [
            {
              label: "Avg %",
              data: chartsData.monthly_avg || new Array(12).fill(0),
              borderColor: "#0284c7",
              backgroundColor: "rgba(2, 132, 199, 0.06)",
              fill: true,
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, max: 100 } },
        },
      });
    }
  };

  return (
    <div id="panel-performance" className="card">
      {summary && summary.measured_metrics.total_assessments_taken === 0 && (
        <div style={{ background: "rgba(2, 132, 199, 0.06)", border: "1px solid rgba(2, 132, 199, 0.2)", borderRadius: "10px", padding: "12px 16px", marginBottom: "14px", display: "flex", alignItems: "center", gap: "12px" }}>
          <span style={{ fontSize: "24px" }}>📊</span>
          <div>
            <div style={{ fontWeight: 700, fontSize: "14px", color: "var(--accent)" }}>
              Awaiting Diagnostic Assessment Records
            </div>
            <div className="small note">
              No assessments or verified marks have been recorded yet for your student profile. Complete an adaptive diagnostic test in the &quot;Test&quot; tab or verify your marksheet to view your calibrated mastery and retention trajectories.
            </div>
          </div>
        </div>
      )}

      <div className="grid-3 row">
        <div className="card" style={{ background: "var(--card-subtle)" }}>
          <div style={{ fontWeight: 800, marginBottom: "6px" }}>Weekly</div>
          <canvas ref={chartWeekRef} width="320" height="160"></canvas>
        </div>
        <div className="card" style={{ background: "var(--card-subtle)" }}>
          <div style={{ fontWeight: 800, marginBottom: "6px" }}>Monthly</div>
          <canvas ref={chartMonthRef} width="320" height="160"></canvas>
        </div>
        <div className="card" style={{ background: "var(--card-subtle)" }}>
          <div style={{ fontWeight: 800, marginBottom: "6px" }}>Yearly</div>
          <canvas ref={chartYearRef} width="320" height="160"></canvas>
        </div>
      </div>

      <div className="hr"></div>

      {summary?.learning_twin && (
        <div className="card" style={{ background: "rgba(2, 132, 199, 0.04)", border: "1px solid rgba(2, 132, 199, 0.2)", marginBottom: "12px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "8px" }}>
            <div style={{ fontWeight: 800, color: "var(--accent)", fontSize: "15px" }}>🤖 AI Learning Twin Status</div>
            <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
              {summary.learning_twin.basis_source && (
                <span className="badge" style={{ color: "var(--accent)", borderColor: "var(--accent)", background: "rgba(56, 189, 248, 0.12)", fontSize: "11px", fontWeight: 700 }}>
                  📍 Derived From: {summary.learning_twin.basis_source}
                </span>
              )}
              <span className="badge" style={{ color: "var(--brand)", borderColor: "var(--brand)", background: "rgba(99, 102, 241, 0.12)" }}>
                {summary.learning_twin.status}
              </span>
            </div>
          </div>
          <div className="hr"></div>
          <div className="grid-3 row">
            <div>
              <label>Current Priority Focus</label>
              <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)" }}>
                {summary.learning_twin.current_focus_concept}
              </div>
              {summary.learning_twin.basis_source && (
                <div style={{ fontSize: "11px", color: "var(--accent)", fontWeight: 600, marginTop: "3px" }}>
                  Priority basis: {summary.learning_twin.basis_source}
                </div>
              )}
            </div>
            <div>
              <label>Cognitive Evidence (Why)</label>
              <div className="small note" style={{ lineHeight: "1.45" }}>{summary.learning_twin.why}</div>
            </div>
            <div>
              <label>Next Best Learning Action</label>
              <div style={{ fontWeight: 600, color: "var(--text)", lineHeight: "1.45" }}>{summary.learning_twin.next_best_action}</div>
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <div style={{ fontWeight: 800, marginBottom: "6px" }}>Daily Attendance (Parents view)</div>
        <div id="attendanceList" className="list" style={{ maxHeight: "200px", overflow: "auto" }}>
          {attendanceLogs.length > 0 ? (
            attendanceLogs.map((log, i) => (
              <li key={i}>
                <span>{log.date}</span>
                <span>{log.studied ? "✅ Studied" : "❌ Missed"}</span>
              </li>
            ))
          ) : (
            <li className="small">No study days recorded yet.</li>
          )}
        </div>
        <div className="note" style={{ marginTop: "8px" }}>
          Parents can verify student activity; &quot;Mark Today Studied&quot; on Dashboard records a day.
        </div>
      </div>
    </div>
  );
}
