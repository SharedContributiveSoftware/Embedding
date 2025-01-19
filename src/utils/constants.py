import json
from pathlib import Path
from typing import Final

BASE_URL: Final[str] = "https://store.steampowered.com/appreviews/50"
SAMPLES_PATH: Final[Path] = Path("./samples")
EMBEDDING_SAMPLE_PATH = SAMPLES_PATH / "mock_embedding.json"
with open(EMBEDDING_SAMPLE_PATH, "r") as fd:
    EMBEDDING_SAMPLE_DATA = json.load(fd)