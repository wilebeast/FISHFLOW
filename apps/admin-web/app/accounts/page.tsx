import { AccountActions } from "../../components/account-actions";
import { AccountCreateForm } from "../../components/account-create-form";
import { FilterForm } from "../../components/filter-form";
import { SimpleTable } from "../../components/table";
import { getAccounts } from "../../lib/api";

export default async function AccountsPage({
  searchParams,
}: {
  searchParams?: { q?: string; login_status?: string; health_status?: string };
}) {
  const accounts = await getAccounts(searchParams);

  return (
    <>
      <AccountCreateForm />
      <FilterForm
        title="Filter Accounts"
        fields={[
          { name: "q", label: "Keyword", type: "text", defaultValue: searchParams?.q },
          {
            name: "login_status",
            label: "Login Status",
            type: "select",
            defaultValue: searchParams?.login_status ?? "",
            options: [
              { label: "All", value: "" },
              { label: "active", value: "active" },
              { label: "expired", value: "expired" },
              { label: "risk", value: "risk" },
              { label: "disabled", value: "disabled" },
            ],
          },
          {
            name: "health_status",
            label: "Health",
            type: "select",
            defaultValue: searchParams?.health_status ?? "",
            options: [
              { label: "All", value: "" },
              { label: "healthy", value: "healthy" },
              { label: "warning", value: "warning" },
              { label: "error", value: "error" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="Accounts"
        rows={accounts}
        emptyText="当前没有账号数据。"
        columns={[
          { key: "id", title: "ID", render: (row) => <code style={{ fontSize: 12 }}>{row.id}</code> },
          { key: "nickname", title: "Nickname", render: (row) => row.nickname },
          { key: "external_account_id", title: "External ID", render: (row) => row.external_account_id },
          { key: "login_status", title: "Login", render: (row) => row.login_status },
          { key: "health_status", title: "Health", render: (row) => row.health_status },
          { key: "risk_level", title: "Risk", render: (row) => row.risk_level },
          { key: "disabled_reason", title: "Disabled Reason", render: (row) => row.disabled_reason ?? "-" },
          { key: "actions", title: "Actions", render: (row) => <AccountActions account={row} /> },
        ]}
      />
    </>
  );
}
