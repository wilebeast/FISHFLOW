import type { ReactNode } from "react";

import { Nav } from "../components/nav";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body style={{ margin: 0, fontFamily: "Georgia, serif", background: "#f5efe4" }}>
        <main style={{ padding: 32, maxWidth: 1280, margin: "0 auto" }}>
          <Nav />
          {children}
        </main>
      </body>
    </html>
  );
}
