"use client";

import React from "react";

export default function AboutTab() {
  return (
    <div id="panel-about" className="card">
      <div className="title">About Mentor Mate — Evidence-Driven Learning</div>
      <div className="subtitle">Clear expectations & offerings for students and parents</div>
      <div className="hr"></div>

      <div className="grid-3 row">
        <div>
          <div style={{ fontWeight: 800 }}>From Students</div>
          <ul className="list">
            <li>Attend daily study slots (45–90 min recommended).</li>
            <li>Attempt weekly tests & review mistakes honestly.</li>
            <li>Keep weak areas & profile updated for better guidance.</li>
            <li>Uploading marksheet within 3 months helps calibrate baseline knowledge tracing.</li>
          </ul>
        </div>

        <div>
          <div style={{ fontWeight: 800 }}>From Parents</div>
          <ul className="list">
            <li>Encourage regular study and review performance weekly.</li>
            <li>Use Attendance & Performance graphs to track progress.</li>
            <li>Provide honest feedback — focus on long-term improvement.</li>
          </ul>
        </div>

        <div>
          <div style={{ fontWeight: 800 }}>What We Provide</div>
          <ul className="list">
            <li>Personalized study plans based on goal & weak areas.</li>
            <li>Targeted quizzes + Aptitude & Reasoning practice.</li>
            <li>Course recommendations tailored to standard & goal.</li>
            <li>Parent-friendly attendance & performance view.</li>
          </ul>
        </div>
      </div>
      <div className="hr"></div>
      <div className="note">
        Mentor Mate is an integrated adaptive AI platform with persistent database state, Bayesian Knowledge Tracing (BKT), and Ebbinghaus spaced repetition.
      </div>
    </div>
  );
}
