import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime, timedelta

# --- PIL & MOVIEPY FIX ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import urllib.request

print("🚀 V18 Viral Machine: Hindi Font Fixed, Sharp Focus Images & Unique Stories Active!")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

# 🟢 डब्बों (Boxes) का 100% पक्का इलाज: स्पेशल हिंदी फॉन्ट
font_path = "NotoSansDevanagari-Bold.ttf"
if not os.path.exists(font_path) or os.path.getsize(font_path) < 20000:
    print("📥 विशालकाय हिंदी फॉन्ट डाउनलोड हो रहा है...")
    try:
        urllib.request.urlretrieve("https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf", font_path)
    except Exception as e: pass

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# 🟢 धुंधली फोटो का इलाज: Ultra-sharp focus और UHD कमांड
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna"], "style": "wide angle shot, highly detailed, ultra-sharp focus, photorealistic mythological scenery, UHD, masterpiece", "hooks": ["श्री कृष्ण का सबसे बड़ा चमत्कार", "गीता का असली ज्ञान", "महाभारत का डरावना रहस्य"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda"], "style": "wide angle shot, ultra-sharp focus, photorealistic natural environment, UHD, highly detailed", "hooks": ["एसिडिटी का 1 मिनट में जड़ से इलाज", "आयुर्वेद के 3 सबसे गुप्त नियम", "गर्म पानी पीने के खतरनाक फायदे"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation"], "style": "wide angle corporate environment, ultra-sharp focus, photorealistic, UHD, highly detailed", "hooks": ["रतन टाटा के सफलता के 5 नियम", "0 इन्वेस्टमेंट से करोड़पति कैसे बनें", "चाणक्य नीति"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology"], "style": "wide angle dark cinematic environment, ultra-sharp focus, ancient ruins, photorealistic, UHD", "hooks": ["कैलाश पर्वत का अनसुलझा रहस्य", "अश्वत्थामा आज भी कहाँ हैं", "समुद्र मंथन का असली सच"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary"], "style": "cinematic wide angle shot, ultra-sharp focus, inspiring environment, photorealistic, UHD", "hooks": ["Atomic Habits: आदतें कैसे बदलें", "Rich Dad Poor Dad की असली सीख", "Power of Subconscious Mind"]}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"\n📝 {channel_name} के लिए एक बिल्कुल नई और अनोखी कहानी खोजी जा रही है...")
    word_limit = "400-450" if is_long_video else "125-140"
    scene_count = 15 if is_long_video else 6

    prompt = f"""You are an expert viral scriptwriter for the YouTube channel '{channel_name}'.
    THEME: "{hook_theme}".
    Length: Exactly {word_limit} words.

    CRITICAL INSTRUCTIONS (FOR VIRAL CONTENT):
    1. NEVER REPEAT PREVIOUS STORIES. Always find a brand new, shocking, and untold specific fact or historical event related to the theme.
    2. NO FLUFF. No generic motivational advice. Give pure, hard facts and real names.
    3. The image 'prompt' MUST start with "Wide angle shot, ultra-sharp focus" to ensure crisp images.
    4. Provide long, detailed Hindi sentences for each scene.
    5. End exactly with: 'ऐसी ही अद्भुत जानकारी के लिए चैनल को अभी सब्सक्राइब करें।'
    
    JSON STRUCTURE EXAMPLE:
    {{
      "title": "Viral Clickbait Title",
      "scenes": [
        {{
          "text": "एक अनोखी और चौंकाने वाली कहानी यहाँ लिखें...", 
          "caption": "SHOCKING", 
          "prompt": "Wide angle shot, ultra-sharp focus, [Subject description], highly detailed environment"
        }}
      ]
    }}
    
    Provide exactly {scene_count} scenes following the JSON structure above."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    # 🟢 एक जैसी कहानी का इलाज: Temperature 0.75 कर दिया है ताकि वो हर बार नया सोचे
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.75}
    
    for attempt in range(5):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60)
            if res.status_code == 200:
                parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
                if parsed.get('scenes'):
                    full_text = " ".join([s['text'] for s in parsed['scenes']])
                    word_count = len(full_text.split())
                    
                    if word_count < 95 and not is_long_video:
                        print(f"⚠️ [रिजेक्ट] कहानी छोटी है ({word_count} शब्द)। 10 सेकंड रुककर दोबारा कोशिश कर रहा है...")
                        time.sleep(10)
                        continue
                        
                    return parsed
            else:
                print(f"⚠️ [Groq API Error] सर्वर एरर: Status {res.status_code}")
                time.sleep(15)
        except Exception as e:
            print(f"⚠️ [Network Error]: {e}")
            time.sleep(10)
            
    raise Exception("🚨 AI Model Failed after 5 retries!")

def download_single_image(idx, p, style_filter, w, h):
    enhanced_prompt = f"{p}, {style_filter}, perfect composition, no blur"
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

def fetch_all_images_safe(scenes, style_filter, is_long_video):
    print("🎨 एकदम साफ (Sharp Focus) तस्वीरें डाउनलोड हो रही हैं...")
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    valid_images, valid_scenes = [], []
    for i, s in enumerate(scenes):
        img_path = download_single_image(i, s['prompt'], style_filter, w, h)
        if img_path:
            valid_images.append(img_path)
            valid_scenes.append(s)
        time.sleep(1)
    if len(valid_images) == 0: raise Exception("Images failed.")
    return valid_images, valid_scenes

def create_human_voice(text, filename):
    print("🎙️ दमदार आवाज़ बन रही है...")
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+5%", volume="+50%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def create_text_clip(caption_text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font_size = 100 if is_long_video else 150
    try: font = ImageFont.truetype("NotoSansDevanagari-Bold.ttf", font_size)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(caption_text, width=35 if is_long_video else 16)
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped, font=font)
        
    x = (w - text_w) // 2
    y = int(h * 0.85) if is_long_video else int(h * 0.65) 
    
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=8, stroke_fill="black", align='center')
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print(f"🎬 {'LONG VIDEO' if is_long_video else 'SHORTS'} Render हो रहा है...")
    main_audio = AudioFileClip(audio_file)
    dur_per_scene = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        img = Image.open(img_path).convert("RGB")
        w, h = (1920, 1080) if is_long_video else (1080, 1920)
        
        bg = img.resize((w, h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(30))
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
        zoom = base.resize(lambda t: 1 + 0.02 * (t/dur_per_scene))
        
        # 🟢 अब हिंदी का कैप्शन जाएगा (English वाला सिस्टम हटा दिया)
        txt = create_text_clip(scenes[i].get('text', '')[:25] + '...', dur_per_scene, is_long_video)
        clips.append(CompositeVideoClip([zoom.set_position('center'), txt.set_position(('center', 'center'))]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    main_audio.close()
    final.close()

def upload_video(token, filename, title, description, tags, category):
    print("🚀 YouTube पर अपलोड हो रहा है...")
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
            print(f"⚠️ Upload fail, retrying... Error: {e}")
            time.sleep(10)
    raise Exception("Upload failed completely.")

def run_network():
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    is_long = True if ist_time.hour in [18, 19] else False 
    
    print(f"\n⚙️ Time: {ist_time.strftime('%I:%M %p')} | Mode: {'LONG' if is_long else 'SHORTS'}")
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    
    for ch_name in channels:
        cfg = CHANNELS_CONFIG[ch_name]
        for attempt in range(3):
            try:
                hook_theme = random.choice(cfg['hooks'])
                data = get_scene_script(ch_name, hook_theme, is_long)
                imgs, valid_scenes = fetch_all_images_safe(data['scenes'], cfg['style'], is_long)
                
                full_text = " ".join([s['text'] for s in valid_scenes])
                create_human_voice(full_text, "v.mp3")
                
                out_file = f"{ch_name}_final.mp4"
                assemble_video(imgs, valid_scenes, out_file, "v.mp3", is_long)
                
                title = data['title'] if is_long else f"{data['title'][:70]} #shorts"
                desc = f"{full_text}\n\n🔥 बेहतरीन प्रोडक्ट्स खरीदें: https://www.amazon.in/?tag=girishbhut07-21"
                
                upload_video(cfg['token'], out_file, title, desc, cfg['tags'], cfg['category'])
                time.sleep(30)
                break 
            except Exception as e: 
                print(f"🛑 Error in {ch_name} (Attempt {attempt+1}): {e}")
                time.sleep(10)

if __name__ == "__main__": 
    run_network()
