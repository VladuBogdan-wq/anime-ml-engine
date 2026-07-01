from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch

model_name = "sentence-transformers/all-MiniLM-L6-v2"
output_dir = Path("./onnx-model")
output_dir.mkdir(exist_ok=True)

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

# Create a dummy input 
dummy_input = tokenizer(
    "sample text for export",
    return_tensors="pt",
    padding="max_length",
    max_length=128,
    truncation=True,
)

print("Exporting to ONNX...")
torch.onnx.export(
    model,
    args=(dummy_input["input_ids"], dummy_input["attention_mask"]),
    f=str(output_dir / "model.onnx"),
    input_names=["input_ids", "attention_mask"],
    output_names=["last_hidden_state"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "last_hidden_state": {0: "batch_size"},
    },
    opset_version=14,
)

tokenizer.save_pretrained(output_dir)

print(f"Done — model and tokenizer saved to {output_dir}/")
print("Files created:")
for f in output_dir.iterdir():
    print(f"  {f.name}")