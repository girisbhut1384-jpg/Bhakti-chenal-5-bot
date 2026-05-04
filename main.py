import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime

# --- PIL & MOVIEPY FIX ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🔓 Security aur Premium Setup chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 100% Pukka Font Downloader (For MASSIVE Text)
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

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

# --- 5 CHANNELS CONFIGURATION ---
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna", "sanatan", "shorts"], "hooks": ["श्री कृष्ण का सबसे बड़ा चमत्कार", "गीता का वह ज्ञान जो जीवन बदल दे", "महाभारत का अनसुना रहस्य", "भगवान शिव का भयंकर क्रोध"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda", "fitness", "shorts"], "hooks": ["एसिडिटी का 1 मिनट में जड़ से इलाज", "आयुर्वेद के 3 सबसे गुप्त नियम", "वजन घटाने का चमत्कारी नुस्खा", "सुबह जल्दी उठने के जादुई फायदे"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation", "money", "shorts"], "hooks": ["रतन टाटा के सफलता के 5 नियम", "0 इन्वेस्टमेंट से करोड़पति कैसे बनें", "गरीबी से अमीरी का सीधा रास्ता", "चाणक्य नीति जो आपको सफल बनाएगी"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology", "history", "shorts"], "hooks": ["कैलाश पर्वत का अनसुलझा और डरावना रहस्य", "अश्वत्थामा आज भी कहाँ भटक रहे हैं", "कलयुग का अंत कैसे और कब होगा", "समुद्र मंथन का असली सच"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary", "knowledge", "shorts"], "hooks": ["Atomic Habits: आदतें कैसे बदलें", "Rich Dad Poor Dad की सबसे बड़ी सीख", "Think and Grow Rich: अमीर बनने का सीक्रेट", "Power of Subconscious Mind का जादू"]}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"\n✅ AI Engine दमदार स्क्रिप्ट लिख रहा है: {hook_theme}")
    word_limit = "350-400" if is_long_video else "85-95"
    scene_count = 15 if is_long_video else 8
    
    prompt = f"""Write a viral Hindi script for {channel_name}. THEME: "{hook_theme}".
    Length: Strictly between {word_limit} words.
    
    RULES:
    1. NO INTRODUCTIONS. START DIRECTLY WITH A SHOCKING HOOK!
    2. Tell a deep, real story or fact. NO boring questions.
    3. Use commas (,) and ellipses (...) for dramatic AI voice pauses.
    4. END EXACTLY WITH: 'सब्सक्राइब करें और बायो में अमेज़न लिंक देखें।'
    
    VISUAL RULES (STRICT MATCHING):
    1. Visuals MUST strictly match the story.
    2. For Hindu gods, use: "Extremely beautiful divine face, highly detailed masterpiece, glowing". NO UGLY FACES.
    3. Ensure {scene_count} logical visual scenes.
    
    CAPTION RULES:
    Provide exactly 1 to 3 ENGLISH words as a caption for EVERY scene (e.g., "SHOCKING", "DIVINE TRUTH"). MUST BE ENGLISH.

    Return ONLY JSON:
    {{
      "title": "Viral Clickbait Hindi Title",
      "scenes": [
        {{
          "text": "Hindi spoken sentence...", 
          "caption": "SHORT ENGLISH CAPTION", 
          "prompt": "Epic highly detailed cinematic image prompt matching the text"
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
                    print("🎯 Script Ready!")
                    return parsed
        except Exception as e:
            time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

def download_single_image(idx, p, w, h):
    # आपके पुराने कोड की तरह बेस्ट इमेज जनरेटर प्रॉम्प्ट
    enhanced_prompt = p + ", highly detailed, masterpiece, 8k, cinematic, extremely beautiful"
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
    print("🎨 शानदार और पक्की तस्वीरें डाउनलोड हो रही हैं...")
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

def create_human_voice(text, filename):
    print("🎙️ एकदम शानदार आवाज़ बन रही है (+10% Speed)...")
    async def _generate():
        for _ in range(3):
            try:
                # आपके पुराने कोड वाली परफेक्ट स्पीड (+10%)
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 HUGE Text, Perfect Stroke, Center Bottom (आपके पुराने कोड का अपडेटेड वर्ज़न)
def create_text_clip(caption_text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # बहुत बड़ा फॉन्ट (शॉर्ट्स में 180, लॉन्ग में 130)
    font_size = 130 if is_long_video else 180
    try: font = ImageFont.truetype("Roboto-Black.ttf", font_size)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(caption_text.upper(), width=30 if is_long_video else 12)
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped, font=font)
        
    x = (w - text_w) // 2
    # गोल्डन पोजीशन: एकदम बीच से थोड़ा नीचे (ताकि फोटो और टेक्स्ट दोनों साफ़ दिखें)
    y = int(h * 0.85) if is_long_video else int(h * 0.65) 
    
    # पीला टेक्स्ट और 12 पिक्सेल का बहुत मोटा काला बॉर्डर
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", align='center')
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

# 🟢 Studio Image Fit (Blur Background Magic - आपके पुराने कोड से)
def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print("🎬 Professional Video Render ho raha hai...")
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
        # Text clip me position already set hai, to bas overlay karna hai
        clips.append(CompositeVideoClip([zoom.set_position('center'), txt.set_position(('center', 'center'))]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(output_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    main_audio.close()
    final.close()

def upload_video(token, filename, title, description, tags, category):
    print("🚀 YouTube par Upload ho raha hai...")
    for _ in range(3):
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
    raise Exception("Upload completely failed.")

def run_network():
    hour = (datetime.utcnow().hour + 5) % 24 
    # शाम 6:30 बजे (IST) के आस-पास लॉन्ग वीडियो मोड चालू होगा
    is_long = True if hour in [18, 19] else False 
    
    print(f"\n⚙️ Network Mode: {'LONG (5-10 Mins)' if is_long else 'SHORTS (35-45 Sec)'}")
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    
    for ch_name in channels:
        cfg = CHANNELS_CONFIG[ch_name]
        for attempt in range(3):
            try:
                data = get_scene_script(ch_name, random.choice(cfg['hooks']), is_long)
                imgs, valid_scenes = fetch_all_images_safe(data['scenes'], is_long)
                
                full_text = " ".join([s['text'] for s in valid_scenes])
                create_human_voice(full_text, "v.mp3")
                
                out_file = f"{ch_name}_final.mp4"
                assemble_video(imgs, valid_scenes, out_file, "v.mp3", is_long)
                
                title = data['title'] if is_long else f"{data['title'][:70]} #shorts"
                desc = f"🔥 बेहतरीन प्रोडक्ट्स खरीदें यहाँ से: https://www.amazon.in/?tag=girishbhut07-21\n\n{full_text}"
                upload_video(cfg['token'], out_file, title, desc, cfg['tags'], cfg['category'])
                
                print(f"✅ {ch_name} Video Live!")
                time.sleep(30)
                break 
            except Exception as e: 
                print(f"🛑 Error in {ch_name} (Attempt {attempt+1}): {e}")
                time.sleep(10)

if __name__ == "__main__": 
    run_network()
