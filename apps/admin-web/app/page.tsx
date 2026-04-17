import Link from "next/link";

const pages = [
  { href: "/products", label: "Products", desc: "管理商品、自动发货开关、规则与模板绑定。" },
  { href: "/conversations", label: "Conversations", desc: "查看会话时间线、人工接管、手动发送消息。" },
  { href: "/orders", label: "Orders", desc: "查看订单状态、支付状态与发货状态。" },
  { href: "/messages", label: "Messages", desc: "查看买家消息、系统入库与自动回复结果。" },
  { href: "/deliveries", label: "Deliveries", desc: "查看自动发货任务、重试次数与执行结果。" },
  { href: "/templates", label: "Templates", desc: "维护回复、发货、FAQ 模板。" },
  { href: "/rules", label: "Rules", desc: "维护全局规则与自动化动作。" },
  { href: "/system", label: "System", desc: "查看 API、数据库、Redis、Worker 的健康状态。" },
];

export default function HomePage() {
  return (
    <section>
      <h1 style={{ marginBottom: 12 }}>FishFlow Admin</h1>
      <p style={{ maxWidth: 720, lineHeight: 1.6 }}>
        当前后台已接上订单、消息和发货任务的读取接口。下面三个页面已经可以直接用于演示数据流。
      </p>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: 16,
          marginTop: 24,
        }}
      >
        {pages.map((page) => (
          <Link
            key={page.href}
            href={page.href}
            style={{
              display: "block",
              textDecoration: "none",
              color: "#2e2217",
              border: "1px solid #ccb89f",
              background: "#fffdf8",
              padding: 20,
            }}
          >
            <strong>{page.label}</strong>
            <p style={{ marginBottom: 0, lineHeight: 1.6 }}>{page.desc}</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
