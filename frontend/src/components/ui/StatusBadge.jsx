export default function StatusBadge({ status }) {
  let bgColor = "bg-gray-100";
  let textColor = "text-gray-700";
  let dotColor = "bg-gray-500";

  const normalizedStatus = status?.toLowerCase() || "";

  switch (normalizedStatus) {
    case "active":
    case "completed":
    case "resolved":
    case "occupied":
      bgColor = "bg-emerald-50";
      textColor = "text-emerald-700";
      dotColor = "bg-emerald-500";
      break;
    case "pending":
    case "open":
    case "investigating":
      bgColor = "bg-amber-50";
      textColor = "text-amber-700";
      dotColor = "bg-amber-500";
      break;
    case "failed":
    case "vacant":
    case "terminated":
      bgColor = "bg-rose-50";
      textColor = "text-rose-700";
      dotColor = "bg-rose-500";
      break;
    default:
      break;
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-1 text-xs font-medium rounded-full ${bgColor} ${textColor} border border-[rgba(0,0,0,0.05)]`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotColor}`}></span>
      {status ? status.charAt(0).toUpperCase() + status.slice(1) : "Unknown"}
    </span>
  );
}
