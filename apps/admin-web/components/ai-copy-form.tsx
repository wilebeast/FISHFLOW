"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { generateAICopy } from "../lib/api";

export function AICopyForm() {
  const router = useRouter();
  const [scene, setScene] = useState("title");
  const [productTitle, setProductTitle] = useState("演示版数字商品");
  const [description, setDescription] = useState("支持自动发货，适合数字商品卖家。");
  const [question, setQuestion] = useState("怎么发货？");
  const [answer, setAnswer] = useState("付款后系统自动发货。");
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>AI Copy Generator</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 760 }}>
        <select value={scene} onChange={(e) => setScene(e.target.value)}>
          <option value="title">title</option>
          <option value="description">description</option>
          <option value="faq">faq</option>
          <option value="rewrite">rewrite</option>
        </select>
        <input value={productTitle} onChange={(e) => setProductTitle(e.target.value)} placeholder="product title" />
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} placeholder="description or highlights" />
        <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="question" />
        <input value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="answer" />
        <button
          type="button"
          onClick={() => {
            startTransition(async () => {
              try {
                setError(null);
                const response = await generateAICopy({
                  scene,
                  product_title: productTitle.trim(),
                  description: description.trim(),
                  highlights: description.trim(),
                  question: question.trim(),
                  answer: answer.trim(),
                });
                setResult(response.content);
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "generate ai copy failed");
              }
            });
          }}
        >
          Generate
        </button>
        {result ? <div style={{ color: "#355e3b", whiteSpace: "pre-wrap" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
