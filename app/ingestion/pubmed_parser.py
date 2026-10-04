import xml.etree.ElementTree as ET

from app.knowledge.schema import Publication


class PubMedParser:

    def parse(self, xml_data: str) -> list[Publication]:
        root = ET.fromstring(xml_data)

        publications = []

        for article in root.findall(".//PubmedArticle"):
            publication = self._parse_article(article)

            if publication:
                publications.append(publication)

        return publications

    def _parse_article(self, article) -> Publication | None:

        pmid_element = article.find(".//PMID")

        if pmid_element is None or not pmid_element.text:
            return None

        pmid = pmid_element.text.strip()

        title_element = article.find(".//ArticleTitle")

        title = ""

        if title_element is not None:
            title = "".join(title_element.itertext()).strip()

        abstract_parts = []

        for abstract_text in article.findall(".//AbstractText"):
            text = "".join(abstract_text.itertext()).strip()

            if text:
                abstract_parts.append(text)

        abstract = "\n".join(abstract_parts) or None

        authors = []

        for author in article.findall(".//Author"):
            last_name = author.findtext("LastName")
            initials = author.findtext("Initials")

            if last_name and initials:
                authors.append(f"{last_name} {initials}")
            elif last_name:
                authors.append(last_name)

        journal = article.findtext(".//Journal/Title")

        publication_year = None

        year_element = article.find(".//PubDate/Year")

        if year_element is not None and year_element.text:
            try:
                publication_year = int(year_element.text)
            except ValueError:
                publication_year = None

        doi = None

        for article_id in article.findall(".//ArticleId"):
            if article_id.attrib.get("IdType") == "doi":
                doi = article_id.text
                break

        keywords = []

        for keyword in article.findall(".//Keyword"):
            if keyword.text:
                keywords.append(keyword.text.strip())

        mesh_terms = []

        for descriptor in article.findall(
            ".//MeshHeading/DescriptorName"
        ):
            if descriptor.text:
                mesh_terms.append(descriptor.text.strip())

        publication_types = []

        for publication_type in article.findall(
            ".//PublicationType"
        ):
            if publication_type.text:
                publication_types.append(
                    publication_type.text.strip()
                )

        return Publication(
            pmid=pmid,
            title=title,
            abstract=abstract,
            authors=authors,
            journal=journal,
            publication_year=publication_year,
            doi=doi,
            keywords=keywords,
            mesh_terms=mesh_terms,
            publication_types=publication_types,
        )