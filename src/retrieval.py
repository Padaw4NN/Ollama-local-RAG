import os
import uuid
import pandas as pd
from typing import Dict


ROOT_DIR = os.path.dirname(os.path.abspath(__name__))


def get_data() -> Dict[str, list]:
    """A simple retrieval funcion to load a CSV file.

    returns:
        A dictionary containing the indices, texts and metadata.
    """
    file_dir = os.path.join(ROOT_DIR, "data")
    file_pth = os.path.join(file_dir, os.listdir(file_dir)[0])

    if not os.path.exists(file_pth):
        raise FileNotFoundError(f"{file_pth}")

    df = pd.read_csv(file_pth)
    
    ids, docs, metadata = [], [], []
    for _, row in df.iterrows():
        ids.append(str(uuid.uuid4()))
        docs.append(row["Title"] + " " + row["Review"])
        metadata.append({
            "date": row["Date"],
            "rating": row["Rating"]
        })

    return {
        "ids": ids,
        "documents": docs,
        "metadata": metadata
    }
