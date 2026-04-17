"use client";

import { startTransition, useState } from "react";

import { testAIReply } from "../lib/api";

export function AIReplyTestForm() {
  const [message, setMessage] = useState("这个商品怎么发货？");
  const [productTitle, setProductTitle] = useState("演示版数字商品");
  const [reply, setReply] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>AI Reply Test</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 760 }}>
        <input value={productTitle} onChange={(e) => setProductTitle(e.target.value)} placeholder="product title" />
        <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={4} placeholder="buyer message" />
        <button
          type="button"
          onClick={() => {
            startTransition(async () => {
              try {
                setError(null);
                const result = await testAIReply({
                  message: message.trim(),
                  product_title: productTitle.trim() || undefined,
                });
                setReply(result.reply);
              } catch (err) {
                setError(err instanceof Error ? err.message : "test ai reply failed");
              }
            });
          }}
        >
          Generate Demo Reply
        </button>
        {reply ? <div style={{ color: "#355e3b", whiteSpace: "pre-wrap" }}>{reply}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
