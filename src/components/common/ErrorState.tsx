// src/components/common/ErrorState.tsx

interface ErrorStateProps {
  message: string;
}

export default function ErrorState({
  message,
}: ErrorStateProps) {
  return (
    <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-6 text-center">
      <p className="text-destructive">
        {message}
      </p>
    </div>
  );
}