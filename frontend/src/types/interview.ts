export type Difficulty = 'Beginner' | 'Intermediate' | 'Advanced';
export type Mode = 'text' | 'voice';

export interface GeneratedQuestion {
  question: string;
  ideal_answer: string;
  keywords: string[];
  topic: string;
}

export interface Feedback {
  score: number;
  strengths: string[];
  weaknesses: string[];
  suggested_improvements: string[];
  keyword_coverage: number;
  clarity_score: number;
  summary: string;
}

export interface StartInterviewResponse {
  interview_id: string;
  current_question_index: number;
  total_questions: number;
  question: GeneratedQuestion;
}

export interface SubmitAnswerResponse {
  feedback: Feedback;
  next_question: GeneratedQuestion | null;
  completed: boolean;
}

export interface FinalReport {
  interview_id: string;
  role: string;
  difficulty: Difficulty;
  total_questions: number;
  average_score: number;
  strengths: string[];
  weaknesses: string[];
  suggested_improvements: string[];
  question_breakdown: Array<{
    question_index: number;
    answer_text: string;
    feedback: Feedback;
  }>;
}
