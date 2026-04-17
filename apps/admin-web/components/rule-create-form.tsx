"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createRule } from "../lib/api";

export function RuleCreateForm() {
  const router = useRouter();
  const [name, setName] = useState("新的消息规则");
  const [contains, setContains] = useState("你好");
  const [replyContent, setReplyContent] = useState("您好，在的。");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Create Rule</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 720 }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="rule name" />
        <input value={contains} onChange={(e) => setContains(e.target.value)} placeholder="contains" />
        <textarea value={replyContent} onChange={(e) => setReplyContent(e.target.value)} rows={3} />
        <button
          type="button"
          onClick={() => {
            if (!name.trim()) {
              setError("rule name is required");
              return;
            }
            if (!contains.trim()) {
              setError("contains is required");
              return;
            }
            if (!replyContent.trim()) {
              setError("reply content is required");
              return;
            }
            startTransition(async () => {
              try {
                setError(null);
                setResult(null);
                await createRule({
                  name: name.trim(),
                  scope: "global",
                  trigger_type: "message_received",
                  conditions: { event: "message_received", contains: contains.trim() },
                  action_type: "reply_text",
                  action_payload: { content: replyContent.trim() },
                });
                setResult("Rule created");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "create rule failed");
              }
            });
          }}
        >
          Create Rule
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
