import { FormEvent, useState } from 'react';

interface Props {
  onStart: (payload: {
    role: string;
    difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
    mode: 'text' | 'voice';
    question_count: number;
  }) => Promise<void>;
  loading: boolean;
}

export function InterviewSetupForm({ onStart, loading }: Props) {
  const [role, setRole] = useState('Software Engineer');
  const [difficulty, setDifficulty] = useState<'Beginner' | 'Intermediate' | 'Advanced'>('Intermediate');
  const [mode, setMode] = useState<'text' | 'voice'>('text');
  const [questionCount, setQuestionCount] = useState(5);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onStart({ role, difficulty, mode, question_count: questionCount });
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>Setup Interview</h2>
      <label>
        Role
        <input value={role} onChange={(e) => setRole(e.target.value)} />
      </label>
      <label>
        Difficulty
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as typeof difficulty)}>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
      </label>
      <label>
        Mode
        <select value={mode} onChange={(e) => setMode(e.target.value as typeof mode)}>
          <option value="text">Text</option>
          <option value="voice">Voice</option>
        </select>
      </label>
      <label>
        Number of Questions
        <input
          type="number"
          min={1}
          max={20}
          value={questionCount}
          onChange={(e) => setQuestionCount(Number(e.target.value))}
        />
      </label>
      <button type="submit" disabled={loading}>
        {loading ? 'Starting...' : 'Start Interview'}
      </button>
    </form>
  );
}
