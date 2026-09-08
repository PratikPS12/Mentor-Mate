import {
  User,
  StudentProfile,
  DashboardSummary,
  StudyPlan,
  AssessmentStartResponse,
  AssessmentAnswerResult,
  TestEvaluationReport,
  CourseItem,
  FreeExternalCourse,
  AIGuidanceResponse,
  PerformanceSummary,
  StudiedStatusResponse,
  StudyMaterialItem,
  StudyMaterialUploadResponse,
} from "./api";

const STORAGE_KEYS = {
  USERS: "mm_local_users",
  CURRENT_USER: "mm_current_user",
  STUDENT_PROFILE: "mm_student_profile",
  STUDY_PLAN: "mm_study_plan",
  ATTENDANCE: "mm_attendance",
  MATERIALS: "mm_materials",
  CONVERSATIONS: "mm_conversations",
};

function getStored<T>(key: string, defaultVal: T): T {
  if (typeof window === "undefined") return defaultVal;
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : defaultVal;
  } catch {
    return defaultVal;
  }
}

function setStored<T>(key: string, val: T): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(key, JSON.stringify(val));
  } catch (err) {
    console.error("Storage error:", err);
  }
}

function createDefaultProfile(name: string, email: string, klass?: string, goal?: string): StudentProfile {
  return {
    student_id: `stu_${Date.now().toString(36)}`,
    name: name || "Student",
    email: email || "student@mentormate.ai",
    age: 16,
    klass: klass || "Class 10 (10th Boards)",
    board: "CBSE",
    goal: goal || "10th Boards (CBSE)",
    school: "Excellence Public School",
    weak_areas: ["Quadratic Equations", "Ray Optics & Lens Formula", "Periodic Trends"],
    enrolled_courses: ["Class 10 CBSE Math Mastery", "Complete 10th Physics Sprint"],
    daily_available_hours: 3.5,
    days_to_exam: 118,
    quick_actions: ["Review Lens Sign Conventions", "Solve 5 Quadratic Roots Problems"],
    dark_mode: false,
    marksheet_verified: false,
  };
}

const DEFAULT_COURSES: CourseItem[] = [
  {
    id: "course_math_10",
    title: "Class 10 CBSE Math Mastery",
    track: "CBSE Class 10",
    tag: "High Yield",
    hours: 24,
    description: "Complete chapter-by-chapter mastery course covering Trigonometry, Polynomials, and Quadratic Equations.",
    modules: [
      {
        id: "mod_m1",
        title: "Quadratic Equations: Factorization & Formula Method",
        duration: "45 mins",
        concept_id: "mth_quad_01",
        summary: "Master the discriminant test D = b^2 - 4ac and roots characterization.",
        formula_note: "x = (-b ± √(b² - 4ac)) / (2a)",
        video_url: "https://www.youtube.com/embed/ZBalWWHY4Go",
        video_title: "Khan Academy: The Quadratic Formula",
        detailed_notes: [
          "Standard quadratic equation form: ax² + bx + c = 0, where a ≠ 0.",
          "Discriminant D = b² - 4ac determines nature of roots:",
          "• If D > 0: Two distinct real roots.",
          "• If D = 0: Two equal real roots (x = -b / 2a).",
          "• If D < 0: No real roots (complex conjugates).",
        ],
        formula_sheet: [
          { name: "Quadratic Formula", formula: "x = (-b ± √D) / 2a", variables: "a, b, c = coefficients", notes: "D must be non-negative for real roots" },
          { name: "Sum of Roots", formula: "α + β = -b / a", variables: "α, β = roots" },
          { name: "Product of Roots", formula: "α · β = c / a", variables: "α, β = roots" },
        ],
      },
      {
        id: "mod_m2",
        title: "Introduction to Trigonometric Ratios",
        duration: "50 mins",
        concept_id: "mth_trig_01",
        summary: "Understanding sine, cosine, tangent and Pythagorean identities.",
        formula_note: "sin²θ + cos²θ = 1",
        video_url: "https://www.youtube.com/embed/PUB0TaZ7bhA",
        video_title: "Trigonometry Fundamentals",
      },
    ],
  },
  {
    id: "course_phy_10",
    title: "Complete 10th Physics Sprint",
    track: "CBSE Class 10",
    tag: "Core Science",
    hours: 20,
    description: "In-depth conceptual grasp of Light: Reflection and Refraction, Electricity, and Magnetic Effects.",
    modules: [
      {
        id: "mod_p1",
        title: "Spherical Mirrors & Mirror Formula",
        duration: "40 mins",
        concept_id: "phy_light_01",
        summary: "Cartesian sign convention and focal length calculations.",
        formula_note: "1/f = 1/v + 1/u, m = -v/u",
        video_url: "https://www.youtube.com/embed/s4sJz_X6V-w",
        video_title: "Light & Spherical Mirrors",
      },
    ],
  },
];

const DEFAULT_EXTERNAL_COURSES: FreeExternalCourse[] = [
  {
    id: "ext_khan_math",
    title: "Khan Academy: Class 10 Math (India)",
    provider: "Khan Academy",
    platform: "Khan Academy / YouTube",
    url: "https://www.khanacademy.org/math/in-in-grade-10-ncert",
    tag: "Free Complete Course",
    track: "CBSE Class 10",
    class_level: "Class 10",
    duration: "40+ hours",
    rating: 4.9,
    badge: "Most Popular",
    description: "Free complete NCERT curriculum for Class 10 with interactive exercises and video lessons.",
  },
  {
    id: "ext_edx_physics",
    title: "Fundamentals of Physics & Mechanics",
    provider: "MIT / edX",
    platform: "edX",
    url: "https://www.edx.org/course/mechanics-review",
    tag: "University Foundation",
    track: "Physics Foundation",
    class_level: "High School & Prep",
    duration: "25 hours",
    rating: 4.8,
    badge: "Interactive Labs",
    description: "Rigorous introductory physics principles covering motion, energy, force vectors, and optics.",
  },
  {
    id: "ext_nptel_chem",
    title: "Basic Chemical Principles & Bonding",
    provider: "NPTEL / IIT",
    platform: "SWAYAM / NPTEL",
    url: "https://nptel.ac.in/courses/104106093",
    tag: "IIT Faculty",
    track: "Chemistry Core",
    class_level: "Secondary & Higher Sec",
    duration: "30 hours",
    rating: 4.7,
    badge: "Official Certification",
    description: "Top IIT professors explaining atomic structure, periodic classification, and chemical bonding.",
  },
];

export async function handleClientFallback<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const method = (options.method || "GET").toUpperCase();
  const url = new URL(endpoint, "https://local.mentormate");
  const path = url.pathname;

  // Tiny artificial latency for natural feel
  await new Promise((resolve) => setTimeout(resolve, 120));

  // 1. Auth: Register
  if (path === "/auth/register" && method === "POST") {
    const body = options.body ? JSON.parse(options.body as string) : {};
    const users = getStored<Record<string, any>>(STORAGE_KEYS.USERS, {});
    const emailKey = (body.email || "demo@mentormate.ai").toLowerCase();

    const user: User = {
      id: `usr_${Date.now()}`,
      name: body.name || "Student",
      email: emailKey,
      role: "student",
      klass: body.klass || "Class 10 (10th Boards)",
      goal: body.goal || "10th Boards (CBSE)",
    };

    users[emailKey] = { ...user, password: body.password || "" };
    setStored(STORAGE_KEYS.USERS, users);

    const profile = createDefaultProfile(user.name, user.email, user.klass, user.goal);
    setStored(STORAGE_KEYS.STUDENT_PROFILE, profile);
    setStored(STORAGE_KEYS.CURRENT_USER, user);

    const token = `mm_token_${Date.now()}`;
    return {
      access_token: token,
      token_type: "bearer",
      user,
    } as unknown as T;
  }

  // 2. Auth: Login
  if (path === "/auth/login" && method === "POST") {
    const body = options.body ? JSON.parse(options.body as string) : {};
    const users = getStored<Record<string, any>>(STORAGE_KEYS.USERS, {});
    const emailKey = (body.email || "demo@mentormate.ai").toLowerCase();
    const existing = users[emailKey];

    const user: User = existing
      ? {
          id: existing.id,
          name: existing.name,
          email: existing.email,
          role: "student",
          klass: existing.klass,
          goal: existing.goal,
        }
      : {
          id: `usr_${Date.now()}`,
          name: emailKey.split("@")[0].replace(/[^a-zA-Z]/g, " ").trim() || "Student",
          email: emailKey,
          role: "student",
          klass: "Class 10 (10th Boards)",
          goal: "10th Boards (CBSE)",
        };

    setStored(STORAGE_KEYS.CURRENT_USER, user);
    let profile = getStored<StudentProfile | null>(STORAGE_KEYS.STUDENT_PROFILE, null);
    if (!profile) {
      profile = createDefaultProfile(user.name, user.email, user.klass, user.goal);
      setStored(STORAGE_KEYS.STUDENT_PROFILE, profile);
    }

    const token = `mm_token_${Date.now()}`;
    return {
      access_token: token,
      token_type: "bearer",
      user,
    } as unknown as T;
  }

  // 3. Auth: Me
  if (path === "/auth/me") {
    let user = getStored<User | null>(STORAGE_KEYS.CURRENT_USER, null);
    if (!user) {
      user = {
        id: "usr_guest",
        name: "Pratik",
        email: "pratik@mentormate.ai",
        role: "student",
        klass: "Class 10 (10th Boards)",
        goal: "10th Boards (CBSE)",
      };
      setStored(STORAGE_KEYS.CURRENT_USER, user);
    }
    let profile = getStored<StudentProfile | null>(STORAGE_KEYS.STUDENT_PROFILE, null);
    if (!profile) {
      profile = createDefaultProfile(user.name, user.email, user.klass, user.goal);
      setStored(STORAGE_KEYS.STUDENT_PROFILE, profile);
    }
    return {
      id: user.id,
      name: user.name,
      email: user.email,
      role: "student",
      profile,
    } as unknown as T;
  }

  // 4. Student Profile
  if (path === "/student/profile") {
    let profile = getStored<StudentProfile | null>(STORAGE_KEYS.STUDENT_PROFILE, null);
    if (!profile) {
      profile = createDefaultProfile("Pratik", "pratik@mentormate.ai");
      setStored(STORAGE_KEYS.STUDENT_PROFILE, profile);
    }

    if (method === "PUT") {
      const updates = options.body ? JSON.parse(options.body as string) : {};
      profile = { ...profile, ...updates };
      setStored(STORAGE_KEYS.STUDENT_PROFILE, profile);
      return { message: "Profile updated successfully", profile } as unknown as T;
    }
    return profile as unknown as T;
  }

  // 5. Attendance
  if (path === "/student/attendance/mark-today") {
    const current = getStored<{ streak_days: number; history: any[] }>(STORAGE_KEYS.ATTENDANCE, {
      streak_days: 3,
      history: [],
    });
    const updatedStreak = current.streak_days + 1;
    const today = new Date().toISOString().split("T")[0];
    current.history.unshift({ date: today, studied: true });
    current.streak_days = updatedStreak;
    setStored(STORAGE_KEYS.ATTENDANCE, current);

    return {
      message: "Recorded attendance in adaptive twin",
      date: today,
      streak_days: updatedStreak,
      streak_percentage: Math.min(100, updatedStreak * 14),
    } as unknown as T;
  }

  if (path === "/student/attendance") {
    const current = getStored<{ streak_days: number; history: any[] }>(STORAGE_KEYS.ATTENDANCE, {
      streak_days: 3,
      history: [
        { date: "2026-09-07", studied: true },
        { date: "2026-09-06", studied: true },
        { date: "2026-09-05", studied: true },
      ],
    });
    return {
      streak: {
        streak_days: current.streak_days,
        max_days: Math.max(7, current.streak_days),
        percentage: Math.min(100, current.streak_days * 14),
      },
      history: current.history,
    } as unknown as T;
  }

  // 6. Dashboard Summary
  if (path === "/student/dashboard") {
    const profile = getStored<StudentProfile | null>(STORAGE_KEYS.STUDENT_PROFILE, null) || createDefaultProfile("Pratik", "pratik@mentormate.ai");
    const att = getStored<{ streak_days: number }>(STORAGE_KEYS.ATTENDANCE, { streak_days: 3 });
    const plan = getStored<StudyPlan | null>(STORAGE_KEYS.STUDY_PLAN, null);

    const summary: DashboardSummary = {
      streak: {
        streak_days: att.streak_days,
        max_days: 7,
        percentage: Math.min(100, att.streak_days * 14),
      },
      today_focus: {
        title: "Mastering Convex Lens Ray Diagrams & Sign Conventions",
        subject: "Physics",
        mastery_percent: 64,
        why: "Adaptive knowledge tracing detected hesitation in focal length sign conventions during your last practice session.",
        next_action: "Review 2-minute formula cheat sheet and complete 3 numerical exercises.",
        has_evidence: true,
        basis_source: "Diagnostic Assessment #1",
        clean_title: "Convex Lens Ray Diagrams",
      },
      upcoming_revision: [
        { concept_id: "phy_optics_01", title: "Refraction & Snell's Law", subject: "Physics", retention_percent: 78, next_review: "Tomorrow, 6:00 PM" },
        { concept_id: "mth_quad_02", title: "Quadratic Roots & Discriminant (b² - 4ac)", subject: "Math", retention_percent: 62, next_review: "Thursday, 7:30 PM" },
        { concept_id: "chm_acid_03", title: "pH Scale & Neutralization Reactions", subject: "Chemistry", retention_percent: 85, next_review: "Saturday, 5:00 PM" },
      ],
      recent_assessment: {
        session_id: "sess_demo_101",
        score: "4/5",
        percentage: 80,
        performance_tier: "Proficient",
        date: "Today",
        irt_ability: {
          theta: 0.85,
          standard_error: 0.28,
          confidence: "High (89%)",
          proficiency_band: "Advanced Tier",
        },
      },
      current_plan: plan,
      enrolled_courses: profile.enrolled_courses,
      student_name: profile.name,
      goal: profile.goal,
      klass: profile.klass,
    };
    return summary as unknown as T;
  }

  // 7. Schedule / Planner
  if (path === "/schedule/generate") {
    const days = Number(url.searchParams.get("days_to_exam") || 118);
    const hours = Number(url.searchParams.get("daily_hours") || 3.5);
    const subjectsRaw = url.searchParams.get("subjects") || "Mathematics, Physics, Chemistry";
    const subjects = subjectsRaw.split(",").map((s) => s.trim());

    const plan: StudyPlan = {
      id: `plan_${Date.now()}`,
      days_to_exam: days,
      daily_hours: hours,
      subjects,
      tasks: [
        {
          id: "task_1",
          type: "study",
          subject: subjects[0] || "Mathematics",
          title: "Quadratic Equations — Root Factorization Practice",
          description: "Solve 6 standard NCERT exercises on splitting middle terms.",
          duration_minutes: 45,
          completed: false,
          reason: "Reinforces high-weightage CBSE algebraic problem solving.",
          time_slot: "06:00 PM - 06:45 PM",
          priority: "High",
          category: "Conceptual Problem Solving",
          suggested_method: "Pomodoro Focus (25m drill + 5m review)",
          tags: ["Algebra", "CBSE 10th", "Core"],
        },
        {
          id: "task_2",
          type: "revision",
          subject: subjects[1] || "Physics",
          title: "Ray Optics: Convex vs Concave Lens Ray Tracing",
          description: "Draw focal ray diagrams for objects beyond 2F, at 2F, and between F and Optical Center.",
          duration_minutes: 40,
          completed: false,
          reason: "Addresses flagged weakness in sign conventions and image formation.",
          time_slot: "07:00 PM - 07:40 PM",
          priority: "High",
          category: "Visual Diagram Review",
          suggested_method: "Active Recall Diagramming",
          tags: ["Optics", "Diagrams", "Formulas"],
        },
        {
          id: "task_3",
          type: "practice",
          subject: subjects[2] || "Chemistry",
          title: "Chemical Equations: Balancing & Redox Reactions",
          description: "Balance 10 oxidation-reduction reactions and identify oxidizing/reducing agents.",
          duration_minutes: 35,
          completed: false,
          reason: "Foundation for upcoming board exam chemical science sections.",
          time_slot: "08:00 PM - 08:35 PM",
          priority: "Medium",
          category: "Speed Drill",
          suggested_method: "Timed Quick Fire",
          tags: ["Chemistry", "Balancing", "NCERT"],
        },
      ],
      completion_rate: 0,
    };

    setStored(STORAGE_KEYS.STUDY_PLAN, plan);
    return plan as unknown as T;
  }

  if (path.includes("/schedule/") && path.includes("/toggle")) {
    const plan = getStored<StudyPlan | null>(STORAGE_KEYS.STUDY_PLAN, null);
    if (plan) {
      const parts = path.split("/");
      const taskId = parts[parts.indexOf("task") + 1];
      const body = options.body ? JSON.parse(options.body as string) : {};
      const completed = body.completed;
      plan.tasks = plan.tasks.map((t) => (t.id === taskId ? { ...t, completed } : t));
      const doneCount = plan.tasks.filter((t) => t.completed).length;
      plan.completion_rate = Math.round((doneCount / plan.tasks.length) * 100);
      setStored(STORAGE_KEYS.STUDY_PLAN, plan);
      return { success: true, completed } as unknown as T;
    }
    return { success: true, completed: true } as unknown as T;
  }

  // 8. Studied Status
  if (path === "/assessment/studied-status") {
    const profile = getStored<StudentProfile | null>(STORAGE_KEYS.STUDENT_PROFILE, null);
    const resp: StudiedStatusResponse = {
      has_studied: true,
      studied_topics: [
        { title: "Quadratic Equations", subject: "Mathematics", source: "study_material", concepts_count: 5 },
        { title: "Ray Optics & Lens Formula", subject: "Physics", source: "enrolled_course", concepts_count: 4 },
        { title: "Acids, Bases & Salts", subject: "Chemistry", source: "completed_plan_task", concepts_count: 3 },
      ],
      suggested_topics: ["Trigonometric Identities", "Electric Current & Ohm's Law", "Metals and Non-metals"],
      goal: profile?.goal || "10th Boards (CBSE)",
      klass: profile?.klass || "Class 10 (10th Boards)",
      syllabus_name: "CBSE Class 10 Board Curriculum",
    };
    return resp as unknown as T;
  }

  // 9. Assessment: Start
  if (path === "/assessment/start") {
    const subject = url.searchParams.get("subject_focus") || "Science & Mathematics";
    const resp: AssessmentStartResponse = {
      session_id: `sess_${Date.now()}`,
      status: "in_progress",
      syllabus_name: "CBSE Class 10 Board Curriculum",
      progress: "Question 1 of 5",
      current_question: {
        id: "q_optics_101",
        concept_id: "phy_optics_01",
        subject: "Physics",
        topic: "Light: Reflection and Refraction",
        difficulty: 0.6,
        question:
          "An object is placed at a distance of 20 cm in front of a convex lens of focal length 10 cm. Where will the image be formed, and what will be its nature?",
        options: [
          "20 cm behind the lens; Real, inverted, same size",
          "10 cm behind the lens; Virtual, erect, magnified",
          "30 cm behind the lens; Real, inverted, diminished",
          "At infinity; Highly enlarged",
        ],
        hints: [
          "Use the lens formula: 1/f = 1/v - 1/u with proper Cartesian sign conventions.",
          "Remember that u is negative (-20 cm) and f is positive (+10 cm) for a convex lens.",
        ],
        question_number: 1,
        total_questions: 5,
      },
    };
    return resp as unknown as T;
  }

  // 10. Assessment: Answer
  if (path.includes("/assessment/") && path.endsWith("/answer")) {
    const body = options.body ? JSON.parse(options.body as string) : {};
    const isCorrect = body.selected_index === 0;

    const resp: AssessmentAnswerResult = {
      is_correct: isCorrect,
      explanation: isCorrect
        ? "Excellent! Since the object is at 2F (u = -20 cm, f = +10 cm), the lens formula 1/v = 1/f + 1/u gives v = +20 cm. The image is real, inverted, and the exact same size (magnification m = -1)."
        : "Incorrect sign convention. Using 1/v = 1/f + 1/u with f = +10 cm and u = -20 cm gives 1/v = 1/10 - 1/20 = 1/20, so v = +20 cm. The image is real, inverted, and located at 2F on the opposite side.",
      diagnosis: isCorrect
        ? undefined
        : {
            error_type: "Sign Convention Confusion",
            description: "Object distance u must always be taken as negative in Cartesian sign conventions.",
            confidence: 0.92,
            remediation_hint: "Always set u = -|value| before substituting into 1/f = 1/v - 1/u.",
          },
      prior_mastery: 0.55,
      posterior_mastery: isCorrect ? 0.72 : 0.48,
      is_complete: true,
      current_score: isCorrect ? "5/5 (100%)" : "4/5 (80%)",
      next_question: null,
      evaluation_report: {
        overall_score: isCorrect ? "5/5" : "4/5",
        percentage: isCorrect ? 100 : 80,
        performance_tier: "Proficient",
        tier_description: "Demonstrates strong grasp of core CBSE concepts with minor sign convention nuances to polish.",
        syllabus_track: "CBSE Class 10",
        subject_breakdown: [
          { subject: "Physics", attempted: 2, correct: isCorrect ? 2 : 1, percentage: isCorrect ? 100 : 50 },
          { subject: "Mathematics", attempted: 2, correct: 2, percentage: 100 },
          { subject: "Chemistry", attempted: 1, correct: 1, percentage: 100 },
        ],
        weaknesses: [
          {
            concept_id: "phy_optics_01",
            subject: "Physics",
            topic: "Lens Formula & Sign Conventions",
            question_snippet: "Convex lens image calculation at 2F",
            error_type: "Sign Convention",
            explanation: "Review focal distances for concave vs convex optical elements.",
            remedial_action: "Review Class 10 Physics Sprint — Module 1 Formula Sheet.",
          },
        ],
        remedial_courses: [
          {
            course_id: "course_phy_10",
            course_title: "Complete 10th Physics Sprint",
            tag: "High Yield",
            reason: "Strengthens ray optics and focal length calculations.",
          },
        ],
        total_weak_areas_logged: 1,
        evaluated_at: new Date().toLocaleDateString(),
      },
    };
    return resp as unknown as T;
  }

  // 11. Socratic Tutor
  if (path === "/tutor/message" && method === "POST") {
    const body = options.body ? JSON.parse(options.body as string) : {};
    const userMsg = (body.message || "").toLowerCase();

    let reply = `Great question! In physics and mathematics, breaking this down into first principles is always the most effective strategy.\n\n` +
      `• **Key Concept**: When dealing with optical or algebraic problems, state your known parameters with their signs clearly.\n` +
      `• **Next Step**: Try writing down the governing formula and see which variable you need to isolate.\n\n` +
      `Would you like me to give you a quick numerical example or walk through the derivation step-by-step?`;

    if (userMsg.includes("lens") || userMsg.includes("light") || userMsg.includes("mirror")) {
      reply = `Let's analyze spherical lenses using Cartesian sign conventions:\n\n` +
        `1. **Object Distance ($u$)**: Light travels from left to right, so the object is always placed on the left: $u$ is **always negative**.\n` +
        `2. **Convex Lens Focal Length ($f$)**: The primary focus is behind the lens, so $f$ is **positive (+)**.\n` +
        `3. **Lens Formula**: $\\frac{1}{f} = \\frac{1}{v} - \\frac{1}{u}$.\n\n` +
        `💡 **Self-Check Question**: If $f = +15\\text{ cm}$ and $u = -30\\text{ cm}$, what will $v$ be? (Hint: The object is at $2F$!)`;
    } else if (userMsg.includes("quadratic") || userMsg.includes("root") || userMsg.includes("math")) {
      reply = `For any quadratic equation $ax^2 + bx + c = 0$:\n\n` +
        `1. Compute the **Discriminant** $D = b^2 - 4ac$.\n` +
        `2. If $D > 0$, you get two distinct real roots.\n` +
        `3. If $D = 0$, you get two equal real roots ($x = -b / 2a$).\n` +
        `4. If $D < 0$, real roots do not exist.\n\n` +
        `Would you like to solve an exam-level problem together right now?`;
    }

    return {
      role: "assistant",
      content: reply,
      pedagogical_state: "scaffolding",
      concept_id: "phy_optics_01",
      concept_name: "Spherical Optics & Sign Conventions",
      citations: ["NCERT Class 10 Science, Chapter 10", "CBSE Marking Scheme Guidelines"],
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    } as unknown as T;
  }

  // 12. Courses Catalog
  if (path === "/courses/catalog") {
    return DEFAULT_COURSES as unknown as T;
  }
  if (path === "/courses/recommended") {
    return DEFAULT_COURSES as unknown as T;
  }
  if (path === "/courses/external/free") {
    return DEFAULT_EXTERNAL_COURSES as unknown as T;
  }

  // 13. Marksheet Upload & Verify
  if (path === "/marksheet/upload") {
    return {
      document_id: `doc_${Date.now()}`,
      status: "processed",
      extraction: {
        candidate_name: "Pratik Sakhare",
        institution: "CBSE Secondary Board",
        exam_session: "2026 Board Examination",
        subjects: [
          { subject: "Mathematics", marks_obtained: 88, maximum_marks: 100, percentage: 88, grade: "A1", confidence: 0.98 },
          { subject: "Science (Physics, Chem, Bio)", marks_obtained: 82, maximum_marks: 100, percentage: 82, grade: "A2", confidence: 0.96 },
          { subject: "Social Science", marks_obtained: 91, maximum_marks: 100, percentage: 91, grade: "A1", confidence: 0.97 },
          { subject: "English Language & Literature", marks_obtained: 89, maximum_marks: 100, percentage: 89, grade: "A1", confidence: 0.99 },
          { subject: "Hindi Course A", marks_obtained: 85, maximum_marks: 100, percentage: 85, grade: "A2", confidence: 0.95 },
        ],
        overall_confidence: 0.97,
        requires_verification: true,
        extraction_note: "High confidence CBSE Marksheet OCR extraction. Ready for calibrated verification.",
      },
    } as unknown as T;
  }

  if (path === "/marksheet/verify") {
    const body = options.body ? JSON.parse(options.body as string) : {};
    const profile = getStored<StudentProfile | null>(STORAGE_KEYS.STUDENT_PROFILE, null);
    if (profile) {
      profile.marksheet_verified = true;
      profile.verified_marks = body.subjects || [];
      setStored(STORAGE_KEYS.STUDENT_PROFILE, profile);
    }
    return { message: "Marksheet verified and calibrated into learning twin model.", success: true } as unknown as T;
  }

  // 14. Academic Guidance
  if (path === "/guidance/generate") {
    const resp: AIGuidanceResponse = {
      success: true,
      guidance: {
        executive_strategy:
          "Targeting a 95%+ Board percentile requires converting moderate-mastery chapters (Optics, Quadratic Roots) into effortless strengths while maintaining regular spaced-retention drills in high-scoring topics.",
        weak_area_action_plan: [
          {
            weak_area: "Convex Lens Sign Conventions & Ray Tracing",
            tactical_remedy: "Practice drawing rays using the optical center rule and focal point rule simultaneously.",
            recommended_practice: "Complete 5 standard CBSE 3-mark ray numericals.",
          },
          {
            weak_area: "Quadratic Equation Discriminant Analysis",
            tactical_remedy: "Double-check the negative sign in (-b ± √D)/(2a) when 'b' is itself negative.",
            recommended_practice: "Timed 15-minute speed test on 10 root calculations.",
          },
        ],
        subject_time_allocation: [
          { subject: "Mathematics", percentage: 40, weekly_hours: 9.8 },
          { subject: "Physics", percentage: 35, weekly_hours: 8.5 },
          { subject: "Chemistry & Biology", percentage: 25, weekly_hours: 6.2 },
        ],
        milestone_timeline: [
          { phase: "Phase 1 (Weeks 1-2)", milestone: "Diagnostic Mastery", action: "Clear all foundational sign convention and algebra doubts." },
          { phase: "Phase 2 (Weeks 3-6)", milestone: "PYQ Drill & Speed", action: "Solve last 7 years of CBSE board question papers." },
          { phase: "Phase 3 (Weeks 7-10)", milestone: "Full Mock Simulations", action: "Complete 3 full-length timed mock exams under exam conditions." },
        ],
        pitfalls_to_avoid: [
          "Skipping unit conversions (e.g. cm vs m in optical power P = 1/f).",
          "Passive reading instead of active problem solving on paper.",
          "Cramming without taking scheduled Pomodoro breaks.",
        ],
      },
    };
    return resp as unknown as T;
  }

  // 15. Performance Summary
  if (path === "/performance/summary") {
    const summary: PerformanceSummary = {
      charts: {
        labels_day: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        by_day: [2.5, 3.2, 4.0, 3.0, 3.8, 4.5, 3.5],
        weekly_avg: [72, 75, 78, 80, 84, 86, 88],
        monthly_avg: [68, 74, 82, 88],
      },
      measured_metrics: {
        total_assessments_taken: 6,
        total_questions_attempted: 38,
        recent_test_scores: [
          { session_id: "sess_01", date: "Sep 5", score: 5, total: 5, percentage: 100 },
          { session_id: "sess_02", date: "Sep 6", score: 4, total: 5, percentage: 80 },
          { session_id: "sess_03", date: "Sep 7", score: 5, total: 5, percentage: 100 },
        ],
      },
      model_estimates: {
        average_mastery: 84.5,
        concepts_tracked: 18,
        concept_masteries: [
          { concept_id: "mth_quad_01", mastery: 88, uncertainty: 0.08, evidence_count: 14 },
          { concept_id: "phy_optics_01", mastery: 72, uncertainty: 0.12, evidence_count: 9 },
          { concept_id: "chm_acid_01", mastery: 90, uncertainty: 0.05, evidence_count: 16 },
        ],
      },
      learning_twin: {
        status: "Active & Calibrating",
        current_focus_concept: "Spherical Lens Sign Conventions",
        basis_source: "Diagnostic Assessment",
        why: "Frequent hesitation on negative object distances.",
        next_best_action: "Practice 3 numerical problems with negative object distances.",
        confidence_level: "High (91%)",
        total_evidence_events: 42,
      },
    };
    return summary as unknown as T;
  }

  // Generic fallback for any other GET/POST endpoint
  return { success: true, message: "OK (Client mode)" } as unknown as T;
}
