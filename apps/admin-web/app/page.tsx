import Link from "next/link";

const pages = [
  { href: "/orders", label: "Orders", desc: "查看订单状态、支付状态与发货状态。" },
  { href: "/messages", label: "Messages", desc: "查看买家消息、系统入库与自动回复结果。" },
  { href: "/deliveries", label: "Deliveries", desc: "查看自动发货任务、重试次数与执行结果。" },
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
