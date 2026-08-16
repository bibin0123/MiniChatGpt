import re


class SmartPaste:

    def __init__(self):
        # Common web junk, navigation, and advertisement patterns to filter out
        self.junk_patterns = [
            r"^\s*cookie\s+policy.*$",
            r"^\s*privacy\s+policy.*$",
            r"^\s*accept\s+all?\s+cookies.*$",
            r"^\s*sign\s+in\s*/?\s*register.*$",
            r"^\s*log\s+in.*$",
            r"^\s*subscribe.*$",
            r"^\s*share\s+on\s+.*$",
            r"^\s*was\s+this\s+helpful\??.*$",
            r"^\s*all\s+rights?\s+reserved.*$",
            r"^\s*copyright\s+©.*$",
            r"^\s*terms\s+of\s+use.*$",
            r"^\s*advertisement.*$",
            r"^\s*promoted\s+content.*$",
            r"^\s*asked\s+\d+.*$",
            r"^\s*modified\s+\d+.*$",
            r"^\s*viewed\s+\d+.*$",
            r"^\s*\d+\s+votes?.*$",
            r"^\s*add\s+a\s+comment.*$",
            r"^\s*improve\s+this\s+question.*$",
            r"^\s*follow\s+us.*$",
            r"^\s*edited\s+[a-z]{3}\s+\d+.*$",
            r"^\s*copy\s+code\s*$",
            r"^\s*https?://\S+\s*$"
        ]

    # -----------------------------------------
    # Advanced Smart Paste
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

        text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

        # 1. Filter out junk lines
        cleaned_lines = self.filter_junk_lines(text)
        if not cleaned_lines:
            cleaned_lines = [text]

        # 2. Extract Concise Title
        title = self.extract_title(cleaned_lines)

        # 3. Detect Category
        category = self.detect_category(text)

        # 4. Properly Arranged Answer
        formatted_answer = self.format_answer(cleaned_lines)

        # 5. Extract Keywords & Tags
        keywords = self.extract_keywords(text)
        tags = self.extract_tags(text)

        return {
            "title": title,
            "category": category,
            "keywords": keywords,
            "tags": tags,
            "answer": formatted_answer
        }

    # -----------------------------------------
    # Filter Out Junk Lines
    # -----------------------------------------

    def filter_junk_lines(self, text):
        lines = text.splitlines()
        clean_lines = []
        seen = set()

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Strip leading line numbers from code blocks
            stripped = re.sub(r"^\d{1,4}\s{1,3}(?=[a-zA-Z#/*])", "", stripped)

            is_junk = False
            for pattern in self.junk_patterns:
                if re.match(pattern, stripped, re.IGNORECASE):
                    is_junk = True
                    break

            if not is_junk:
                if stripped not in seen or len(stripped) > 40:
                    clean_lines.append(stripped)
                    seen.add(stripped)

        return clean_lines

    # -----------------------------------------
    # Extract Title (Accurate and Concise)
    # -----------------------------------------

    def extract_title(self, lines):
        for line in lines:
            # Skip code blocks or syntax lines
            if line.startswith("```") or line.endswith("{") or line.endswith(";"):
                continue

            raw = re.sub(r"^\#+\s*", "", line)
            raw = re.sub(r"^\*\*(.*)\*\*$", r"\1", raw)
            raw = re.sub(r"\s*[\-\|]\s*(Stack Overflow|GeeksforGeeks|W3Schools|MDN|GitHub|YouTube|Wikipedia|Medium).*", "", raw, flags=re.IGNORECASE)
            raw = re.sub(r"^\d+[\.\)]\s*", "", raw)
            raw = raw.strip()

            # Clean special characters but keep spaces & alphanumerics
            clean = re.sub(r"[^\w\s\-\?\.\:]", "", raw).strip()

            words = clean.split()
            if len(words) >= 1:
                # Limit title to max 6 words for accuracy while remaining concise
                short_words = words[:6]
                title_str = " ".join(short_words)
                # Keep question marks if original line had it
                if "?" in raw and not title_str.endswith("?"):
                    title_str += "?"
                return title_str.title()

        return "Knowledge Note"

    # -----------------------------------------
    # Detect Category
    # -----------------------------------------

    def detect_category(self, text):
        text_lower = text.lower()

        if any(w in text_lower for w in ["select ", "create database", "drop database", "show databases", "table", "sql", "mysql", "postgresql", "where "]):
            return "SQL"
        elif any(w in text_lower for w in ["def ", "import ", "python", "print(", "class ", "self.", "pip install"]):
            return "Python"
        elif any(w in text_lower for w in ["git ", "commit", "github", "git push", "repository", "branch"]):
            return "Git"
        elif any(w in text_lower for w in ["tkinter", "ttk.", "mainloop", "widget", "canvas"]):
            return "Tkinter"
        elif any(w in text_lower for w in ["react", "jsx", "usestate", "useeffect", "component"]):
            return "React"
        elif any(w in text_lower for w in ["django", "models.model", "views.py", "urlpatterns"]):
            return "Django"
        elif any(w in text_lower for w in ["linux", "bash", "sudo", "apt", "chmod", "systemctl"]):
            return "Linux"

        return "General"

    # -----------------------------------------
    # Format Answer Properly (Clean Sentence & Paragraph Arrangement)
    # -----------------------------------------

    def format_answer(self, lines):
        formatted_blocks = []
        in_code_block = False
        code_lines = []

        for line in lines:
            line_str = line.strip()

            if line_str.startswith("```"):
                if in_code_block:
                    in_code_block = False
                    formatted_blocks.append("```\n" + "\n".join(code_lines) + "\n```")
                    code_lines = []
                else:
                    in_code_block = True
                continue

            if in_code_block:
                code_lines.append(line)
                continue

            is_code_line = (
                line_str.startswith(("git ", "sudo ", "pip ", "npm ", "python ", "curl ", "SELECT ", "DROP ", "CREATE ", "SHOW ")) or
                line_str.endswith(";") or
                (line_str.startswith("def ") and line_str.endswith(":")) or
                (line_str.startswith("class ") and line_str.endswith(":"))
            )

            # Detect headings
            is_markdown_header = line_str.startswith("#")
            is_colon_header = line_str.endswith(":") and len(line_str) < 80 and not is_code_line
            is_short_heading = len(line_str) < 45 and not line_str.endswith((".", "!", "?", ";", ",", "}")) and not is_code_line and not line_str.startswith(("-", "*", "1.", "2.", "3.", "4.", "5."))

            # Detect List Items
            is_list_item = line_str.startswith(("- ", "* ", "• ")) or re.match(r"^\d+[\.\)]\s+", line_str)

            if is_markdown_header or is_colon_header or is_short_heading:
                clean_h = re.sub(r"^\#+\s*", "", line_str).strip()
                clean_h = re.sub(r"^\d+[\.\)]\s*", "", clean_h)
                if clean_h and not (clean_h.startswith("**") and clean_h.endswith("**")):
                    clean_h = f"**{clean_h}**"
                if clean_h:
                    formatted_blocks.append(clean_h)
            elif is_list_item or is_code_line:
                formatted_blocks.append(line_str)
            else:
                # Dense text paragraph: split long walls of sentences into clean multi-line paragraphs
                sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", line_str)
                if len(sentences) > 1:
                    # Group sentences into small readable chunks (2-3 sentences per paragraph block)
                    current_p = []
                    for sent in sentences:
                        current_p.append(sent)
                        if len(current_p) >= 2:
                            formatted_blocks.append(" ".join(current_p))
                            current_p = []
                    if current_p:
                        formatted_blocks.append(" ".join(current_p))
                else:
                    formatted_blocks.append(line_str)

        if code_lines:
            formatted_blocks.append("```\n" + "\n".join(code_lines) + "\n```")

        return "\n\n".join(formatted_blocks)

    # -----------------------------------------
    # Extract Keywords
    # -----------------------------------------

    def extract_keywords(self, text):
        words = re.findall(r"[A-Za-z0-9_]+", text.lower())

        ignore = {
            "the", "and", "for", "with", "this", "that", "from",
            "into", "your", "have", "will", "using", "about", "after",
            "been", "before", "being", "between", "both", "but", "by",
            "can", "could", "did", "does", "each", "from", "further",
            "had", "has", "have", "having", "here", "how", "its", "just",
            "more", "most", "must", "only", "other", "our", "out", "over",
            "same", "some", "such", "than", "them", "then", "there", "these",
            "they", "this", "those", "through", "under", "until", "what",
            "when", "where", "which", "while", "who", "whom", "why", "would",
            "http", "https", "com", "www", "org", "html", "page", "code", "answer",
            "step", "steps", "note", "example"
        }

        keywords = []
        for word in words:
            if len(word) < 3 or word in ignore or word.isdigit():
                continue
            if word not in keywords:
                keywords.append(word)

        return keywords[:5]

    # -----------------------------------------
    # Extract Tags
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
            "sql": "SQL",
            "git": "Git",
            "github": "GitHub"
        }

        for key, value in mapping.items():
            if key in text_lower:
                tags.append(value)

        if "web" in text_lower or "http" in text_lower:
            tags.append("Web")

        return list(set(tags))[:5]