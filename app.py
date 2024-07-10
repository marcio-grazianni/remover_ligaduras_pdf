import fitz  # PyMuPDF
import os

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

    # Iterar sobre todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, filename.replace(".pdf", "_.pdf"))
            doc = fitz.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                
                for ligature, replacement in ligatures.items():
                    text = text.replace(ligature, replacement)
                
                page.clean_contents()
                for ligature, replacement in ligatures.items():
                    text_instances = page.search_for(ligature)
                    for inst in text_instances:
                        page.insert_text(inst[:0], replacement, fontsize=12, color=(0, 0, 0))

            doc.save(output_path)
            print(f"Ligaduras removidas e salvo: {output_path}")

# Exemplo de uso
current_folder = os.getcwd()  # Pasta atual
remove_ligatures_in_folder(current_folder)
