from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    try:
        result = summarizer(text, max_length=60, min_length=20, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        return text 