"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { bindProductRule, bindProductTemplate, toggleAutoDelivery, type ProductItem } from "../lib/api";

export function ProductActions({ product }: { product: ProductItem }) {
  const router = useRouter();
  const [deliveryTemplateId, setDeliveryTemplateId] = useState(product.delivery_template_id ?? "");
  const [faqTemplateId, setFaqTemplateId] = useState(product.faq_template_id ?? "");
  const [ruleId, setRuleId] = useState(product.rule_profile_id ?? "");
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
        setError(err instanceof Error ? err.message : "product action failed");
      }
    });
  };

  return (
    <div style={{ display: "grid", gap: 8 }}>
      <div style={{ fontSize: 12, color: "#735f48" }}>
        Use IDs from the Rules and Templates pages.
      </div>
      <button type="button" onClick={() => run(() => toggleAutoDelivery(product.id), "Auto delivery updated")}>
        Toggle Auto Delivery
      </button>
      <input value={ruleId} onChange={(e) => setRuleId(e.target.value)} placeholder="rule id" />
      <button type="button" onClick={() => ruleId.trim() && run(() => bindProductRule(product.id, ruleId), "Rule bound")}>
        Bind Rule
      </button>
      <input value={deliveryTemplateId} onChange={(e) => setDeliveryTemplateId(e.target.value)} placeholder="delivery template id" />
      <button
        type="button"
        onClick={() =>
          deliveryTemplateId.trim() &&
          run(() => bindProductTemplate(product.id, "delivery", deliveryTemplateId), "Delivery template bound")
        }
      >
        Bind Delivery Template
      </button>
      <input value={faqTemplateId} onChange={(e) => setFaqTemplateId(e.target.value)} placeholder="faq template id" />
      <button
        type="button"
        onClick={() =>
          faqTemplateId.trim() &&
          run(() => bindProductTemplate(product.id, "faq", faqTemplateId), "FAQ template bound")
        }
      >
        Bind FAQ Template
      </button>
      {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
      {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
    </div>
  );
}
