import os
import sys
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../output")

def generate_blog(product):
    name = product.get("productName", "").strip()
    category = product.get("category", "")
    desc = product.get("description", "")
    link = product.get("affiliateLink", "")
    hashtags = product.get("hashtags", "")

    keywords = ", ".join(["#" + h.strip("#") for h in hashtags.split()][:6])

    blog_md = f"""
# {name} – Honest Review ({datetime.now().year})

Are you struggling with {category.lower()} concerns and looking for something that **actually works**?  
🛍️ **{name}** might be the solution you've been waiting for!

---

## What is {name}?

{desc}

👉 **Category:** {category}  
👉 **Where to Buy:** [{name}]({link})

---

## Features 🧪 + Benefits 💛

- Helps improve your {category.lower()}
- Made for daily use
- Versatile and beginner-friendly
- Value for money
- Recommended by many users

---

## How to Use

Use {name} consistently to see visible results.  
Follow the instructions on the product packaging for best results.

---

## Pros & Cons

| Pros | Cons |
|------|------|
| Effective results | Results may vary |
| Easy to apply/use | May not suit everyone |
| Affordable | Requires consistent usage |
| Available online | Stock issues sometimes |

---

## FAQs ❓

**Is it safe for all skin/hair types?**  
Yes, generally suitable — but patch test recommended.

**How long does it take to show results?**  
Varies person to person — usually a few weeks of consistent usage.

**Is it beginner-friendly?**  
Absolutely yes!

---

## ⭐ Final Verdict

If you're dealing with {category.lower()} issues and want **real change**, {name} is definitely worth a try.

🛒 **Buy Now / Check Price Here:**  
👉 {link}

---

## Keywords used for SEO
{keywords}

*Written by {datetime.now().strftime('%B %Y')} Affiliate Team*
"""
    return blog_md


def save_blog(productId, blog_md):
    product_out = os.path.join(OUTPUT_DIR, productId)
    os.makedirs(product_out, exist_ok=True)

    md_path = os.path.join(product_out, "blog.md")
    html_path = os.path.join(product_out, "blog.html")

    # Save Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(blog_md)

    # Convert to HTML
    html_content = blog_md.replace("\n", "<br>")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Blog saved as:", md_path, "and", html_path)
    return md_path, html_path


if __name__ == "__main__":
    input_data = sys.argv[1]
    data = eval(input_data)
    blog_md = generate_blog(data)
    save_blog(data["productId"], blog_md)
