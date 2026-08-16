import re
from rapidfuzz import fuzz


class SearchEngine:

    def __init__(self):
        pass

    # -----------------------------------------
    # Search & Filter
    # -----------------------------------------

    def search(self, data, text, category_filter=None):
        text = text.strip().lower()

        # If no query text and no category filter, return all data
        if not text and not category_filter:
            return data

        results = []

        for item in data:
            # Apply category filter if specified
            if category_filter and category_filter.lower() != "all":
                item_cat = item.get("category", "").lower()
                if item_cat != category_filter.lower():
                    continue

            if not text:
                item_copy = item.copy()
                item_copy["score"] = 100
                results.append(item_copy)
                continue

            score = self.score(item, text)

            # Adaptive threshold based on query length
            min_threshold = 15 if len(text) <= 2 else 35

            if score >= min_threshold:
                item_copy = item.copy()
                item_copy["score"] = score
                results.append(item_copy)

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    # -----------------------------------------
    # Calculate Precision Score
    # -----------------------------------------

    def score(self, item, text):
        query = text.strip().lower()

        if not query:
            return 0

        title = item.get("title", "").lower()
        category = item.get("category", "").lower()
        keywords = [k.lower() for k in item.get("keywords", [])]
        tags = [t.lower() for t in item.get("tags", [])]
        answer = item.get("answer", "").lower()

        keywords_text = " ".join(keywords)
        tags_text = " ".join(tags)

        # 1. Direct Title / Category / Tag StartsWith (Highest Priority for short queries)
        if title.startswith(query) or category.startswith(query) or any(t.startswith(query) for t in tags):
            return 100.0

        if any(k.startswith(query) for k in keywords):
            return 95.0

        # 2. Direct Substring Match
        if query in title:
            return 90.0
        if query in category or query in tags_text:
            return 85.0
        if query in keywords_text:
            return 80.0
        if query in answer:
            return 70.0

        # 3. Multi-word & Fuzzy Search Scoring
        query_words = [w for w in re.findall(r"\w+", query) if w]
        if not query_words:
            return 0

        word_scores = []
        for q in query_words:
            w_score = max(
                self.score_field(q, title) * 1.0,
                self.score_field(q, tags_text) * 0.95,
                self.score_field(q, keywords_text) * 0.90,
                self.score_field(q, category) * 0.85,
                self.score_field(q, answer) * 0.65
            )
            word_scores.append(w_score)

        avg_score = sum(word_scores) / len(word_scores)

        return min(100.0, round(avg_score, 2))

    # -----------------------------------------
    # Calculate Score for Single Field
    # -----------------------------------------

    def score_field(self, q, field_text):
        if not field_text:
            return 0

        field_text_lower = field_text.lower()
        is_short_query = len(q) <= 2

        if field_text_lower.startswith(q):
            return 95

        if q in field_text_lower:
            return 85

        # Fuzzy match for typos
        field_words = re.findall(r"\w+", field_text_lower)
        max_fuzzy = 0

        for w in field_words:
            if is_short_query:
                if w.startswith(q):
                    max_fuzzy = max(max_fuzzy, 80)
            else:
                sim = fuzz.ratio(q, w)
                if sim >= 70:
                    max_fuzzy = max(max_fuzzy, sim)

        return max_fuzzy

    # -----------------------------------------
    # Categories
    # -----------------------------------------

    def categories(self, data):
        return sorted({item.get("category", "General") for item in data if item.get("category")})

    # -----------------------------------------
    # Related Items
    # -----------------------------------------

    def related(self, item, data):
        return [
            row for row in data
            if row.get("category") == item.get("category") and row.get("id") != item.get("id")
        ]