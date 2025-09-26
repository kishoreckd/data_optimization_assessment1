from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

class SentimentPipeline:
    """This Class is used to get the sentiment pipeline as default"""
    _pipeline = None

    @classmethod
    def get_pipeline(cls):
        """This Function is used to get the sentiment pipeline"""
        if cls._pipeline is None:
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            model = AutoModelForSequenceClassification.from_pretrained(model_name, local_files_only=True)
            tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
            cls._pipeline = pipeline(
                "sentiment-analysis",
                model=model,
                tokenizer=tokenizer,
                device=-1   
            )
        return cls._pipeline
    
    @classmethod
    def cleanup(cls):
        """This Function is used to cleanup the sentiment pipeline"""
        if cls._pipeline is not None:
            del cls._pipeline
            cls._pipeline = None
            print("Sentiment pipeline unloaded.")
            return True
        return False


def get_sentiment_pipeline():
    """This Function is used to get the sentiment pipeline as dependency"""
    return SentimentPipeline.get_pipeline()