import { useMemo, useState } from 'react';
import { getFinalReport, startInterview, submitAnswer, submitVoiceAnswer } from '../api/client';
import { Feedback, FinalReport, GeneratedQuestion } from '../types/interview';

export function useInterview() {
  const [interviewId, setInterviewId] = useState<string | null>(null);
  const [question, setQuestion] = useState<GeneratedQuestion | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [report, setReport] = useState<FinalReport | null>(null);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [answered, setAnswered] = useState(0);
  const [loading, setLoading] = useState(false);

  const completed = useMemo(() => report !== null, [report]);

  async function start(payload: {
    role: string;
    difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
    mode: 'text' | 'voice';
    question_count?: number;
  }) {
    setLoading(true);
    try {
      const data = await startInterview(payload);
      setInterviewId(data.interview_id);
      setQuestion(data.question);
      setTotalQuestions(data.total_questions);
      setAnswered(0);
      setFeedback(null);
      setReport(null);
    } finally {
      setLoading(false);
    }
  }

  async function answerText(text: string) {
    if (!interviewId) return;
    setLoading(true);
    try {
      const result = await submitAnswer(interviewId, text);
      handleSubmitResult(result);
    } finally {
      setLoading(false);
    }
  }

  async function answerVoice(blob: Blob) {
    if (!interviewId) return;
    setLoading(true);
    try {
      const result = await submitVoiceAnswer(interviewId, blob);
      handleSubmitResult(result);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitResult(result: {
    feedback: Feedback;
    next_question: GeneratedQuestion | null;
    completed: boolean;
  }) {
    setFeedback(result.feedback);
    setAnswered((value) => value + 1);

    if (result.completed && interviewId) {
      const finalReport = await getFinalReport(interviewId);
      setQuestion(null);
      setReport(finalReport);
    } else {
      setQuestion(result.next_question);
    }
  }

  return {
    interviewId,
    question,
    feedback,
    report,
    completed,
    totalQuestions,
    answered,
    loading,
    start,
    answerText,
    answerVoice
  };
}
