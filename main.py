import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
import re
import textwrap
from datetime import datetime

# --- PIL & MOVIEPY FIX START (यह एरर को हमेशा के लिए रोकेगा) ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# अगर MoviePy पुराना 'ANTIALIAS' मांगेगा, तो हम उसे नया 'LANCZOS' दे देंगे
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)
# --- PIL & MOVIEPY FIX END ---

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🔓 5-Channel Premium & Safe Machine Started (With PIL Fix)...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

# --- MASTER CHANNEL DICTIONARY ---
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {
        "token": os.environ.get("TOKEN_GBYOUTUBER"),
        "category": "22", "tags": ["bhakti", "radhe radhe", "satsang", "sanatan dharma"],
        "hooks": ["krishna miracle stories", "power of chanting radhe", "karma lessons from geeta"]
    },
    "HEALTH_AYURVEDA": {
        "token": os.environ.get("TOKEN_HEALTH"),
        "category": "26", "tags": ["health tips", "ayurveda", "gharelu nuskhe", "healthy lifestyle"],
        "hooks": ["ayurvedic cure for acidity", "morning habits for extreme energy", "hidden benefits of tulsi"]
    },
    "SUCCESS_BUSINESS": {
        "token": os.environ.get("TOKEN_SUCCESS"),
        "category": "27", "tags": ["business ideas", "motivation", "success tips", "investment hindi"],
        "hooks": ["rich dad poor dad rules", "how to start zero investment business", "chanakya niti for success"]
    },
    "SANATAN_RAHASYA": {
        "token": os.environ.get("TOKEN_SANATAN"),
        "category": "24", "tags": ["sanatan rahasya", "mythology facts", "hinduism", "mahabharat"],
        "hooks": ["unsolved mysteries of kailash", "weapons of mahabharat", "kalki avatar facts"]
    },
    "BOOK_SUMMARIES": {
        "token": os.environ.get("TOKEN_BOOK"),
        "category": "27", "tags": ["book summary hindi", "audiobook hindi", "best books", "self help"],
        "hooks": ["atomic habits summary", "psychology of money lessons", "think and grow rich secrets"]
    }
}

# 🟢 Safe JSON Extractor
def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

# 🟢 Script Generator 
def get_ai_script(channel_name, hook_theme, is_long_video=False):
    print(f"\n✅ {channel_name} ke liye dumdaar script likhi jaa rahi hai... (Long: {is_long_video})")
    word_count = "350-400" if is_long_video else "80-90"
    num_prompts = 12 if is_long_video else 6
    
    prompt = f"""Write a viral Hindi YouTube script for channel type: {channel_name}.
    Topic/Hook: "{hook_theme}".
    LENGTH: Exactly {word_count} words. 
    STYLE: Highly engaging, no boring intros. Direct value.
    ENDING: "ऐसी ही शानदार जानकारी और बेहतरीन प्रोडक्ट्स/किताबों के लिए चैनल सब्सक्राइब करें और डिस्क्रिप्शन में दिया अमेज़न लिंक ज़रूर चेक करें।"
    
    Return ONLY pure JSON:
    {{
      "title": "Viral Clickbait Hindi Title",
      "script": "Full hindi script here...",
      "captions": ["HOOK 1", "FACT 2", "AMAZING", "SUBSCRIBE", "LINK IN BIO", "SHOCKING"],
      "prompts": ["Image 1 prompt", "Image 2 prompt", "Image 3 prompt", "Image 4 prompt", "Image 5 prompt", "Image 6 prompt", "Image 7 prompt", "Image 8 prompt", "Image 9 prompt", "Image 10 prompt", "Image 11 prompt", "Image 12 prompt"]
    }}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                if parsed.get('script'):
                    print("🎯 Script Ready!")
                    return parsed['title'], parsed['script'].replace("*", ""), parsed['prompts'][:num_prompts], parsed['captions']
            else:
                print(f"API Error: {response.text}")
        except Exception as e: 
            print(f"Groq retry {attempt+1}... Error: {e}")
            time.sleep(2)
    raise Exception("🚨 AI Model Failed after 3 retries!")

# 🟢 Safe AI Image Fetcher
def fetch_ai_images(prompts, is_long_video=False):
    print("🎨 Pollinations AI se unique images ban rahi hain...")
    image_files, seed = [], random.randint(1000, 99999)
    headers = {"User-Agent": "Mozilla/5.0"}
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + ', highly detailed, 8k')}?width={w}&height={h}&nologo=true&seed={seed+i}"
        fname = f"ai_scene_{i}.jpg"
        for _ in range(3): 
            try:
                res = requests.get(url, headers=headers, timeout=30) 
                if res.status_code == 200: 
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    break
            except: time.sleep(3)
    return image_files

# 🟢 Human Voice Generator
def create_human_voice(text, filename):
    print("🎙️ AI Voice ban rahi hai...")
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 HUGE Text, Perfect Stroke
def create_centered_text_clip(text, duration, is_long_video):
    canvas_w, canvas_h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try: font = ImageFont.truetype("Roboto-Black.ttf", 130 if not is_long_video else 90)
    except: font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text.upper(), width=15 if not is_long_video else 30) 
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped_text, font=font)
        
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    if is_long_video: y = int(canvas_h * 0.75) 
    
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=8, stroke_fill="black", align='center')
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

# 🟢 Studio Image Fit Magic
def process_image_for_video(img_path, output_path, is_long_video):
    img = Image.open(img_path).convert("RGB")
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    
    bg = img.resize((w, h), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=40))
    
    ratio = w / img.width
    new_h = int(img.height * ratio)
    
    if new_h > h:
        ratio = h / img.height
        new_w = int(img.width * ratio)
        fg = img.resize((new_w, h), Image.Resampling.LANCZOS)
        bg.paste(fg, ((w - new_w) // 2, 0))
    else:
        fg = img.resize((w, new_h), Image.Resampling.LANCZOS)
        bg.paste(fg, (0, (h - new_h) // 2))
        
    bg.save(output_path)
    return output_path

# 🟢 Video Assembler (Fixed)
def make_video(image_files, captions, final_vid, audio_file, is_long_video):
    print("🎬 Professional Video Render ho raha hai...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    
    for i, img_path in enumerate(image_files):
        fixed_img_path = f"fixed_{i}.jpg"
        process_image_for_video(img_path, fixed_img_path, is_long_video)
        
        base_clip = ImageClip(fixed_img_path)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.04 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip() and not is_long_video:
            try:
                txt_clip = create_centered_text_clip(cap_text, time_per_image, is_long_video)
                txt_clip = txt_clip.set_position(('center', 0.65), relative=True) 
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(w, h)).set_duration(time_per_image)
            except Exception as e: 
                print(f"Text clip error (ignored): {e}")
                final_clip = zoomed_clip
        else: final_clip = zoomed_clip
        
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

# 🟢 Safe Uploader
def upload_video(token, filename, title, description, tags, category):
    print("🚀 YouTube par Upload ho raha hai...")
    for attempt in range(3):
        try:
            creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
            youtube = build("youtube", "v3", credentials=creds)
            request = youtube.videos().insert(
                part="snippet,status",
                body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
                media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
            )
            request.execute()
            print("✅ Upload Success!")
            return
        except Exception as e:
            print(f"Upload fail, retrying... Error: {e}")
            time.sleep(10)

# 🟢 5-Channel Master Runner
def run_network():
    current_hour = datetime.utcnow().hour
    is_long_video = True if current_hour in [17, 18, 19] else False
    print(f"\n⚙️ Network Mode: {'LONG VIDEO' if is_long_video else 'SHORTS'}")
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)

    for ch_name in channels:
        for attempt in range(3): 
            try:
                config = CHANNELS_CONFIG[ch_name]
                if not config["token"]: break
                
                hook = random.choice(config["hooks"])
                title, script, prompts, captions = get_ai_script(ch_name, hook, is_long_video)
                image_files = fetch_ai_images(prompts, is_long_video)
                create_human_voice(script, "temp_voice.mp3")
                
                out_file = f"{ch_name}_final.mp4"
                make_video(image_files, captions, out_file, "temp_voice.mp3", is_long_video)
                
                final_title = f"{title}" if is_long_video else f"{title[:70]} #shorts"
                final_desc = f"🔥 बेहतरीन किताबें और ज़रूरी प्रोडक्ट्स यहाँ से खरीदें: https://www.amazon.in/?tag=girishbhut07-21\n\n{script}"
                
                upload_video(config["token"], out_file, final_title, final_desc, config["tags"], config["category"])
                print(f"✅ {ch_name} Completed!")
                
                delay = random.randint(300, 600)
                print(f"⏳ Agle channel ke liye {delay/60:.1f} minute ka wait...\n")
                time.sleep(delay)
                break 
                
            except Exception as e:
                print(f"🛑 {ch_name} me Error: {e}. Machine dobara koshish kar rahi hai...")
                time.sleep(10)

if __name__ == "__main__":
    run_network()
