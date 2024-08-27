from pathlib import Path

import fitz
from tqdm import tqdm


def merge_pages(src_path: Path, tgt_path: Path) -> None:

    pdf = fitz.open(src_path)
    pages_num = pdf.page_count
    merged_pdf = fitz.open()

    for i in range(0, pages_num, 4):
        # 创建一个新的页面，宽度、高度为两个页面的宽度、高度
        new_page = merged_pdf.new_page(
            width=pdf[0].rect.width * 2,
            height=pdf[0].rect.height * 2,
        )

        for j in range(4):
            # 如果页数超过总页数，退出循环
            if i + j >= pages_num:
                break
            page = pdf[i + j]

            # 计算当前页面在新页面中的偏移量
            x_offset = (j % 2) * pdf[0].rect.width
            y_offset = (j // 2) * pdf[0].rect.height

            # 将当前页面显示到新页面的指定位置
            new_page.show_pdf_page(
                fitz.Rect(
                    x_offset,
                    y_offset,
                    x_offset + page.rect.width,
                    y_offset + page.rect.height,
                ),
                pdf,
                i + j,
            )

    merged_pdf.save(tgt_path)
    merged_pdf.close()


def merge_pdfs(src_dir: Path, output_file: Path) -> None:

    merged_pdf = fitz.open()

    for pdf_file in tqdm(src_dir.glob("*.pdf"), desc="Merging PDFs"):
        pdf = fitz.open(pdf_file)
        merged_pdf.insert_pdf(pdf)

    merged_pdf.save(output_file)
    merged_pdf.close()


def main() -> None:
    source_dir = Path("docs")  # 源文件目录
    target_dir = Path("merge")  # 目标文件目录
    target_dir.mkdir(exist_ok=True)

    # 遍历源目录中的每个 PDF 文件，并将其页面合并
    for pdf_file in tqdm(source_dir.glob("*.pdf"), desc="Merging pages"):
        dest_file = target_dir / pdf_file.name
        merge_pages(pdf_file, dest_file)

    # 将目标目录中的所有 PDF 文件合并成一个 PDF 文件
    merge_pdfs(target_dir, target_dir / "merge.pdf")


if __name__ == "__main__":
    main()
