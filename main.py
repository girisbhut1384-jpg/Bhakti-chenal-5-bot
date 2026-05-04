import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime

# --- PIL & MOVIEPY FIX ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = Image.LANCZOS
if not hasattr(Image, 'Resampling'): Image.Resampling = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🚀 V4 Master Machine: Anti-Crash & Safe Downloader Active...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# --- CHANNELS CONFIG ---
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "radhe radhe"], "hooks": ["श्री कृष्ण के चमत्कार", "गीता का सार"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda"], "hooks": ["एसिडिटी का इलाज", "तुलसी के फायदे"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation"], "hooks": ["अमीर बनने के नियम", "बिज़नेस आईडिया"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology"], "hooks": ["कैलाश का रहस्य", "अश्वत्थामा का सच"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary"], "hooks": ["Atomic Habits hindi", "Rich Dad Poor Dad summary"]}
}

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"📝 {channel_name} के लिए सीन-बाय-सीन स्क्रिप्ट तैयार हो रही है...")
    word_limit = "400" if is_long_video else "70"
    scene_count = 15 if is_long_video else 6
    
    prompt = f"""Write a viral Hindi script for {channel_name} on theme "{hook_theme}".
    Length: Exactly {word_limit} words. Style: Direct, Shocking.
    No 'Namaskar' or 'Hello'. Start with the hook.
    ENDING: "सब्सक्राइब करें और बायो में अमेज़न लिंक देखें।"
    
    CRITICAL: Provide {scene_count} logical scenes. Each scene must have a visual prompt matching the text exactly.
    Return ONLY JSON:
    {{
      "title": "Viral Title",
      "scenes": [
        {{"text": "Hindi sentence", "prompt": "Detailed English image prompt matching this sentence"}},
        ...
      ]
    }}"""

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                        headers={"Authorization": f"Bearer {GROQ_KEY}"},
                        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.6})
    match = re.search(r'\{[\s\S]*\}', res.json()['choices'][0]['message']['content'])
    if not match: raise Exception("Invalid JSON from Groq")
    return json.loads(match.group(0))

def download_single_image(idx, p, w, h):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + ', highly detailed, realistic, 8k')}?width={w}&height={h}&nologo=true&seed={random.randint(10000,99999)}"
    fname = f"scene_{idx}.jpg"
    
    for attempt in range(4): # 4 bar try karega agar file corrupt hui
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200 and len(r.content) > 5000: # File minimum 5KB ki honi chahiye
                with open(fname, "wb") as f: f.write(r.content)
                
                # STRICT Validation: Kya ye sach me photo hai?
                try:
                    img = Image.open(fname)
                    img.verify() 
                    return fname
                except Exception as img_err:
                    print(f"File corrupt hai, retry kar rahe hain... {img_err}")
        except Exception as req_err: 
            print(f"Download fail, retry... {req_err}")
        time.sleep(2) # Retry se pehle thoda wait
    return None

def fetch_all_images_safe(scenes, is_long_video):
    print("🎨 तस्वीरें सुरक्षित तरीके से डाउनलोड हो रही हैं (Anti-Block Mode)...")
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    valid_images = []
    valid_scenes = []
    
    for i, s in enumerate(scenes):
        img_path = download_single_image(i, s['prompt'], w, h)
        if img_path:
            valid_images.append(img_path)
            valid_scenes.append(s)
        time.sleep(1) # IP block hone se bachane ke liye 1 second ka gap
        
    if len(valid_images) == 0:
        raise Exception("Zero valid images downloaded. API Blocked or Network Error.")
        
    return valid_images, valid_scenes

async def create_voice(text, filename):
    comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%")
    await comm.save(filename)

def create_text_clip(text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("Roboto-Black.ttf", 90 if is_long_video else 115)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(text.upper(), width=30 if is_long_video else 15)
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped, font=font)
        
    x = (w - text_w) // 2
    y = (h - text_h) // 2
    if is_long_video: y = int(h * 0.8)
    
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=8, stroke_fill="black", align='center')
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print("🎬 वीडियो रेंडरिंग (Safe & Fast Mode)...")
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
        txt = create_text_clip(scenes[i]['text'], dur_per_scene, is_long_video)
        clips.append(CompositeVideoClip([zoom.set_position('center'), txt.set_position('center')]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    # ultrafast aur 4 threads ke sath fast render hoga
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
    hour = (datetime.utcnow().hour + 5) % 24 # Rough IST
    is_long = True if hour in [18, 19] else False
    print(f"⚙️ Network Mode: {'LONG' if is_long else 'SHORTS'}")
    
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
                desc = f"खरीदें यहाँ से: https://www.amazon.in/?tag=girishbhut07-21\n\n{full_text}"
                upload(cfg['token'], out_file, title, desc, cfg['tags'], cfg['category'])
                
                print(f"✅ {ch_name} डन!")
                time.sleep(60) # 1 min Anti-spam gap
                break # Success, move to next channel
            except Exception as e: 
                print(f"❌ Error in {ch_name} (Attempt {attempt+1}): {e}")
                time.sleep(10)

if __name__ == "__main__": run()
