import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🚀 5-Channel Master Auto-Machine Started...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

# --- API KEYS ---
GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# --- MASTER CHANNEL DICTIONARY ---
CHANNELS_CONFIG = {
    "GB_YOUTUBER": {
        "token": os.environ.get("TOKEN_GBYOUTUBER"),
        "category": "22", "tags": ["bhakti", "radhe radhe", "satsang", "sanatan dharma", "krishna"],
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

def get_ai_script(channel_name, hook_theme, is_long_video=False):
    print(f"📝 {channel_name} ke liye script likhi jaa rahi hai... (Long: {is_long_video})")
    word_count = "350-400" if is_long_video else "80-90"
    num_prompts = 12 if is_long_video else 5
    
    prompt = f"""Write a viral Hindi YouTube script for channel type: {channel_name}.
    Topic/Hook: "{hook_theme}".
    LENGTH: Exactly {word_count} words. 
    STYLE: Highly engaging, no boring intros. Direct value.
    ENDING: "ऐसी ही शानदार जानकारी और बेहतरीन प्रोडक्ट्स/किताबों के लिए चैनल सब्सक्राइब करें और डिस्क्रिप्शन में दिया अमेज़न लिंक ज़रूर चेक करें।"
    
    Return ONLY pure JSON (no markdown):
    {{
      "title": "Viral Clickbait Hindi Title",
      "script": "Full hindi script here...",
      "captions": ["HOOK 1", "FACT 2", "AMAZING", "SUBSCRIBE"],
      "prompts": ["highly detailed realistic photo of ...", "cinematic shot of ..."] (Generate {num_prompts} unique visual prompts)
    }}"""

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                        headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
                        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7})
    data = json.loads(re.search(r'\{[\s\S]*\}', res.json()['choices'][0]['message']['content']).group(0))
    return data['title'], data['script'], data['prompts'], data['captions']

def fetch_ai_images(prompts, is_long_video=False):
    print("🎨 Pollinations AI se unique images ban rahi hain...")
    image_files = []
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width={w}&height={h}&nologo=true&seed={random.randint(1000,99999)}"
        fname = f"scene_{i}.jpg"
        for _ in range(3):
            try:
                res = requests.get(url, timeout=30)
                if res.status_code == 200:
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    break
            except: time.sleep(2)
    return image_files

def create_voice(text, filename):
    print("🎙️ AI Voice ban rahi hai...")
    async def _generate():
        comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+5%")
        await comm.save(filename)
    asyncio.run(_generate())

def make_video(image_files, captions, output_vid, audio_file, is_long_video):
    print("🎬 Video render ho raha hai...")
    audio = AudioFileClip(audio_file)
    time_per_image = audio.duration / len(image_files)
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    clips = []

    for i, img_path in enumerate(image_files):
        img = Image.open(img_path).resize((w, h), Image.Resampling.LANCZOS)
        img.save(img_path)
        
        base_clip = ImageClip(img_path)
        # Ken Burns Zoom
        clip = base_clip.resize(lambda t: 1 + 0.03 * (t / time_per_image)).set_duration(time_per_image)
        
        if not is_long_video and i < len(captions): # Shorts ke liye badha text
            txt_img = Image.new('RGBA', (w, h), (0,0,0,0))
            draw = ImageDraw.Draw(txt_img)
            font = ImageFont.truetype("Roboto-Black.ttf", 120)
            text = textwrap.fill(captions[i].upper(), width=15)
            draw.multiline_text((w//2, h//2 + 200), text, font=font, fill="#FFE81F", stroke_width=8, stroke_fill="black", align='center', anchor="mm")
            txt_img.save("temp_txt.png")
            txt_clip = ImageClip("temp_txt.png").set_duration(time_per_image)
            clip = CompositeVideoClip([clip.set_position(('center', 'center')), txt_clip])
            
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose").set_audio(audio)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    audio.close(); final.close()

def upload_to_youtube(token, filename, title, desc, tags, category):
    print("🚀 YouTube par Upload ho raha hai...")
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": category}, 
              "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    ).execute()
    print("✅ Upload Success!")

def run_network():
    current_hour = datetime.utcnow().hour
    # Agar shaam 6 baje (18:00 UTC ke aas paas) run hota hai, to Long video banega
    is_long_video = True if current_hour in [17, 18, 19] else False
    vid_type_str = "LONG VIDEO" if is_long_video else "SHORTS"
    
    print(f"\n⚙️ Network Run Started! Mode: {vid_type_str}")
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels) # Har bar upload sequence alag hoga (Anti-spam)

    for ch_name in channels:
        try:
            config = CHANNELS_CONFIG[ch_name]
            if not config["token"]: continue
            
            hook = random.choice(config["hooks"])
            title, script, prompts, captions = get_ai_script(ch_name, hook, is_long_video)
            
            image_files = fetch_ai_images(prompts, is_long_video)
            create_voice(script, "temp_voice.mp3")
            
            out_file = f"{ch_name}_final.mp4"
            make_video(image_files, captions, out_file, "temp_voice.mp3", is_long_video)
            
            final_title = f"{title}" if is_long_video else f"{title[:70]} #shorts"
            final_desc = f"🔥 बेहतरीन किताबें और ज़रूरी प्रोडक्ट्स यहाँ से खरीदें: https://www.amazon.in/?tag=girishbhut07-21\n\n{script}"
            
            upload_to_youtube(config["token"], out_file, final_title, final_desc, config["tags"], config["category"])
            
            # Anti-Spam Gap between channels (5 to 10 minutes)
            delay = random.randint(300, 600)
            print(f"⏳ Agle channel ke liye {delay/60:.1f} minute ka wait...\n")
            time.sleep(delay)
            
        except Exception as e:
            print(f"❌ {ch_name} me Error: {e}")

if __name__ == "__main__":
    run_network()
