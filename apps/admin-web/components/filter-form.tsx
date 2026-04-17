type Field =
  | { name: string; label: string; type: "text"; placeholder?: string; defaultValue?: string }
  | { name: string; label: string; type: "select"; options: Array<{ label: string; value: string }>; defaultValue?: string };

export function FilterForm({
  title,
  fields,
}: {
  title: string;
  fields: Field[];
}) {
  return (
    <form method="get" style={{ marginBottom: 24, border: "1px solid #d8c9b2", background: "#fffdf8", padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>{title}</h2>
      <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", alignItems: "end" }}>
        {fields.map((field) => (
          <label key={field.name} style={{ display: "grid", gap: 6 }}>
            <span>{field.label}</span>
            {field.type === "text" ? (
              <input name={field.name} defaultValue={field.defaultValue} placeholder={field.placeholder} style={{ padding: 8 }} />
            ) : (
              <select name={field.name} defaultValue={field.defaultValue} style={{ padding: 8 }}>
                {field.options.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            )}
          </label>
        ))}
        <div style={{ display: "flex", gap: 8 }}>
          <button type="submit">Apply</button>
          <a href="." style={{ alignSelf: "center", color: "#2e2217" }}>
            Reset
          </a>
        </div>
      </div>
    </form>
  );
}
