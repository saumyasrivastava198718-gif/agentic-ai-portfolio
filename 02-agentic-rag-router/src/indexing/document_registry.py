import hashlib
import json
from pathlib import Path


class DocumentRegistry:
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent.parent
        self.registry_path = (
            project_root / "data" / "index_registry.json"
        )

    def compute_hash(self, file_path: str) -> str:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            while True:
                block = file.read(8192)

                if not block:
                    break

                sha256.update(block)

        return sha256.hexdigest()

    def _load_registry(self):
        if not self.registry_path.exists():
            return {}

        with open(
            self.registry_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def _save_registry(self, registry):
        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.registry_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                registry,
                file,
                indent=4
            )

    def is_indexed(self, file_hash: str) -> bool:
        registry = self._load_registry()
        return file_hash in registry

    def register(
        self,
        file_hash: str,
        filename: str
    ):
        registry = self._load_registry()

        registry[file_hash] = {
            "filename": filename,
            "status": "indexed"
        }

        self._save_registry(registry)