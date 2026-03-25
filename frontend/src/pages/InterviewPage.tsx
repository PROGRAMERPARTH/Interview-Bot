import { useState } from 'react';
import { FeedbackCard } from '../components/FeedbackCard';
import { InterviewSetupForm } from '../components/InterviewSetupForm';
import { ProgressHeader } from '../components/ProgressHeader';
import { QuestionCard } from '../components/QuestionCard';
import { useInterview } from '../hooks/useInterview';

export function InterviewPage() {
  const [mode, setMode] = useState<'text' | 'voice'>('text');
  const { question, feedback, report, totalQuestions, answered, loading, start, answerText, answerVoice } = useInterview();

  return (
    <main className="layout">
      <ProgressHeader answered={answered} total={totalQuestions} />

      {!question && !report && (
        <InterviewSetupForm
          loading={loading}
          onStart={async (payload) => {
            setMode(payload.mode);
            await start(payload);
          }}
        />
      )}

      {question && (
        <QuestionCard
          question={question}
          mode={mode}
          loading={loading}
          onSubmitText={answerText}
          onSubmitVoice={answerVoice}
        />
      )}

      <FeedbackCard feedback={feedback} />

      {report && (
        <section className="card">
          <h2>Final Performance Report</h2>
          <p><strong>Average Score:</strong> {report.average_score}/10</p>
          <p><strong>Top Strengths:</strong> {report.strengths.join(', ') || 'N/A'}</p>
          <p><strong>Top Weaknesses:</strong> {report.weaknesses.join(', ') || 'N/A'}</p>
          <p><strong>Recommended Focus:</strong> {report.suggested_improvements.join(', ') || 'N/A'}</p>
        </section>
      )}
    </main>
  );
}
