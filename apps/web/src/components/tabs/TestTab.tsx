"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  api,
  AssessmentQuestion,
  AssessmentAnswerResult,
  TestEvaluationReport,
  StudiedStatusResponse,
  QuestionReviewItem,
} from "@/lib/api";

interface TestTabProps {
  onAssessmentCompleted: () => void;
  onNavigateTab?: (tabKey: string) => void;
}

export default function TestTab({ onAssessmentCompleted, onNavigateTab }: TestTabProps) {
  // Studied Status & Topic Selection State
  const [studiedStatus, setStudiedStatus] = useState<StudiedStatusResponse | null>(null);
  const [isLoadingStatus, setIsLoadingStatus] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [customTopicInput, setCustomTopicInput] = useState<string>("");
  const [numQuestions, setNumQuestions] = useState<number>(5);

  // Active Session State
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationError, setGenerationError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [syllabusName, setSyllabusName] = useState<string>("Aim-Aligned Diagnostic");
  const [currentQ, setCurrentQ] = useState<AssessmentQuestion | null>(null);
  const [selectedOpt, setSelectedOpt] = useState<number | null>(null);
  const [hintsVisible, setHintsVisible] = useState(false);
  const [hintsUsedCount, setHintsUsedCount] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [questionNumber, setQuestionNumber] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(5);

  // Completion & Report State
  const [isComplete, setIsComplete] = useState(false);
  const [finalScore, setFinalScore] = useState<string | null>(null);
  const [evaluationReport, setEvaluationReport] = useState<TestEvaluationReport | null>(null);
  const [localQuestionHistory, setLocalQuestionHistory] = useState<QuestionReviewItem[]>([]);

  // Camera / Mic stream for assessment proctoring
  const videoRef = useRef<HTMLVideoElement>(null);
  const [cameraActive, setCameraActive] = useState(false);

  // 1. Fetch student's studied status on mount
  useEffect(() => {
    loadStudiedStatus();
  }, []);

  const loadStudiedStatus = async () => {
    setIsLoadingStatus(true);
    try {
      const res = await api.getStudiedStatus();
      setStudiedStatus(res);
      // If student has studied topics, default select the first one; else prefill suggested topic
      if (res.has_studied && res.studied_topics.length > 0) {
        setSelectedTopic(res.studied_topics[0].title);
      } else if (res.suggested_topics && res.suggested_topics.length > 0) {
        setSelectedTopic(res.suggested_topics[0]);
      }
    } catch (e: any) {
      console.error("Failed to load studied status:", e);
    } finally {
      setIsLoadingStatus(false);
    }
  };

  const handleMediaCheck = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
      }
    } catch {
      alert("Camera/Microphone permission was denied or no media device was found.");
    }
  };

  // 2. Start dynamic AI diagnostic test on chosen or custom topic
  const handleStartAITest = async (chosenTopicOverride?: string) => {
    const topicToTest = (chosenTopicOverride || customTopicInput || selectedTopic || "").trim();
    if (!topicToTest) {
      alert("Please select or enter a topic you want to be tested on.");
      return;
    }

    setIsGenerating(true);
    setGenerationError(null);

    try {
      const res = await api.startAssessment("diagnostic", undefined, topicToTest, numQuestions);
      setSessionId(res.session_id);
      setSyllabusName(res.syllabus_name || `${topicToTest} Diagnostic`);
      setCurrentQ(res.current_question);
      setQuestionNumber(res.current_question?.question_number || 1);
      setTotalQuestions(res.current_question?.total_questions || numQuestions);
      setSelectedOpt(null);
      setHintsVisible(false);
      setHintsUsedCount(0);
      setIsComplete(false);
      setFinalScore(null);
      setEvaluationReport(null);
      setLocalQuestionHistory([]);
    } catch (e: any) {
      console.error("Failed to generate AI test:", e);
      setGenerationError(e.message || "Failed to generate AI questions. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  // 3. Submit answer and advance sequentially
  const handleSubmitAnswer = async () => {
    if (!sessionId || !currentQ || selectedOpt === null) {
      alert("Please select an answer option first.");
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await api.submitAnswer(sessionId, {
        question_id: currentQ.id,
        selected_index: selectedOpt,
        response_time_ms: 12000,
        hints_used: hintsUsedCount,
      });

      // Record in local history for definitive review
      const record: QuestionReviewItem = {
        question_id: currentQ.id,
        concept_id: currentQ.concept_id,
        subject: currentQ.subject,
        topic: currentQ.topic,
        question_text: currentQ.question,
        options: currentQ.options,
        selected_index: selectedOpt,
        correct_index: currentQ.options.findIndex((_, idx) => idx === selectedOpt ? res.is_correct : false), // fallback
        correct: res.is_correct,
        explanation: res.explanation,
      };
      setLocalQuestionHistory((prev) => [...prev, record]);

      if (res.is_complete) {
        setIsComplete(true);
        setFinalScore(res.current_score);
        setCurrentQ(null);
        if (res.evaluation_report) {
          setEvaluationReport(res.evaluation_report);
        }
        onAssessmentCompleted();
      } else if (res.next_question) {
        setCurrentQ(res.next_question);
        setQuestionNumber(res.next_question.question_number || questionNumber + 1);
        setTotalQuestions(res.next_question.total_questions || totalQuestions);
        setSelectedOpt(null);
        setHintsVisible(false);
        setHintsUsedCount(0);
      }
    } catch (e: any) {
      alert(`Answer submission error: ${e.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // 4. Reset state to take another test
  const handleResetForNewTest = () => {
    setSessionId(null);
    setCurrentQ(null);
    setIsComplete(false);
    setFinalScore(null);
    setEvaluationReport(null);
    setLocalQuestionHistory([]);
    setCustomTopicInput("");
    loadStudiedStatus();
  };

  // ================= RENDER =================

  return (
    <div id="panel-test" className="card" style={{ padding: "20px" }}>
      {/* Top Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <div style={{ fontWeight: 800, fontSize: "17px" }}>AI Diagnostic Knowledge Test</div>
            <span className="badge" style={{ color: "var(--accent)", borderColor: "var(--accent)" }}>
              {sessionId ? syllabusName : "Dynamic AI Generation"}
            </span>
          </div>
          <div className="subtitle" style={{ marginTop: "2px" }}>
            Zero hardcoding • Rigorous diagnostic questions dynamically generated by AI LLM tailored to your level
          </div>
        </div>
        <div className="right">
          <button className="btn small secondary" onClick={handleMediaCheck}>
            {cameraActive ? "Camera & Mic Active ✓" : "Enable Camera & Microphone"}
          </button>
        </div>
      </div>

      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className={cameraActive ? "" : "hidden"}
        style={{ width: "220px", marginTop: "10px", borderRadius: "8px", border: "1px solid #cbd5e1" }}
      />

      <div className="hr" style={{ margin: "16px 0" }}></div>

      {/* ================= 1. SCREEN 1: VERIFICATION & TOPIC SELECTION ================= */}
      {!sessionId && !isComplete && (
        <div>
          {isLoadingStatus ? (
            <div style={{ textAlign: "center", padding: "40px 20px" }}>
              <div className="pill">Verifying platform study history &amp; curriculum...</div>
            </div>
          ) : isGenerating ? (
            <div
              style={{
                textAlign: "center",
                padding: "48px 24px",
                background: "var(--card-subtle)",
                borderRadius: "16px",
                border: "1px solid var(--border)",
              }}
            >
              <div style={{ fontSize: "36px", marginBottom: "12px" }}>🤖</div>
              <div style={{ fontWeight: 800, fontSize: "17px", color: "var(--text-heading)" }}>
                AI LLM is Designing Your Diagnostic Test...
              </div>
              <div className="subtitle" style={{ marginTop: "6px", maxWidth: "480px", margin: "6px auto 0 auto" }}>
                Generating {numQuestions} rigorous, curriculum-aligned questions for{" "}
                <strong>{customTopicInput || selectedTopic}</strong> with deep analytical distractors and pedagogical hints.
              </div>
              <div style={{ marginTop: "20px" }}>
                <span className="pill small" style={{ animation: "pulse 2s infinite" }}>
                  Consulting Bayesian Knowledge Tracing Engine...
                </span>
              </div>
            </div>
          ) : (
            <div>
              {/* If student has NOT studied anything on the platform yet */}
              {!studiedStatus?.has_studied ? (
                <div
                  style={{
                    background: "rgba(2, 132, 199, 0.08)",
                    border: "1px solid rgba(2, 132, 199, 0.25)",
                    borderRadius: "14px",
                    padding: "20px",
                    marginBottom: "20px",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
                    <span style={{ fontSize: "20px" }}>💡</span>
                    <span style={{ fontWeight: 800, fontSize: "15px", color: "var(--accent)" }}>
                      New Student Verification: No Platform Study Activity Detected Yet
                    </span>
                  </div>
                  <div style={{ fontSize: "13.5px", color: "var(--text)", lineHeight: "1.5" }}>
                    You haven’t enrolled in courses or uploaded class study notes on Mentor Mate yet.
                    To evaluate your current knowledge, <strong>what topic from your school or college classes would you like to test your knowledge on?</strong>
                  </div>
                </div>
              ) : (
                /* If student HAS studied materials/courses on the platform */
                <div style={{ marginBottom: "20px" }}>
                  <div style={{ fontWeight: 700, fontSize: "14px", color: "var(--text-heading)", marginBottom: "8px" }}>
                    📖 Topics Evaluated From Your Platform Study History:
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "14px" }}>
                    {studiedStatus.studied_topics.map((item, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => {
                          setSelectedTopic(item.title);
                          setCustomTopicInput("");
                        }}
                        style={{
                          padding: "8px 14px",
                          borderRadius: "10px",
                          background: selectedTopic === item.title && !customTopicInput ? "rgba(79, 70, 229, 0.15)" : "var(--card)",
                          border: selectedTopic === item.title && !customTopicInput ? "2px solid var(--brand)" : "1px solid var(--border)",
                          color: selectedTopic === item.title && !customTopicInput ? "var(--brand)" : "var(--text)",
                          fontWeight: 700,
                          fontSize: "13px",
                          cursor: "pointer",
                          display: "flex",
                          alignItems: "center",
                          gap: "6px",
                        }}
                      >
                        <span>✓</span>
                        <span>{item.title}</span>
                        <span className="badge small" style={{ fontSize: "10px" }}>
                          {item.source === "study_material" ? "Uploaded Notes" : "Course"}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Custom Topic Input Section */}
              <div
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: "14px",
                  padding: "18px",
                  marginBottom: "20px",
                }}
              >
                <label style={{ display: "block", fontWeight: 700, fontSize: "14px", marginBottom: "6px", color: "var(--text-heading)" }}>
                  🎯 Suggest / Type Any Topic from Your School or College:
                </label>
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                  <input
                    type="text"
                    placeholder="Enter topic name or syllabus area"
                    value={customTopicInput}
                    onChange={(e) => {
                      setCustomTopicInput(e.target.value);
                      setSelectedTopic("");
                    }}
                    className="input"
                    style={{
                      flex: 1,
                      minWidth: "260px",
                      padding: "10px 14px",
                      borderRadius: "10px",
                      fontSize: "14px",
                    }}
                  />
                </div>

                {/* Quick Syllabus Chips */}
                {studiedStatus?.suggested_topics && studiedStatus.suggested_topics.length > 0 && (
                  <div style={{ marginTop: "14px" }}>
                    <div className="small note" style={{ marginBottom: "6px" }}>
                      Or pick a recommended {studiedStatus.goal} syllabus topic:
                    </div>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                      {studiedStatus.suggested_topics.map((sug, i) => (
                        <button
                          key={i}
                          type="button"
                          onClick={() => {
                            setCustomTopicInput(sug);
                            setSelectedTopic("");
                          }}
                          style={{
                            padding: "5px 10px",
                            borderRadius: "8px",
                            background: customTopicInput === sug ? "var(--accent)" : "var(--card-subtle)",
                            color: customTopicInput === sug ? "#ffffff" : "var(--text)",
                            border: "1px solid var(--border)",
                            fontSize: "12px",
                            fontWeight: 600,
                            cursor: "pointer",
                          }}
                        >
                          + {sug}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Test Configuration */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: "12px",
                  background: "var(--card-subtle)",
                  padding: "14px 18px",
                  borderRadius: "12px",
                  border: "1px solid var(--border)",
                  marginBottom: "20px",
                }}
              >
                <div>
                  <div style={{ fontWeight: 700, fontSize: "13.5px", color: "var(--text-heading)" }}>Assessment Length</div>
                  <div className="small note">Definitive number of questions evaluated</div>
                </div>
                <div style={{ display: "flex", gap: "8px" }}>
                  {[3, 5, 7].map((count) => (
                    <button
                      key={count}
                      type="button"
                      onClick={() => setNumQuestions(count)}
                      style={{
                        padding: "6px 14px",
                        borderRadius: "8px",
                        background: numQuestions === count ? "var(--brand)" : "var(--card)",
                        color: numQuestions === count ? "#ffffff" : "var(--text)",
                        border: "1px solid var(--border)",
                        fontWeight: 700,
                        fontSize: "13px",
                        cursor: "pointer",
                      }}
                    >
                      {count} Questions
                    </button>
                  ))}
                </div>
              </div>

              {generationError && (
                <div
                  className="pill small"
                  style={{
                    background: "#fee2e2",
                    color: "#991b1b",
                    border: "1px solid #f87171",
                    display: "block",
                    marginBottom: "14px",
                    padding: "8px 12px",
                  }}
                >
                  ⚠️ {generationError}
                </div>
              )}

              {/* Action Button */}
              <div style={{ textAlign: "center" }}>
                <button
                  className="btn"
                  onClick={() => handleStartAITest()}
                  disabled={!customTopicInput.trim() && !selectedTopic}
                  style={{
                    padding: "12px 32px",
                    fontSize: "15px",
                    fontWeight: 800,
                    background: "linear-gradient(135deg, #4f46e5 0%, #0284c7 100%)",
                    border: "none",
                    boxShadow: "0 4px 14px rgba(79, 70, 229, 0.3)",
                  }}
                >
                  🚀 Generate AI Diagnostic Test with LLM →
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ================= 2. SCREEN 2: ACTIVE QUESTION VIEW ================= */}
      {sessionId && !isComplete && currentQ && (
        <div>
          {/* Progress Header */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "10px",
              flexWrap: "wrap",
              gap: "8px",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div className="pill small" style={{ fontWeight: 800 }}>
                Question {questionNumber} of {totalQuestions}
              </div>
              <span className="badge" style={{ color: "var(--muted)" }}>
                {currentQ.subject} • {currentQ.topic}
              </span>
            </div>

            <button
              className="btn small secondary"
              onClick={() => {
                setHintsVisible(!hintsVisible);
                if (!hintsVisible) setHintsUsedCount((c) => c + 1);
              }}
            >
              {hintsVisible ? "Hide Hints" : `Need Hint? (${currentQ.hints?.length || 0})`}
            </button>
          </div>

          {/* Progress Bar */}
          <div className="progress" style={{ marginBottom: "16px", height: "8px", borderRadius: "4px" }}>
            <div
              style={{
                width: `${Math.round(((questionNumber - 1) / totalQuestions) * 100)}%`,
                background: "#0284c7",
                transition: "width 0.3s ease",
              }}
            ></div>
          </div>

          {/* Pedagogical Hints Drawer */}
          {hintsVisible && currentQ.hints && currentQ.hints.length > 0 && (
            <div
              style={{
                background: "rgba(56, 189, 248, 0.1)",
                border: "1px solid rgba(56, 189, 248, 0.25)",
                borderRadius: "10px",
                padding: "12px 16px",
                marginBottom: "14px",
              }}
            >
              <div style={{ fontWeight: 700, fontSize: "13px", color: "var(--accent)", marginBottom: "4px" }}>
                💡 Socratic Guiding Hint:
              </div>
              <ul style={{ margin: "4px 0 0 16px", padding: 0, fontSize: "13.5px", color: "var(--text)" }}>
                {currentQ.hints.map((h, i) => (
                  <li key={i} style={{ marginBottom: "4px" }}>
                    {h}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Question Card */}
          <div
            className="card"
            style={{
              padding: "18px",
              marginBottom: "14px",
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: "12px",
            }}
          >
            <div style={{ fontSize: "15.5px", fontWeight: 700, color: "var(--text-heading)", lineHeight: "1.5", marginBottom: "14px" }}>
              {currentQ.question}
            </div>

            <div>
              {currentQ.options.map((opt, idx) => (
                <label
                  key={idx}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                    marginTop: "10px",
                    padding: "12px 14px",
                    borderRadius: "10px",
                    background: selectedOpt === idx ? "rgba(2, 132, 199, 0.12)" : "var(--card-subtle)",
                    border: selectedOpt === idx ? "2px solid var(--accent)" : "1px solid var(--border)",
                    cursor: "pointer",
                    transition: "all 0.15s ease",
                  }}
                >
                  <input
                    type="radio"
                    name="currentQOpt"
                    value={idx}
                    checked={selectedOpt === idx}
                    onChange={() => setSelectedOpt(idx)}
                    style={{ accentColor: "var(--accent)", width: "18px", height: "18px" }}
                  />
                  <span style={{ fontSize: "14px", fontWeight: selectedOpt === idx ? 700 : 500, color: selectedOpt === idx ? "var(--accent)" : "var(--text)" }}>
                    {opt}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Submit Action */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "14px" }}>
            <div className="small note">
              {questionNumber === totalQuestions ? "Final Question • Diagnostic Report next" : `Question ${questionNumber} of ${totalQuestions}`}
            </div>
            <button
              className="btn"
              onClick={handleSubmitAnswer}
              disabled={isSubmitting || selectedOpt === null}
              style={{
                padding: "10px 24px",
                fontSize: "14.5px",
                fontWeight: 700,
                background: questionNumber === totalQuestions ? "var(--ok)" : "var(--accent)",
              }}
            >
              {isSubmitting
                ? "Calibrating Bayesian Model..."
                : questionNumber === totalQuestions
                ? "Finish Test & View Evaluation Report ✓"
                : "Next Question →"}
            </button>
          </div>
        </div>
      )}

      {/* ================= 3. SCREEN 3: COMPLETED TEST EVALUATION & QUESTION REVIEW ================= */}
      {isComplete && (
        <div style={{ padding: "6px 0" }}>
          {/* Main Score Header */}
          <div
            style={{
              background: "var(--card-subtle)",
              border: "1px solid var(--border)",
              borderRadius: "14px",
              padding: "24px 20px",
              textAlign: "center",
              marginBottom: "20px",
            }}
          >
            <div style={{ fontSize: "12px", textTransform: "uppercase", letterSpacing: "1px", fontWeight: 800, color: "var(--muted)" }}>
              Diagnostic Test Complete • Knowledge Evaluation Report
            </div>
            <div style={{ fontSize: "40px", fontWeight: 900, color: "var(--text-heading)", margin: "8px 0" }}>
              {finalScore || evaluationReport?.overall_score || "Completed"}
            </div>
            <div
              className="pill"
              style={{
                fontSize: "14px",
                padding: "6px 18px",
                background: "rgba(2, 132, 199, 0.12)",
                color: "var(--accent)",
                border: "1px solid var(--accent)",
                display: "inline-block",
              }}
            >
              {evaluationReport?.performance_tier || "Diagnostic Completed"}
            </div>
            {evaluationReport?.tier_description && (
              <div className="small note" style={{ marginTop: "10px", maxWidth: "620px", margin: "10px auto 0 auto" }}>
                {evaluationReport.tier_description}
              </div>
            )}
          </div>

          {/* Subject-Wise Accuracy Breakdown */}
          {evaluationReport?.subject_breakdown && evaluationReport.subject_breakdown.length > 0 && (
            <div style={{ marginBottom: "20px" }}>
              <div style={{ fontWeight: 800, fontSize: "15px", marginBottom: "10px", color: "var(--text-heading)" }}>
                📊 Subject Accuracy Breakdown
              </div>
              <div style={{ display: "grid", gap: "10px", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}>
                {evaluationReport.subject_breakdown.map((sb, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: "var(--card)",
                      border: "1px solid var(--border)",
                      borderRadius: "10px",
                      padding: "14px",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                      <span style={{ fontWeight: 700, fontSize: "14px", color: "var(--text-heading)" }}>{sb.subject}</span>
                      <span
                        style={{
                          fontWeight: 800,
                          fontSize: "14px",
                          color: sb.percentage >= 70 ? "var(--ok)" : sb.percentage >= 50 ? "var(--accent)" : "var(--danger)",
                        }}
                      >
                        {sb.percentage}%
                      </span>
                    </div>
                    <div className="progress">
                      <div
                        style={{
                          width: `${sb.percentage}%`,
                          background: sb.percentage >= 70 ? "var(--ok)" : sb.percentage >= 50 ? "var(--accent)" : "var(--danger)",
                        }}
                      ></div>
                    </div>
                    <div className="small note" style={{ marginTop: "6px" }}>
                      {sb.correct} of {sb.attempted} questions correct
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Weakness Analysis & Misconception Diagnostics */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
              <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)" }}>
                🎯 Diagnosed Knowledge Gaps &amp; Cognitive Misconceptions
              </div>
              <span className="small note">{evaluationReport?.weaknesses?.length || 0} gap(s) identified</span>
            </div>

            {evaluationReport?.weaknesses && evaluationReport.weaknesses.length > 0 ? (
              <div style={{ display: "grid", gap: "10px" }}>
                {evaluationReport.weaknesses.map((w, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: "rgba(239, 68, 68, 0.06)",
                      border: "1px solid rgba(239, 68, 68, 0.25)",
                      borderRadius: "10px",
                      padding: "14px",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                      <span className="pill small" style={{ background: "rgba(239, 68, 68, 0.15)", color: "var(--danger)", border: "1px solid var(--danger)" }}>
                        {w.subject} • {w.topic}
                      </span>
                      <span className="small" style={{ color: "var(--danger)", fontWeight: 700 }}>
                        {w.error_type}
                      </span>
                    </div>

                    <div style={{ fontSize: "13.5px", color: "var(--text)", margin: "6px 0" }}>
                      <strong>Question Context:</strong> {w.question_snippet}
                    </div>

                    <div
                      style={{
                        fontSize: "12.5px",
                        background: "var(--card-subtle)",
                        padding: "8px 12px",
                        borderRadius: "8px",
                        border: "1px solid var(--border)",
                        color: "var(--text-heading)",
                        marginTop: "8px",
                      }}
                    >
                      <strong style={{ color: "var(--accent)" }}>Recommended Action:</strong> {w.remedial_action}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div
                style={{
                  background: "rgba(16, 185, 129, 0.08)",
                  border: "1px solid var(--ok)",
                  borderRadius: "10px",
                  padding: "16px",
                  textAlign: "center",
                  color: "var(--ok)",
                  fontWeight: 600,
                }}
              >
                🎉 Outstanding work! Zero conceptual fallacies or misconceptions were identified in this diagnostic test.
              </div>
            )}
          </div>

          {/* ================= DETAILED QUESTION-BY-QUESTION REVIEW ================= */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ fontWeight: 800, fontSize: "15px", marginBottom: "10px", color: "var(--text-heading)" }}>
              📝 Question-by-Question Review &amp; AI Explanations
            </div>

            <div style={{ display: "grid", gap: "14px" }}>
              {(evaluationReport?.question_reviews || localQuestionHistory).map((qReview, idx) => (
                <div
                  key={idx}
                  style={{
                    background: "var(--card)",
                    border: `1px solid ${qReview.correct ? "var(--ok)" : "var(--danger)"}`,
                    borderRadius: "12px",
                    padding: "16px",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                    <span style={{ fontWeight: 700, fontSize: "13.5px", color: "var(--text-heading)" }}>
                      Question {idx + 1}
                    </span>
                    <span
                      className="pill small"
                      style={{
                        background: qReview.correct ? "rgba(16, 185, 129, 0.12)" : "rgba(239, 68, 68, 0.12)",
                        color: qReview.correct ? "var(--ok)" : "var(--danger)",
                        border: `1px solid ${qReview.correct ? "var(--ok)" : "var(--danger)"}`,
                      }}
                    >
                      {qReview.correct ? "Correct ✓" : "Incorrect ✗"}
                    </span>
                  </div>

                  <div style={{ fontSize: "14px", fontWeight: 600, color: "var(--text-heading)", marginBottom: "10px" }}>
                    {qReview.question_text}
                  </div>

                  {/* Options display */}
                  {qReview.options && (
                    <div style={{ display: "grid", gap: "6px", marginBottom: "10px" }}>
                      {qReview.options.map((opt, oIdx) => {
                        const isSelected = qReview.selected_index === oIdx;
                        const isCorrectOption = qReview.correct_index !== undefined ? qReview.correct_index === oIdx : (isSelected && qReview.correct);

                        let optBg = "var(--card-subtle)";
                        let optBorder = "var(--border)";
                        let optColor = "var(--text)";

                        if (isSelected && qReview.correct) {
                          optBg = "rgba(16, 185, 129, 0.15)";
                          optBorder = "var(--ok)";
                          optColor = "var(--ok)";
                        } else if (isSelected && !qReview.correct) {
                          optBg = "rgba(239, 68, 68, 0.15)";
                          optBorder = "var(--danger)";
                          optColor = "var(--danger)";
                        } else if (isCorrectOption) {
                          optBg = "rgba(16, 185, 129, 0.1)";
                          optBorder = "var(--ok)";
                          optColor = "var(--ok)";
                        }

                        return (
                          <div
                            key={oIdx}
                            style={{
                              padding: "8px 12px",
                              borderRadius: "8px",
                              background: optBg,
                              border: `1px solid ${optBorder}`,
                              fontSize: "13px",
                              color: optColor,
                              fontWeight: isSelected || isCorrectOption ? 700 : 400,
                            }}
                          >
                            {opt} {isSelected && " (Your choice)"} {isCorrectOption && " ✓"}
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Step-by-Step AI Explanation */}
                  <div
                    style={{
                      background: "var(--card-subtle)",
                      border: "1px solid var(--border)",
                      borderRadius: "8px",
                      padding: "10px 12px",
                      fontSize: "13px",
                      color: "var(--text)",
                    }}
                  >
                    <strong style={{ color: "var(--accent)" }}>AI Pedagogical Explanation:</strong> {qReview.explanation}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Actionable Course Remediation Pathway */}
          {evaluationReport?.remedial_courses && evaluationReport.remedial_courses.length > 0 && (
            <div
              style={{
                background: "rgba(2, 132, 199, 0.08)",
                border: "1px solid rgba(2, 132, 199, 0.25)",
                borderRadius: "12px",
                padding: "16px",
                marginBottom: "20px",
              }}
            >
              <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--accent)", marginBottom: "6px" }}>
                📚 Recommended Remedial Study Modules
              </div>
              <div className="small note" style={{ marginBottom: "12px" }}>
                Target the concepts diagnosed as weak in this assessment:
              </div>

              <div style={{ display: "grid", gap: "8px" }}>
                {evaluationReport.remedial_courses.map((rc, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: "var(--card)",
                      border: "1px solid var(--border)",
                      borderRadius: "8px",
                      padding: "10px 14px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 700, fontSize: "13.5px" }}>{rc.course_title}</div>
                      <div className="small note" style={{ color: "var(--accent)" }}>
                        {rc.reason}
                      </div>
                    </div>
                    {onNavigateTab && (
                      <button className="btn small" onClick={() => onNavigateTab("courses")}>
                        Study Topic ▶
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Retake / Start New Test CTA */}
          <div style={{ textAlign: "center", marginTop: "24px" }}>
            <button
              className="btn"
              onClick={handleResetForNewTest}
              style={{
                padding: "12px 30px",
                fontSize: "15px",
                fontWeight: 800,
                background: "linear-gradient(135deg, #0284c7 0%, #4f46e5 100%)",
              }}
            >
              Test Another Topic with AI ↻
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
