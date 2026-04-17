import { FilterForm } from "../../components/filter-form";
import { ConversationActions } from "../../components/conversation-actions";
import { SimpleTable } from "../../components/table";
import { getConversations } from "../../lib/api";

export default async function ConversationsPage({
  searchParams,
}: {
  searchParams?: { product_id?: string; handoff_status?: string; buyer_id?: string };
}) {
  const conversations = await getConversations(searchParams);

  return (
    <>
      <FilterForm
        title="Filter Conversations"
        fields={[
          { name: "product_id", label: "Product ID", type: "text", defaultValue: searchParams?.product_id },
          { name: "buyer_id", label: "Buyer ID", type: "text", defaultValue: searchParams?.buyer_id },
          {
            name: "handoff_status",
            label: "Handoff",
            type: "select",
            defaultValue: searchParams?.handoff_status ?? "",
            options: [
              { label: "All", value: "" },
              { label: "bot", value: "bot" },
              { label: "human", value: "human" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="Conversations"
        rows={conversations}
        emptyText="当前没有会话数据。"
        columns={[
          { key: "external_conversation_id", title: "External ID", render: (row) => row.external_conversation_id },
          { key: "buyer_id", title: "Buyer", render: (row) => row.buyer_id ?? "-" },
          { key: "current_stage", title: "Stage", render: (row) => row.current_stage },
          { key: "handoff_status", title: "Handoff", render: (row) => row.handoff_status },
          { key: "unread_count", title: "Unread", render: (row) => row.unread_count },
          { key: "summary", title: "Summary", render: (row) => row.summary ?? "-" },
          { key: "actions", title: "Actions", render: (row) => <ConversationActions conversation={row} /> },
        ]}
      />
    </>
  );
}
