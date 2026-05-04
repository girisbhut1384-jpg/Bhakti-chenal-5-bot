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

print("🚀 V7 Master Machine: HUGE Text, Massive Variety & Pro Story Mode Active...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

# 100% पक्का फॉन्ट डाउनलोडर (ताकि अक्षर कभी छोटे न हों)
if not os.path.exists("Roboto-Black.ttf") or os.path.getsize("Roboto-Black.ttf") < 10000:
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# --- MASSIVE VARIETY CHANNELS CONFIG (हर चैनल के लिए 10+ नए टॉपिक) ---
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna", "sanatan"], "hooks": ["श्री कृष्ण का सबसे बड़ा चमत्कार", "गीता का वह ज्ञान जो जीवन बदल दे", "महाभारत का अनसुना रहस्य", "भगवान शिव का भयंकर क्रोध", "हनुमान जी की असली शक्ति", "रामायण का सबसे बड़ा राज", "कर्म का असली सिद्धांत", "स्वर्ग और नर्क का सच", "कलयुग की डरावनी भविष्यवाणियां", "भगवान विष्णु के अवतार"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda", "fitness"], "hooks": ["एसिडिटी का 1 मिनट में जड़ से इलाज", "आयुर्वेद के 3 सबसे गुप्त नियम", "वजन घटाने का चमत्कारी नुस्खा", "सुबह जल्दी उठने के जादुई फायदे", "चेहरे पर चमक लाने का तरीका", "बालों का झड़ना हमेशा के लिए रोकें", "हड्डियों को लोहे जैसा मजबूत कैसे बनाएं", "नींद न आने का अचूक आयुर्वेदिक उपाय", "गर्म पानी पीने के खतरनाक फायदे", "डायबिटीज का घरेलू इलाज"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation", "money"], "hooks": ["रतन टाटा के सफलता के 5 नियम", "0 इन्वेस्टमेंट से करोड़पति कैसे बनें", "गरीबी से अमीरी का सीधा रास्ता", "चाणक्य नीति जो आपको सफल बनाएगी", "धीरूभाई अंबानी की सीक्रेट कहानी", "शेयर मार्केट का कड़वा सच", "पैसे से पैसा बनाने की ट्रिक", "सफल लोगों की 3 सबसे बड़ी आदतें", "टाइम मैनेजमेंट का सबसे बड़ा सीक्रेट", "जॉब छोड़कर बिज़नेस कैसे शुरू करें"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology", "history"], "hooks": ["कैलाश पर्वत का अनसुलझा और डरावना रहस्य", "अश्वत्थामा आज भी कहाँ भटक रहे हैं", "कलयुग का अंत कैसे और कब होगा", "समुद्र मंथन का असली सच", "रावण का शव आज भी कहाँ रखा है", "द्वारका नगरी के डूबने का रहस्य", "महाभारत के 3 सबसे घातक अस्त्र", "ब्रह्मास्त्र की असली ताकत", "पाताल लोक कहाँ है", "नाग लोक की सच्ची और खौफनाक कहानी"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary", "knowledge"], "hooks": ["Atomic Habits: आदतें कैसे बदलें", "Rich Dad Poor Dad की सबसे बड़ी सीख", "Think and Grow Rich: अमीर बनने का सीक्रेट", "Power of Subconscious Mind का जादू", "The Secret किताब का खतरनाक सच", "48 Laws of Power (सत्ता के नियम)", "Deep Work: फोकस कैसे बढ़ाएं", "Psychology of Money (पैसे का मनोविज्ञान)", "How to Win Friends की शानदार सीख", "Ego is the Enemy का सारांश"]}
}

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"📝 {channel_name} के लिए दमदार और ज्ञानवर्धक कहानी लिखी जा रही है: {hook_theme}")
    word_limit = "380-420" if is_long_video else "95-105"
    scene_count = 15 if is_long_video else 8
    
    prompt = f"""Write a viral, extremely engaging Hindi script for {channel_name} on the theme "{hook_theme}".
    Length: Strictly between {word_limit} words.
    
    CRITICAL STORY RULES (VIRAL RETENTION):
    1. Tell a gripping story or share a mind-blowing fact. NEVER ask empty questions like "Kya aap jante hain". Provide real, deep knowledge!
    2. Start with a 3-second extremely shocking hook.
    3. Make the narrative fast-paced, powerful, and mysterious or inspiring (depending on channel).
    4. END EXACTLY WITH: "सब्सक्राइब करें और बायो में लिंक देखें।"
    
    CRITICAL VISUAL RULES:
    1. If the topic is Hindu Gods, use "extremely beautiful face, highly symmetric, divine glowing aura, ultra-realistic masterpiece".
    2. Ensure exactly {scene_count} logical visual scenes.
    
    CRITICAL CAPTION RULES:
    - Provide exactly 1 to 3 ENGLISH words as a caption for EVERY scene (e.g., "SHOCKING TRUTH", "DIVINE POWER", "SECRET UNVEILED"). MUST BE IN ENGLISH ROMAN LETTERS.

    Return ONLY JSON:
    {{
      "title": "Viral Clickbait Title",
      "scenes": [
        {{
          "text": "Hindi spoken sentence delivering a fact/story...", 
          "caption": "SHORT ENGLISH CAPTION", 
          "prompt": "Epic highly detailed cinematic image prompt in English"
        }},
        ...
      ]
    }}"""

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                        headers={"Authorization": f"Bearer {GROQ_KEY}"},
                        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.75})
    match = re.search(r'\{[\s\S]*\}', res.json()['choices'][0]['message']['content'])
    if not match: raise Exception("Invalid JSON from Groq")
    return json.loads(match.group(0))

def download_single_image(idx, p, w, h):
    # सीक्रेट कोड: 100% सुन्दर, सिनेमैटिक और हाई-क्वालिटी तस्वीरें
    enhanced_prompt = p + ", ultra-realistic, cinematic lighting, masterpiece, perfectly beautiful, divine, 8k resolution"
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
    print("🎨 हाई-क्वालिटी और बेहद सुन्दर तस्वीरें डाउनलोड हो रही हैं...")
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
    comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%")
    await comm.save(filename)

def create_text_clip(caption_text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 🟢 HUGE FONT SIZE (शॉर्ट्स में 180 साइज़, लॉन्ग में 120)
    font_size = 120 if is_long_video else 180
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
    
    # 🟢 PERFECT POSITION: एकदम बीच में नहीं, बल्कि नीचे की तरफ!
    if is_long_video:
        y = int(h * 0.85) # लॉन्ग वीडियो में एकदम नीचे सबटाइटल
    else:
        y = int(h * 0.70) # शॉर्ट्स में चेहरे से नीचे, ताकि फोटो भी दिखे और टेक्स्ट भी
    
    # Yellow text with super thick black stroke
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", align='center')
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print("🎬 वीडियो रेंडरिंग (Huge Text & Hollywood Mode)...")
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
        # Text is already positioned internally, just overlay it
        clips.append(CompositeVideoClip([zoom.set_position('center'), txt.set_position(('center', 'top'))]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    main_audio.close()
    final.close()

def upload(token, fname, title, desc, tags, cat):
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
    is_long = True if hour in [18, 19] else False 
    
    print(f"⚙️ Network Mode: {'LONG (5-10 Mins)' if is_long else 'SHORTS (35-45 Sec)'}")
    
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
