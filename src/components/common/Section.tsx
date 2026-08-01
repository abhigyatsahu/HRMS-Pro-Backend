// src/components/common/Section.tsx

import type { PropsWithChildren } from "react";

export default function Section({
  children,
}: PropsWithChildren) {
  return (
    <section className="rounded-xl border bg-card p-6">
      {children}
    </section>
  );
}