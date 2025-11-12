"""Simple tkinter GUI that wraps PDF merging and QR generation helpers."""

from datetime import datetime
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from merge_pdf import merge_pdfs
from make_qr import create_qr


def resource_path(asset: str) -> Path:
    """Resolve asset path for both source runs and PyInstaller bundles."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base / asset


class UtilityApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("DMZTools")
        self.resizable(False, False)
        icon_path = resource_path("logo.ico")
        if icon_path.is_file():
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        description = ttk.Label(
            self,
            text="DMZTools merges two PDFs and builds shareable QR codes entirely on your PC.",
            wraplength=360,
            justify="center",
        )
        description.pack(padx=10, pady=(10, 0))

        notebook = ttk.Notebook(self, padding=10)
        notebook.pack(fill="both", expand=True)

        merge_frame = ttk.Frame(notebook, padding=10)
        qr_frame = ttk.Frame(notebook, padding=10)
        notebook.add(merge_frame, text="Merge PDFs")
        notebook.add(qr_frame, text="Create QR")

        self._build_merge_tab(merge_frame)
        self._build_qr_tab(qr_frame)

    def _build_merge_tab(self, container: ttk.Frame) -> None:
        self.pdf_paths: list[str] = []
        self.pdf_out_name_var = tk.StringVar()

        ttk.Label(container, text="PDF files (ordered as they will appear):").grid(row=0, column=0, columnspan=3, sticky="w")

        list_frame = ttk.Frame(container)
        list_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")
        self.pdf_listbox = tk.Listbox(list_frame, height=6, width=60, selectmode=tk.EXTENDED)
        self.pdf_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.pdf_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.pdf_listbox.configure(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(container)
        button_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Add PDFs", command=self._add_pdfs).grid(row=0, column=0, padx=2)
        ttk.Button(button_frame, text="Remove Selected", command=self._remove_selected_pdfs).grid(row=0, column=1, padx=2)
        ttk.Button(button_frame, text="Clear List", command=self._clear_pdf_list).grid(row=0, column=2, padx=2)

        ttk.Label(container, text="Output name (optional)").grid(row=3, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.pdf_out_name_var, width=50).grid(
            row=3,
            column=1,
            padx=(5, 5),
            pady=2,
            sticky="ew",
        )
        ttk.Label(container, text="Defaults to merged-<timestamp>.pdf in the first PDF's folder.").grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="w",
        )

        merge_btn = ttk.Button(container, text="Merge PDFs", command=self._handle_merge)
        merge_btn.grid(row=5, column=0, columnspan=3, pady=(10, 0), sticky="ew")

    def _build_qr_tab(self, container: ttk.Frame) -> None:
        self.url_var = tk.StringVar()
        self.qr_out_name_var = tk.StringVar()

        ttk.Label(container, text="URL").grid(row=0, column=0, sticky="w")
        url_entry = ttk.Entry(container, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, columnspan=2, pady=2, sticky="ew")

        ttk.Label(container, text="Output name (optional)").grid(row=1, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.qr_out_name_var, width=50).grid(
            row=1,
            column=1,
            columnspan=2,
            padx=(5, 5),
            pady=2,
            sticky="ew",
        )

        ttk.Label(container, text="Defaults to qr-<timestamp>.png in this folder.").grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w",
        )

        qr_btn = ttk.Button(container, text="Generate QR", command=self._handle_qr)
        qr_btn.grid(row=3, column=0, columnspan=3, pady=(10, 0), sticky="ew")

    def _add_pdfs(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if not paths:
            return
        for path in paths:
            if path and path not in self.pdf_paths:
                self.pdf_paths.append(path)
        self._refresh_pdf_listbox()

    def _remove_selected_pdfs(self) -> None:
        selected = self.pdf_listbox.curselection()
        if not selected:
            return
        for index in reversed(selected):
            del self.pdf_paths[index]
        self._refresh_pdf_listbox()

    def _clear_pdf_list(self) -> None:
        if not self.pdf_paths:
            return
        self.pdf_paths.clear()
        self._refresh_pdf_listbox()

    def _refresh_pdf_listbox(self) -> None:
        self.pdf_listbox.delete(0, tk.END)
        for idx, path in enumerate(self.pdf_paths, start=1):
            display = f"{idx}. {Path(path).name}"
            self.pdf_listbox.insert(tk.END, display)

    def _handle_merge(self) -> None:
        if len(self.pdf_paths) < 2:
            messagebox.showerror("Need more PDFs", "Add at least two PDF files to merge.")
            return
        missing = [path for path in self.pdf_paths if not Path(path).is_file()]
        if missing:
            missing_display = "\n".join(missing[:5])
            if len(missing) > 5:
                missing_display += "\n..."
            messagebox.showerror("Missing file", f"These PDFs could not be found:\n{missing_display}")
            return
        output_name = self.pdf_out_name_var.get().strip()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_name = output_name if output_name else "merged"
        base_name = base_name.rstrip(".")
        if base_name.lower().endswith(".pdf"):
            base_name = base_name[:-4]
        if not base_name:
            base_name = "merged"
        full_name = f"{base_name}-{timestamp}.pdf"
        output_folder = Path(self.pdf_paths[0]).parent
        output = output_folder / full_name
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            merge_pdfs(self.pdf_paths, str(output))
            messagebox.showinfo("Success", f"Merged PDF saved to:\n{output}")
        except Exception as exc:
            messagebox.showerror("Merge failed", str(exc))

    def _handle_qr(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Missing URL", "Enter the URL to encode.")
            return
        name_input = self.qr_out_name_var.get().strip()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_name = name_input if name_input else "qr"
        base_name = base_name.rstrip(".")
        base_name = base_name[:-4] if base_name.lower().endswith(".png") else base_name
        full_name = f"{base_name}-{timestamp}.png"
        output = Path.cwd() / full_name
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            create_qr(url, str(output))
            messagebox.showinfo("Success", f"QR code saved to:\n{output}")
        except Exception as exc:
            messagebox.showerror("QR failed", str(exc))


if __name__ == "__main__":
    app = UtilityApp()
    app.mainloop()
