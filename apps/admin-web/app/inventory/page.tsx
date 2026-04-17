import { FilterForm } from "../../components/filter-form";
import { InventoryActions } from "../../components/inventory-actions";
import { InventoryCreateForm } from "../../components/inventory-create-form";
import { SimpleTable } from "../../components/table";
import { getInventory } from "../../lib/api";

export default async function InventoryPage({
  searchParams,
}: {
  searchParams?: { resource_type?: string; status?: string; product_id?: string };
}) {
  const items = await getInventory(searchParams);

  return (
    <>
      <InventoryCreateForm />
      <FilterForm
        title="Filter Inventory"
        fields={[
          {
            name: "resource_type",
            label: "Type",
            type: "select",
            defaultValue: searchParams?.resource_type ?? "",
            options: [
              { label: "All", value: "" },
              { label: "card", value: "card" },
              { label: "link", value: "link" },
              { label: "text", value: "text" },
            ],
          },
          {
            name: "status",
            label: "Status",
            type: "select",
            defaultValue: searchParams?.status ?? "",
            options: [
              { label: "All", value: "" },
              { label: "available", value: "available" },
              { label: "allocated", value: "allocated" },
              { label: "disabled", value: "disabled" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="Inventory"
        rows={items}
        emptyText="当前没有库存数据。"
        columns={[
          { key: "id", title: "ID", render: (row) => <code style={{ fontSize: 12 }}>{row.id}</code> },
          { key: "resource_type", title: "Type", render: (row) => row.resource_type },
          { key: "code", title: "Code", render: (row) => row.code ?? "-" },
          { key: "status", title: "Status", render: (row) => row.status },
          { key: "allocated_order_id", title: "Allocated Order", render: (row) => row.allocated_order_id ?? "-" },
          { key: "note", title: "Note", render: (row) => row.note ?? "-" },
          { key: "actions", title: "Actions", render: (row) => <InventoryActions item={row} /> },
        ]}
      />
    </>
  );
}
