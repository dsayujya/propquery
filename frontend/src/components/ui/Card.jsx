export default function Card({ children, title, subtitle, className = "" }) {
  return (
    <div className={`card ${className}`}>
      {(title || subtitle) && (
        <div className="px-6 py-4 border-b border-[var(--color-taupe-border)]">
          {title && <h3 className="text-lg font-semibold text-[var(--color-charcoal-txt)]">{title}</h3>}
          {subtitle && <p className="text-sm text-[var(--color-taupe-txt)] mt-1">{subtitle}</p>}
        </div>
      )}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
