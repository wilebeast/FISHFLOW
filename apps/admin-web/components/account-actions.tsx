"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { accountHealthCheck, disableAccount, type AccountItem } from "../lib/api";

export function AccountActions({ account }: { account: AccountItem }) {
  const router = useRouter();
  const [reason, setReason] = useState("disabled by operator");
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
        setError(err instanceof Error ? err.message : "account action failed");
      }
    });
  };

  return (
    <div style={{ display: "grid", gap: 8 }}>
      <button type="button" onClick={() => run(() => accountHealthCheck(account.id), "Health checked")}>
        Health Check
      </button>
      <input value={reason} onChange={(e) => setReason(e.target.value)} placeholder="disable reason" />
      <button
        type="button"
        onClick={() => reason.trim() && run(() => disableAccount(account.id, reason.trim()), "Account disabled")}
      >
        Disable
      </button>
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
