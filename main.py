import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime

# --- PIL & MOVIEPY FIX (एरर रोकने के लिए) ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🚀 V8 Final Master Machine: 100% Human Voice, Perfect Big Text & Real Images Active...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 🟢 100% GUARANTEED FONT DOWNLOADER (ताकि अक्षर कभी छोटे न हों)
font_path = "Roboto-Black.ttf"
if not os.path.exists(font_path) or os.path.getsize(font_path) < 10000:
    print("📥 शानदार फॉन्ट डाउनलोड हो रहा है...")
    try:
        r = requests.get("https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")
        with open(font_path, "wb") as f: f.write(r.content)
    except Exception as e:
        print("Font Download Error:", e)

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# --- MASSIVE VARIETY CHANNELS CONFIG ---
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna", "sanatan"], "hooks": ["श्री कृष्ण का सबसे बड़ा चमत्कार", "गीता का वह ज्ञान जो जीवन बदल दे", "महाभारत का अनसुना रहस्य", "भगवान शिव का भयंकर क्रोध"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda", "fitness"], "hooks": ["एसिडिटी का 1 मिनट में जड़ से इलाज", "आयुर्वेद के 3 सबसे गुप्त नियम", "वजन घटाने का चमत्कारी नुस्खा", "सुबह जल्दी उठने के जादुई फायदे"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation", "money"], "hooks": ["रतन टाटा के सफलता के 5 नियम", "0 इन्वेस्टमेंट से करोड़पति कैसे बनें", "गरीबी से अमीरी का सीधा रास्ता", "चाणक्य नीति जो आपको सफल बनाएगी"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology", "history"], "hooks": ["कैलाश पर्वत का अनसुलझा और डरावना रहस्य", "अश्वत्थामा आज भी कहाँ भटक रहे हैं", "कलयुग का अंत कैसे और कब होगा", "समुद्र मंथन का असली सच"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary", "knowledge"], "hooks": ["Atomic Habits: आदतें कैसे बदलें", "Rich Dad Poor Dad की सबसे बड़ी सीख", "Think and Grow Rich: अमीर बनने का सीक्रेट", "Power of Subconscious Mind का जादू"]}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"📝 {channel_name} के लिए दमदार और ज्ञानवर्धक कहानी लिखी जा रही है: {hook_theme}")
    word_limit = "350-400" if is_long_video else "85-95"
    scene_count = 15 if is_long_video else 8
    
    prompt = f"""Write a viral, engaging Hindi script for {channel_name} on the theme "{hook_theme}".
    Length: Strictly between {word_limit} words.
    
    CRITICAL VOICE & EMOTION RULES (FOR NATURAL HUMAN TTS):
    1. You MUST use heavy punctuation to force natural pauses in the AI voice.
    2. Use commas (,) for short breaths, periods (.) for full stops, and ellipses (...) for deep suspenseful pauses.
    3. Use question marks (?) for curiosity and exclamation marks (!) for excitement.
    4. Make it sound like a passionate human storyteller narrating a thrilling tale.
    
    CRITICAL STORY RULES:
    1. DO NOT ask "Kya aap jante hain". Start with a shocking fact or a highly inspiring story immediately.
    2. Tell a real, engaging narrative. Make the viewer want to stay till the end.
    3. END EXACTLY WITH: "सब्सक्राइब करें और बायो में लिंक देखें।"
    
    CRITICAL VISUAL RULES (STRICT MATCHING):
    1. The 'prompt' for the image MUST EXACTLY MATCH the spoken 'text'.
    2. If speaking about a rich businessman, the prompt MUST say "Successful rich businessman in suit, cinematic". 
    3. If speaking about Lord Krishna, the prompt MUST say "Beautiful divine Lord Krishna, highly symmetric face, glowing". 
    4. NO SAD, WEAK, OR UGLY FACES. Everything must be Epic, Positive, and High Quality.
    
    CRITICAL CAPTION RULES:
    - Provide exactly 1 to 3 ENGLISH words as a caption for EVERY scene (e.g., "SHOCKING TRUTH", "DIVINE POWER"). MUST BE IN ENGLISH ROMAN LETTERS.

    Return ONLY JSON:
    {{
      "title": "Viral Clickbait Title",
      "scenes": [
        {{
          "text": "Hindi spoken sentence with lots of commas, pauses..., and emotion!...", 
          "caption": "SHORT ENGLISH CAPTION", 
          "prompt": "Epic highly detailed cinematic image prompt matching the text exactly"
        }},
        ...
      ]
    }}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    
    for attempt in range(3):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60)
            if res.status_code == 200:
                parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
                if parsed.get('scenes'):
                    return parsed
        except Exception as e:
            print(f"Groq retry {attempt+1}... Error: {e}")
            time.sleep(2)
    raise Exception("🚨 AI Model Failed after 3 retries!")

def download_single_image(idx, p, w, h):
    # सीक्रेट प्रॉम्प्ट: हमेशा सुन्दर और सिनेमैटिक तस्वीरें ही बनेंगी
    enhanced_prompt = p + ", ultra-realistic, cinematic lighting, vivid colors, masterpiece, highly detailed, perfect divine faces, 8k resolution"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}?width={w}&height={h}&nologo=true&seed={random.randint(10000,99999)}"
    fname = f"scene_{idx}.jpg"
    
    for attempt in range(4):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(fname, "wb") as f: f.write(r.content)
                try:
                    Image.open(fname).verify() 
                    return fname
                except: pass
        except: pass
        time.sleep(2)
    return None

def fetch_all_images_safe(scenes, is_long_video):
    print("🎨 एकदम सही और शानदार तस्वीरें डाउनलोड हो रही हैं...")
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    valid_images, valid_scenes = [], []
    for i, s in enumerate(scenes):
        img_path = download_single_image(i, s['prompt'], w, h)
        if img_path:
            valid_images.append(img_path)
            valid_scenes.append(s)
        time.sleep(1)
    if len(valid_images) == 0: raise Exception("Images failed.")
    return valid_images, valid_scenes

async def create_voice(text, filename):
    # 🟢 100% NATURAL VOICE (Speed Normal +0%, No Robot Sound)
    print("🎙️ इंसानों जैसी सस्पेंस वाली आवाज़ बन रही है...")
    comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+0%")
    await comm.save(filename)

def create_text_clip(caption_text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 🟢 HUGE FONT SIZE (शॉर्ट्स के लिए 160)
    font_size = 120 if is_long_video else 160
    try: font = ImageFont.truetype("Roboto-Black.ttf", font_size)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(caption_text.upper(), width=30 if is_long_video else 14)
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped, font=font)
        
    x = (w - text_w) // 2
    # 🟢 PERFECT POSITION (70% नीचे ताकि फोटो भी दिखे और टेक्स्ट भी)
    y = int(h * 0.85) if is_long_video else int(h * 0.70) 
    
    # 🟢 THICK STROKE FOR VISIBILITY
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", align='center')
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print("🎬 वीडियो रेंडरिंग (Pro Viral Mode)...")
    main_audio = AudioFileClip(audio_file)
    dur_per_scene = main_audio.duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        img = Image.open(img_path).convert("RGB")
        w, h = (1920, 1080) if is_long_video else (1080, 1920)
        
        bg = img.resize((w, h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
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
            
        proc_name = f"proc_{i}.jpg"
        bg.save(proc_name)
        
        base = ImageClip(proc_name).set_duration(dur_per_scene)
        zoom = base.resize(lambda t: 1 + 0.04 * (t/dur_per_scene))
        
        txt = create_text_clip(scenes[i].get('caption', ''), dur_per_scene, is_long_video)
        clips.append(CompositeVideoClip([zoom.set_position('center'), txt.set_position(('center', 'top'))]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    main_audio.close()
    final.close()

def upload(token, fname, title, desc, tags, cat):
    print("🚀 YouTube पर अपलोड हो रहा है...")
    for _ in range(3):
        try:
            creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
            service = build("youtube", "v3", credentials=creds)
            service.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": cat}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(fname, chunksize=-1, resumable=True)).execute()
            return
        except Exception as e:
            print(f"Upload failed: {e}. Retrying...")
            time.sleep(10)
    raise Exception("Upload completely failed.")

def run():
    hour = (datetime.utcnow().hour + 5) % 24 
    # शाम 6:30 बजे (IST) के आस-पास लॉन्ग वीडियो मोड चालू होगा
    is_long = True if hour in [18, 19] else False 
    
    print(f"⚙️ Network Mode: {'LONG (5-10 Mins)' if is_long else 'SHORTS (40-50 Sec)'}")
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    
    for ch_name in channels:
        cfg = CHANNELS_CONFIG[ch_name]
        for attempt in range(3):
            try:
                data = get_scene_script(ch_name, random.choice(cfg['hooks']), is_long)
                imgs, valid_scenes = fetch_all_images_safe(data['scenes'], is_long)
                
                full_text = " ".join([s['text'] for s in valid_scenes])
                asyncio.run(create_voice(full_text, "v.mp3"))
                
                out_file = f"{ch_name}_final.mp4"
                assemble_video(imgs, valid_scenes, out_file, "v.mp3", is_long)
                
                title = data['title'] if is_long else f"{data['title'][:70]} #shorts"
                desc = f"बेहतरीन प्रोडक्ट्स खरीदें यहाँ से: https://www.amazon.in/?tag=girishbhut07-21\n\n{full_text}"
                upload(cfg['token'], out_file, title, desc, cfg['tags'], cfg['category'])
                
                print(f"✅ {ch_name} डन!")
                time.sleep(30)
                break 
            except Exception as e: 
                print(f"❌ Error in {ch_name} (Attempt {attempt+1}): {e}")
                time.sleep(10)

if __name__ == "__main__": run()
