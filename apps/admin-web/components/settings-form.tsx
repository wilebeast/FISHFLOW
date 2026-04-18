"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { exportSettings, importSettings, saveSetting, type AppSettingItem } from "../lib/api";

export function SettingsForm({ settings }: { settings: AppSettingItem[] }) {
  const router = useRouter();
  const existing = settings[0];
  const [key, setKey] = useState(existing?.key ?? "app.branding");
  const [valueText, setValueText] = useState(
    JSON.stringify(existing?.value_json ?? { name: "FishFlow", mode: "demo" }, null, 2),
  );
  const [exported, setExported] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Settings</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 760 }}>
        <input value={key} onChange={(e) => setKey(e.target.value)} placeholder="setting key" />
        <textarea value={valueText} onChange={(e) => setValueText(e.target.value)} rows={8} />
        <button
          type="button"
          onClick={() => {
            startTransition(async () => {
              try {
                setError(null);
                const parsed = JSON.parse(valueText);
                await saveSetting({ key: key.trim(), value_json: parsed });
                setResult("Setting saved");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "save setting failed");
              }
            });
          }}
        >
          Save Setting
        </button>
        <button
          type="button"
          onClick={() => {
            startTransition(async () => {
              try {
                setError(null);
                const data = await exportSettings();
                setExported(JSON.stringify(data, null, 2));
              } catch (err) {
                setError(err instanceof Error ? err.message : "export settings failed");
              }
            });
          }}
        >
          Export Settings
        </button>
        <button
          type="button"
          onClick={() => {
            startTransition(async () => {
              try {
                setError(null);
                await importSettings(JSON.parse(valueText));
                setResult("Settings imported");
                router.refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "import settings failed");
              }
            });
          }}
        >
          Import From JSON
        </button>
        {exported ? <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>{exported}</pre> : null}
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
