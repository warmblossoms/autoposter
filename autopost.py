import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Load credentials from GitHub Secrets OR local environment
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

if not creds_json:
    print("❌ GOOGLE_CREDENTIALS_JSON not found")
    exit()

# Convert JSON string into dict
creds_dict = eval(creds_json)

# Define required Google API scopes
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
gc = gspread.authorize(creds)

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

print("✅ Connected to Google Sheet successfully!")

# Read all rows
rows = sheet.get_all_records()
print(f"📋 Total products found: {len(rows)}")

import random

# Function to generate SEO title
def generate_title(product_name):
    templates = [
        f"Top Benefits of Using {product_name} in India 🇮🇳",
        f"{product_name}: Must-Have Product for Indian Beauty Lovers ✨",
        f"Transform Your Look with {product_name}! 💖",
        f"Why Indians are Loving {product_name} 😍",
        f"{product_name} Review: Worth Buying? 🔥"
    ]
    return random.choice(templates)

# Function to generate SEO description
def generate_description(product_name, affiliate_link):
    return (
        f"Discover why everyone is talking about {product_name}! ✨\n"
        f"Affordable, effective & trending beauty essential in India 🇮🇳\n\n"
        f"Buy Now 👉 {affiliate_link}\n"
        f"#BeautyProducts #TrendingIndia #SkincareIndia"
    )

# Function to generate ALT text for Pinterest
def generate_alt_text(product_name):
    return f"Aesthetic product image of {product_name} for beauty lovers in India."

# Function to generate Hashtags
def generate_hashtags():
    tags = [
        "#TrendingInIndia", "#BeautyFinds", "#ViralProducts",
        "#AffordableBeauty", "#MustHave", "#SkinCareIndia",
        "#MakeupIndia", "#HairCareIndia", "#FashionFinds"
    ]
    random.shuffle(tags)
    return " ".join(tags[:7])

# Function to generate reel script text
def generate_reel_script(product_name):
    return (
        f"{product_name} Review 🌸\n"
        f"✨ Benefits\n"
        f"😍 Results\n"
        f"📌 Swipe Up to Shop!"
    )
import requests

def download_images(row):
    image_files = []
    for i in range(1, 6):
        img_url = row.get(f"image_{i}_url")
        if img_url:
            try:
                response = requests.get(img_url, stream=True)
                file_path = f"/tmp/{row['id']}_{i}.jpg"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                image_files.append(file_path)
            except Exception as e:
                print(f"❌ Failed to download image {i}: {e}")
    return image_files
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
import uuid

def create_reel(image_files, title_text):
    clips = []

    for img in image_files:
        try:
            img_clip = ImageClip(img).set_duration(2.0)
            img_clip = img_clip.resize(height=1920).set_position(("center", "center"))
            clips.append(img_clip)
        except Exception as e:
            print(f"❌ Error creating clip: {e}")

    if not clips:
        print("❌ No valid images to create video")
        return None

    final_clip = concatenate_videoclips(clips, method="compose")

    # Add Title Text Overlay
    text_clip = TextClip(
        title_text,
        fontsize=70,
        color='white',
        stroke_color='black',
        stroke_width=3,
        method='caption',
        font='Arial'
    ).set_position(('center', 140)).set_duration(final_clip.duration)

    composite = CompositeVideoClip([final_clip, text_clip])

    video_path = f"/tmp/reel_{uuid.uuid4().hex}.mp4"
    composite.write_videofile(video_path, fps=24, codec="libx264", audio=False)

    return video_path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path, file_name):
    drive_service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)

    file_metadata = {
        'name': file_name,
        'mimeType': 'video/mp4'
    }

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    file_id = uploaded_file.get("id")

    # Make file public
    drive_service.permissions().create(
        fileId=file_id,
        body={'role': 'reader', 'type': 'anyone'}
    ).execute()

    link = f"https://drive.google.com/file/d/{file_id}/preview"
    print("📤 Uploaded Video URL:", link)

    return link


def update_sheet(row_index, column, value):
    sheet.update_cell(row_index, column, value)
    print(f"➡️ Updated row {row_index}, column {column}")
def process_products():
    rows = sheet.get_all_records()
    for index, row in enumerate(rows, start=2):  # row 2 = first product
        status = row.get("status", "").lower()

        if status != "pending" and status != "":
            continue  # skip if already generated

        print(f"📌 Processing product row {index}")

        product_name = row.get("product_name")
        affiliate_link = row.get("affiliate_link")

        # Generate SEO content
        title = generate_title(product_name)
        desc = generate_description(product_name, affiliate_link)
        alt_text = generate_alt_text(product_name)
        hashtags = generate_hashtags()
        reel_script = generate_reel_script(product_name)

        # Download Images
        image_files = download_images(row)
        if not image_files:
            print("❌ No images found... skipping product!")
            continue

        # Create Reel Video
        video_path = create_reel(image_files, title)
        if not video_path:
            print("❌ Could not create video... skipping product!")
            continue

        # Upload video to Google Drive
        video_link = upload_to_drive(video_path, f"{product_name}.mp4")

        # Update Google Sheet
        update_sheet(index, 12, title)        # generated_title
        update_sheet(index, 13, desc)         # generated_description
        update_sheet(index, 14, alt_text)     # generated_alt
        update_sheet(index, 15, hashtags)     # hashtags
        update_sheet(index, 16, reel_script)  # reel_script
        update_sheet(index, 17, video_link)   # video_drive_links
        update_sheet(index, 2, "ready")       # status = ready

        print(f"✨ Product updated Successfully!")

    print("🎯 All pending products processed!")


if __name__ == "__main__":
    process_products()
