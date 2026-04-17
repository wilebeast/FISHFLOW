import Link from "next/link";

const items = [
  { href: "/", label: "Overview" },
  { href: "/products", label: "Products" },
  { href: "/conversations", label: "Conversations" },
  { href: "/orders", label: "Orders" },
  { href: "/messages", label: "Messages" },
  { href: "/deliveries", label: "Deliveries" },
  { href: "/templates", label: "Templates" },
  { href: "/rules", label: "Rules" },
  { href: "/system", label: "System" },
];

export function Nav() {
  return (
    <nav style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
      {items.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          style={{
            textDecoration: "none",
            color: "#2e2217",
            padding: "8px 12px",
            border: "1px solid #ccb89f",
            background: "#fffaf2",
          }}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
