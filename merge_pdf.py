from collections.abc import Sequence

from PyPDF2 import PdfReader, PdfWriter


def merge_pdfs(pdf_paths: Sequence[str], merged_pdf: str) -> None:
    """Merge an arbitrary list of PDFs into a single file."""
    writer = PdfWriter()
    for path in pdf_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(merged_pdf, "wb") as out_file:
        writer.write(out_file)


def merge_two_pdfs(pdf_a: str, pdf_b: str, merged_pdf: str) -> None:
    """Backward-compatible helper that delegates to merge_pdfs."""
    merge_pdfs((pdf_a, pdf_b), merged_pdf)

if __name__ == "__main__":
    merge_two_pdfs(
        r"C:\projects\dmztools\example-a.pdf",
        r"C:\projects\dmztools\example-b.pdf",
        r"C:\projects\dmztools\merged-output.pdf",
    )
