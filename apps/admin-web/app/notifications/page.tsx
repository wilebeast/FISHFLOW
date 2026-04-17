import { NotificationConfigForm } from "../../components/notification-config-form";
import { SimpleTable } from "../../components/table";
import { getNotificationConfigs } from "../../lib/api";

export default async function NotificationsPage() {
  const configs = await getNotificationConfigs();

  return (
    <>
      <NotificationConfigForm configs={configs} />
      <SimpleTable
        title="Notification Configs"
        rows={configs}
        emptyText="当前没有通知配置。"
        columns={[
          { key: "id", title: "ID", render: (row) => <code style={{ fontSize: 12 }}>{row.id}</code> },
          { key: "channel", title: "Channel", render: (row) => row.channel },
          { key: "name", title: "Name", render: (row) => row.name },
          { key: "target", title: "Target", render: (row) => row.target ?? "-" },
          { key: "enabled", title: "Enabled", render: (row) => String(row.enabled) },
        ]}
      />
    </>
  );
}
