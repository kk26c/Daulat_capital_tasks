import pdfplumber
from transformers import pipeline
import os


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text.strip()


def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8")


def summarize_text(text):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    text_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    
    summary = ""
    for chunk in text_chunks:
        result = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + "\n"
    
    return summary.strip()


def save_summary(summary, output_path="summary.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"✅ Summary saved to {output_path}")


if __name__ == "__main__":
    pdf_file = "earnings_call.pdf"  
    
    if not os.path.exists(pdf_file):
        print("❌ PDF file not found.")
    else:
        print("📄 Extracting text...")
        text = extract_text(pdf_file)
        
        print("🧹 Cleaning text...")
        clean = clean_text(text)

        print("🧠 Summarizing...")
        summary = summarize_text(clean)

        print("💾 Saving summary...")
        save_summary(summary)
