import { SimpleTable } from "../../components/table";
import { getAdminActions, getSystemErrors } from "../../lib/api";

export default async function AuditPage() {
  const [actions, events] = await Promise.all([getAdminActions({ limit: 50 }), getSystemErrors()]);

  return (
    <>
      <SimpleTable
        title="Admin Actions"
        rows={actions}
        emptyText="当前没有后台操作日志。"
        columns={[
          { key: "created_at", title: "Time", render: (row) => row.created_at },
          { key: "actor", title: "Actor", render: (row) => row.actor },
          { key: "action", title: "Action", render: (row) => row.action },
          { key: "target_type", title: "Target Type", render: (row) => row.target_type },
          { key: "target_id", title: "Target ID", render: (row) => row.target_id },
          {
            key: "payload",
            title: "Payload",
            render: (row) => <code style={{ fontSize: 12 }}>{JSON.stringify(row.payload)}</code>,
          },
        ]}
      />
      <SimpleTable
        title="System Events"
        rows={events}
        emptyText="当前没有系统事件。"
        columns={[
          { key: "created_at", title: "Time", render: (row) => row.created_at },
          { key: "event_type", title: "Event", render: (row) => row.event_type },
          { key: "severity", title: "Severity", render: (row) => row.severity },
          { key: "source", title: "Source", render: (row) => row.source },
          { key: "message", title: "Message", render: (row) => row.message ?? "-" },
        ]}
      />
    </>
  );
}
