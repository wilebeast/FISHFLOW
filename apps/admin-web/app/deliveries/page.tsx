import { FilterForm } from "../../components/filter-form";
import { getDeliveries } from "../../lib/api";
import { DeliveryActions } from "../../components/delivery-actions";
import { SimpleTable } from "../../components/table";

export default async function DeliveriesPage({
  searchParams,
}: {
  searchParams?: { limit?: string };
}) {
  const deliveries = await getDeliveries({ limit: searchParams?.limit ? Number(searchParams.limit) : undefined });

  return (
    <>
      <FilterForm
        title="Filter Deliveries"
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
        title="Deliveries"
        rows={deliveries}
        emptyText="当前没有发货任务，先触发订单支付事件。"
        columns={[
          { key: "order_id", title: "Order ID", render: (row) => row.order_id },
          { key: "delivery_type", title: "Type", render: (row) => row.delivery_type },
          { key: "status", title: "Status", render: (row) => row.status },
          { key: "attempt_count", title: "Attempts", render: (row) => `${row.attempt_count}/${row.max_attempts}` },
          { key: "result_message", title: "Result", render: (row) => row.result_message ?? row.last_error ?? "-" },
          { key: "created_at", title: "Created", render: (row) => new Date(row.created_at).toLocaleString() },
          { key: "actions", title: "Actions", render: (row) => <DeliveryActions task={row} /> },
        ]}
      />
    </>
  );
}
