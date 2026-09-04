export default function Topbar({ title }) {
  return (
    <header className="bg-white border-b border-[var(--color-taupe-border)] px-8 py-4 flex items-center justify-between">
      <h2 className="text-lg font-semibold text-[var(--color-charcoal-txt)]">
        {title}
      </h2>
      <div className="flex items-center gap-4">
        {/* Placeholder for global actions if any */}
        <button className="text-[var(--color-taupe-txt)] hover:text-[var(--color-charcoal-txt)] transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
        </button>
      </div>
    </header>
  );
}
