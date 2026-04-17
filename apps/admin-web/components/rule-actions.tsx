"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { setRuleEnabled, type RuleItem } from "../lib/api";

export function RuleActions({ rule }: { rule: RuleItem }) {
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
              await setRuleEnabled(rule.id, !rule.enabled);
              setResult(rule.enabled ? "Rule disabled" : "Rule enabled");
              router.refresh();
            } catch (err) {
              setError(err instanceof Error ? err.message : "toggle rule failed");
            } finally {
              setBusy(false);
            }
          });
        }}
      >
        {busy ? "Updating..." : rule.enabled ? "Disable" : "Enable"}
      </button>
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
