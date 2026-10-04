import json
from pathlib import Path

from app.knowledge.knowledge_record import KnowledgeRecord


class KnowledgeStore:
    def __init__(self, path: str | Path = "data/knowledge.jsonl"):
        self.path = Path(path)

    def save(self, record: KnowledgeRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    record.model_dump(),
                    ensure_ascii=False,
                )
                + "\n"
            )

    def save_many(self, records: list[KnowledgeRecord]) -> None:
        for record in records:
            self.save(record)

    def load_all(self) -> list[KnowledgeRecord]:
        if not self.path.exists():
            return []

        records = []

        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                data = json.loads(line)
                records.append(KnowledgeRecord.model_validate(data))

        return records

    def count(self) -> int:
        return len(self.load_all())