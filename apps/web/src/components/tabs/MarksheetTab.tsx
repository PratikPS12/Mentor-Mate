"use client";

import React, { useState } from "react";
import { api, StudentProfile } from "@/lib/api";

interface MarksheetTabProps {
  profile: StudentProfile | null;
  onMarksheetVerified: () => void;
}

interface SubjectEntry {
  subject: string;
  marks_obtained: number;
  maximum_marks: number;
  percentage: number;
  grade: string;
  confidence: number;
}

export default function MarksheetTab({ profile, onMarksheetVerified }: MarksheetTabProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [docId, setDocId] = useState<string | null>(null);
  const [candidateName, setCandidateName] = useState<string>(profile?.name || "");
  const [institution, setInstitution] = useState<string>(profile?.school || "Affiliated School");
  const [examSession, setExamSession] = useState<string>("Academic Session 2025-26");
  const [subjects, setSubjects] = useState<SubjectEntry[]>([]);
  const [ocrConfidence, setOcrConfidence] = useState<number>(0);
  const [extractionNote, setExtractionNote] = useState<string>("");
  const [isAnalyzed, setIsAnalyzed] = useState(false);
  const [showUploadForm, setShowUploadForm] = useState(!profile?.marksheet_verified);

  // New subject row inputs
  const [newSubName, setNewSubName] = useState("");
  const [newSubObtained, setNewSubObtained] = useState<number | "">("");
  const [newSubMax, setNewSubMax] = useState<number | "">(100);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    setFile(selected);
    setIsAnalyzed(false);
    setDocId(null);
    setSubjects([]);
  };

  const handleScan = async () => {
    // Strict requirement: proceed ONLY if a marksheet file has been uploaded by the user
    if (!file) {
      alert("No marksheet file selected. Please choose a PDF, JPG, PNG, or TXT file to proceed.");
      return;
    }

    setIsScanning(true);
    try {
      const res = await api.uploadMarksheet(file);
      setDocId(res.document_id);
      const ext = res.extraction;
      setCandidateName(ext.candidate_name || profile?.name || "Student");
      setInstitution(ext.institution || profile?.school || "Affiliated School");
      setExamSession(ext.exam_session || "Academic Session");
      setOcrConfidence(ext.overall_confidence || 0);
      setExtractionNote(ext.extraction_note || "");
      setSubjects(ext.subjects || []);
      setIsAnalyzed(true);
    } catch (e: any) {
      alert(`OCR Extraction error: ${e.message}`);
    } finally {
      setIsScanning(false);
    }
  };

  const handleAddSubject = () => {
    if (!newSubName.trim()) {
      alert("Please enter a subject name.");
      return;
    }
    const obtained = Number(newSubObtained);
    const maxMarks = Number(newSubMax) || 100;
    if (isNaN(obtained) || obtained < 0 || obtained > maxMarks) {
      alert(`Marks obtained must be between 0 and ${maxMarks}`);
      return;
    }
    const pct = Math.round((obtained / maxMarks) * 1000) / 10;
    const grade = pct >= 90 ? "A1" : pct >= 80 ? "A2" : pct >= 70 ? "B1" : pct >= 60 ? "B2" : "C";

    setSubjects([
      ...subjects,
      {
        subject: newSubName.trim(),
        marks_obtained: obtained,
        maximum_marks: maxMarks,
        percentage: pct,
        grade,
        confidence: 1.0,
      },
    ]);

    setNewSubName("");
    setNewSubObtained("");
    setNewSubMax(100);
  };

  const handleRemoveSubject = (index: number) => {
    setSubjects(subjects.filter((_, i) => i !== index));
  };

  const handleVerifyAndCalibrate = async () => {
    if (!file) {
      alert("A marksheet file must be uploaded before baseline calibration can proceed.");
      return;
    }
    if (!docId) {
      alert("Please click 'Analyze (OCR & Document AI)' first to extract records from your document.");
      return;
    }
    if (subjects.length === 0) {
      alert("Please add at least one subject and score from your marksheet before confirming.");
      return;
    }

    setIsVerifying(true);
    try {
      await api.verifyMarksheet({
        document_id: docId,
        student_name: candidateName,
        institution,
        exam_session: examSession,
        subjects,
      });
      alert("Marksheet verified successfully! Student model baseline calibrated across your subjects ✅");
      setShowUploadForm(false);
      onMarksheetVerified();
    } catch (e: any) {
      alert(`Verification failed: ${e.message}`);
    } finally {
      setIsVerifying(false);
    }
  };

  return (
    <div id="panel-uploads" className="card">
      {/* Existing Verified Marksheet Overview */}
      {profile?.marksheet_verified && profile.verified_marks && profile.verified_marks.length > 0 && !showUploadForm && (
        <div style={{ marginBottom: "16px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
            <div>
              <div style={{ fontWeight: 800, fontSize: "16px", color: "var(--ok)" }}>
                ✅ Verified Academic Record Active
              </div>
              <div className="subtitle">
                Calibrated against {profile.name}&apos;s verified marksheet • Institution: {profile.school || profile.board}
              </div>
            </div>
            <button className="btn small secondary" onClick={() => setShowUploadForm(true)}>
              Upload New / Updated Marksheet ↻
            </button>
          </div>

          <div className="hr"></div>

          <div style={{ display: "grid", gap: "10px", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))" }}>
            {profile.verified_marks.map((sub, i) => (
              <div
                key={i}
                style={{
                  background: "var(--card-subtle)",
                  padding: "10px 14px",
                  borderRadius: "10px",
                  border: "1px solid var(--border)",
                }}
              >
                <div style={{ fontWeight: 700, fontSize: "14px", color: "var(--text-heading)" }}>{sub.subject}</div>
                <div style={{ fontSize: "18px", fontWeight: 800, color: sub.percentage < 75 ? "var(--danger)" : "var(--accent)", marginTop: "4px" }}>
                  {sub.marks_obtained} / {sub.maximum_marks}
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", color: "var(--muted)", marginTop: "4px" }}>
                  <span>{sub.percentage}%</span>
                  <span style={{ fontWeight: 600 }}>Grade: {sub.grade || "A"}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="note" style={{ marginTop: "12px" }}>
            Cognitive Student Model: Concepts corresponding to these verified scores are calibrated in your Bayesian Knowledge Tracing engine.
          </div>
        </div>
      )}

      {/* Marksheet Upload Flow */}
      {showUploadForm && (
        <div className="row">
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <label style={{ fontSize: "14px", fontWeight: 700 }}>
                Step 1: Upload Genuine Marksheet Document (PDF / JPG / PNG / TXT)
              </label>
              {profile?.marksheet_verified && (
                <button
                  className="btn small secondary"
                  onClick={() => setShowUploadForm(false)}
                >
                  Cancel
                </button>
              )}
            </div>

            <div
              style={{
                marginTop: "8px",
                padding: "20px",
                border: "2px dashed #cbd5e1",
                borderRadius: "12px",
                background: file ? "#f0fdf4" : "#f8fafc",
                textAlign: "center",
                cursor: "pointer",
              }}
              onClick={() => document.getElementById("fileInput")?.click()}
            >
              <input
                id="fileInput"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.txt"
                style={{ display: "none" }}
                onChange={handleFileChange}
              />
              {file ? (
                <div>
                  <div style={{ fontSize: "28px" }}>📄</div>
                  <div style={{ fontWeight: 800, color: "var(--ok)", marginTop: "6px" }}>
                    {file.name}
                  </div>
                  <div className="small note">
                    {(file.size / 1024).toFixed(1)} KB • Ready for automated OCR analysis
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: "28px" }}>📁</div>
                  <div style={{ fontWeight: 700, marginTop: "6px" }}>
                    Click here or browse to select your marksheet
                  </div>
                  <div className="small note">
                    Accepts official board results, semester marksheets, or grade certificates.
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="note">
            ⚠️ Requirement: Document analysis and baseline calibration proceed <strong>only</strong> after an authentic marksheet is uploaded and verified.
          </div>

          <div className="right">
            <button
              className="btn"
              onClick={handleScan}
              disabled={!file || isScanning}
              style={{ opacity: !file ? 0.5 : 1.0, cursor: !file ? "not-allowed" : "pointer" }}
            >
              {isScanning ? "Analyzing Document (OCR & AI)..." : "Analyze (OCR & Document AI)"}
            </button>
          </div>

          {/* Step 2: Verification & Review Table */}
          {isAnalyzed && (
            <div
              style={{
                marginTop: "16px",
                background: "var(--card-subtle)",
                padding: "16px",
                borderRadius: "12px",
                border: "1px solid var(--border)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <div>
                  <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)" }}>
                    Step 2: Review Extracted Academic Records
                  </div>
                  <div className="subtitle">
                    Candidate: <strong>{candidateName}</strong> • Institution: <strong>{institution}</strong>
                  </div>
                </div>
                {ocrConfidence > 0 && (
                  <span className="badge" style={{ color: "var(--accent)", borderColor: "var(--accent)" }}>
                    OCR Quality: {Math.round(ocrConfidence * 100)}%
                  </span>
                )}
              </div>

              {extractionNote && (
                <div
                  className="small"
                  style={{
                    padding: "8px 12px",
                    borderRadius: "8px",
                    background: subjects.length > 0 ? "rgba(2, 132, 199, 0.08)" : "rgba(245, 158, 11, 0.1)",
                    color: subjects.length > 0 ? "#0369a1" : "#92400e",
                    marginBottom: "12px",
                  }}
                >
                  {extractionNote}
                </div>
              )}

              {/* Subject Table */}
              <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
                  <thead>
                    <tr style={{ textAlign: "left", borderBottom: "2px solid #e2e8f0" }}>
                      <th style={{ padding: "8px" }}>Subject</th>
                      <th style={{ padding: "8px" }}>Marks Obtained</th>
                      <th style={{ padding: "8px" }}>Max Marks</th>
                      <th style={{ padding: "8px" }}>Percentage</th>
                      <th style={{ padding: "8px" }}>Grade</th>
                      <th style={{ padding: "8px" }}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {subjects.length > 0 ? (
                      subjects.map((sub, idx) => (
                        <tr key={idx} style={{ borderBottom: "1px solid #e2e8f0" }}>
                          <td style={{ padding: "8px", fontWeight: 700 }}>{sub.subject}</td>
                          <td style={{ padding: "8px" }}>{sub.marks_obtained}</td>
                          <td style={{ padding: "8px" }}>{sub.maximum_marks}</td>
                          <td style={{ padding: "8px" }}>{sub.percentage}%</td>
                          <td style={{ padding: "8px" }}>
                            <span className="badge">{sub.grade || "—"}</span>
                          </td>
                          <td style={{ padding: "8px" }}>
                            <button
                              className="btn small secondary"
                              onClick={() => handleRemoveSubject(idx)}
                              style={{ color: "#ef4444" }}
                            >
                              ✕ Remove
                            </button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={6} style={{ padding: "16px", textAlign: "center", color: "#64748b" }}>
                          No subjects extracted yet. Add your marksheet subjects using the inputs below.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Add / Correct Subject Row */}
              <div
                style={{
                  marginTop: "12px",
                  padding: "10px",
                  background: "#ffffff",
                  borderRadius: "8px",
                  border: "1px solid #e2e8f0",
                  display: "grid",
                  gap: "8px",
                  gridTemplateColumns: "2fr 1fr 1fr auto",
                  alignItems: "center",
                }}
              >
                <input
                  className="input"
                  placeholder="Subject Name"
                  value={newSubName}
                  onChange={(e) => setNewSubName(e.target.value)}
                />
                <input
                  className="input"
                  type="number"
                  placeholder="Marks Obtained"
                  value={newSubObtained}
                  onChange={(e) => setNewSubObtained(e.target.value ? Number(e.target.value) : "")}
                />
                <input
                  className="input"
                  type="number"
                  placeholder="Max Marks"
                  value={newSubMax}
                  onChange={(e) => setNewSubMax(e.target.value ? Number(e.target.value) : "")}
                />
                <button className="btn small" onClick={handleAddSubject}>
                  + Add Subject
                </button>
              </div>

              {/* Step 3: Confirm & Calibrate */}
              <div className="right" style={{ marginTop: "16px" }}>
                <button
                  className="btn"
                  onClick={handleVerifyAndCalibrate}
                  disabled={isVerifying || subjects.length === 0}
                  style={{
                    opacity: subjects.length === 0 ? 0.5 : 1.0,
                    cursor: subjects.length === 0 ? "not-allowed" : "pointer",
                  }}
                >
                  {isVerifying ? "Calibrating Student Model..." : "Confirm & Calibrate Baseline ✓"}
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Study Materials & Lecture Notes (Grounded RAG Section) */}
      <StudyNotesSection />
    </div>
  );
}

function StudyNotesSection() {
  const [noteFile, setNoteFile] = useState<File | null>(null);
  const [noteTitle, setNoteTitle] = useState("");
  const [noteSubject, setNoteSubject] = useState("Mathematics");
  const [isUploading, setIsUploading] = useState(false);
  const [notesList, setNotesList] = useState<Array<{ id: string; title: string; filename: string; subject: string; chunks_count: number; created_at?: string }>>([]);
  const [isLoadingNotes, setIsLoadingNotes] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  const fetchNotes = async () => {
    setIsLoadingNotes(true);
    try {
      const res = await api.getUploadedNotes();
      setNotesList(res.materials || []);
    } catch {
      // ignore
    } finally {
      setIsLoadingNotes(false);
    }
  };

  React.useEffect(() => {
    fetchNotes();
  }, []);

  const handleUploadNotes = async () => {
    if (!noteFile) {
      alert("Please select a study material or lecture notes file (PDF, TXT).");
      return;
    }
    setIsUploading(true);
    setUploadMessage(null);
    try {
      const res = await api.uploadStudyNotes(noteFile, noteTitle.trim() || noteFile.name, noteSubject);
      setUploadMessage(`Success! Ingested "${res.title}" into ${res.chunks_indexed} semantic knowledge chunks.`);
      setNoteFile(null);
      setNoteTitle("");
      await fetchNotes();
    } catch (e: any) {
      alert(`Upload failed: ${e.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ marginTop: "32px", borderTop: "2px dashed var(--border)", paddingTop: "24px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "12px", marginBottom: "16px" }}>
        <div>
          <h3 style={{ margin: "0 0 4px 0", fontSize: "17px", fontWeight: 800, color: "var(--text-heading)" }}>
            📚 Grounded Knowledge Base & Study Notes (RAG)
          </h3>
          <p style={{ margin: 0, fontSize: "13px", color: "var(--muted)" }}>
            Upload lecture slides, personal formula sheets, or coaching notes (PDF, TXT). Mentor will index them into vector embeddings and cite them when answering your questions!
          </p>
        </div>
        <button className="btn ghost small" onClick={fetchNotes} disabled={isLoadingNotes}>
          {isLoadingNotes ? "Refreshing..." : "🔄 Refresh Notes"}
        </button>
      </div>

      {uploadMessage && (
        <div style={{ padding: "10px 14px", background: "rgba(16, 185, 129, 0.14)", border: "1px solid var(--ok)", borderRadius: "8px", color: "var(--ok)", fontSize: "13px", marginBottom: "14px", fontWeight: 600 }}>
          ✅ {uploadMessage}
        </div>
      )}

      {/* Upload Box */}
      <div style={{ background: "var(--card-subtle)", border: "1px solid var(--border)", borderRadius: "10px", padding: "16px", marginBottom: "20px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "12px", marginBottom: "12px" }}>
          <div>
            <label style={{ display: "block", fontSize: "12px", fontWeight: 700, color: "var(--muted)", marginBottom: "4px" }}>
              Document Title
            </label>
            <input
              className="input"
              placeholder="Enter document title or chapter name"
              value={noteTitle}
              onChange={(e) => setNoteTitle(e.target.value)}
            />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "12px", fontWeight: 700, color: "var(--muted)", marginBottom: "4px" }}>
              Subject
            </label>
            <select
              className="input"
              value={noteSubject}
              onChange={(e) => setNoteSubject(e.target.value)}
            >
              <option value="Mathematics">Mathematics</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Biology">Biology</option>
              <option value="General">General / Other</option>
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: "12px", fontWeight: 700, color: "var(--muted)", marginBottom: "4px" }}>
              File (PDF or TXT)
            </label>
            <input
              type="file"
              accept=".pdf,.txt"
              className="input"
              style={{ padding: "6px" }}
              onChange={(e) => setNoteFile(e.target.files?.[0] || null)}
            />
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            className="btn small"
            onClick={handleUploadNotes}
            disabled={isUploading || !noteFile}
            style={{ opacity: !noteFile || isUploading ? 0.6 : 1 }}
          >
            {isUploading ? "Chunking & Vector Indexing..." : "⚡ Ingest into RAG Vector Store"}
          </button>
        </div>
      </div>

      {/* Indexed Notes Table */}
      <div>
        <div style={{ fontWeight: 700, fontSize: "14px", color: "var(--text-heading)", marginBottom: "8px" }}>
          Indexed RAG Knowledge Documents ({notesList.length})
        </div>
        {notesList.length === 0 ? (
          <div style={{ padding: "16px", background: "var(--card-subtle)", borderRadius: "8px", textAlign: "center", color: "var(--muted)", fontSize: "13px", border: "1px solid var(--border)" }}>
            No study notes uploaded yet. Upload your PDF notes above to ground your AI Mentor in your personal class curriculum.
          </div>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table className="table" style={{ width: "100%", fontSize: "13px" }}>
              <thead>
                <tr>
                  <th>Title / Material</th>
                  <th>Subject</th>
                  <th>Filename</th>
                  <th>Indexed Chunks</th>
                  <th>Grounding Status</th>
                </tr>
              </thead>
              <tbody>
                {notesList.map((n) => (
                  <tr key={n.id}>
                    <td style={{ fontWeight: 600, color: "var(--text-heading)" }}>📄 {n.title}</td>
                    <td><span className="badge">{n.subject}</span></td>
                    <td style={{ color: "var(--muted)" }}>{n.filename}</td>
                    <td><strong style={{ color: "var(--accent)" }}>{n.chunks_count} chunks</strong></td>
                    <td>
                      <span className="badge" style={{ background: "rgba(16, 185, 129, 0.12)", color: "var(--ok)", borderColor: "var(--ok)" }}>
                        ✓ Grounded in Tutor RAG
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
