import chromadb
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="campus_policy_chunks"
)


def get_policy_source(metric: str) -> str:
    """
    Map each sustainability metric to its
    corresponding campus policy document.
    """

    metric = metric.lower().strip()

    policy_map = {
        "energy": "energy_policy.txt",
        "water": "water_policy.txt",
        "waste": "waste_policy.txt",
    }

    return policy_map.get(
        metric,
        f"{metric}_policy.txt"
    )


def retrieve_policy(
    metric: str,
    query: str,
    n_results: int = 2
) -> dict:
    """
    Retrieve policy guidance relevant to the
    requested sustainability metric.

    Retrieval is restricted to the matching
    policy document so that an energy anomaly
    cannot accidentally retrieve water policy,
    and vice versa.
    """

    policy_source = get_policy_source(metric)

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={
            "source": policy_source
        }
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    retrieved_documents = []

    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        retrieved_documents.append({
            "source": metadata.get(
                "source",
                policy_source
            ),
            "chunk": metadata.get(
                "chunk",
                0
            ),
            "document": document,
            "distance": distance
        })

    # Chroma distance is NOT a calibrated probability.
    # We use it only as a simple retrieval-strength
    # heuristic for the hackathon confidence pipeline.
    if distances:

        best_distance = distances[0]

        retrieval_confidence = round(
            max(
                0.0,
                min(
                    1.0,
                    1.0 - best_distance
                )
            ),
            2
        )

    else:
        retrieval_confidence = 0.0

    return {
        "metric": metric,
        "query": query,
        "policy_source": policy_source,
        "results": retrieved_documents,
        "retrieval_confidence": retrieval_confidence,
        "grounded": len(retrieved_documents) > 0
    }


if __name__ == "__main__":

    result = retrieve_policy(
        metric="water",
        query=(
            "Water consumption anomaly at Hostel C. "
            "Campus event may explain the increase. "
            "Check water usage validation, sensor "
            "verification, investigation and safe "
            "operational guidance."
        )
    )

    print(
        "\n========== RAG RETRIEVAL TEST ==========\n"
    )

    print(
        "Policy Source:",
        result["policy_source"]
    )

    print(
        "Retrieval Confidence:",
        result["retrieval_confidence"]
    )

    print(
        "Grounded:",
        result["grounded"]
    )

    for item in result["results"]:

        print("\nSource:")
        print(item["source"])

        print("\nChunk:")
        print(item["chunk"])

        print("\nRetrieved Policy:")
        print(item["document"])

        print("\nDistance:")
        print(item["distance"])

    print(
        "\n=========================================\n"
    )