import { FilterForm } from "../../components/filter-form";
import { RuleActions } from "../../components/rule-actions";
import { RuleCreateForm } from "../../components/rule-create-form";
import { SimpleTable } from "../../components/table";
import { getRules } from "../../lib/api";

export default async function RulesPage({
  searchParams,
}: {
  searchParams?: { scope?: string; trigger_type?: string; enabled?: string };
}) {
  const rules = await getRules({
    scope: searchParams?.scope,
    trigger_type: searchParams?.trigger_type,
    enabled:
      searchParams?.enabled === "true"
        ? true
        : searchParams?.enabled === "false"
          ? false
          : undefined,
  });

  return (
    <>
      <RuleCreateForm />
      <FilterForm
        title="Filter Rules"
        fields={[
          {
            name: "scope",
            label: "Scope",
            type: "select",
            defaultValue: searchParams?.scope ?? "",
            options: [
              { label: "All", value: "" },
              { label: "global", value: "global" },
              { label: "account", value: "account" },
              { label: "product", value: "product" },
            ],
          },
          {
            name: "trigger_type",
            label: "Trigger",
            type: "select",
            defaultValue: searchParams?.trigger_type ?? "",
            options: [
              { label: "All", value: "" },
              { label: "message_received", value: "message_received" },
              { label: "order_paid", value: "order_paid" },
              { label: "delivery_failed", value: "delivery_failed" },
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
        title="Rules"
        rows={rules}
        emptyText="当前没有规则数据。"
        columns={[
          { key: "name", title: "Name", render: (row) => row.name },
          { key: "scope", title: "Scope", render: (row) => row.scope },
          { key: "trigger_type", title: "Trigger", render: (row) => row.trigger_type },
          { key: "priority", title: "Priority", render: (row) => row.priority },
          { key: "action_type", title: "Action", render: (row) => row.action_type },
          { key: "enabled", title: "Enabled", render: (row) => String(row.enabled) },
          { key: "actions", title: "Actions", render: (row) => <RuleActions rule={row} /> },
        ]}
      />
    </>
  );
}
