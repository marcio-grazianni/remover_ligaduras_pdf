import fitz  # PyMuPDF
import os
from ebooklib import epub

def remove_ligatures_in_folder(folder_path):
    ligatures = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        # Adicione mais ligaduras conforme necessário
    }

    def replace_ligatures(text):
        for ligature, replacement in ligatures.items():
            text = text.replace(ligature, replacement)
        return text

    # Iterar sobre todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, filename.replace(".pdf", ".epub"))
            doc = fitz.open(pdf_path)

            full_text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if block["type"] == 0:  # Texto
                        for line in block["lines"]:
                            line_text = ""
                            for span in line["spans"]:
                                new_text = replace_ligatures(span["text"])
                                line_text += new_text + " "
                            line_text = line_text.rstrip()
                            full_text += line_text + "<br/>"
                        full_text += "<br/>"

            # Criar o ePub
            book = epub.EpubBook()
            book.set_identifier(filename)
            book.set_title(filename.replace(".pdf", ""))
            book.set_language('en')

            # Criar o capítulo e adicionar ao livro
            chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_01.xhtml', lang='en')
            chapter.content = f'<html><body><p>{full_text}</p></body></html>'
            book.add_item(chapter)

            # Definir a TOC
            book.toc = (epub.Link('chap_01.xhtml', 'Chapter 1', 'chapter1'),)

            # Adicionar CSS
            style = 'BODY { font-family: Arial, sans-serif; }'
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
            book.add_item(nav_css)

            # Definir as folhas de estilo
            book.spine = ['nav', chapter]

            # Escrever o arquivo
            epub.write_epub(output_path, book, {})

            print(f"Ligaduras removidas e salvo: {output_path}")

# Exemplo de uso
current_folder = os.getcwd()  # Pasta atual
remove_ligatures_in_folder(current_folder)
