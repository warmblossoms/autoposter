import os
import sys
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../output")

def generate_caption(product):
    name = product.get("productName", "").strip()
    category = product.get("category", "")
    link = product.get("affiliateLink", "")
    hashtags = product.get("hashtags", "")

    caption = f"""{name}

✨ Best pick in {category}
🔗 Buy now: {link}

{hashtags}

Follow for more 💛
"""

    return caption


def save_caption(productId, caption):
    product_out = os.path.join(OUTPUT_DIR, productId)
    os.makedirs(product_out, exist_ok=True)

    file_path = os.path.join(product_out, "caption.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(caption)

    print("Caption saved to:", file_path)
    return file_path


if __name__ == "__main__":
    input_data = sys.argv[1]
    data = eval(input_data)
    caption = generate_caption(data)
    save_caption(data["productId"], caption)
