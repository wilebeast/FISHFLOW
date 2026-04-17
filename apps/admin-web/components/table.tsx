import type { ReactNode } from "react";

type Column<T> = {
  key: string;
  title: string;
  render: (row: T) => ReactNode;
};

export function SimpleTable<T>({
  title,
  rows,
  columns,
  emptyText,
}: {
  title: string;
  rows: T[];
  columns: Column<T>[];
  emptyText: string;
}) {
  return (
    <section style={{ marginBottom: 28 }}>
      <h2 style={{ marginBottom: 12 }}>{title}</h2>
      <div style={{ overflowX: "auto", border: "1px solid #d8c9b2", background: "#fffdf8" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 900 }}>
          <thead>
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  style={{
                    textAlign: "left",
                    padding: 12,
                    borderBottom: "1px solid #d8c9b2",
                    background: "#f3e8d8",
                  }}
                >
                  {column.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan={columns.length} style={{ padding: 16, color: "#735f48" }}>
                  {emptyText}
                </td>
              </tr>
            ) : (
              rows.map((row, index) => (
                <tr key={index}>
                  {columns.map((column) => (
                    <td key={column.key} style={{ padding: 12, borderBottom: "1px solid #eee2d0" }}>
                      {column.render(row)}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
