import re
from rapidfuzz import fuzz


class SearchEngine:

    def __init__(self):
        pass

    # -----------------------------------------
    # Search
    # -----------------------------------------

    def search(self, data, text):

        text = text.strip().lower()

        if not text:
            return data

        results = []

        for item in data:

            score = self.score(item, text)

            if score >= 50:

                item_copy = item.copy()

                item_copy["score"] = score

                results.append(item_copy)

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    # -----------------------------------------
    # Calculate Score
    # -----------------------------------------

    def score(self, item, text):

        query = text.strip().lower()

        if not query:
            return 0

        query_words = [
            w for w in re.findall(r"\w+", query)
            if w
        ]

        if not query_words:
            return 0

        title = item.get("title", "")
        category = item.get("category", "")
        keywords = " ".join(item.get("keywords", []))
        tags = " ".join(item.get("tags", []))
        answer = item.get("answer", "")

        word_scores = []

        for q in query_words:

            w_score = max(
                self.score_field(q, title) * 1.0,
                self.score_field(q, tags) * 0.95,
                self.score_field(q, keywords) * 0.90,
                self.score_field(q, category) * 0.85,
                self.score_field(q, answer) * 0.75
            )

            word_scores.append(w_score)

        avg_score = sum(word_scores) / len(word_scores)

        # Bonus if the full query phrase appears intact
        phrase_bonus = 0
        all_text = f"{title} {category} {keywords} {tags} {answer}".lower()

        if query in all_text:
            phrase_bonus = 10

        return min(100.0, round(avg_score + phrase_bonus, 2))

    # -----------------------------------------
    # Calculate Score for Single Field
    # -----------------------------------------

    def score_field(self, q, field_text):

        if not field_text:
            return 0

        field_text_lower = field_text.lower()
        is_short_query = len(q) <= 3

        # 1. Exact match
        if q == field_text_lower:
            return 100

        # 2. Standalone word or word prefix match (e.g. "git" matches "git", "github")
        pattern = r"\b" + re.escape(q)

        if re.search(pattern, field_text_lower):
            return 95

        # 3. Substring match (for queries > 3 chars)
        if not is_short_query and q in field_text_lower:
            return 70

        # 4. Fuzzy match against words for typos
        field_words = re.findall(r"\w+", field_text_lower)
        max_fuzzy = 0

        for w in field_words:

            if is_short_query:
                if q == w:
                    max_fuzzy = max(max_fuzzy, 90)

            else:
                sim = fuzz.ratio(q, w)

                if sim >= 75:
                    max_fuzzy = max(max_fuzzy, sim)

        return max_fuzzy

    # -----------------------------------------
    # Categories
    # -----------------------------------------

    def categories(self, data):

        return sorted(

            {

                item["category"]

                for item in data

            }

        )

    # -----------------------------------------
    # Related
    # -----------------------------------------

    def related(self, item, data):

        return [

            row

            for row in data

            if row["category"] == item["category"]

            and row["id"] != item["id"]

        ]