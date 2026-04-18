import { AICopyForm } from "../../../components/ai-copy-form";
import { FilterForm } from "../../../components/filter-form";
import { SimpleTable } from "../../../components/table";
import { getAICopyHistory } from "../../../lib/api";

export default async function AICopyPage({
  searchParams,
}: {
  searchParams?: { scene?: string };
}) {
  const history = await getAICopyHistory({ scene: searchParams?.scene });

  return (
    <>
      <AICopyForm />
      <FilterForm
        title="Filter AI Copy History"
        fields={[
          {
            name: "scene",
            label: "Scene",
            type: "select",
            defaultValue: searchParams?.scene ?? "",
            options: [
              { label: "All", value: "" },
              { label: "title", value: "title" },
              { label: "description", value: "description" },
              { label: "faq", value: "faq" },
              { label: "rewrite", value: "rewrite" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="AI Copy History"
        rows={history}
        emptyText="当前没有 AI 文案记录。"
        columns={[
          { key: "created_at", title: "Time", render: (row) => row.created_at },
          { key: "scene", title: "Scene", render: (row) => row.scene },
          { key: "operator", title: "Operator", render: (row) => row.operator },
          {
            key: "output_payload",
            title: "Output",
            render: (row) => <code style={{ fontSize: 12 }}>{JSON.stringify(row.output_payload)}</code>,
          },
        ]}
      />
    </>
  );
}
