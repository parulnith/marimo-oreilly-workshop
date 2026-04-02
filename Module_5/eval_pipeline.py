from module_5 import get_client, classify_batch, summarize_results

client = get_client(base_url="http://localhost:11434/v1")

texts = [
    "The new model is significantly faster and more accurate.",
    "Latency increased after the update. Very disappointed.",
    "Works about the same as before. No complaints.",
]

results = classify_batch(client, texts, model="gemma3:1b")
summary = summarize_results(results)

print(results[["model", "text", "label", "confidence"]].to_string(index=False))
print()
print(f"Total      : {summary['total']}")
print(f"Successful : {summary['successful']}")
print(f"Labels     : {summary['label_counts']}")
print(f"Avg conf   : {summary['avg_confidence']:.0%}")
