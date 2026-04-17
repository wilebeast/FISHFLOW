"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createAccount } from "../lib/api";

export function AccountCreateForm() {
  const router = useRouter();
  const [nickname, setNickname] = useState("Demo Account");
  const [externalAccountId, setExternalAccountId] = useState("acc_demo_new");
  const [riskLevel, setRiskLevel] = useState("low");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Create Account</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 640 }}>
        <input value={nickname} onChange={(e) => setNickname(e.target.value)} placeholder="nickname" />
        <input
          value={externalAccountId}
          onChange={(e) => setExternalAccountId(e.target.value)}
          placeholder="external_account_id"
        />
        <select value={riskLevel} onChange={(e) => setRiskLevel(e.target.value)}>
          <option value="low">low</option>
          <option value="medium">medium</option>
          <option value="high">high</option>
        </select>
        <button
          type="button"
          disabled={busy}
          onClick={() => {
            if (!nickname.trim() || !externalAccountId.trim()) {
              setError("nickname and external_account_id are required");
              return;
            }
            setBusy(true);
            setError(null);
            setResult(null);
            startTransition(async () => {
              try {
                await createAccount({
                  nickname: nickname.trim(),
                  external_account_id: externalAccountId.trim(),
                  risk_level: riskLevel,
                });
                setResult("Account created");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "create account failed");
              } finally {
                setBusy(false);
              }
            });
          }}
        >
          {busy ? "Creating..." : "Create Account"}
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
