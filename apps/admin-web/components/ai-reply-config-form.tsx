"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createAIReplyConfig, updateAIReplyConfig, type AIReplyConfigItem } from "../lib/api";

export function AIReplyConfigForm({ config }: { config: AIReplyConfigItem | null }) {
  const router = useRouter();
  const [provider, setProvider] = useState(config?.provider ?? "openai-compatible");
  const [model, setModel] = useState(config?.model ?? "gpt-5-mini");
  const [systemPrompt, setSystemPrompt] = useState(
    config?.system_prompt ?? "You are a concise sales assistant.",
  );
  const [temperature, setTemperature] = useState(String(config?.temperature ?? 0.2));
  const [maxTokens, setMaxTokens] = useState(String(config?.max_tokens ?? 200));
  const [enabled, setEnabled] = useState(config?.enabled ?? true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>AI Reply Config</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 760 }}>
        <input value={provider} onChange={(e) => setProvider(e.target.value)} placeholder="provider" />
        <input value={model} onChange={(e) => setModel(e.target.value)} placeholder="model" />
        <textarea value={systemPrompt} onChange={(e) => setSystemPrompt(e.target.value)} rows={5} />
        <input value={temperature} onChange={(e) => setTemperature(e.target.value)} placeholder="temperature" />
        <input value={maxTokens} onChange={(e) => setMaxTokens(e.target.value)} placeholder="max tokens" />
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
                setResult(null);
                const payload = {
                  provider: provider.trim(),
                  model: model.trim(),
                  system_prompt: systemPrompt.trim(),
                  temperature: Number(temperature),
                  max_tokens: Number(maxTokens),
                  enabled,
                };
                if (config) {
                  await updateAIReplyConfig(config.id, payload);
                  setResult("AI reply config updated");
                } else {
                  await createAIReplyConfig(payload);
                  setResult("AI reply config created");
                }
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "save ai reply config failed");
              }
            });
          }}
        >
          {config ? "Update AI Reply Config" : "Create AI Reply Config"}
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
