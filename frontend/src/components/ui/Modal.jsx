import { X } from "lucide-react";

export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="bg-[var(--color-off-white)] w-full max-w-lg rounded-md shadow-xl border border-[var(--color-taupe-border)] overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--color-taupe-border)]">
          <h3 className="text-lg font-semibold text-[var(--color-charcoal-txt)]">{title}</h3>
          <button 
            onClick={onClose} 
            className="text-[var(--color-taupe-txt)] hover:text-[var(--color-charcoal-txt)]"
          >
            <X size={20} />
          </button>
        </div>
        <div className="p-6 max-h-[80vh] overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
}
