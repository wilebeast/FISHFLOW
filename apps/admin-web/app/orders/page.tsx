import { getOrders } from "../../lib/api";
import { OrderActions } from "../../components/order-actions";
import { SimpleTable } from "../../components/table";

export default async function OrdersPage() {
  const orders = await getOrders();

  return (
    <SimpleTable
      title="Orders"
      rows={orders}
      emptyText="当前没有订单数据，先通过 API 创建订单或导入种子数据。"
      columns={[
        { key: "external_order_id", title: "External ID", render: (row) => row.external_order_id },
        { key: "buyer_id", title: "Buyer", render: (row) => row.buyer_id ?? "-" },
        { key: "amount", title: "Amount", render: (row) => `${row.amount} ${row.currency}` },
        { key: "order_status", title: "Order", render: (row) => row.order_status },
        { key: "pay_status", title: "Pay", render: (row) => row.pay_status },
        { key: "delivery_status", title: "Delivery", render: (row) => row.delivery_status },
        { key: "created_at", title: "Created", render: (row) => new Date(row.created_at).toLocaleString() },
        { key: "actions", title: "Actions", render: (row) => <OrderActions order={row} /> },
      ]}
    />
  );
}
