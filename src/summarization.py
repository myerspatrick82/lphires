import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def main():
    # Load the model
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

    # Read and split bios
    with open("scrape.txt", "r", encoding="utf-8") as f:
        content = f.read()

    bios = content.split("=== ")
    bios = [bio for bio in bios if bio.strip()]  # Remove empty entries

    n = len(bios)
    sample_indices = [int(i * n / 20) for i in range(20)]

    summarization = open("summarizations.txt", "w", encoding="utf-8")

    for i in sample_indices:
        bio = bios[i]
        try:
            lines = bio.strip().splitlines()
            name = lines[0].strip("= ").strip()
            text = " ".join(lines[1:]).strip()

            input_ids = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
            output = model.generate(input_ids, min_length=200, max_length=300)
            summary = tokenizer.decode(output[0], skip_special_tokens=True)
            print("summary for", name)
            summarization.write(f"\nSummary for {name}:\n{summary}")

        except Exception as e:
            print(f"Failed to process {i}: {e}")

if __name__ == "__main__":
    main()