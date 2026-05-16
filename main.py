import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime, timedelta

# --- PIL & MOVIEPY SETUP ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import urllib.request

print("🛡️ V25: Ultimate Cinematic Pro Engine Active!")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

font_path = "NotoSansDevanagari-Bold.ttf"
if not os.path.exists(font_path):
    print("📥 फॉन्ट डाउनलोड हो रहा है...")
    try: urllib.request.urlretrieve("https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf", font_path)
    except: pass

GROQ_KEY = os.environ.get("GROQ_API_KEY")
ELEVENLABS_KEY = os.environ.get("ELEVENLABS_API_KEY") 
CLIENT_ID = "768932543756-7e17ufdmt7r67urc9krua7t69vps6h57.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# पत्तों जैसे डिफेक्ट और खराब चेहरों को रोकने के लिए कड़ा एआई फ़िल्टर
ANATOMY_FILTER = "highly detailed cinematic portrait, flawless human face, 8k resolution, photorealistic, perfect hands, sharp focus, historical accuracy, studio lighting, award winning photography, no distortions, no artifact defects"

CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna", "motivation", "shorts"], "style": f"lord krishna dynamic ancient look, grand palace background, {ANATOMY_FILTER}", "hooks": ["श्री कृष्ण का वो गुप्त श्राप जो आज भी सच है", "महाभारत का सबसे भयानक सच जो छुपाया गया"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda", "fitness", "shorts"], "style": f"ancient ayurvedic herbs, premium cinematic macro shot, {ANATOMY_FILTER}", "hooks": ["सोने से पहले एक बूंद तेल का ये चमत्कार", "दूध के साथ ये चीज खाना साक्षात जहर है"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation", "success", "shorts"], "style": f"ultra premium business empire cinematic style, {ANATOMY_FILTER}", "hooks": ["धीरूभाई अंबानी की वो गुप्त चाल जिसने इतिहास बदला", "रतन टाटा का वो एक फैसला जिसने फोर्ड को झुकाया"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology", "history", "shorts"], "style": f"dark mysterious ancient indian temple, mystical golden glow, {ANATOMY_FILTER}", "hooks": ["जगन्नाथ मंदिर का वो रहस्य जो विज्ञान भी नहीं सुलझा पाया", "केदारनाथ के नीचे छुपा है त्रिकाल का सच"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary", "learning", "shorts"], "style": f"epic inspiring dark library moody atmosphere, {ANATOMY_FILTER}", "hooks": ["दिमाग को १० गुना तेज करने का गुप्त नियम", "अमीरों का वो सीक्रेट जो स्कूल में कभी नहीं पढ़ाया जाता"]}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"\n📝 {channel_name} के लिए प्रो-स्क्रिप्ट लिखी जा रही है...")
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rand_id = random.randint(100000, 999999)
    
    word_limit = "400 to 550" if is_long_video else "75 to 110"
    scene_count = 15 if is_long_video else 5

    # स्क्रिप्ट के अंदर से बकवास खत्म करने और सस्पेंस लाने का कड़ा निर्देश (Prompt)
    prompt = f"""[SYSTEM SEED: {current_time_str} - {rand_id}]
You are the world's highest-paid documentary filmmaker for '{channel_name}'. THEME: "{hook_theme}"
CRITICAL RULES:
1. DO NOT START with generic words like "क्या आप जानते हैं" or "दोस्तों".
2. Scene 1 MUST be a direct, shocking, high-suspense hook statement.
3. Every scene MUST deliver actual deep information, micro-stories, or shocking historical facts. Keep the suspense alive until the very last line.
4. "text" MUST be in intense Devanagari Hindi with commas (,) for slow cinematic dramatic pauses.
5. "prompt" MUST be in ENGLISH. Describe the exact historical character or subject. No text inside images. Never generate generic modern faces unless requested.
6. "caption" MUST be 2-3 heavy words in Hindi.
7. Total word count of "text" combined MUST be between {word_limit} words.

JSON STRUCTURE:
{{
  "title": "Shocking Clickbait Hindi Title",
  "scenes": [
    {{"text": "गंभीर और रहस्यमयी हिंदी फैक्ट या कहानी...", "caption": "धमाकेदार कैप्शन", "prompt": "Detailed cinematic visual scene..."}}
  ]
}}
Total Scenes: {scene_count}. End the last scene text with: 'ऐसी ही अद्भुत जानकारियों के लिए हमारे साथ अभी जुड़ें।'"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.80}
    
    for _ in range(5):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60)
            if res.status_code == 200:
                parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
                if parsed.get('scenes'): 
                    full_text = " ".join([s.get('text', '') for s in parsed['scenes']])
                    wc = len(full_text.split())
                    min_w, max_w = (300, 650) if is_long_video else (50, 140)
                    if min_w <= wc <= max_w: return parsed
            time.sleep(5)
        except: time.sleep(5)
    raise Exception("AI Scripting Failed")

def download_single_image(idx, p, style_filter, w, h):
    seed = random.randint(1000000, 9999999)
    enhanced_prompt = f"{p}, {style_filter}"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}?width={w}&height={h}&nologo=true&enhance=true&seed={seed}"
    fname = f"scene_{idx}.jpg"
    for _ in range(3):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            if r.status_code == 200 and len(r.content) > 10000:
                with open(fname, "wb") as f: f.write(r.content)
                Image.open(fname).verify(); return fname
        except: pass
        time.sleep(2)
    return None

def fetch_all_images_safe(scenes, style_filter, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    valid_images, valid_scenes = [], []
    for i, s in enumerate(scenes):
        img_path = download_single_image(i, s.get('prompt', 'Cinematic view'), style_filter, w, h)
        if img_path: valid_images.append(img_path); valid_scenes.append(s)
    if not valid_images: raise Exception("Image Generation Failed")
    return valid_images, valid_scenes

def create_voice(text, filename):
    print("🎙️ गंभीर और इंसानी आवाज़ जनरेट हो रही है...")
    async def _generate():
        # गति को -4% धीमा किया गया है ताकि रोबोटिक टोन खत्म हो और आवाज में भारीपन आए
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-4%", volume="+60%") 
        await communicate.save(filename)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def download_bgm_safe():
    bgm_file = "epic_bgm.mp3"
    if not os.path.exists(bgm_file):
        print("🎵 सस्पेंस मिस्ट्री BGM डाउनलोड हो रहा है...")
        try:
            url = "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                with open(bgm_file, "wb") as f: f.write(r.content)
        except: pass
    return bgm_file if os.path.exists(bgm_file) else None

def create_text_clip(caption_text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fsize = 100 if is_long_video else 140
    try: font = ImageFont.truetype(font_path, fsize)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(caption_text, width=28 if is_long_video else 14)
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    except: tw, th = draw.textsize(wrapped, font=font)
    
    # टेक्स्ट की पोजीशन को बीच से हटाकर नीचे (Bottom 15%) शिफ्ट किया गया ताकि चेहरों पर ओवरलैप न हो
    x, y = (w - tw) // 2, int(h * 0.82) if is_long_video else int(h * 0.80)
    draw.multiline_text((x+5, y+5), wrapped, font=font, fill="black", align='center')
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=9, stroke_fill="black", align='center')
    
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print(f"🎬 प्रो-लेवल वीडियो रेंडरिंग चालू...")
    voice_audio = AudioFileClip(audio_file)
    
    bgm_path = download_bgm_safe()
    if bgm_path:
        bgm_audio = AudioFileClip(bgm_path).volumex(0.07)
        if bgm_audio.duration < voice_audio.duration: bgm_audio = bgm_audio.loop(duration=voice_audio.duration)
        else: bgm_audio = bgm_audio.subclip(0, voice_audio.duration)
        final_audio = CompositeAudioClip([voice_audio, bgm_audio])
    else:
        final_audio = voice_audio

    dur_per_scene = voice_audio.duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        img = Image.open(img_path).convert("RGB")
        w, h = (1920, 1080) if is_long_video else (1080, 1920)
        
        bg = img.resize((w, h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
        ratio = w / img.width
        new_h = int(img.height * ratio)
        if new_h > h:
            ratio = h / img.height; new_w = int(img.width * ratio)
            fg = img.resize((new_w, h), Image.Resampling.LANCZOS)
            bg.paste(fg, ((w - new_w) // 2, 0))
        else:
            fg = img.resize((w, new_h), Image.Resampling.LANCZOS)
            bg.paste(fg, (0, (h - new_h) // 2))
            
        proc_name = f"proc_{i}.jpg"
        bg.save(proc_name)
        
        base = ImageClip(proc_name).set_duration(dur_per_scene).set_position('center')
        zoom = base.resize(lambda t: 1 + 0.05 * (t/dur_per_scene)) 
        txt = create_text_clip(scenes[i].get('caption', ''), dur_per_scene, is_long_video)
        clips.append(CompositeVideoClip([zoom, txt]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(final_audio)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    voice_audio.close(); final.close()

def upload_video(token, filename, title, description, tags, category):
    print(f"🚀 YouTube पर प्रीमियम वीडियो अपलोड हो रहा है: {title}")
    try:
        creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
        youtube = build("youtube", "v3", credentials=creds)
        request = youtube.videos().insert(
            part="snippet,status",
            body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public"}},
            media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
        )
        request.execute()
        print("✅ धमाका! बिल्कुल नया प्रीमियम वीडियो लाइव हो गया है।")
    except Exception as e: 
        print(f"❌ YouTube Upload Fail: {e}")

def run_network():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    is_long = True if ist_now.hour in [18, 19, 20] else False 
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    
    for ch_name in channels:
        cfg = CHANNELS_CONFIG[ch_name]
        try:
            data = get_scene_script(ch_name, random.choice(cfg['hooks']), is_long)
            imgs, valid_scenes = fetch_all_images_safe(data['scenes'], cfg['style'], is_long)
            full_txt = " ".join([s.get('text', '') for s in valid_scenes])
            create_voice(full_txt, "v.mp3")
            
            out = f"{ch_name}_final.mp4"
            assemble_video(imgs, valid_scenes, out, "v.mp3", is_long)
            
            title = data.get('title', 'Viral Video') if is_long else f"{data.get('title', 'Viral')[:70]} #shorts"
            
            # बेहतर एसईओ (SEO) डिस्क्रिप्शन फॉर्मेट
            desc = f"✨ {title}\n\n{full_txt[:200]}...\n\n📌 ऐसी ही और अनसुनी कहानियों के लिए चैनल को तुरंत सब्सक्राइब करें!\n\n🔥 Best Deals: https://www.amazon.in/?tag=girishbhut07-21"
            
            upload_video(cfg['token'], out, title, desc, cfg['tags'], cfg['category'])
            time.sleep(15) 
        except Exception as e: print(f"🛑 {ch_name} में क्रैश से बचाया गया: {e}")

if __name__ == "__main__": 
    run_network()
