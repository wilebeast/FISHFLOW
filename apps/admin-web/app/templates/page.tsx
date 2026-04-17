import { FilterForm } from "../../components/filter-form";
import { TemplateActions } from "../../components/template-actions";
import { TemplateCreateForm } from "../../components/template-create-form";
import { SimpleTable } from "../../components/table";
import { getTemplates } from "../../lib/api";

export default async function TemplatesPage({
  searchParams,
}: {
  searchParams?: { template_type?: string; enabled?: string; q?: string };
}) {
  const templates = await getTemplates({
    template_type: searchParams?.template_type,
    enabled:
      searchParams?.enabled === "true"
        ? true
        : searchParams?.enabled === "false"
          ? false
          : undefined,
    q: searchParams?.q,
  });

  return (
    <>
      <TemplateCreateForm />
      <FilterForm
        title="Filter Templates"
        fields={[
          { name: "q", label: "Keyword", type: "text", defaultValue: searchParams?.q },
          {
            name: "template_type",
            label: "Type",
            type: "select",
            defaultValue: searchParams?.template_type ?? "",
            options: [
              { label: "All", value: "" },
              { label: "reply", value: "reply" },
              { label: "delivery", value: "delivery" },
              { label: "faq", value: "faq" },
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
        title="Templates"
        rows={templates}
        emptyText="当前没有模板数据。"
        columns={[
          {
            key: "id",
            title: "ID",
            render: (row) => (
              <code style={{ fontSize: 12, whiteSpace: "nowrap" }}>
                {row.id}
              </code>
            ),
          },
          { key: "name", title: "Name", render: (row) => row.name },
          { key: "template_type", title: "Type", render: (row) => row.template_type },
          { key: "category", title: "Category", render: (row) => row.category ?? "-" },
          { key: "description", title: "Description", render: (row) => row.description ?? "-" },
          { key: "version", title: "Version", render: (row) => row.version },
          { key: "enabled", title: "Enabled", render: (row) => String(row.enabled) },
          { key: "actions", title: "Actions", render: (row) => <TemplateActions template={row} /> },
        ]}
      />
    </>
  );
}
