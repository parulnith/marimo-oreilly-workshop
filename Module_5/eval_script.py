from sentiment_classifier import compare_two_models, get_client

client = get_client(base_url="http://localhost:11434/v1")

texts = [
    "The new model is significantly faster and more accurate.",
    "Latency increased after the update. Very disappointed.",
    "Works about the same as before. No complaints.",
]

results = compare_two_models(client, texts, model_a="gemma3:1b", model_b="qwen2.5:0.5b")

print(results[["model", "text", "label", "confidence"]].to_string(index=False))
print()
print(f"Total rows : {len(results)}")
print(f"Errors     : {(results['label'] == 'error').sum()}")
print(f"Avg conf   : {results.loc[results['label'] != 'error', 'confidence'].mean():.0%}")
