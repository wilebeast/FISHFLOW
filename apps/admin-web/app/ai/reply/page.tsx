import { AIReplyConfigForm } from "../../../components/ai-reply-config-form";
import { AIReplyTestForm } from "../../../components/ai-reply-test-form";
import { SimpleTable } from "../../../components/table";
import { getAIReplyConfig, getAIReplyLogs } from "../../../lib/api";

export default async function AIReplyPage() {
  const [config, logs] = await Promise.all([getAIReplyConfig(), getAIReplyLogs()]);

  return (
    <>
      <AIReplyConfigForm config={config} />
      <AIReplyTestForm />
      <SimpleTable
        title="AI Reply Logs"
        rows={logs}
        emptyText="当前没有 AI 调用日志。"
        columns={[
          { key: "created_at", title: "Time", render: (row) => row.created_at },
          { key: "scene", title: "Scene", render: (row) => row.scene },
          { key: "model", title: "Model", render: (row) => row.model },
          { key: "status", title: "Status", render: (row) => row.status },
          { key: "latency_ms", title: "Latency", render: (row) => `${row.latency_ms} ms` },
          {
            key: "response_snapshot",
            title: "Reply",
            render: (row) => <code style={{ fontSize: 12 }}>{JSON.stringify(row.response_snapshot)}</code>,
          },
        ]}
      />
    </>
  );
}
