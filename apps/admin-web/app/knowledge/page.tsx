import { FilterForm } from "../../components/filter-form";
import { KnowledgeForm } from "../../components/knowledge-form";
import { SimpleTable } from "../../components/table";
import { getKnowledge } from "../../lib/api";

export default async function KnowledgePage({
  searchParams,
}: {
  searchParams?: { category?: string; enabled?: string };
}) {
  const items = await getKnowledge({
    category: searchParams?.category,
    enabled:
      searchParams?.enabled === "true"
        ? true
        : searchParams?.enabled === "false"
          ? false
          : undefined,
  });

  return (
    <>
      <KnowledgeForm items={items} />
      <FilterForm
        title="Filter Knowledge"
        fields={[
          {
            name: "category",
            label: "Category",
            type: "select",
            defaultValue: searchParams?.category ?? "",
            options: [
              { label: "All", value: "" },
              { label: "faq", value: "faq" },
              { label: "pre_sale", value: "pre_sale" },
              { label: "after_sale", value: "after_sale" },
              { label: "delivery", value: "delivery" },
            ],
          },
          {
            name: "enabled",
            label: "Enabled",
            type: "select",
            defaultValue: searchParams?.enabled ?? "",
            options: [
              { label: "All", value: "" },
              { label: "true", value: "true" },
              { label: "false", value: "false" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="Knowledge Items"
        rows={items}
        emptyText="当前没有知识库内容。"
        columns={[
          { key: "category", title: "Category", render: (row) => row.category },
          { key: "question", title: "Question", render: (row) => row.question },
          { key: "answer", title: "Answer", render: (row) => row.answer },
          { key: "enabled", title: "Enabled", render: (row) => String(row.enabled) },
        ]}
      />
    </>
  );
}
