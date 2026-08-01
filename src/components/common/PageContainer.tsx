// src/components/common/PageContainer.tsx

import type { PropsWithChildren } from "react";

export default function PageContainer({
  children,
}: PropsWithChildren) {
  return (
    <div className="mx-auto w-full space-y-6">
      {children}
    </div>
  );
}