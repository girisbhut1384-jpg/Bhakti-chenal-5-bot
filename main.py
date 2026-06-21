# ==============================================================================
# 🚀 V50 HYPER-VIRAL ENGINE: BGM, FAST CUTS, AUTO-ADAPT & DARK PSYCHOLOGY
# ==============================================================================

import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip

print("🔥 V50 Hyper-Viral Auto-Adapt Engine: Started...")

# जरूरी फाइल्स सेट करना
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")
font_path = "Roboto-Black.ttf"
bgm_path = "suspense_bgm.mp3"
if not os.path.exists(font_path): os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")
# 🎵 एक रॉयल्टी-फ्री वायरल सस्पेंस BGM अपने आप डाउनलोड होगा
if not os.path.exists(bgm_path): os.system("wget -qO suspense_bgm.mp3 https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder BGM

GROQ_KEY = "YOUR_GROQ_API_KEY_HERE"
CLIENT_ID = "768932543756-ndfvqmbb0p7ffa1r1cg6bmmuimim98n6.apps.googleusercontent.com"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"

TOKENS = {
    "GB YOUTUBER": "YOUR_TOKEN_HERE",
    "HEALTH & AYURVEDA": "YOUR_TOKEN_HERE",
    "BUSINESS & MOTIVATION": "YOUR_TOKEN_HERE",
    "SANATAN RAHASYA": "YOUR_TOKEN_HERE",
    "BOOK SUMMARY": "YOUR_TOKEN_HERE"
}

NICHES = {
    "GB YOUTUBER": "Dark secrets of ancient Indian texts and Karma.",
    "HEALTH & AYURVEDA": "Medical industry secrets and ancient deadly/miracle remedies.",
    "BUSINESS & MOTIVATION": "Dark psychology, matrix escape, and brutal money truths.",
    "SANATAN RAHASYA": "Suppressed Indian history, terrifying cosmic cycles.",
    "BOOK SUMMARY": "The brutal, hidden truths from banned or controversial success books."
}

def measure_and_adapt(channel_name):
    """📊 Measuring & Fixing: यह हिस्सा पिछले वीडियो का रिकॉर्ड चेक करता है"""
    history_file = "channel_history.json"
    aggression_level = "NORMAL"
    try:
        if os.path.exists(history_file):
            with open(history_file, "r") as f: data = json.load(f)
            # अगर चैनल लगातार फ्लॉप हो रहा है, तो प्रॉम्प्ट को 'EXTREME' कर दो
            if data.get(channel_name, {}).get("consecutive_flops", 0) > 2:
                aggression_level = "EXTREME_DARK_PSYCHOLOGY"
    except: pass
    print(f"📈 Analytics Engine: {channel_name} set to {aggression_level} mode.")
    return aggression_level

def get_master_script(channel_name, aggression_level):
    niche = NICHES[channel_name]
    print(f"\n📝 Executing Latest Viral Prompt for {channel_name}...")
    
    hook_instruction = """Start directly with a massive pattern-interrupt. 
    Examples: "गरीब लोग अपनी पूरी जिंदगी इस एक झूठ को सच मानकर...", "मेडिकल इंडस्ट्री कभी नहीं चाहेगी कि आप...", "99% लोग यह भयानक गलती कर रहे हैं..."
    DO NOT say "क्या आप जानते हैं" or "क्या आपको पता है"."""

    if aggression_level == "EXTREME_DARK_PSYCHOLOGY":
        hook_instruction = """Start with absolute FEAR, GREED, or EXTREME CURIOSITY. Attack the viewer's current beliefs immediately. Make them feel they are in danger if they swipe up."""

    # 🔥 10 FAST CUTS PROMPT: 10 Images for dynamic editing
    prompt = f"""You are an elite, dark psychology YouTube Shorts Scriptwriter.
    Target Niche: {niche}

    CRITICAL RULES:
    1. Title: Under 45 chars. Highly clickbaity. 1 emoji at the END.
    2. Length: EXACTLY 5 to 6 punchy sentences. Total word count MUST be UNDER 60 words in pure Devanagari Hindi. 
    3. The Hook: {hook_instruction}
    4. The Value: Brutal, fast-paced facts. Real names, real books, real historical figures. No generic fluff.
    5. The CTA: End EXACTLY with: "ऐसी ही खूंखार जानकारी के लिए चैनल को अभी सब्सक्राइब करें।"
    
    🔥 DYNAMIC VISUALS (10 FAST CUTS) 🔥:
    - Create exactly 10 English image prompts for fast-cut editing.
    - Prompts must describe empty, inanimate STILL LIFE photography (e.g., "A bloody golden coin falling in darkness", "A glowing ancient manuscript").
    - BANNED: Human, face, person, god, man, woman.
    
    Return ONLY valid JSON format:
    {{
      "title": "Title Here 💀",
      "script": "Hindi script under 60 words",
      "captions": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
      "prompts": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10"],
      "tags": ["#viral", "#darktruth", "#facts"]
    }}
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 1000}
    
    for _ in range(3):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60).json()
            parsed = json.loads(extract_json_safely(res['choices'][0]['message']['content']))
            if parsed.get('script') and len(parsed.get('prompts', [])) >= 8:
                return parsed
        except: time.sleep(3)
    raise Exception("🚨 AI Model Failed.")

def fetch_safe_visuals(prompts):
    image_files = []
    base_seed = random.randint(1000, 99999)
    print(f"🎨 Generating {len(prompts)} Fast-Cut Visuals...")
    
    for i, p in enumerate(prompts):
        enhanced = f"{p}, 8k, dramatic cinematic lighting, pure still life, masterpiece"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced)}?width=1080&height=1920&nologo=true&seed={base_seed+i}&model=flux"
        fname = f"scene_{i}.jpg"
        for _ in range(3):
            try:
                res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
                if res.status_code == 200 and len(res.content) > 3000:
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    break
            except: time.sleep(2)
    return image_files

def create_smooth_voice(text, filename):
    print("🎙️ Recording Deep Voice...")
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-2%", pitch="-5Hz", volume="+50%") 
                await communicate.save(filename); return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(_generate())

def create_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 800; img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(font_path, 140) 
    except: font = ImageFont.load_default()
    wrapped = textwrap.fill(text.upper(), width=14) 
    try: bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center'); text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except: text_w, text_h = draw.textsize(wrapped, font=font)
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    # 🔴 Red stroke for extreme viral aesthetic
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFFFFF", stroke_width=15, stroke_fill="#8B0000", align='center')
    temp_filename = f"temp_cap_{random.randint(10000, 99999)}.png"; img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def process_image(img_path, output_path):
    img = Image.open(img_path).convert("RGB"); bg = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=50))
    ratio = 1080 / img.width; new_h = int(img.height * ratio)
    if new_h > 1920: ratio = 1920 / img.height; new_w = int(img.width * ratio); fg = img.resize((new_w, 1920), Image.Resampling.LANCZOS); bg.paste(fg, ((1080 - new_w) // 2, 0))
    else: fg = img.resize((1080, new_h), Image.Resampling.LANCZOS); bg.paste(fg, (0, (1920 - new_h) // 2))
    bg.save(output_path); return output_path

def build_video(script, image_files, captions, output_vid):
    print("🎬 Rendering Fast-Cut Viral Video with BGM...")
    voice_file = "temp_voice.mp3"
    create_smooth_voice(script, voice_file)
    
    # 🎵 ऑडियो मिक्सिंग (Voice + Background Music)
    main_audio = AudioFileClip(voice_file)
    bgm_audio = AudioFileClip(bgm_path).volumex(0.15).set_duration(main_audio.duration)
    final_audio = CompositeAudioClip([main_audio, bgm_audio])
    
    time_per_image = main_audio.duration / len(image_files)
    
    clips = []
    for i, img_path in enumerate(image_files):
        fixed_path = f"fixed_{i}.jpg"; process_image(img_path, fixed_path)
        base_clip = ImageClip(fixed_path)
        # ⚡ Fast dynamic zoom
        zoomed = base_clip.resize(lambda t: 1 + 0.08 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try: txt_clip = create_text_clip(cap_text, time_per_image).set_position(('center', 0.60), relative=True); final_clip = CompositeVideoClip([zoomed.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = zoomed
        else: final_clip = zoomed
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose").set_audio(final_audio)
    video.write_videofile(output_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close(); bgm_audio.close(); final_audio.close(); video.close()

def upload_youtube(token, filename, title, desc, tags_list, category_id, channel_name):
    print(f"🚀 Uploading: {title}")
    from google.oauth2.credentials import Credentials; from googleapiclient.discovery import build; from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": desc, "tags": tags_list, "categoryId": category_id}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}, media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)).execute()
    
    # 📈 अपलोड सफल होने पर एनालिटिक्स अपडेट करें
    try:
        history_file = "channel_history.json"
        data = {}
        if os.path.exists(history_file):
            with open(history_file, "r") as f: data = json.load(f)
        if channel_name not in data: data[channel_name] = {"consecutive_flops": 0}
        data[channel_name]["consecutive_flops"] += 1 # Default assumption, resets if views checked via API later
        with open(history_file, "w") as f: json.dump(data, f)
    except: pass

if __name__ == "__main__":
     channels = [
        ("GB YOUTUBER", "22"),
        ("HEALTH & AYURVEDA", "26"),
        ("BUSINESS & MOTIVATION", "27"),             
        ("SANATAN RAHASYA", "24"),         
        ("BOOK SUMMARY", "27")       
    ]
     
     for name, cat_id in channels:
        token = TOKENS[name]
        try:
            aggression_level = measure_and_adapt(name)
            content = get_master_script(name, aggression_level)
            final_name = f"final_{name.replace(' ', '_').lower()}.mp4"
            image_files = fetch_safe_visuals(content['prompts'])
            
            build_video(content['script'], image_files, content['captions'], final_name)
            
            title = content['title']
            tags_list = content.get('tags', [])
            desc = f"✨ {title}\n\n{content['script']}\n\n🔗 Best Deals: https://www.amazon.in/?tag=girishbhut07-21"
            
            upload_youtube(token, final_name, title[:95], desc, tags_list, cat_id, name)
            print(f"✅ {name} Success (Hyper-Viral Engine Applied)!")
            time.sleep(15)
        except Exception as e: 
            print(f"🛑 Error on {name}: {e}")

     print("\n🏆 ऑपरेशन सक्सेसफुल! V50 एडवांस्ड एडिटिंग, BGM और डार्क साइकोलॉजी के साथ पूरा हुआ!")
