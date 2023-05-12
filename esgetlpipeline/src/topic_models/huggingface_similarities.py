from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TokenClassificationPipeline,
)


class HuggingFaceKeywordExtractor:
    def __init__(self, model_name_or_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)
        self.pipeline = TokenClassificationPipeline(
            model=self.model, tokenizer=self.tokenizer
        )

    def extract_keywords(self, filepath, top_n=10):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        return self.extract_keywords_from_text(text, top_n=top_n)

    def extract_keywords_from_text(self, text, top_n=10):
        # Tokenize and classify tokens
        token_scores = self.pipeline(text)

        # Filter and sort keywords by score
        keywords = [t for t in token_scores if t["entity"] != "O"]
        keywords.sort(key=lambda x: x["score"], reverse=True)

        # Get the top-ranked keywords
        top_keywords = keywords[:top_n]
        return [k["word"] for k in top_keywords]


extractor = HuggingFaceKeywordExtractor(
    model_name_or_path="dbmdz/bert-large-cased-finetuned-conll03-english"
)
keywords = extractor.extract_keywords(
    "../plaintext/Starbucks_Global_Social_Impact_Report.txt", top_n=10
)
print(keywords)
