import { FilterForm } from "../../components/filter-form";
import { getMessages } from "../../lib/api";
import { MessageInjectForm } from "../../components/message-inject-form";
import { SimpleTable } from "../../components/table";

export default async function MessagesPage({
  searchParams,
}: {
  searchParams?: { limit?: string };
}) {
  const messages = await getMessages({ limit: searchParams?.limit ? Number(searchParams.limit) : undefined });

  return (
    <>
      <MessageInjectForm />
      <FilterForm
        title="Filter Messages"
        fields={[
          {
            name: "limit",
            label: "Limit",
            type: "select",
            defaultValue: searchParams?.limit ?? "50",
            options: [
              { label: "20", value: "20" },
              { label: "50", value: "50" },
              { label: "100", value: "100" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="Messages"
        rows={messages}
        emptyText="当前没有消息数据，先调用 /events/messages/received 注入消息。"
        columns={[
          { key: "external_message_id", title: "External ID", render: (row) => row.external_message_id ?? "-" },
          { key: "sender_type", title: "Sender", render: (row) => row.sender_type },
          { key: "direction", title: "Direction", render: (row) => row.direction },
          { key: "processed_status", title: "Processed", render: (row) => row.processed_status },
          { key: "content", title: "Content", render: (row) => row.content },
          { key: "created_at", title: "Created", render: (row) => new Date(row.created_at).toLocaleString() },
        ]}
      />
    </>
  );
}
