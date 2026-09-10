from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


collection = client.get_or_create_collection(
    name="campus_policy_chunks"
)


def chunk_text(
    text: str,
    chunk_size: int = 80
) -> list[str]:

    words = text.split()

    chunks = []

    for start in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[start:start + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


all_documents = []
all_metadatas = []
all_ids = []


for file_path in DOCUMENTS_DIR.glob("*.txt"):

    text = file_path.read_text(
        encoding="utf-8"
    )

    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

        all_documents.append(chunk)

        all_metadatas.append({
            "source": file_path.name,
            "chunk": index
        })

        all_ids.append(
            f"{file_path.stem}_chunk_{index}"
        )


if all_documents:

    collection.upsert(
        documents=all_documents,
        metadatas=all_metadatas,
        ids=all_ids
    )

    print(
        f"Successfully indexed "
        f"{len(all_documents)} policy chunks."
    )

else:

    print("No policy documents found.")