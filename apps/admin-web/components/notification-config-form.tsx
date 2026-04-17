"use client";

import { startTransition, useState } from "react";
import { useRouter } from "next/navigation";

import { createNotificationConfig, testNotification, updateNotificationConfig, type NotificationConfigItem } from "../lib/api";

export function NotificationConfigForm({ configs }: { configs: NotificationConfigItem[] }) {
  const router = useRouter();
  const existing = configs[0];
  const [channel, setChannel] = useState(existing?.channel ?? "webhook");
  const [name, setName] = useState(existing?.name ?? "Default Webhook");
  const [target, setTarget] = useState(existing?.target ?? "https://example.com/webhook");
  const [enabled, setEnabled] = useState(existing?.enabled ?? true);
  const [testMessage, setTestMessage] = useState("FishFlow notification test");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const save = () => {
    startTransition(async () => {
      try {
        setError(null);
        setResult(null);
        if (existing) {
          await updateNotificationConfig(existing.id, {
            name: name.trim(),
            target: target.trim(),
            enabled,
          });
          setResult("Notification config updated");
        } else {
          await createNotificationConfig({
            channel,
            name: name.trim(),
            target: target.trim(),
            enabled,
          });
          setResult("Notification config created");
        }
        router.refresh();
      } catch (err) {
        setError(err instanceof Error ? err.message : "save notification config failed");
      }
    });
  };

  const runTest = () => {
    startTransition(async () => {
      try {
        setError(null);
        setResult(null);
        await testNotification({ message: testMessage.trim() || "FishFlow notification test" });
        setResult("Notification test recorded");
        router.refresh();
      } catch (err) {
        setError(err instanceof Error ? err.message : "notification test failed");
      }
    });
  };

  return (
    <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Notification Config</h2>
      <div style={{ display: "grid", gap: 12, maxWidth: 720 }}>
        <select value={channel} onChange={(e) => setChannel(e.target.value)}>
          <option value="webhook">webhook</option>
          <option value="feishu">feishu</option>
          <option value="email">email</option>
        </select>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="config name" />
        <input value={target} onChange={(e) => setTarget(e.target.value)} placeholder="target" />
        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />
          Enabled
        </label>
        <button type="button" onClick={save}>
          {existing ? "Update Notification Config" : "Create Notification Config"}
        </button>
        <textarea value={testMessage} onChange={(e) => setTestMessage(e.target.value)} rows={3} placeholder="test message" />
        <button type="button" onClick={runTest}>
          Send Test
        </button>
        {result ? <div style={{ color: "#355e3b" }}>{result}</div> : null}
        {error ? <div style={{ color: "#a63a2f" }}>{error}</div> : null}
      </div>
    </section>
  );
}
