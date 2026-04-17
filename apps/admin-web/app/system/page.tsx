import { SimpleTable } from "../../components/table";
import { getQueueHealth, getSystemErrors, getSystemHealth } from "../../lib/api";

export default async function SystemPage() {
  const health = await getSystemHealth();
  const queue = await getQueueHealth();
  const errors = await getSystemErrors();

  return (
    <>
      <section style={{ marginBottom: 24, display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}>
        {[
          { label: "API", value: health?.api ?? "unknown" },
          { label: "Database", value: health?.database ?? "unknown" },
          { label: "Redis", value: health?.redis ?? "unknown" },
          { label: "Worker", value: queue?.worker ?? health?.worker ?? "unknown" },
        ].map((item) => (
          <div key={item.label} style={{ border: "1px solid #ccb89f", background: "#fffdf8", padding: 16 }}>
            <strong>{item.label}</strong>
            <div style={{ marginTop: 8 }}>{item.value}</div>
          </div>
        ))}
      </section>
      <section style={{ marginBottom: 24, border: "1px solid #ccb89f", background: "#fffdf8", padding: 16 }}>
        <h2 style={{ marginTop: 0 }}>Queue</h2>
        <pre style={{ marginBottom: 0, whiteSpace: "pre-wrap" }}>{JSON.stringify(queue, null, 2)}</pre>
      </section>
      <SimpleTable
        title="Recent System Events"
        rows={errors}
        emptyText="当前没有系统事件。"
        columns={[
          { key: "event_type", title: "Event", render: (row) => row.event_type },
          { key: "severity", title: "Severity", render: (row) => row.severity },
          { key: "source", title: "Source", render: (row) => row.source },
          { key: "message", title: "Message", render: (row) => row.message ?? "-" },
          { key: "created_at", title: "Created", render: (row) => new Date(row.created_at).toLocaleString() },
        ]}
      />
    </>
  );
}
