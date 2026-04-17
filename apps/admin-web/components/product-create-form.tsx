"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createProduct } from "../lib/api";

export function ProductCreateForm() {
  const router = useRouter();
  const [externalProductId, setExternalProductId] = useState("prod_demo_new");
  const [title, setTitle] = useState("新的演示商品");
  const [category, setCategory] = useState("digital");
  const [price, setPrice] = useState("9.90");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Create Product</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 640 }}>
        <input value={externalProductId} onChange={(e) => setExternalProductId(e.target.value)} placeholder="external_product_id" />
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="title" />
        <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="category" />
        <input value={price} onChange={(e) => setPrice(e.target.value)} placeholder="price" />
        <button
          type="button"
          disabled={busy}
          onClick={() => {
            if (!externalProductId.trim()) {
              setError("external_product_id is required");
              return;
            }
            if (!title.trim()) {
              setError("title is required");
              return;
            }
            if (Number.isNaN(Number(price)) || Number(price) < 0) {
              setError("price must be a valid non-negative number");
              return;
            }
            setBusy(true);
            setError(null);
            setResult(null);
            startTransition(async () => {
              try {
                await createProduct({
                  external_product_id: externalProductId.trim(),
                  title: title.trim(),
                  category: category.trim(),
                  price: Number(price),
                  delivery_mode: "auto",
                });
                setResult("Product created");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "create product failed");
              } finally {
                setBusy(false);
              }
            });
          }}
        >
          {busy ? "Creating..." : "Create Product"}
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
