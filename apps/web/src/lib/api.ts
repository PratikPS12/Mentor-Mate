import { handleClientFallback } from "./clientFallback";

const getApiBase = () => {
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== "undefined") {
    const isHttps = window.location.protocol === "https:";
    const host = window.location.hostname || "127.0.0.1";
    const isLocalhost = host === "localhost" || host === "127.0.0.1";

    // If on a public production HTTPS host (like Vercel)
    if (isHttps && !isLocalhost) {
      // If envUrl is explicitly set to an HTTPS endpoint, use it
      if (envUrl && envUrl.startsWith("https://")) {
        return envUrl;
      }
      // Otherwise, return empty to use ultra-fast seamless client demo fallback
      return "";
    }

    if (envUrl) return envUrl;
    return `${window.location.protocol}//${host}:8000/api/v1`;
  }
  if (envUrl) return envUrl;
  return "http://127.0.0.1:8000/api/v1";
};


export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  klass?: string;
  goal?: string;
}

export interface StudentProfile {
  student_id: string;
  name: string;
  email: string;
  age?: number | string;
  klass: string;
  board: string;
  goal: string;
  school?: string;
  weak_areas: string[];
  enrolled_courses: string[];
  daily_available_hours: number;
  days_to_exam: number;
  quick_actions: string[];
  dark_mode: boolean;
  marksheet_verified?: boolean;
  verified_marks?: Array<{
    subject: string;
    marks_obtained: number;
    maximum_marks: number;
    percentage: number;
    grade?: string;
  }>;
}

export interface StudyPlanTask {
  id: string;
  type: string;
  subject: string;
  title: string;
  description: string;
  duration_minutes: number;
  completed: boolean;
  reason: string;
  time_slot?: string;
  priority?: string;
  category?: string;
  suggested_method?: string;
  tags?: string[];
}

export interface StudyPlan {
  id: string;
  days_to_exam: number;
  daily_hours: number;
  subjects: string[];
  tasks: StudyPlanTask[];
  completion_rate?: number;
}

export interface DashboardSummary {
  streak: {
    streak_days: number;
    max_days: number;
    percentage: number;
  };
  today_focus: {
    title: string;
    subject: string;
    mastery_percent: number;
    why: string;
    next_action: string;
    has_evidence: boolean;
    basis_source?: string;
    concept_id?: string;
    clean_title?: string;
  } | null;
  upcoming_revision: Array<{
    concept_id: string;
    title: string;
    subject: string;
    retention_percent: number;
    next_review: string;
  }>;
  recent_assessment: {
    session_id: string;
    score: string;
    percentage: number;
    performance_tier: string;
    date: string;
    irt_ability?: {
      theta: number;
      standard_error: number;
      confidence: string;
      proficiency_band: string;
    };
  } | null;
  current_plan: StudyPlan | null;
  enrolled_courses: string[];
  student_name: string;
  goal: string;
  klass: string;
}

export interface AssessmentQuestion {
  id: string;
  concept_id: string;
  subject: string;
  topic: string;
  difficulty: number;
  question: string;
  options: string[];
  hints: string[];
  question_number?: number;
  total_questions?: number;
}

export interface WeaknessDiagnostic {
  concept_id: string;
  subject: string;
  topic: string;
  question_snippet: string;
  error_type: string;
  explanation: string;
  remedial_action: string;
}

export interface SubjectBreakdown {
  subject: string;
  attempted: number;
  correct: number;
  percentage: number;
}

export interface RemedialCourseRef {
  course_id: string;
  course_title: string;
  tag: string;
  reason: string;
}

export interface QuestionReviewItem {
  question_id?: string;
  concept_id?: string;
  subject?: string;
  topic?: string;
  question_text: string;
  options?: string[];
  selected_index: number;
  correct_index?: number;
  correct: boolean;
  explanation: string;
}

export interface StudiedTopic {
  title: string;
  subject: string;
  source: 'study_material' | 'enrolled_course' | 'completed_plan_task';
  material_id?: string;
  concepts_count?: number;
  summary?: string;
}

export interface StudiedStatusResponse {
  has_studied: boolean;
  studied_topics: StudiedTopic[];
  suggested_topics: string[];
  goal: string;
  klass: string;
  syllabus_name: string;
}

export interface TestEvaluationReport {
  overall_score: string;
  percentage: number;
  performance_tier: string;
  tier_description: string;
  syllabus_track: string;
  subject_breakdown: SubjectBreakdown[];
  weaknesses: WeaknessDiagnostic[];
  remedial_courses: RemedialCourseRef[];
  question_reviews?: QuestionReviewItem[];
  total_weak_areas_logged: number;
  evaluated_at: string;
}

export interface AssessmentAnswerResult {
  is_correct: boolean;
  explanation: string;
  diagnosis?: {
    error_type: string;
    description: string;
    confidence: number;
    remediation_hint: string;
  };
  prior_mastery: number;
  posterior_mastery: number;
  is_complete: boolean;
  current_score: string;
  next_question?: AssessmentQuestion | null;
  evaluation_report?: TestEvaluationReport | null;
}

export interface AssessmentStartResponse {
  session_id: string;
  status: string;
  syllabus_name?: string;
  progress: string;
  current_question: AssessmentQuestion | null;
}

export interface FormulaItem {
  name: string;
  formula: string;
  variables: string;
  notes?: string;
}

export interface WorkedExample {
  problem: string;
  solution_steps: string[];
  key_insight?: string;
}

export interface StudyResource {
  title: string;
  type: string;
  url: string;
}

export interface CourseModule {
  id: string;
  title: string;
  duration: string;
  concept_id: string;
  summary: string;
  formula_note: string;
  video_url?: string;
  video_title?: string;
  detailed_notes?: string[];
  formula_sheet?: FormulaItem[];
  worked_examples?: WorkedExample[];
  pitfalls?: string[];
  study_materials?: StudyResource[];
  practice_question?: {
    q: string;
    options: string[];
    answer_index: number;
    explanation: string;
  };
}

export interface CourseItem {
  id: string;
  title: string;
  track: string;
  tag: string;
  hours: number;
  description?: string;
  concept_id?: string;
  reason?: string;
  fit_score?: number;
  is_weakness_remedy?: boolean;
  modules?: CourseModule[];
}

export interface FreeExternalCourse {
  id: string;
  title: string;
  platform: string;
  provider: string;
  url: string;
  tag: string;
  track: string;
  class_level: string;
  duration: string;
  rating: number;
  badge: string;
  description: string;
}

export interface GeneratedStudyQuestion {
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}

export interface StudyMaterialAnalysis {
  summary: string;
  key_concepts: string[];
  key_formulas: string[];
  difficulty_level: string;
  estimated_study_minutes: number;
  study_recommendation: string;
  generated_questions: GeneratedStudyQuestion[];
  course_module?: {
    title: string;
    duration: string;
    detailed_notes: string[];
    pitfalls?: string[];
    formula_note?: string;
  };
}

export interface StudyMaterialItem {
  id?: string;
  material_id?: string;
  title: string;
  subject: string;
  filename: string;
  ocr_engine?: string;
  word_count?: number;
  chunks_indexed?: number;
  chunks_count?: number;
  analysis?: StudyMaterialAnalysis;
  linked_course_name?: string;
  created_at?: string;
}

export interface StudyMaterialUploadResponse {
  status: string;
  material_id: string;
  title: string;
  subject: string;
  filename: string;
  ocr_engine: string;
  word_count: number;
  chunks_indexed: number;
  analysis: StudyMaterialAnalysis;
  linked_course_name: string;
  created_at: string;
}

export interface PerformanceSummary {
  charts: {
    labels_day: string[];
    by_day: number[];
    weekly_avg: number[];
    monthly_avg: number[];
  };
  measured_metrics: {
    total_assessments_taken: number;
    total_questions_attempted: number;
    recent_test_scores: Array<{
      session_id: string;
      date: string;
      score: number;
      total: number;
      percentage: number;
    }>;
  };
  model_estimates: {
    average_mastery: number;
    concepts_tracked: number;
    concept_masteries: Array<{
      concept_id: string;
      mastery: number;
      uncertainty: number;
      evidence_count: number;
    }>;
  };
  learning_twin: {
    status: string;
    current_focus_concept: string;
    basis_source?: string;
    why: string;
    next_best_action: string;
    confidence_level: string;
    total_evidence_events: number;
  };
}

export interface AIGuidanceResponse {
  success: boolean;
  guidance: {
    executive_strategy: string;
    weak_area_action_plan: Array<{
      weak_area: string;
      tactical_remedy: string;
      recommended_practice: string;
    }>;
    subject_time_allocation: Array<{
      subject: string;
      percentage: number;
      weekly_hours: number;
    }>;
    milestone_timeline: Array<{
      phase: string;
      milestone: string;
      action: string;
    }>;
    pitfalls_to_avoid: string[];
  };
}

class ApiClient {
  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("mm_auth_token");
  }

  setToken(token: string) {
    if (typeof window !== "undefined") {
      localStorage.setItem("mm_auth_token", token);
    }
  }

  clearToken() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("mm_auth_token");
    }
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }

    const apiBase = getApiBase();

    // If running in production on Vercel without an external cloud backend,
    // or if the URL is empty, execute directly in local client storage.
    if (!apiBase) {
      return handleClientFallback<T>(endpoint, options);
    }

    try {
      const res = await fetch(`${apiBase}${endpoint}`, {
        ...options,
        headers,
      });

      if (!res.ok) {
        let errMsg = "An error occurred";
        try {
          const errJson = await res.json();
          errMsg = errJson.detail || errJson.message || errMsg;
        } catch {
          errMsg = res.statusText || errMsg;
        }
        throw new Error(errMsg);
      }

      return await res.json();
    } catch (err: any) {
      // If network is unreachable, connection refused, or mixed-content blocked
      const isNetworkError =
        err instanceof TypeError ||
        !err.message ||
        err.message.includes("fetch") ||
        err.message.includes("NetworkError") ||
        err.message.includes("Failed to fetch");

      if (isNetworkError) {
        console.info(`[MentorMate] Backend at '${apiBase}' unreachable. Seamlessly activating local storage fallback.`);
        return handleClientFallback<T>(endpoint, options);
      }
      throw err;
    }
  }

  // Auth
  async register(data: { name: string; email: string; password: string; klass?: string; goal?: string }) {
    const res = await this.request<{ access_token: string; token_type: string; user: User }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
    this.setToken(res.access_token);
    return res;
  }

  async login(data: { email: string; password: string }) {
    const res = await this.request<{ access_token: string; token_type: string; user: User }>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
    this.setToken(res.access_token);
    return res;
  }

  async getMe() {
    return this.request<{ id: string; name: string; email: string; role: string; profile: StudentProfile }>("/auth/me");
  }

  // Student Profile
  async getProfile(): Promise<StudentProfile> {
    return this.request<StudentProfile>("/student/profile");
  }

  async updateProfile(data: Partial<StudentProfile>): Promise<{ message: string; profile: StudentProfile }> {
    return this.request<{ message: string; profile: StudentProfile }>("/student/profile", {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async markTodayStudied(): Promise<{ message: string; date: string; streak_days: number; streak_percentage: number }> {
    return this.request("/student/attendance/mark-today", { method: "POST" });
  }

  async getAttendance(): Promise<{ streak: { streak_days: number; max_days: number; percentage: number }; history: Array<{ date: string; studied: boolean }> }> {
    return this.request("/student/attendance");
  }

  async getDashboardSummary(): Promise<DashboardSummary> {
    return this.request<DashboardSummary>("/student/dashboard");
  }

  // Marksheet
  async uploadMarksheet(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    return this.request<{
      document_id: string;
      status: string;
      extraction: {
        candidate_name: string;
        institution: string;
        exam_session: string;
        subjects: Array<{
          subject: string;
          marks_obtained: number;
          maximum_marks: number;
          percentage: number;
          grade: string;
          confidence: number;
        }>;
        overall_confidence: number;
        requires_verification: boolean;
        extraction_note?: string;
      };
    }>("/marksheet/upload", {
      method: "POST",
      body: formData,
    });
  }

  async verifyMarksheet(payload: {
    document_id: string;
    student_name: string;
    institution: string;
    exam_session: string;
    subjects: Array<{
      subject: string;
      marks_obtained: number;
      maximum_marks: number;
      percentage: number;
      grade: string;
      confidence: number;
    }>;
  }) {
    return this.request("/marksheet/verify", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  async uploadStudyNotes(file: File, title?: string, subject?: string) {
    const formData = new FormData();
    formData.append("file", file);
    const q = new URLSearchParams();
    if (title) q.append("title", title);
    if (subject) q.append("subject", subject);
    const qs = q.toString() ? `?${q.toString()}` : "";
    return this.request<{
      status: string;
      document_id: string;
      title: string;
      filename: string;
      subject: string;
      chunks_indexed: number;
      message: string;
    }>(`/marksheet/notes/upload${qs}`, {
      method: "POST",
      body: formData,
    });
  }

  async getUploadedNotes() {
    return this.request<{
      materials: Array<{
        id: string;
        document_id: string;
        title: string;
        filename: string;
        subject: string;
        chunks_count: number;
        created_at?: string;
      }>;
    }>("/marksheet/notes");
  }

  // Full AI OCR & Document Intelligence Methods
  async uploadStudyMaterial(file: File, title?: string, subject?: string): Promise<StudyMaterialUploadResponse> {
    const formData = new FormData();
    formData.append("file", file);
    const q = new URLSearchParams();
    if (title) q.append("title", title);
    if (subject) q.append("subject", subject);
    const qs = q.toString() ? `?${q.toString()}` : "";
    return this.request<StudyMaterialUploadResponse>(`/marksheet/study-material/upload${qs}`, {
      method: "POST",
      body: formData,
    });
  }

  async getStudyMaterials(): Promise<{ materials: StudyMaterialItem[] }> {
    return this.request<{ materials: StudyMaterialItem[] }>("/marksheet/study-material");
  }

  async getStudyMaterialDetail(materialId: string): Promise<StudyMaterialItem> {
    return this.request<StudyMaterialItem>(`/marksheet/study-material/${encodeURIComponent(materialId)}`);
  }

  // Assessment
  async getStudiedStatus(): Promise<StudiedStatusResponse> {
    return this.request<StudiedStatusResponse>("/assessment/studied-status");
  }

  async startAssessment(
    type: string = "diagnostic",
    subject?: string,
    topic?: string,
    numQuestions: number = 5
  ): Promise<AssessmentStartResponse> {
    const params = new URLSearchParams();
    params.set("assessment_type", type);
    if (subject) params.set("subject_focus", subject);
    if (topic) params.set("topic", topic);
    if (numQuestions) params.set("num_questions", String(numQuestions));
    return this.request<AssessmentStartResponse>(`/assessment/start?${params.toString()}`, { method: "POST" });
  }

  async submitAnswer(sessionId: string, payload: {
    question_id: string;
    selected_index: number;
    response_time_ms: number;
    hints_used: number;
  }): Promise<AssessmentAnswerResult> {
    return this.request(`/assessment/${sessionId}/answer`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  async getAssessmentResults(sessionId: string) {
    return this.request(`/assessment/${sessionId}/results`);
  }

  // Schedule / Planner
  async generatePlan(daysToExam: number = 180, dailyHours: number = 3.0, subjects: string = "Math, Physics, Chemistry"): Promise<StudyPlan> {
    return this.request(`/schedule/generate?days_to_exam=${daysToExam}&daily_hours=${dailyHours}&subjects=${encodeURIComponent(subjects)}`, {
      method: "POST",
    });
  }

  async toggleTask(planId: string, taskId: string, completed: boolean) {
    return this.request(`/schedule/${planId}/task/${taskId}/toggle`, {
      method: "POST",
      body: JSON.stringify({ completed }),
    });
  }

  // Tutor
  async sendTutorMessage(message: string, conceptId?: string, sessionId?: string) {
    return this.request<{
      role: string;
      content: string;
      pedagogical_state: string;
      concept_id?: string;
      concept_name?: string;
      practice_question?: any;
      citations: string[];
      timestamp: string;
    }>("/tutor/message", {
      method: "POST",
      body: JSON.stringify({ message, concept_id: conceptId, session_id: sessionId }),
    });
  }

  async getConversations() {
    return this.request<Array<{
      id: string;
      user_message: string;
      tutor_reply: string;
      pedagogical_state: string;
      created_at: string;
    }>>("/tutor/conversations");
  }

  // Courses & Recommendations
  async getCatalog(track?: string): Promise<CourseItem[]> {
    const q = track && track !== "All" ? `?track=${encodeURIComponent(track)}` : "";
    return this.request(`/courses/catalog${q}`);
  }

  async getRecommendations(): Promise<CourseItem[]> {
    return this.request("/courses/recommended");
  }

  async enrollCourse(courseTitle: string) {
    return this.request("/courses/enroll", {
      method: "POST",
      body: JSON.stringify({ course_title: courseTitle }),
    });
  }

  async unenrollCourse(courseTitle: string) {
    return this.request("/courses/unenroll", {
      method: "POST",
      body: JSON.stringify({ course_title: courseTitle }),
    });
  }

  async getCourseDetail(courseId: string): Promise<CourseItem> {
    return this.request(`/courses/${encodeURIComponent(courseId)}`);
  }

  async getFreeExternalCourses(): Promise<FreeExternalCourse[]> {
    return this.request("/courses/external/free");
  }

  // AI Academic Guidance
  async generateGuidance(payload: {
    goal?: string;
    klass?: string;
    daily_hours?: number;
    weak_areas?: string[];
    subjects?: string[];
  }): Promise<AIGuidanceResponse> {
    return this.request("/guidance/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  // Performance
  async getPerformanceSummary(): Promise<PerformanceSummary> {
    return this.request("/performance/summary");
  }
}

export const api = new ApiClient();
