# Use a pipeline as a high-level helper
from transformers import pipeline
import random
from transformers import AutoModel
import re
# pipe = pipeline("text-generation", model="succinctly/text2image-prompt-generator")

# pipe.save_model(path="text2image-prompt-generator") 

#model_path = "~/.cache/huggingface/hub/models--succinctly--text2image-prompt-generator/snapshots/b7e96e38b77149daaded8f5101cdc81482330b4b"

model_path = "../../models/text2image-prompt-generator"
#model = AutoModel.from_pretrained(model_path)
pipe = pipeline(
    "text-generation",
    model=model_path,
    #local_files_only=True  # This forces to use cached files only
)

starting_text = "Patagonia"
print(f"Starting text: {starting_text}")
response = pipe(
    starting_text, 
    max_length=random.randint(60, 90), 
    num_return_sequences=8,
    truncation=True  # Add this to address the truncation warning
)

print(response)

response_list = []
for x in response:
    resp = x['generated_text'].strip()
    if resp != starting_text and len(resp) > (len(starting_text) + 4) and resp.endswith((":", "-", "—")) is False:
        response_list.append(resp)

response_end = "\n".join(response_list)
response_end = re.sub('[^ ]+\.[^ ]+','', response_end)
response_end = response_end.replace("<", "").replace(">", "")
# if response_end != "":
#     return response_end
# if count == 5:
#     return response_end

print(response_list)