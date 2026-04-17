"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createInventoryItem } from "../lib/api";

export function InventoryCreateForm() {
  const router = useRouter();
  const [resourceType, setResourceType] = useState("card");
  const [code, setCode] = useState("CARD-DEMO-001");
  const [content, setContent] = useState("演示卡密内容");
  const [note, setNote] = useState("demo stock");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Create Inventory Item</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 640 }}>
        <select value={resourceType} onChange={(e) => setResourceType(e.target.value)}>
          <option value="card">card</option>
          <option value="link">link</option>
          <option value="text">text</option>
        </select>
        <input value={code} onChange={(e) => setCode(e.target.value)} placeholder="code" />
        <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={4} placeholder="content" />
        <input value={note} onChange={(e) => setNote(e.target.value)} placeholder="note" />
        <button
          type="button"
          onClick={() => {
            if (!content.trim()) {
              setError("content is required");
              return;
            }
            startTransition(async () => {
              try {
                setError(null);
                setResult(null);
                await createInventoryItem({
                  resource_type: resourceType,
                  code: code.trim() || undefined,
                  content: content.trim(),
                  note: note.trim() || undefined,
                });
                setResult("Inventory item created");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "create inventory item failed");
              }
            });
          }}
        >
          Create Inventory Item
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
