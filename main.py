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

print("🚀 V20 Final Masterpiece: Human Voice, Strict Time Limits & Perfect Anatomy Active!")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

font_path = "NotoSansDevanagari-Bold.ttf"
if not os.path.exists(font_path) or os.path.getsize(font_path) < 20000:
    print("📥 हिंदी फॉन्ट डाउनलोड हो रहा है...")
    try:
        url = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf"
        urllib.request.urlretrieve(url, font_path)
    except Exception as e: print(f"Font Error: {e}")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# 🟢 टेढ़े-मेढ़े हाथ-पैरों का पक्का इलाज (Anatomy Lock)
ANATOMY_FILTER = "anatomically correct, flawless face, perfectly drawn hands, symmetrical body, hyper-realistic, no deformities, clear facial features"

CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna"], "style": f"wide angle cinematic, {ANATOMY_FILTER}, 8k", "hooks": ["श्री कृष्ण का सबसे बड़ा चमत्कार", "गीता का रहस्य", "महाभारत का गुप्त सच"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda"], "style": f"hyper-realistic nature, {ANATOMY_FILTER}, 8k", "hooks": ["आयुर्वेद का 1 गुप्त नियम", "गर्म पानी पीने के खतरनाक फायदे"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation"], "style": f"professional corporate photography, {ANATOMY_FILTER}, 8k", "hooks": ["रतन टाटा की सफलता का राज", "चाणक्य नीति"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology"], "style": f"dark mysterious cinematic, {ANATOMY_FILTER}, 8k", "hooks": ["कैलाश पर्वत का अनसुलझा रहस्य", "समुद्र मंथन का असली सच"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary"], "style": f"cinematic inspiring environment, {ANATOMY_FILTER}, 8k", "hooks": ["Atomic Habits की असली सीख", "Rich Dad Poor Dad का सच"]}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"\n📝 {channel_name} के लिए इंसानों जैसी असली कहानी लिखी जा रही है...")
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rand_id = random.randint(100000, 999999)
    
    # 🟢 लम्बाई का एकदम पक्का गणित: Shorts = 70-90 words, Long = 400-600 words
    word_limit = "400 to 550" if is_long_video else "70 to 85"
    scene_count = 15 if is_long_video else 5

    prompt = f"""[SYSTEM SEED: {current_time_str} - {rand_id}] 
    You are a viral scriptwriter for '{channel_name}'. THEME: "{hook_theme}".
    Length: You MUST write exactly between {word_limit} words total.

    CRITICAL RULES FOR HUMAN VOICE & PERFECT IMAGES:
    1. WRITE LIKE A REAL HUMAN. Use commas (,) and full stops (.) naturally so the AI voice takes breathing pauses. Do not sound robotic.
    2. NEVER WRITE BORING FACTS. Tell a highly specific, untold story.
    3. The image 'prompt' MUST NOT contain complex human actions (no running, fighting, or lifting). Keep characters static, simple, and facing the camera to avoid anatomy deformities.
    4. End the script exactly with: 'ऐसी ही अद्भुत जानकारी के लिए चैनल को अभी सब्सक्राइब करें।'
    
    JSON STRUCTURE:
    {{
      "title": "Viral Clickbait Title",
      "scenes": [
        {{
          "text": "Human-like Hindi story text with natural commas...", 
          "caption": "SHORT", 
          "prompt": "Wide angle, simple portrait, highly detailed..."
        }}
      ]
    }}
    Provide exactly {scene_count} scenes."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    
    for _ in range(5):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60)
            if res.status_code == 200:
                parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
                if parsed.get('scenes'): 
                    # 🟢 लम्बाई की सख्त चेकिंग
                    full_text = " ".join([s['text'] for s in parsed['scenes']])
                    word_count = len(full_text.split())
                    if not is_long_video and (word_count < 65 or word_count > 100):
                        print(f"⚠️ [रिजेक्ट] शब्द सीमा गलत है ({word_count})। 30-40 सेकंड के लिए दोबारा लिख रहा है...")
                        time.sleep(5)
                        continue
                    return parsed
            time.sleep(5)
        except: time.sleep(5)
    raise Exception("AI Failed")

def download_single_image(idx, p, style_filter, w, h):
    seed_value = random.randint(1000000, 9999999)
    enhanced_prompt = f"{p}, {style_filter}"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}?width={w}&height={h}&nologo=true&enhance=true&seed={seed_value}"
    
    fname = f"scene_{idx}.jpg"
    for _ in range(4):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            if r.status_code == 200 and len(r.content) > 10000:
                with open(fname, "wb") as f: f.write(r.content)
                Image.open(fname).verify() 
                return fname
        except: pass
        time.sleep(2)
    return None

def fetch_all_images_safe(scenes, style_filter, is_long_video):
    print("🎨 साफ-सुथरी और असली दिखने वाली तस्वीरें डाउनलोड हो रही हैं...")
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    valid_images, valid_scenes = [], []
    for i, s in enumerate(scenes):
        img_path = download_single_image(i, s['prompt'], style_filter, w, h)
        if img_path:
            valid_images.append(img_path)
            valid_scenes.append(s)
    if len(valid_images) == 0: raise Exception("Images failed.")
    return valid_images, valid_scenes

def create_human_voice(text, filename):
    print("🎙️ बिल्कुल असली इंसान जैसी आवाज़ बन रही है (नॉर्मल स्पीड)...")
    async def _generate():
        for _ in range(3):
            try:
                # 🟢 आवाज़ की स्पीड एकदम नॉर्मल कर दी है ताकि रोबोट जैसा न लगे
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+0%", volume="+50%") 
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
    
    font_size = 110 if is_long_video else 160
    try: font = ImageFont.truetype(font_path, font_size)
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
            time.sleep(10)

def run_network():
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    is_long = True if ist_time.hour in [18, 19] else False 
    
    print(f"\n⚙️ Time: {ist_time.strftime('%I:%M %p')} | Mode: {'LONG' if is_long else 'SHORTS'}")
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    
    for ch_name in channels:
        cfg = CHANNELS_CONFIG[ch_name]
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
        except Exception as e:
            print(f"🛑 Error in {ch_name}: {e}")

if __name__ == "__main__": 
    run_network()
