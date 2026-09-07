"use client";

import React, { useState, useEffect } from "react";
import { StudentProfile } from "@/lib/api";

interface ProfileTabProps {
  profile: StudentProfile | null;
  onSaveProfile: (updated: Partial<StudentProfile>) => Promise<void>;
}

interface FormErrors {
  name?: string;
  age?: string;
  goal?: string;
  school?: string;
}

export default function ProfileTab({ profile, onSaveProfile }: ProfileTabProps) {
  const [name, setName] = useState<string>("");
  const [age, setAge] = useState<number | string>("");
  const [klass, setKlass] = useState<string>("10");
  const [goal, setGoal] = useState<string>("");
  const [school, setSchool] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [weak, setWeak] = useState<string>("");
  const [courseNote, setCourseNote] = useState<string>("");
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [saveSuccessMsg, setSaveSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    if (profile) {
      setName(profile.name || "");
      const rawAge = profile.age;
      if (rawAge !== undefined && rawAge !== null && rawAge !== "") {
        const parsed = Number(rawAge);
        setAge(!isNaN(parsed) && parsed >= 10 && parsed <= 100 ? parsed : "");
      } else {
        setAge("");
      }
      setKlass(profile.klass || "10");
      setGoal(profile.goal || "");
      setSchool(profile.school || "");
      setEmail(profile.email || "");
      setWeak(profile.weak_areas ? profile.weak_areas.join(", ") : "");
      setCourseNote(profile.enrolled_courses ? profile.enrolled_courses.join(", ") : "");
    }
  }, [profile]);

  const activeErrors = Object.entries(errors)
    .filter(([_, msg]) => typeof msg === "string" && msg.trim().length > 0)
    .map(([_, msg]) => msg as string);

  const validate = (): boolean => {
    const errs: FormErrors = {};

    const trimmedName = name.trim();
    if (!trimmedName) {
      errs.name = "Full Name is required.";
    } else if (trimmedName.length < 2) {
      errs.name = "Full Name must be at least 2 characters.";
    } else if (trimmedName.length > 60) {
      errs.name = "Full Name cannot exceed 60 characters.";
    }

    if (age !== "" && age !== undefined && age !== null) {
      const numAge = Number(age);
      if (isNaN(numAge) || !Number.isInteger(numAge)) {
        errs.age = "Age must be a valid whole number.";
      } else if (numAge < 10) {
        errs.age = "Age must be at least 10.";
      } else if (numAge > 100) {
        errs.age = "Age cannot exceed 100.";
      }
    }

    const trimmedGoal = goal.trim();
    if (!trimmedGoal) {
      errs.goal = "Target exam or educational goal is required.";
    } else if (trimmedGoal.length > 100) {
      errs.goal = "Target goal cannot exceed 100 characters.";
    }

    if (school && school.trim().length > 100) {
      errs.school = "Institution name cannot exceed 100 characters.";
    }

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleAgeChange = (val: string) => {
    setAge(val);
    setErrors((prev) => {
      const next = { ...prev };
      if (val === "") {
        delete next.age;
        return next;
      }
      const num = Number(val);
      if (isNaN(num) || !Number.isInteger(num)) {
        next.age = "Age must be a whole number.";
      } else if (num < 10) {
        next.age = "Age must be at least 10.";
      } else if (num > 100) {
        next.age = "Age cannot exceed 100.";
      } else {
        delete next.age;
      }
      return next;
    });
  };

  const handleNameChange = (val: string) => {
    setName(val);
    setErrors((prev) => {
      const next = { ...prev };
      const trimmed = val.trim();
      if (!trimmed) {
        next.name = "Full Name is required.";
      } else if (trimmed.length < 2) {
        next.name = "Name must be at least 2 characters.";
      } else if (trimmed.length > 60) {
        next.name = "Name cannot exceed 60 characters.";
      } else {
        delete next.name;
      }
      return next;
    });
  };

  const handleSubmit = async () => {
    setSaveSuccessMsg(null);
    if (!validate()) {
      return;
    }

    setIsSaving(true);
    try {
      const weakList = weak.split(",").map((s) => s.trim()).filter(Boolean);
      const courseList = courseNote.split(",").map((s) => s.trim()).filter(Boolean);
      const validatedAge = age !== "" && age !== undefined && age !== null ? Number(age) : undefined;

      await onSaveProfile({
        name: name.trim(),
        age: validatedAge,
        klass,
        goal: goal.trim(),
        school: school.trim() || undefined,
        weak_areas: weakList,
        enrolled_courses: courseList,
      });
      setSaveSuccessMsg("Profile saved successfully to Mentor Mate database ✅");
      setTimeout(() => setSaveSuccessMsg(null), 5000);
    } catch (e: any) {
      alert(`Failed to save profile: ${e.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const getStandardTracksForKlass = (k: string): string[] => {
    if (k === "10") {
      return [
        "10th Boards (CBSE)",
        "10th Boards (ICSE)",
        "State Board",
        "NTSE & Olympiad",
        "Foundation (JEE/NEET)",
      ];
    }
    if (k === "11" || k === "12") {
      return [
        "JEE (Main & Advanced)",
        "NEET Medical",
        "State CET",
        "CUET Entrance",
        "12th Senior Secondary Boards",
      ];
    }
    // Undergraduate / Degree
    return [
      "GATE",
      "Software Engineering & Placements",
      "Data Science & AI",
      "CAT",
      "GRE / Higher Studies",
      "University Semester Core",
    ];
  };

  const handleKlassChange = (newKlass: string) => {
    setKlass(newKlass);
    const tracks = getStandardTracksForKlass(newKlass);
    setGoal(tracks[0]);
    setErrors((prev) => {
      const next = { ...prev };
      delete next.goal;
      return next;
    });
  };

  return (
    <div id="panel-profile" className="card" style={{ display: "grid", gap: "14px" }}>
      {saveSuccessMsg && (
        <div
          style={{
            padding: "10px 14px",
            background: "rgba(16, 185, 129, 0.14)",
            border: "1px solid var(--ok)",
            borderRadius: "8px",
            color: "var(--ok)",
            fontWeight: 600,
            fontSize: "13px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <span>{saveSuccessMsg}</span>
          <button
            onClick={() => setSaveSuccessMsg(null)}
            style={{ background: "none", border: "none", cursor: "pointer", fontWeight: 700, color: "var(--ok)" }}
          >
            ✕
          </button>
        </div>
      )}

      {activeErrors.length > 0 && (
        <div
          style={{
            padding: "10px 14px",
            background: "rgba(239, 68, 68, 0.1)",
            border: "1px solid #ef4444",
            borderRadius: "8px",
            color: "#b91c1c",
            fontSize: "13px",
          }}
        >
          <strong>Please resolve input errors:</strong>
          <ul style={{ margin: "4px 0 0 16px", padding: 0 }}>
            {activeErrors.map((err, i) => (
              <li key={i}>{err}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid-3 row">
        <div>
          <label htmlFor="pName">
            Full Name <span style={{ color: "#ef4444" }}>*</span>
          </label>
          <input
            id="pName"
            className="input"
            value={name}
            onChange={(e) => handleNameChange(e.target.value)}
            style={{ borderColor: errors.name ? "#ef4444" : undefined }}
            placeholder="Enter full name"
            maxLength={60}
          />
          {errors.name && (
            <div style={{ color: "#dc2626", fontSize: "11.5px", marginTop: "3px", fontWeight: 600 }}>
              ⚠️ {errors.name}
            </div>
          )}
        </div>

        <div>
          <label htmlFor="pAge">Age</label>
          <input
            id="pAge"
            type="number"
            min="10"
            max="100"
            className="input"
            value={age}
            onChange={(e) => handleAgeChange(e.target.value)}
            style={{ borderColor: errors.age ? "#ef4444" : undefined }}
            placeholder="Enter age"
          />
          {errors.age && (
            <div style={{ color: "#dc2626", fontSize: "11.5px", marginTop: "3px", fontWeight: 600 }}>
              ⚠️ {errors.age}
            </div>
          )}
        </div>

        <div>
          <label htmlFor="pClass">Academic Level</label>
          <select
            id="pClass"
            className="input"
            value={klass}
            onChange={(e) => handleKlassChange(e.target.value)}
          >
            <option value="10">Class 10 (10th Boards)</option>
            <option value="11">Class 11 (Senior Secondary)</option>
            <option value="12">Class 12 (Board & Entrances)</option>
            <option value="Degree">College Undergraduate (Degree)</option>
          </select>
        </div>

        <div style={{ gridColumn: "1/-1" }}>
          <label htmlFor="pGoal">
            Target Exam or Educational Goal <span style={{ color: "#ef4444" }}>*</span>
          </label>
          <input
            id="pGoal"
            className="input"
            value={goal}
            onChange={(e) => {
              setGoal(e.target.value);
              setErrors((prev) => {
                const next = { ...prev };
                if (e.target.value.trim()) delete next.goal;
                return next;
              });
            }}
            placeholder="Enter target exam or educational goal"
            maxLength={100}
            style={{ borderColor: errors.goal ? "#ef4444" : undefined }}
          />
          {errors.goal && (
            <div style={{ color: "#dc2626", fontSize: "11.5px", marginTop: "3px", fontWeight: 600 }}>
              ⚠️ {errors.goal}
            </div>
          )}
          <div style={{ marginTop: "6px", display: "flex", flexWrap: "wrap", gap: "6px", alignItems: "center" }}>
            <span style={{ fontSize: "11px", color: "var(--muted)", fontWeight: 600 }}>
              Standard tracks:
            </span>
            {getStandardTracksForKlass(klass).map((track) => {
              const isSelected = goal.toLowerCase().trim() === track.toLowerCase().trim();
              return (
                <button
                  key={track}
                  type="button"
                  onClick={() => {
                    setGoal(track);
                    setErrors((prev) => {
                      const next = { ...prev };
                      delete next.goal;
                      return next;
                    });
                  }}
                  style={{
                    fontSize: "11px",
                    padding: "3px 8px",
                    borderRadius: "14px",
                    border: isSelected ? "1.5px solid var(--brand)" : "1px solid var(--border)",
                    background: isSelected ? "rgba(99, 102, 241, 0.15)" : "var(--card)",
                    color: isSelected ? "var(--brand)" : "var(--text)",
                    fontWeight: isSelected ? 700 : 500,
                    cursor: "pointer",
                  }}
                >
                  {isSelected ? "✓ " : ""}{track}
                </button>
              );
            })}
          </div>
        </div>

        <div>
          <label htmlFor="pSchool">School / Institute / University</label>
          <input
            id="pSchool"
            className="input"
            placeholder="Enter institution or university name"
            value={school}
            onChange={(e) => setSchool(e.target.value)}
            maxLength={100}
          />
        </div>

        <div>
          <label htmlFor="pEmail">Email</label>
          <input
            id="pEmail"
            className="input"
            value={email}
            disabled
            title="Registered account email"
          />
        </div>

        <div style={{ gridColumn: "1/-1", display: "grid", gap: "10px", gridTemplateColumns: "repeat(2, minmax(0, 1fr))" }}>
          <div>
            <label htmlFor="pWeak">Weak Areas (Optional)</label>
            <input
              id="pWeak"
              className="input"
              value={weak}
              onChange={(e) => setWeak(e.target.value)}
              placeholder="Enter weak areas separated by commas"
            />
          </div>
          <div>
            <label htmlFor="pCourseNote">Enrolled Courses (Optional)</label>
            <input
              id="pCourseNote"
              className="input"
              placeholder="Enter enrolled courses or modules separated by commas"
              value={courseNote}
              onChange={(e) => setCourseNote(e.target.value)}
            />
          </div>
        </div>
      </div>
      <div className="right" style={{ marginTop: "14px" }}>
        <button
          className="btn"
          onClick={handleSubmit}
          disabled={isSaving || activeErrors.length > 0}
          style={{ opacity: isSaving || activeErrors.length > 0 ? 0.7 : 1.0 }}
        >
          {isSaving ? "Saving..." : "Save Profile"}
        </button>
      </div>
    </div>
  );
}
