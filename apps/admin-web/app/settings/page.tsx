import { SettingsForm } from "../../components/settings-form";
import { SimpleTable } from "../../components/table";
import { getSettings } from "../../lib/api";

export default async function SettingsPage() {
  const settings = await getSettings();

  return (
    <>
      <SettingsForm settings={settings} />
      <SimpleTable
        title="App Settings"
        rows={settings}
        emptyText="当前没有设置项。"
        columns={[
          { key: "key", title: "Key", render: (row) => row.key },
          { key: "value_json", title: "Value", render: (row) => <code style={{ fontSize: 12 }}>{JSON.stringify(row.value_json)}</code> },
          { key: "updated_at", title: "Updated At", render: (row) => row.updated_at },
        ]}
      />
    </>
  );
}
