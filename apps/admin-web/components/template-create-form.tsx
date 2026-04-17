"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createTemplate } from "../lib/api";

export function TemplateCreateForm() {
  const router = useRouter();
  const [name, setName] = useState("新的回复模板");
  const [templateType, setTemplateType] = useState("reply");
  const [category, setCategory] = useState("sales");
  const [content, setContent] = useState("您好，这里是模板内容。");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Create Template</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 720 }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="name" />
        <select value={templateType} onChange={(e) => setTemplateType(e.target.value)}>
          <option value="reply">reply</option>
          <option value="delivery">delivery</option>
          <option value="faq">faq</option>
        </select>
        <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="category" />
        <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={4} />
        <button
          type="button"
          onClick={() => {
            if (!name.trim()) {
              setError("name is required");
              return;
            }
            if (!content.trim()) {
              setError("content is required");
              return;
            }
            startTransition(async () => {
              try {
                setError(null);
                setResult(null);
                await createTemplate({ template_type: templateType, name: name.trim(), category: category.trim(), content: content.trim() });
                setResult("Template created");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "create template failed");
              }
            });
          }}
        >
          Create Template
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
