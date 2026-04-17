"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { allocateInventoryItem, disableInventoryItem, type InventoryItem } from "../lib/api";

export function InventoryActions({ item }: { item: InventoryItem }) {
  const router = useRouter();
  const [orderId, setOrderId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const run = (task: () => Promise<unknown>, successMessage: string) => {
    startTransition(async () => {
      try {
        setError(null);
        setResult(null);
        await task();
        setResult(successMessage);
        router.refresh();
      } catch (err) {
        setError(err instanceof Error ? err.message : "inventory action failed");
      }
    });
  };

  return (
    <div style={{ display: "grid", gap: 8 }}>
      <input value={orderId} onChange={(e) => setOrderId(e.target.value)} placeholder="order uuid for allocation" />
      <button
        type="button"
        onClick={() => orderId.trim() && run(() => allocateInventoryItem(item.id, orderId.trim()), "Inventory allocated")}
      >
        Allocate
      </button>
      <button type="button" onClick={() => run(() => disableInventoryItem(item.id), "Inventory disabled")}>
        Disable
      </button>
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
