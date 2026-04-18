import Link from "next/link";

const pages = [
  { href: "/accounts", label: "Accounts", desc: "管理多账号接入、健康检查、风险等级与禁用状态。" },
  { href: "/inventory", label: "Inventory", desc: "管理卡密池、资源库存、订单分配与禁用。" },
  { href: "/products", label: "Products", desc: "管理商品、自动发货开关、规则与模板绑定。" },
  { href: "/conversations", label: "Conversations", desc: "查看会话时间线、人工接管、手动发送消息。" },
  { href: "/orders", label: "Orders", desc: "查看订单状态、支付状态与发货状态。" },
  { href: "/messages", label: "Messages", desc: "查看买家消息、系统入库与自动回复结果。" },
  { href: "/deliveries", label: "Deliveries", desc: "查看自动发货任务、重试次数与执行结果。" },
  { href: "/templates", label: "Templates", desc: "维护回复、发货、FAQ 模板。" },
  { href: "/rules", label: "Rules", desc: "维护全局规则与自动化动作。" },
  { href: "/notifications", label: "Notifications", desc: "配置飞书、Webhook 等通知通道并执行测试。" },
  { href: "/audit", label: "Audit", desc: "查看后台操作日志与系统事件。" },
  { href: "/ai/reply", label: "AI Reply", desc: "维护 AI 回复配置并查看调用日志。" },
  { href: "/ai/copy", label: "AI Copy", desc: "生成商品标题、描述、FAQ 和客服改写文案。" },
  { href: "/knowledge", label: "Knowledge", desc: "维护商品 FAQ、售前售后知识和启停状态。" },
  { href: "/analytics", label: "Analytics", desc: "查看消息、接管、发货成功率等概览数据。" },
  { href: "/settings", label: "Settings", desc: "维护全局配置、导入导出应用设置。" },
  { href: "/system", label: "System", desc: "查看 API、数据库、Redis、Worker 的健康状态。" },
];

export default function HomePage() {
  return (
    <section>
      <h1 style={{ marginBottom: 12 }}>FishFlow Admin</h1>
      <p style={{ maxWidth: 720, lineHeight: 1.6 }}>
        当前后台已经覆盖 V1.0 的核心管理面：账号、库存、商品、会话、模板、规则、通知、审计、AI 回复、AI 文案、知识库、报表和设置。
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
