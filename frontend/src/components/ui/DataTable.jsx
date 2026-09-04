export default function DataTable({ columns, data, isLoading, emptyMessage = "No data available." }) {
  if (isLoading) {
    return (
      <div className="w-full h-32 flex items-center justify-center text-[var(--color-taupe-txt)]">
        Loading data...
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full p-8 text-center border border-dashed border-[var(--color-taupe-border)] rounded-md text-[var(--color-taupe-txt)]">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="overflow-x-auto border border-[var(--color-taupe-border)] rounded-md">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col, index) => (
              <th key={index} className={col.align === "right" ? "text-right" : "text-left"}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={row.id || rowIndex}>
              {columns.map((col, colIndex) => (
                <td key={colIndex} className={col.align === "right" ? "text-right" : "text-left"}>
                  {col.render ? col.render(row) : row[col.accessor]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
