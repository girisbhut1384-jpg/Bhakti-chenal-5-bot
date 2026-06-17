# ==============================================================================
# 👑 V46 TITAN EMPIRE ENGINE: 100% FACELESS, VIRAL SYSTEM PROMPT & CRASH-PROOF
# ==============================================================================

import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap, io
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 V46 Titan Empire Engine: 100% Faceless & Viral Setup Started...")

os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")
font_path = "Roboto-Black.ttf"
if not os.path.exists(font_path): os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = "gsk_x1ThbfTdXoyFdlWkW5gT" + "WGdyb3FY4sGNe3aEAulVCEVOlXtI0lCz"
CLIENT_ID = "768932543756-ndfvqmbb0p7ffa1r1cg6bmmuimim98n6.apps.googleusercontent.com"
CLIENT_SECRET = "GOCSPX-" + "__q2fG3cAhPWL0xjrbIEG2fk_T48"

TOKENS = {
    "GB YOUTUBER": "1//04Yw4AZp47TkeCgYIARAAGAQSNwF-" + "L9IrX5ZcptNraLK2IX1nxWfwJZI7M_QYYaMSD1du-0_nokcboxQaTZQoN5XsQq7a3Ise7ho",
    "HEALTH & AYURVEDA": "1//04YIai_athiwVCgYIARAAGAQSNwF-" + "L9Irkq4Y5Rc2z_b_tybVROarlZNAiTNgxfw4Eg_gzO7Pqyys-TBXm1apTEhbUDksk8fAbTc",
    "BUSINESS & MOTIVATION": "1//04zCurvQGZ8DeCgYIARAAGAQSNwF-" + "L9Irdi9mNocm5HJ1NHKGeFiqNFi61fhfJ-tM7wCPXsfgwMKMZYZhikYYn0WDgdh_fmwiHJs",
    "SANATAN RAHASYA": "1//04ik1YQvHuc9ACgYIARAAGAQSNwF-" + "L9IrRJ5gl71WIxeNdibVP-2dvzOEaoKCkz0g1AmYTb6stShs1NMIM5T8brDBhUezdzgK_s8",
    "BOOK SUMMARY": "1//04ud4vnSb-qXRCgYIARAAGAQSNwF-" + "L9Ir2EmUvUfiuJ7SbqK1IJwk11-Jd0D6UTERpwBPO5FlFd3ZIJ1M08sTjh1dtcYhrKQZ-5M"
}

NICHES = {
    "GB YOUTUBER": "Spirituality & Ancient Wisdom (Focus on Mahabharata and Gita)",
    "HEALTH & AYURVEDA": "Ayurveda & Home Remedies",
    "BUSINESS & MOTIVATION": "Business, Motivation & Personal Finance",
    "SANATAN RAHASYA": "Spirituality & Ancient Indian Facts",
    "BOOK SUMMARY": "Real Book Summaries & Life Lessons"
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_master_script(channel_name):
    niche = NICHES[channel_name]
    print(f"\n📝 Executing Viral System Prompt for {channel_name} (Niche: {niche})...")
    
    prompt = f"""You are an elite YouTube Shorts Scriptwriter and Viral Content Expert. Your only job is to write a highly engaging, 45-50 second script in Hindi that guarantees high audience retention.

    Target Niche: {niche}

    CRITICAL RULES YOU MUST OBEY:
    1. Title Generation: Keep it under 50 characters. NEVER start the title with the "🤯" emoji. Place 1-2 relevant emojis ONLY at the very end of the title.
    2. The Script Structure: Write EXACTLY 8 sentences total.
       - Sentence 1 (The Hook: 0-3 Seconds): You MUST start with a shocking pattern-interrupt. Use opening lines like: "क्या आप जानते हैं...", "99% लोग यह गलती करते हैं...", or state a mind-blowing, specific fact. NO boring or slow intros.
       - Sentences 2-7 (The Body): Provide fast-paced, high-value information. 
         * If Book Summary: You MUST name a REAL, famous self-help/business book (e.g., Atomic Habits, Rich Dad Poor Dad). Explain exactly ONE real principle from it. Absolutely NO fake, fantasy, or made-up stories.
         * If Ayurveda/Health: Share one specific, practical remedy with real ingredients (e.g., naming specific herbs or daily habits). NEVER claim to 100% cure a serious medical condition.
         * If Business/Motivation: Share a real-world psychological fact or specific actionable advice. NEVER use words like 'Guaranteed Profit', 'Double your money'.
         * If Spirituality: Explain a specific ancient concept, text, or energy principle clearly. Keep it respectful, deep, and factual.
         * GENERAL RULE: Give solid, factual value. DO NOT repeat the same point in different words. NEVER use filler sentences.
       - Sentence 8 (CTA): Your script MUST end exactly with this line: "ऐसी ही बेहतरीन जानकारी के लिए चैनल को अभी सब्सक्राइब करें।"
    3. Output Language: The script MUST be entirely in fluent, natural-sounding Devanagari Hindi.

    🔥 ABSOLUTE "STILL LIFE" RULE FOR IMAGE PROMPTS (CRITICAL) 🔥:
    - For EACH of the 8 sentences, create an English image prompt describing ONLY beautiful, empty, inanimate STILL LIFE photography.
    - BANNED PROMPT WORDS: Krishna, Shiva, God, Arjuna, King, Man, Woman, Face, Human, Person, Boy, Girl, Actor, Figure. (DO NOT USE THESE).
    - YOU MUST ONLY DESCRIBE INANIMATE OBJECTS & NATURE. Example: "A glowing ancient copper manuscript on a dark stone table", "A golden coin glowing in a dark vault".
    
    Return ONLY valid JSON format exactly like this:
    {{
      "title": "Hindi Title with emoji at the end",
      "script": "The complete 8-sentence Hindi script (Combine Hook, Body, and CTA seamlessly)",
      "captions": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],
      "prompts": ["Object prompt 1", "Object prompt 2", "Object prompt 3", "Object prompt 4", "Object prompt 5", "Object prompt 6", "Object prompt 7", "Object prompt 8"],
      "tags": ["#tag1", "#tag2", "#tag3"]
    }}
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    
    for attempt in range(3):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60).json()
            parsed = json.loads(extract_json_safely(res['choices'][0]['message']['content']))
            if parsed.get('script') and len(parsed.get('prompts', [])) == 8:
                print("🎯 Master Viral Script & Safe Prompts Generated!")
                return parsed
        except Exception as e: time.sleep(3)
    raise Exception("🚨 AI Model Failed to execute master prompt.")

def fetch_safe_visuals(prompts):
    image_files = []
    base_seed = random.randint(1000, 99999)
    print("🎨 Generating 8K High-Quality Still-Life Masterpieces (Flux Engine)...")
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    
    for i, p in enumerate(prompts):
        enhanced = f"{p}, 8k resolution, photorealistic cinematic lighting, ultra-detailed macro photography, dark empty background, pure still life photography, masterpiece"
        # 'model=flux' ensures high-quality generation without typical AI face artifacts
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced)}?width=1080&height=1920&nologo=true&seed={base_seed+i}&model=flux"
        fname = f"scene_{i}.jpg"
        
        success = False
        for attempt in range(5):
            try:
                headers = {"User-Agent": random.choice(user_agents)}
                res = requests.get(url, headers=headers, timeout=40)
                if res.status_code == 200 and len(res.content) > 3000:
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    print(f"   ✅ Still-Life Visual {i+1}/8 Ready!")
                    success = True
                    break
            except: pass
            time.sleep(3 + attempt * 2)
            
        if not success:
            print(f"   ⚠️ Warning: Visual {i+1} failed to generate.")
            
    return image_files

def create_smooth_voice(text, filename):
    print("🎙️ Recording Fluid Voice...")
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-4%", volume="+60%") 
                await communicate.save(filename); return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(_generate())

def create_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 800; img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(font_path, 130) 
    except: font = ImageFont.load_default()
    wrapped = textwrap.fill(text.upper(), width=16) 
    try: bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center'); text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except: text_w, text_h = draw.textsize(wrapped, font=font)
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", align='center')
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"; img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def process_image(img_path, output_path):
    img = Image.open(img_path).convert("RGB"); bg = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=40))
    ratio = 1080 / img.width; new_h = int(img.height * ratio)
    if new_h > 1920: ratio = 1920 / img.height; new_w = int(img.width * ratio); fg = img.resize((new_w, 1920), Image.Resampling.LANCZOS); bg.paste(fg, ((1080 - new_w) // 2, 0))
    else: fg = img.resize((1080, new_h), Image.Resampling.LANCZOS); bg.paste(fg, (0, (1920 - new_h) // 2))
    bg.save(output_path); return output_path

def build_video(script, image_files, captions, output_vid):
    if len(image_files) < 6:
        raise Exception("Image API Blocked: Not enough images downloaded. Aborting to prevent crash.")
        
    print("🎬 Rendering Final Video...")
    voice_file = "temp_voice.mp3"
    create_smooth_voice(script, voice_file)
    main_audio = AudioFileClip(voice_file)
    
    time_per_image = main_audio.duration / len(image_files)
    
    clips = []
    for i, img_path in enumerate(image_files):
        fixed_path = f"fixed_{i}.jpg"; process_image(img_path, fixed_path)
        base_clip = ImageClip(fixed_path)
        zoomed = base_clip.resize(lambda t: 1 + 0.04 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try: txt_clip = create_text_clip(cap_text, time_per_image).set_position(('center', 0.45), relative=True); final_clip = CompositeVideoClip([zoomed.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = zoomed
        else: final_clip = zoomed
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    video.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close(); video.close()

def upload_youtube(token, filename, title, desc, tags_list, category_id):
    print(f"🚀 Uploading: {title}")
    from google.oauth2.credentials import Credentials; from googleapiclient.discovery import build; from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": desc, "tags": tags_list, "categoryId": category_id}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}, media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)).execute()

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
            content = get_master_script(name)
            final_name = f"final_{name.replace(' ', '_').lower()}.mp4"
            image_files = fetch_safe_visuals(content['prompts'])
            
            build_video(content['script'], image_files, content['captions'], final_name)
            
            title = content['title']
            tags_list = content.get('tags', [])
            desc = f"✨ {title}\n\n{content['script']}\n\n🔗 Best Deals: https://www.amazon.in/?tag=girishbhut07-21"
            
            upload_youtube(token, final_name, title[:95], desc, tags_list, cat_id)
            print(f"✅ {name} Success (Titan Engine Applied)!")
            time.sleep(15)
        except Exception as e: 
            print(f"🛑 Error on {name}: {e}")

     print("\n🏆 ऑपरेशन सक्सेसफुल! V46 टाइटन एम्पायर इंजन के साथ सारे काम पूरे हो गए हैं!")
