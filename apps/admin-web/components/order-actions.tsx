"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { markOrderPaid, type OrderItem } from "../lib/api";

export function OrderActions({ order }: { order: OrderItem }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const disabled = busy || order.pay_status === "paid";

  return (
    <div>
      <button
        type="button"
        disabled={disabled}
        onClick={() => {
          setBusy(true);
          setError(null);
          setResult(null);
          startTransition(async () => {
            try {
              await markOrderPaid(order.id);
              setResult("Marked as paid");
              router.refresh();
            } catch (err) {
              setError(err instanceof Error ? err.message : "mark paid failed");
            } finally {
              setBusy(false);
            }
          });
        }}
      >
        {busy ? "Processing..." : "Mark Paid"}
      </button>
      {result ? <div style={{ color: "#355e3b", marginTop: 6 }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f", marginTop: 6 }}>{error}</div> : null}
    </div>
  );
}
