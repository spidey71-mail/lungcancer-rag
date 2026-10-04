# LungCancer-RAG

> **Evidence-Centric Biomedical RAG for Lung Cancer Gene Research**

LungCancer-RAG is an experimental biomedical Retrieval-Augmented Generation (RAG) system designed to automatically construct a research-oriented knowledge base from biomedical literature.

The long-term objective is to support **lung-cancer gene discovery and ranking with traceable evidence**, rather than relying solely on language-model knowledge.

---

## 1. Project Objective

The system aims to build an automated pipeline that converts biomedical literature into a structured, evidence-oriented knowledge base.

The intended pipeline is:

```text
                    Biomedical Literature
                            │
                            ▼
                    PubMed API Retrieval
                            │
                            ▼
                    Candidate Publications
                            │
                            ▼
                       Relevance
                         Filtering
                            │
                            ▼
                    Evidence Extraction
                            │
                            ▼
                  Structured Knowledge Base
                            │
                            ▼
                         RAG
                            │
                            ▼
                 Evidence-Grounded Answers
                            │
                            ▼
                  Lung-Cancer Gene Ranking
```

The key design principle is:

> **The RAG system should retrieve evidence from biomedical literature rather than relying on the LLM's internal knowledge alone.**

---

# 2. Why Automated Knowledge Construction?

Traditional biomedical RAG systems often depend on a manually prepared corpus:

```text
Researcher
   ↓
Find papers
   ↓
Download papers
   ↓
Read/filter papers
   ↓
Clean documents
   ↓
Chunk documents
   ↓
Create embeddings
   ↓
Build vector database
```

This process is:

- time-consuming
- difficult to reproduce
- dependent on manual judgment
- difficult to scale
- vulnerable to inconsistent document selection

LungCancer-RAG investigates whether this process can be automated while maintaining **relevance, traceability, and evidence quality**.

---

# 3. Current Automated Ingestion Pipeline

The current implementation begins with PubMed.

```text
Research Objective
       │
       ▼
   PubMed Query
       │
       ▼
   PubMed Search
       │
       ▼
      PMIDs
       │
       ▼
 Article Retrieval
       │
       ▼
   XML Records
       │
       ▼
 Structured Publications
       │
       ▼
 Relevance Filtering
```

The system currently retrieves:

- PMID
- title
- abstract
- journal
- publication year
- authors
- DOI
- keywords
- MeSH terms

This structured representation forms the foundation for downstream evidence extraction.

---

# 4. Initial Retrieval Experiment

### Query

The first experiment used the broad PubMed query:

```text
lung cancer AND gene
```

The system requested:

```text
5 publications
```

The PubMed API successfully returned:

```text
PMIDs retrieved: 5
```

The retrieved publications were successfully parsed:

```text
Publications discovered : 5
Successfully parsed     : 5
Failed                   : 0
```

Therefore:

```text
Retrieval success = 5/5
Parsing success   = 5/5
```

This establishes that the automated PubMed ingestion layer is functioning correctly.

---

# 5. First Relevance Filtering Baseline

The first relevance filter was intentionally implemented as a **deterministic lexical baseline**.

A publication was considered relevant when it contained:

```text
Lung-cancer context
        AND
Molecular/gene context
        AND
Abstract available
```

The filter searches for predefined vocabulary related to:

### Lung-cancer context

```text
lung cancer
NSCLC
SCLC
lung adenocarcinoma
lung squamous cell carcinoma
lung neoplasm
```

### Molecular context

```text
gene
mutation
biomarker
protein
genomic
molecular
pathway
```

### Evidence context

```text
prognosis
survival
risk
susceptibility
therapy
treatment
therapeutic
association
```

Each decision is accompanied by an explanation rather than only a binary label.

Example:

```text
KEEP

Lung terms : lung cancer
Molecular  : gene
Evidence   : association, risk, susceptibility

Reasons:
✓ lung-cancer context detected
✓ molecular/gene context detected
✓ biomedical evidence context detected
✓ abstract available
```

---

# 6. Baseline Result

For the initial five-paper experiment:

```text
Candidate publications : 5
Relevant (KEEP)        : 5
Rejected               : 0
Relevance rate         : 100%
```

At first glance, this may appear successful.

However, **100% relevance is not necessarily a good result**.

Manual inspection of the retrieved publications exposed an important limitation.

---

# 7. What the Experiment Revealed

Several papers satisfied the lexical rules but were not necessarily strong evidence for the actual research objective of:

> **lung-cancer gene association, characterization, prognosis, susceptibility, or therapeutic relevance.**

For example, one retrieved publication focused primarily on:

```text
TGFBR1
Pan-cancer prognosis
Gastric cancer
```

while the lexical filter detected terms such as:

```text
lung squamous cell carcinoma
gene
genomic
protein
prognosis
```

and therefore classified the document as:

```text
KEEP
```

Another retrieved paper concerned phytochemicals and multi-target cancer therapy and was also retained because the required vocabulary appeared in the document.

This demonstrates a fundamental limitation.

---

# 8. Research Finding: Lexical Filtering Is Not Sufficient

The current experiment demonstrates that:

> **Simple keyword/lexical matching is insufficient for constructing a high-quality biomedical evidence corpus.**

The reason is that lexical filtering determines relevance largely from the **presence of words**, rather than understanding the **relationship between concepts**.

For example:

```text
"lung cancer"
+
"gene"
```

does not necessarily mean:

```text
Gene ↔ Lung Cancer
```

A document may mention both concepts while primarily investigating:

- another cancer type
- a drug
- a pathway
- a general review
- a non-lung-cancer population
- an unrelated biological mechanism

Therefore, a biomedical RAG system cannot safely treat:

```text
keyword present = evidence relevant
```

---

# 9. Important Distinction

The system therefore separates two different tasks:

```text
Candidate Discovery
        ≠
Evidence Relevance
```

### Candidate discovery

Should prioritize:

> **High recall**

We want to retrieve potentially useful papers even if some irrelevant papers are included.

### Evidence filtering

Should prioritize:

> **High precision**

We want the final knowledge base to contain documents that actually support the research question.

Therefore:

```text
PubMed Search
     ↓
High Recall
     ↓
Candidate Corpus
     ↓
Semantic/Evidence Filtering
     ↓
High Precision
     ↓
Evidence Corpus
```

This distinction is central to the design of LungCancer-RAG.

---

# 10. Current Research Gap

The baseline experiment identifies the first research gap being addressed by this project:

> **How can biomedical literature be automatically filtered for research-specific evidence rather than merely matched using keywords?**

The desired system should understand relationships such as:

```text
EGFR
  │
  ├── associated with → NSCLC
  ├── mutation → EGFR exon 19 deletion
  ├── therapeutic relevance → EGFR inhibitors
  └── evidence → PMID / publication
```

rather than simply detecting:

```text
"EGFR"
"lung cancer"
```

in the same document.

---

# 11. Current Limitations of the Baseline

The current lexical baseline has several known limitations.

### 1. Keyword dependence

The system depends on predefined vocabulary.

A paper using an unexpected synonym may be missed.

### 2. Context blindness

The filter does not fully understand which cancer type is the primary focus of the publication.

### 3. Relationship blindness

The system detects the presence of concepts but does not establish relationships between them.

### 4. False positives

A paper can mention lung cancer and genes without being strong evidence for lung-cancer gene research.

### 5. Lexical overlap

Simple substring matching can produce overlapping matches.

For example:

```text
lung cancer
```

may be detected inside:

```text
non-small cell lung cancer
```

This is a known limitation of the current baseline.

---

# 12. Proposed Improvement

The next stage is to move beyond purely lexical filtering.

The planned architecture is:

```text
                PubMed
                  │
                  ▼
          Query Expansion
                  │
                  ▼
        Candidate Retrieval
                  │
                  ▼
            Deduplication
                  │
                  ▼
       Lexical Baseline
                  │
                  ▼
       Semantic Relevance
           Filtering
                  │
                  ▼
        Evidence Extraction
                  │
                  ▼
        Structured Knowledge
                  │
                  ▼
              RAG
```

Semantic filtering will allow the system to compare the **research intent** with the meaning of the publication rather than relying solely on word occurrence.

---

# 13. Evaluation Strategy

The project will not simply claim that the improved filter is better.

Different ingestion strategies will be experimentally compared:

```text
Method 1
Lexical filtering
        │
        ▼
Baseline

Method 2
Semantic embedding filtering
        │
        ▼
Semantic baseline

Method 3
Hybrid / evidence-aware filtering
        │
        ▼
Proposed approach
```

The approaches can be evaluated using metrics such as:

- Precision
- Recall
- F1-score
- False-positive rate
- False-negative rate
- Retrieval coverage

This allows the project to demonstrate whether the proposed knowledge-construction method actually improves the quality of the evidence corpus.

---

# 14. Reproducibility

The ingestion pipeline is being developed incrementally with automated tests.

Current test status:

```text
PubMed search test       ✅
PubMed fetch test        ✅
Relevant paper test      ✅
Irrelevant paper test    ✅

Total:
4/4 tests passed
```

The project follows a checkpoint-based development workflow so that each major stage can be independently validated and reproduced.

---

# 15. Current Status

### Automated Knowledge Construction

| Component | Status |
|---|---|
| UV environment | ✅ |
| PubMed API client | ✅ |
| PubMed search | ✅ |
| Article retrieval | ✅ |
| XML parsing | ✅ |
| Structured publication schema | ✅ |
| Lexical relevance baseline | ✅ |
| Unit tests | ✅ |
| Real PubMed experiment | ✅ |
| Semantic relevance filtering | 🔄 Next |
| Evidence extraction | ⏳ |
| Knowledge database | ⏳ |
| RAG retrieval | ⏳ |
| Gene ranking | ⏳ |
| LoRA-v2 research model | ⏳ |
| Hallucination evaluation | ⏳ |
| Langfuse monitoring | ⏳ |

---

# 16. Key Review Takeaway

The first experiment does **not** demonstrate that lexical filtering solves biomedical knowledge construction.

Instead, it demonstrates why a stronger approach is necessary.

### Review statement

> **"We initially implemented a deterministic lexical filtering baseline for automated PubMed ingestion. Although it successfully identified documents containing lung-cancer and molecular terminology, manual inspection showed that lexical co-occurrence does not guarantee research relevance. This motivated the transition toward semantic and evidence-aware document filtering, where the system must determine whether the publication actually provides evidence relevant to lung-cancer gene research."**

This observation becomes the motivation for the next stage of LungCancer-RAG.

---

## Current Checkpoint

```text
CHECKPOINT 4A — Automated Ingestion + Lexical Baseline

PubMed Retrieval       ✅
Structured Parsing     ✅
Lexical Filtering      ✅
Unit Testing           ✅
Real-world Evaluation  ✅

Important Finding:
Lexical filtering alone is insufficient for
high-quality biomedical evidence ingestion.
```

**Next objective:** develop a stronger relevance mechanism that evaluates **semantic and research-specific relevance**, while retaining the lexical system as the baseline for comparison.

// Checkpoint 4B — Multi-Query Candidate Discovery

8 biomedical query families
40 retrieval slots
19 unique publications
21 duplicate retrievals
52.5% duplicate rate
PMID-level deduplication
Query-level provenance tracking

// A single lexical query provides a narrow retrieval path. The controlled multi-query strategy expands discovery across mutation, prognosis, biomarker, survival, therapy, NSCLC, LUAD, and LUSC dimensions. PMID-level deduplication prevents duplicate documents from entering the downstream corpus while preserving the query provenance that led to each candidate.

// ## Automated Knowledge Construction

The system is designed to construct a traceable biomedical knowledge base
from PubMed literature rather than directly dumping retrieved documents
into a vector database.

### Current Pipeline

PubMed API
→ Query Construction
→ Candidate Retrieval
→ Deduplication
→ Relevance Filtering
→ Evidence Scoring
→ Knowledge Record

### Evidence Scoring

Each candidate publication is evaluated across multiple dimensions:

- Lung-cancer disease context
- Molecular/genomic context
- Biomedical evidence context
- Gene-specificity
- Evidence strength

The resulting score is accompanied by explicit evidence hits and reasons,
making the filtering process explainable.

### Knowledge Records

Relevant publications are transformed into structured knowledge records.

Each record preserves:

- PMID
- Publication metadata
- Gene symbols
- Disease context
- Molecular evidence
- Evidence types
- Evidence score
- Evidence reasons
- PubMed provenance
- Retrieval query

This prevents loss of source traceability when the data is later converted
into RAG documents and embeddings.

### Research Significance

A conventional ingestion pipeline may retrieve documents and immediately
embed them. This makes it difficult to determine why a document entered the
knowledge base.

Our pipeline introduces an intermediate evidence-aware representation:

Publication
→ Relevance
→ Evidence Score
→ Knowledge Record
→ RAG Document
→ Embedding

This provides an auditable path from generated answers back to the original
biomedical publication.

//The system does not directly dump PubMed search results into the RAG knowledge base. It performs controlled candidate retrieval, deduplication, relevance assessment, explainable evidence scoring, and provenance-preserving knowledge construction before downstream RAG processing.

//## Knowledge Document Construction

Evidence-backed knowledge records are converted into retrieval-ready
documents before embedding.

The document representation preserves:

- Publication metadata
- Gene symbols
- Disease context
- Molecular evidence
- Evidence types
- Evidence score
- Evidence reasons
- PMID
- PubMed provenance
- Retrieval query

The system separates knowledge representation from retrieval
representation.

KnowledgeRecord
→ KnowledgeDocument
→ Chunking
→ Embedding
→ Vector Database

This separation allows different document representations to be
evaluated experimentally without changing the underlying biomedical
knowledge extraction process.

//what we are putting into the RAG
Title: EGFR mutations in non-small cell lung cancer
PMID: TEST001
Genes: EGFR
Disease Context: lung cancer, non-small cell lung cancer
Molecular Evidence: mutation
Evidence Types: prognosis, survival
Evidence Score: 0.8800
Evidence Reasons: gene-specific evidence

METADATA:
{'pmid': 'TEST001', 'source': 'PubMed', 'query': 'lung cancer AND gene', 'journal': None, 'publication_year': None, 'doi': None, 'genes': ['EGFR'], 'disease_context': ['lung cancer', 'non-small cell lung cancer'], 'molecular_evidence': ['mutation'], 'evidence_types': ['prognosis', 'survival'], 'evidence_score': 0.88}
(lungcancer-rag) PS D:\lungcancer-rag> 