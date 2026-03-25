export function ProgressHeader({ answered, total }: { answered: number; total: number }) {
  const percent = total ? Math.round((answered / total) * 100) : 0;
  return (
    <header className="card">
      <h1>AI Interviewer Bot</h1>
      <p>
        Progress: {answered}/{total} ({percent}%)
      </p>
    </header>
  );
}
