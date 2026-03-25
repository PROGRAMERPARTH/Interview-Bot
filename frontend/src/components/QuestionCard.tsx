import { useRef, useState } from 'react';
import { GeneratedQuestion } from '../types/interview';

interface Props {
  question: GeneratedQuestion;
  mode: 'text' | 'voice';
  loading: boolean;
  onSubmitText: (answer: string) => Promise<void>;
  onSubmitVoice: (audio: Blob) => Promise<void>;
}

export function QuestionCard({ question, mode, loading, onSubmitText, onSubmitVoice }: Props) {
  const [answer, setAnswer] = useState('');
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);

  async function handleTextSubmit() {
    if (!answer.trim()) return;
    await onSubmitText(answer);
    setAnswer('');
  }

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    chunks.current = [];
    recorder.ondataavailable = (event) => chunks.current.push(event.data);
    recorder.onstop = async () => {
      const blob = new Blob(chunks.current, { type: 'audio/webm' });
      await onSubmitVoice(blob);
    };
    recorder.start();
    mediaRecorder.current = recorder;
    setRecording(true);
  }

  function stopRecording() {
    mediaRecorder.current?.stop();
    setRecording(false);
  }

  return (
    <section className="card">
      <h2>Question</h2>
      <p>{question.question}</p>
      {mode === 'text' ? (
        <>
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer"
            rows={6}
          />
          <button disabled={loading} onClick={handleTextSubmit}>
            Submit Answer
          </button>
        </>
      ) : (
        <div>
          {!recording ? (
            <button disabled={loading} onClick={startRecording}>Start Recording</button>
          ) : (
            <button disabled={loading} onClick={stopRecording}>Stop & Submit</button>
          )}
        </div>
      )}
    </section>
  );
}
