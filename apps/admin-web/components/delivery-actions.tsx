"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { retryDelivery, type DeliveryItem } from "../lib/api";

export function DeliveryActions({ task }: { task: DeliveryItem }) {
  const router = useRouter();
  const [expanded, setExpanded] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const canRetry = task.status !== "success";

  return (
    <div style={{ display: "grid", gap: 8 }}>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <button type="button" onClick={() => setExpanded((value) => !value)}>
          {expanded ? "Hide Detail" : "Show Detail"}
        </button>
        <button
          type="button"
          disabled={!canRetry || busy}
          onClick={() => {
            setBusy(true);
            setError(null);
            setResult(null);
            startTransition(async () => {
              try {
                await retryDelivery(task.id);
                setResult("Retry queued");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "retry failed");
              } finally {
                setBusy(false);
              }
            });
          }}
        >
          {busy ? "Retrying..." : "Retry"}
        </button>
      </div>
      {expanded ? (
        <pre
          style={{
            margin: 0,
            padding: 12,
            whiteSpace: "pre-wrap",
            background: "#f7f1e7",
            border: "1px solid #e1d3bf",
          }}
        >
          {JSON.stringify(
            {
              idempotency_key: task.idempotency_key,
              payload_snapshot: task.payload_snapshot,
              result_message: task.result_message,
              last_error: task.last_error,
              executed_at: task.executed_at,
            },
            null,
            2,
          )}
        </pre>
      ) : null}
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
