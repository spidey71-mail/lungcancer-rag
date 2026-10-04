from dataclasses import dataclass

from app.knowledge.schema import Publication


LUNG_CANCER_TERMS = {
    "lung cancer",
    "lung carcinoma",
    "lung neoplasm",
    "non-small cell lung cancer",
    "non-small-cell lung cancer",
    "nsclc",
    "small cell lung cancer",
    "small-cell lung cancer",
    "sclc",
    "lung adenocarcinoma",
    "lung squamous cell carcinoma",
    "lung squamous carcinoma",
    "lung cancer",
}


MOLECULAR_TERMS = {
    "gene",
    "genes",
    "mutation",
    "mutations",
    "variant",
    "variants",
    "biomarker",
    "biomarkers",
    "genomic",
    "genome",
    "gene expression",
    "protein",
    "oncogene",
    "tumor suppressor",
    "molecular",
    "pathway",
}


EVIDENCE_TERMS = {
    "prognosis",
    "prognostic",
    "diagnosis",
    "diagnostic",
    "survival",
    "susceptibility",
    "risk",
    "therapeutic",
    "therapy",
    "treatment",
    "drug response",
    "response",
    "target",
    "clinical",
    "association",
}


@dataclass
class RelevanceResult:
    relevant: bool
    lung_cancer_hits: list[str]
    molecular_hits: list[str]
    evidence_hits: list[str]
    reasons: list[str]


class RelevanceFilter:

    def evaluate(
        self,
        publication: Publication,
    ) -> RelevanceResult:

        text_parts = [
            publication.title or "",
            publication.abstract or "",
            " ".join(publication.keywords),
            " ".join(publication.mesh_terms),
        ]

        text = " ".join(text_parts).lower()

        lung_hits = self._find_matches(
            text,
            LUNG_CANCER_TERMS,
        )

        molecular_hits = self._find_matches(
            text,
            MOLECULAR_TERMS,
        )

        evidence_hits = self._find_matches(
            text,
            EVIDENCE_TERMS,
        )

        reasons = []

        if lung_hits:
            reasons.append("lung-cancer context detected")

        if molecular_hits:
            reasons.append("molecular/gene context detected")

        if evidence_hits:
            reasons.append("biomedical evidence context detected")

        if publication.abstract:
            reasons.append("abstract available")

        relevant = (
            bool(lung_hits)
            and bool(molecular_hits)
            and bool(publication.abstract)
        )

        return RelevanceResult(
            relevant=relevant,
            lung_cancer_hits=lung_hits,
            molecular_hits=molecular_hits,
            evidence_hits=evidence_hits,
            reasons=reasons,
        )

    @staticmethod
    def _find_matches(
        text: str,
        terms: set[str],
    ) -> list[str]:

        return sorted(
            term
            for term in terms
            if term in text
        )