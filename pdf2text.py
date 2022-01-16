def pdf2text(pdf_file):
    from PyPDF2 import PdfFileReader
    from tqdm import tqdm

    reader = PdfFileReader(pdf_file)
    for page in tqdm(reader.pages, ascii=True, desc="Converting PDF to text"):
        yield page.extractText()

if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 3, "Usage: python pdf2text.py <input-file> <output-file>"
    _, input_file, output_file = argv
    with open(output_file, 'w') as output_fp:
        for text in pdf2text(input_file):
            output_fp.write(text)
