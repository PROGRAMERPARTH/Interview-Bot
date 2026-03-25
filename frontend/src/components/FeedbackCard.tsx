import { Feedback } from '../types/interview';

export function FeedbackCard({ feedback }: { feedback: Feedback | null }) {
  if (!feedback) return null;

  return (
    <section className="card">
      <h2>Feedback</h2>
      <p><strong>Score:</strong> {feedback.score}/10</p>
      <p><strong>Summary:</strong> {feedback.summary}</p>
      <p><strong>Strengths:</strong> {feedback.strengths.join(', ') || 'N/A'}</p>
      <p><strong>Weaknesses:</strong> {feedback.weaknesses.join(', ') || 'N/A'}</p>
      <p><strong>Suggested Improvements:</strong> {feedback.suggested_improvements.join(', ') || 'N/A'}</p>
      <p><strong>Keyword Coverage:</strong> {Math.round(feedback.keyword_coverage * 100)}%</p>
    </section>
  );
}
