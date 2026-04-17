"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { injectTestMessage } from "../lib/api";

export function MessageInjectForm() {
  const router = useRouter();
  const [externalConversationId, setExternalConversationId] = useState("conv_demo_001");
  const [content, setContent] = useState("你好，在吗");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Inject Test Message</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 640 }}>
        <label>
          <div>External Conversation ID</div>
          <input
            value={externalConversationId}
            onChange={(event) => setExternalConversationId(event.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </label>
        <label>
          <div>Content</div>
          <textarea
            value={content}
            onChange={(event) => setContent(event.target.value)}
            rows={4}
            style={{ width: "100%", padding: 8 }}
          />
        </label>
        <div>
          <button
            type="button"
            disabled={busy}
            onClick={() => {
              if (!externalConversationId.trim()) {
                setError("External Conversation ID is required");
                return;
              }
              if (!content.trim()) {
                setError("Content is required");
                return;
              }
              setBusy(true);
              setError(null);
              setResult(null);
              startTransition(async () => {
                try {
                  const response = await injectTestMessage({
                    external_conversation_id: externalConversationId.trim(),
                    content: content.trim(),
                  });
                  setResult(response.detail ?? response.status);
                  router.refresh();
                } catch (err) {
                  setError(err instanceof Error ? err.message : "inject message failed");
                } finally {
                  setBusy(false);
                }
              });
            }}
          >
            {busy ? "Submitting..." : "Inject Message"}
          </button>
        </div>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
