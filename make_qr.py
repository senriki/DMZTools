import qrcode

def create_qr(url: str, output_path: str) -> None:
    img = qrcode.make(url)
    img.save(output_path)

if __name__ == "__main__":
    create_qr(
        "https://example.com/shareable-link",
        r"C:\projects\dmztools\my_link_qr.png",
    )
