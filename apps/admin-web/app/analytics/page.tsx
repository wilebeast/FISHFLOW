import { SimpleTable } from "../../components/table";
import { getAnalyticsHistory, getAnalyticsOverview } from "../../lib/api";

export default async function AnalyticsPage() {
  const [overview, history] = await Promise.all([getAnalyticsOverview(), getAnalyticsHistory()]);

  return (
    <>
      <section style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
        <h2 style={{ marginTop: 0 }}>Analytics Overview</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 }}>
          <div>Snapshot: {overview?.snapshot_date ?? "-"}</div>
          <div>Messages: {overview?.message_count ?? 0}</div>
          <div>Auto Reply: {overview?.auto_reply_count ?? 0}</div>
          <div>Handoffs: {overview?.handoff_count ?? 0}</div>
          <div>Delivery Success: {overview?.delivery_success_count ?? 0}</div>
          <div>Delivery Fail: {overview?.delivery_fail_count ?? 0}</div>
        </div>
      </section>
      <SimpleTable
        title="Analytics History"
        rows={history}
        emptyText="当前没有报表快照。"
        columns={[
          { key: "snapshot_date", title: "Date", render: (row) => row.snapshot_date },
          { key: "message_count", title: "Messages", render: (row) => row.message_count },
          { key: "auto_reply_count", title: "Auto Reply", render: (row) => row.auto_reply_count },
          { key: "handoff_count", title: "Handoffs", render: (row) => row.handoff_count },
          { key: "delivery_success_count", title: "Delivery Success", render: (row) => row.delivery_success_count },
          { key: "delivery_fail_count", title: "Delivery Fail", render: (row) => row.delivery_fail_count },
        ]}
      />
    </>
  );
}
