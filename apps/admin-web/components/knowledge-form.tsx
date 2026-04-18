"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createKnowledge, updateKnowledge, type KnowledgeItem } from "../lib/api";

export function KnowledgeForm({ items }: { items: KnowledgeItem[] }) {
  const router = useRouter();
  const existing = items[0];
  const [category, setCategory] = useState(existing?.category ?? "faq");
  const [question, setQuestion] = useState(existing?.question ?? "怎么发货？");
  const [answer, setAnswer] = useState(existing?.answer ?? "付款后系统自动发货。");
  const [enabled, setEnabled] = useState(existing?.enabled ?? true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Knowledge Item</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 760 }}>
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="faq">faq</option>
          <option value="pre_sale">pre_sale</option>
          <option value="after_sale">after_sale</option>
          <option value="delivery">delivery</option>
        </select>
        <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="question" />
        <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} rows={4} placeholder="answer" />
        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />
          Enabled
        </label>
        <button
          type="button"
          onClick={() => {
            startTransition(async () => {
              try {
                setError(null);
                if (existing) {
                  await updateKnowledge(existing.id, {
                    category,
                    question: question.trim(),
                    answer: answer.trim(),
                    enabled,
                  });
                  setResult("Knowledge updated");
                } else {
                  await createKnowledge({
                    category,
                    question: question.trim(),
                    answer: answer.trim(),
                    enabled,
                  });
                  setResult("Knowledge created");
                }
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "save knowledge failed");
              }
            });
          }}
        >
          {existing ? "Update Knowledge" : "Create Knowledge"}
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
