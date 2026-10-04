import re

from app.knowledge.evidence_score import EvidenceScore
from app.knowledge.schema import Publication


class EvidenceScorer:
    """
    Deterministic baseline evidence scorer.

    This is intentionally explainable and rule-based.
    It will serve as the baseline before introducing
    semantic or LLM-based evidence assessment.
    """

    DISEASE_TERMS = {
        "lung cancer",
        "lung adenocarcinoma",
        "lung squamous cell carcinoma",
        "non-small cell lung cancer",
        "small cell lung cancer",
        "lung neoplasm",
        "nsclc",
        "luad",
        "lusc",
        "sclc",
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
        "molecular",
        "genomic",
        "genome",
        "protein",
        "pathway",
        "expression",
    }

    EVIDENCE_TERMS = {
        "association",
        "associated",
        "risk",
        "susceptibility",
        "prognosis",
        "prognostic",
        "survival",
        "clinical",
        "response",
        "therapy",
        "therapeutic",
        "treatment",
        "diagnostic",
        "validation",
        "experimental",
    }

    GENE_SYMBOLS = {
        "EGFR",
        "KRAS",
        "TP53",
        "ALK",
        "ROS1",
        "BRAF",
        "MET",
        "RET",
        "ERBB2",
        "HER2",
        "STK11",
        "KEAP1",
        "NTRK1",
        "NTRK2",
        "NTRK3",
        "PIK3CA",
        "RB1",
        "PTEN",
        "ATM",
        "SMARCA4",
        "NF1",
    }

    def evaluate(self, publication: Publication) -> EvidenceScore:
        text = self._build_text(publication)

        disease_hits = self._find_terms(
            text,
            self.DISEASE_TERMS,
        )

        molecular_hits = self._find_terms(
            text,
            self.MOLECULAR_TERMS,
        )

        evidence_hits = self._find_terms(
            text,
            self.EVIDENCE_TERMS,
        )

        gene_hits = self._find_terms(
            text,
            self.GENE_SYMBOLS,
        )

        disease_score = self._score_dimension(
            len(disease_hits),
            maximum=3,
        )

        molecular_score = self._score_dimension(
            len(molecular_hits),
            maximum=4,
        )

        evidence_score = self._score_dimension(
            len(evidence_hits),
            maximum=4,
        )

        gene_specificity_score = self._score_dimension(
            len(gene_hits),
            maximum=2,
        )

        total_score = (
            0.30 * disease_score
            + 0.25 * molecular_score
            + 0.25 * evidence_score
            + 0.20 * gene_specificity_score
        )

        reasons = []

        if disease_hits:
            reasons.append(
                "lung-cancer disease context detected"
            )

        if molecular_hits:
            reasons.append(
                "molecular/genomic context detected"
            )

        if evidence_hits:
            reasons.append(
                "biomedical evidence context detected"
            )

        if gene_hits:
            reasons.append(
                "specific lung-cancer gene symbols detected"
            )

        if publication.abstract:
            reasons.append(
                "abstract available"
            )

        return EvidenceScore(
            disease_score=round(disease_score, 4),
            molecular_score=round(molecular_score, 4),
            evidence_score=round(evidence_score, 4),
            gene_specificity_score=round(
                gene_specificity_score,
                4,
            ),
            total_score=round(total_score, 4),
            disease_hits=disease_hits,
            molecular_hits=molecular_hits,
            evidence_hits=evidence_hits,
            gene_hits=gene_hits,
            reasons=reasons,
        )

    @staticmethod
    def _build_text(publication: Publication) -> str:
        parts = [
            publication.title or "",
            publication.abstract or "",
            " ".join(publication.keywords),
            " ".join(publication.mesh_terms),
        ]

        return " ".join(parts).lower()

    @staticmethod
    def _find_terms(
        text: str,
        terms: set[str],
    ) -> list[str]:
        hits = []

        for term in sorted(terms):
            pattern = rf"\b{re.escape(term.lower())}\b"

            if re.search(pattern, text):
                hits.append(term)

        return hits

    @staticmethod
    def _score_dimension(
        hits: int,
        maximum: int,
    ) -> float:
        if hits <= 0:
            return 0.0

        return min(hits / maximum, 1.0)