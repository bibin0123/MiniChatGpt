import re


class SmartPaste:

    def __init__(self):
        pass

    # -----------------------------------------
    # Parse Clipboard Text
    # -----------------------------------------

    def parse(self, text):

        text = text.strip()

        if not text:
            return {
                "title": "",
                "category": "General",
                "keywords": [],
                "tags": [],
                "answer": ""
            }

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        title = ""
        if lines:
            raw_title = lines[0]
            raw_title = re.sub(r"^\#+\s*", "", raw_title)
            raw_title = re.sub(r"^\*\*(.*)\*\*$", r"\1", raw_title)
            title = raw_title.strip()

        formatted_answer = self.format_text(text)
        keywords = self.extract_keywords(text)
        tags = self.extract_tags(text)

        return {
            "title": title,
            "category": "General",
            "keywords": keywords,
            "tags": tags,
            "answer": formatted_answer
        }

    # -----------------------------------------
    # Format Text: Headings bold, sentences on next line with one line gap
    # -----------------------------------------

    def format_text(self, text):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return ""

        formatted_blocks = []

        for index, line in enumerate(lines):

            is_heading = (
                index == 0 or
                line.endswith(":") or
                line.startswith("#") or
                (len(line) < 60 and not line.endswith((".", "!", "?")))
            )

            if is_heading:
                clean_heading = re.sub(r"^\#+\s*", "", line).strip()

                if not (clean_heading.startswith("**") and clean_heading.endswith("**")):
                    clean_heading = f"**{clean_heading}**"

                formatted_blocks.append(clean_heading)

            else:
                sentences = self.split_sentences(line)

                for sentence in sentences:
                    if sentence:
                        formatted_blocks.append(sentence)

        return "\n\n".join(formatted_blocks)

    # -----------------------------------------
    # Split Paragraph into Sentences
    # -----------------------------------------

    def split_sentences(self, text):

        protected_text = text
        abbreviations = ["e.g.", "i.e.", "vs.", "etc.", "Dr.", "Mr.", "Mrs.", "Ms.", "Prof."]

        for abbr in abbreviations:
            protected_text = protected_text.replace(abbr, abbr.replace(".", "___DOT___"))

        raw_sentences = re.split(r"(?<=[.!?])\s+", protected_text)

        sentences = []
        for s in raw_sentences:
            s_restored = s.replace("___DOT___", ".").strip()
            if s_restored:
                sentences.append(s_restored)

        return sentences

    # -----------------------------------------
    # Keywords
    # -----------------------------------------

    def extract_keywords(self, text):

        words = re.findall(
            r"[A-Za-z0-9_]+",
            text.lower()
        )

        ignore = {
            "the", "and", "for", "with", "this", "that", "from",
            "into", "your", "have", "will", "using", "about", "after",
            "been", "before", "being", "between", "both", "but", "by",
            "can", "could", "did", "does", "each", "from", "further",
            "had", "has", "have", "having", "here", "how", "its", "just",
            "more", "most", "must", "only", "other", "our", "out", "over",
            "same", "some", "such", "than", "them", "then", "there", "these",
            "they", "this", "those", "through", "under", "until", "what",
            "when", "where", "which", "while", "who", "whom", "why", "would"
        }

        keywords = []

        for word in words:
            if len(word) < 3 or word in ignore:
                continue

            if word not in keywords:
                keywords.append(word)

        return keywords[:20]

    # -----------------------------------------
    # Tags
    # -----------------------------------------

    def extract_tags(self, text):

        tags = []
        text_lower = text.lower()

        mapping = {
            "python": "Python",
            "tkinter": "Tkinter",
            "mysql": "MySQL",
            "postgresql": "PostgreSQL",
            "react": "React",
            "django": "Django",
            "flask": "Flask",
            "docker": "Docker",
            "linux": "Linux",
            "windows": "Windows",
            "json": "JSON",
            "api": "API",
            "sql": "SQL"
        }

        for key, value in mapping.items():
            if key in text_lower:
                tags.append(value)

        return tags