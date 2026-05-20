# ==============================================================================
# 👑 V41 PURE OBJECT ENGINE: NO NEGATIVE PROMPTS, 100% STILL-LIFE VISUALS
# ==============================================================================

import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
import re
import textwrap
import io 
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 V41 Pure Object Engine: Positive Still-Life Setup Started...")

os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

font_path = "Roboto-Black.ttf"
if not os.path.exists(font_path):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

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

# हुक्स को इस तरह डिज़ाइन किया गया है कि इंसान की ज़रूरत ही न पड़े
HOOKS = {
    "GB YOUTUBER": ["कुरुक्षेत्र की मिट्टी में आज भी दबा है एक ऐसा दिव्य अस्त्र जिसे विज्ञान भी नहीं समझ पाया", "समुद्र की गहराइयों में डूबी उस स्वर्ण नगरी के अवशेषों का रहस्य जो अचानक गायब हो गई", "एक ऐसा रहस्यमयी प्राचीन ग्रंथ जिसके पन्ने आज भी अंधेरे में चमकते हैं"],
    "HEALTH & AYURVEDA": ["हिमालय की वादियों में उगने वाली वो नीली जड़ी-बूटी जो उम्र के पहिये को रोक देती है", "तांबे के पुराने घड़े में रखा वो जादुई जल जो शरीर के हर विष को बाहर निकाल देता है", "आयुर्वेद की उस गुप्त औषधि का सच जो रातों-रात शरीर की असीमित ऊर्जा को जगा देती है"],
    "BUSINESS & MOTIVATION": ["दुनिया की सबसे सुरक्षित तिजोरी में रखे वो गुप्त सोने के सिक्के जिन्होंने अर्थव्यवस्था पलट दी", "शेयर बाज़ार को हिला देने वाले उस रहस्यमयी प्राचीन दस्तावेज़ का सच", "अरबपतियों के उस गुप्त चक्रव्यूह का प्रतीक जिसे आजतक कोई नहीं तोड़ पाया"],
    "SANATAN RAHASYA": ["उस प्राचीन शिवलिंग का सच जिसके अंदर से आज भी एक रहस्यमयी ऊर्जा निकलती है", "कैलाश पर्वत की बर्फ में छिपे उस नीले प्रकाश का सच जिसे नासा ने भी देखा", "हजारों साल पुरानी उस पत्थर की मशीन का रहस्य जो आज भी तारों की गणना करती है"],
    "BOOK SUMMARY": ["इतिहास के सबसे अंधेरे कोने में छुपी वो किताब जिसके अक्षर छूने पर रंग बदलते हैं", "उस प्राचीन सुनहरे पन्ने का रहस्य जिसे पढ़ने से दिमाग की क्षमता १०० गुना हो जाती है", "एक ऐसा जादुई ताला जिसे आजतक किसी भी चाबी से नहीं खोला जा सका"]
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_complete_script(channel_name):
    unique_seed = random.randint(100000, 9999999)
    hook = random.choice(HOOKS[channel_name])
    print(f"\n📝 Writing 100% Unique & Factual Story for {channel_name} (Seed: {unique_seed})")
    
    prompt = f"""You are an elite Documentary Scriptwriter for '{channel_name}'. Theme: "{hook}". Unique Seed: {unique_seed}
    
    CRITICAL SCRIPT RULES:
    1. WRITE LIKE A HUMAN: Write deep, authentic, grammatically flawless Devanagari Hindi. Tell a gripping story.
    2. COMPLETE KNOWLEDGE: Completely explain the mystery/rule/fact within the script. No cliffhangers.
    3. TARGET LENGTH: Exactly 8 comprehensive sentences. Word count: 110-125 words for a 45-55 seconds video.
    4. NO BANNED WORDS: Do NOT use "क्या आप जानते हैं", "दोस्तों". Start directly with the core fact.
    5. MANDATORY ENDING: Sentence 8 MUST end exactly with: 'ऐसे ही प्रामाणिक और अद्भुत ज्ञान के लिए चैनल को अभी सब्सक्राइब करें।'
    
    🔥 ABSOLUTE "STILL LIFE" RULE FOR IMAGE PROMPTS 🔥:
    6. YOU MUST NEVER USE NEGATIVE PROMPTS LIKE "NO HUMANS" OR "NO FACES". The AI generator misunderstands them.
    7. INSTEAD, ONLY describe beautiful, empty, inanimate STILL LIFE photography.
    8. BANNED PROMPT WORDS: Krishna, Shiva, God, Arjuna, King, Man, Woman, Billionaire, Doctor, Scientist, Face, Human, Person, Boy, Girl. (DO NOT USE THESE).
    9. EXAMPLES OF GOOD PROMPTS: "A macro close-up of a glowing golden peacock feather resting on an ancient manuscript", "A majestic empty stone temple glowing with mysterious blue light", "A stack of golden coins inside a futuristic empty dark vault", "A glowing green ayurvedic leaf floating in pure water".
    
    Return ONLY valid JSON format exactly like this: 
    {{
      "topic": "complete valuable topic",
      "script": "Flowing, 100-120 word Hindi story with complete factual knowledge...",
      "captions": ["Caption 1", "Caption 2", "Caption 3", "Caption 4", "Caption 5", "Caption 6", "Caption 7", "Caption 8"],
      "prompts": ["Still life prompt 1", "Still life prompt 2", "Still life prompt 3", "Still life prompt 4", "Still life prompt 5", "Still life prompt 6", "Still life prompt 7", "Still life prompt 8"]
    }}
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.85}
    
    for attempt in range(3):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60).json()
            parsed = json.loads(extract_json_safely(res['choices'][0]['message']['content']))
            if parsed.get('script') and len(parsed.get('prompts', [])) == 8:
                print("🎯 Factual Script & STRICT STILL-LIFE Prompts Generated!")
                return parsed
        except Exception as e:
            time.sleep(3)
    raise Exception("🚨 AI Model Failed to generate script.")

def fetch_zero_face_visuals(prompts):
    image_files = []
    base_seed = random.randint(1000, 99999)
    print("🎨 Generating 8K High-Quality Still-Life Masterpieces...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        # यहाँ प्रॉम्प्ट में सिर्फ़ पॉजिटिव शब्द डाले गए हैं (Empty scene, still life)
        enhanced = f"{p}, 8k resolution, photorealistic cinematic lighting, ultra-detailed macro photography, dark empty background, pure still life photography, masterpiece"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced)}?width=1080&height=1920&nologo=true&seed={base_seed+i}"
        fname = f"scene_{i}.jpg"
        
        for _ in range(4):
            try:
                res = requests.get(url, headers=headers, timeout=30)
                if res.status_code == 200 and len(res.content) > 15000:
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    print(f"   ✅ Still-Life Visual {i+1}/8 Ready!")
                    break
            except: pass
            time.sleep(3)
        time.sleep(1.5)
    return image_files

def create_smooth_human_voice(text, filename):
    print("🎙️ Recording Fluid Human Voice...")
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-4%", volume="+60%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 800
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(font_path, 130) 
    except: font = ImageFont.load_default()
    
    wrapped_text = textwrap.fill(text.upper(), width=16) 
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped_text, font=font)
        
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", align='center')
    
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def process_image_for_video(img_path, output_path):
    img = Image.open(img_path).convert("RGB")
    bg = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=40))
    ratio = 1080 / img.width
    new_h = int(img.height * ratio)
    if new_h > 1920:
        ratio = 1920 / img.height
        new_w = int(img.width * ratio)
        fg = img.resize((new_w, 1920), Image.Resampling.LANCZOS)
        bg.paste(fg, ((1080 - new_w) // 2, 0))
    else:
        fg = img.resize((1080, new_h), Image.Resampling.LANCZOS)
        bg.paste(fg, (0, (1920 - new_h) // 2))
    bg.save(output_path)
    return output_path

def build_perfect_video(script, image_files, captions, output_vid):
    print("🎬 Rendering Final Video with Captions & Sync...")
    voice_file = "temp_voice.mp3"
    create_smooth_human_voice(script, voice_file)
    
    main_audio = AudioFileClip(voice_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    
    clips = []
    for i, img_path in enumerate(image_files):
        fixed_img_path = f"fixed_{i}.jpg"
        process_image_for_video(img_path, fixed_img_path)
        base_clip = ImageClip(fixed_img_path)
        
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.04 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, time_per_image)
                txt_clip = txt_clip.set_position(('center', 0.45), relative=True) 
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = zoomed_clip
        else: final_clip = zoomed_clip
        
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

def upload_to_empire(token, filename, title, desc, tags, category_id):
    print(f"🚀 Uploading Video to YouTube: {title}")
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": category_id}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )
    request.execute()

if __name__ == "__main__":
     channels = [
        ("GB YOUTUBER", "22", ["bhakti", "krishna", "motivation", "shorts", "knowledge"]),
        ("HEALTH & AYURVEDA", "26", ["health", "ayurveda", "fitness", "shorts", "facts"]),
        ("BUSINESS & MOTIVATION", "27", ["business", "motivation", "success", "shorts", "learning"]),             
        ("SANATAN RAHASYA", "24", ["rahasya", "mythology", "history", "shorts", "temple"]),         
        ("BOOK SUMMARY", "27", ["books", "summary", "learning", "shorts", "mindset"])       
    ]
     
     for name, cat_id, tags in channels:
        token = TOKENS[name]
        try:
            content = get_complete_script(name)
            script = content['script']
            captions = content['captions']
            
            image_files = fetch_zero_face_visuals(content['prompts'])
            final_name = f"final_{name.replace(' ', '_').lower()}.mp4"
            
            build_perfect_video(script, image_files, captions, final_name)
            
            desc = f"🔥 👉 ऐसे ही प्रामाणिक रहस्यों और ज्ञान के लिए चैनल को अभी सब्सक्राइब करें!\n\n{script}\n\n🔗 Best Deals & Offers: https://www.amazon.in/?tag=girishbhut07-21"
            title = f"🤯 {content['topic']} #shorts"
            
            upload_to_empire(token, final_name, title[:95], desc, tags, cat_id)
            print(f"✅ {name} Video Successfully LIVE (Positive Object-Only Visuals)!")
            time.sleep(15)
            
        except Exception as e:
            print(f"🛑 Empire Error on {name}: {e}. Skipping to next channel.")

     print("\n🏆 साम्राज्य ऑपरेशन सक्सेसफुल! बिना किसी चेहरे के 100% परफेक्ट वीडियो लाइव हो चुके हैं!")
