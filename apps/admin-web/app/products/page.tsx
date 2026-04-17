import { FilterForm } from "../../components/filter-form";
import { ProductActions } from "../../components/product-actions";
import { ProductCreateForm } from "../../components/product-create-form";
import { SimpleTable } from "../../components/table";
import { getProducts } from "../../lib/api";

export default async function ProductsPage({
  searchParams,
}: {
  searchParams?: { q?: string; status?: string; delivery_mode?: string };
}) {
  const products = await getProducts(searchParams);

  return (
    <>
      <ProductCreateForm />
      <FilterForm
        title="Filter Products"
        fields={[
          { name: "q", label: "Keyword", type: "text", placeholder: "title", defaultValue: searchParams?.q },
          {
            name: "status",
            label: "Status",
            type: "select",
            defaultValue: searchParams?.status ?? "",
            options: [
              { label: "All", value: "" },
              { label: "active", value: "active" },
              { label: "inactive", value: "inactive" },
            ],
          },
          {
            name: "delivery_mode",
            label: "Delivery Mode",
            type: "select",
            defaultValue: searchParams?.delivery_mode ?? "",
            options: [
              { label: "All", value: "" },
              { label: "auto", value: "auto" },
              { label: "manual", value: "manual" },
            ],
          },
        ]}
      />
      <SimpleTable
        title="Products"
        rows={products}
        emptyText="当前没有商品数据。"
        columns={[
          { key: "external_product_id", title: "External ID", render: (row) => row.external_product_id },
          { key: "title", title: "Title", render: (row) => row.title },
          { key: "category", title: "Category", render: (row) => row.category ?? "-" },
          { key: "price", title: "Price", render: (row) => row.price },
          { key: "delivery_mode", title: "Mode", render: (row) => row.delivery_mode },
          { key: "auto_delivery_enabled", title: "Auto", render: (row) => String(row.auto_delivery_enabled) },
          { key: "status", title: "Status", render: (row) => row.status },
          { key: "actions", title: "Actions", render: (row) => <ProductActions product={row} /> },
        ]}
      />
    </>
  );
}
