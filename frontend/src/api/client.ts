import axios from 'axios';
import { FinalReport, StartInterviewResponse, SubmitAnswerResponse } from '../types/interview';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
});

export async function startInterview(payload: {
  role: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  mode: 'text' | 'voice';
  question_count?: number;
}): Promise<StartInterviewResponse> {
  const { data } = await api.post('/api/v1/interviews', payload);
  return data;
}

export async function submitAnswer(interviewId: string, answer: string): Promise<SubmitAnswerResponse> {
  const { data } = await api.post(`/api/v1/interviews/${interviewId}/answer`, { answer });
  return data;
}

export async function submitVoiceAnswer(interviewId: string, audio: Blob): Promise<SubmitAnswerResponse> {
  const form = new FormData();
  form.append('audio', audio, 'answer.webm');
  const { data } = await api.post(`/api/v1/interviews/${interviewId}/answer/voice`, form);
  return data;
}

export async function getFinalReport(interviewId: string): Promise<FinalReport> {
  const { data } = await api.get(`/api/v1/interviews/${interviewId}/report`);
  return data;
}
