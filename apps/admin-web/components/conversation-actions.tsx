"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { handoffConversation, releaseConversation, sendConversationMessage, type ConversationItem } from "../lib/api";

export function ConversationActions({ conversation }: { conversation: ConversationItem }) {
  const router = useRouter();
  const [content, setContent] = useState("您好，在的，请问需要哪款商品？");
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
        setError(err instanceof Error ? err.message : "conversation action failed");
      }
    });
  };

  return (
    <div style={{ display: "grid", gap: 8 }}>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <button type="button" onClick={() => run(() => handoffConversation(conversation.id), "Conversation handed off")}>
          Handoff
        </button>
        <button type="button" onClick={() => run(() => releaseConversation(conversation.id), "Conversation released")}>
          Release
        </button>
      </div>
      <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={3} />
      <button
        type="button"
        onClick={() => {
          if (!content.trim()) {
            setError("Message content is required");
            return;
          }
          run(() => sendConversationMessage(conversation.id, content.trim()), "Message sent");
        }}
      >
        Send Message
      </button>
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
