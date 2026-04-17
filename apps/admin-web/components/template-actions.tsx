"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { updateTemplate, type TemplateItem } from "../lib/api";

export function TemplateActions({ template }: { template: TemplateItem }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <div>
      <button
        type="button"
        disabled={busy}
        onClick={() => {
          setBusy(true);
          startTransition(async () => {
            try {
              setError(null);
              setResult(null);
              await updateTemplate(template.id, { enabled: !template.enabled });
              setResult(template.enabled ? "Template disabled" : "Template enabled");
              router.refresh();
            } catch (err) {
              setError(err instanceof Error ? err.message : "update template failed");
            } finally {
              setBusy(false);
            }
          });
        }}
      >
        {busy ? "Updating..." : template.enabled ? "Disable" : "Enable"}
      </button>
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
