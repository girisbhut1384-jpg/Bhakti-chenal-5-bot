import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime, timedelta

# --- PIL & MOVIEPY SETUP ---
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import urllib.request

print("🔥 V22: 100% Viral Match & Human Voice Engine Active!")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

font_path = "NotoSansDevanagari-Bold.ttf"

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-hvbk02bm5avqesa1649892ufb73v11mq.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# 🟢 एनाटॉमी और क्वालिटी फिल्टर (इमेज खराब होने से रोकने के लिए)
ANATOMY_FILTER = "anatomically correct, flawless face, perfectly drawn hands, symmetrical body, hyper-realistic, no deformities, clear facial features, 8k resolution, cinematic lighting"

CHANNELS_CONFIG = {
    "GB_YOUTUBER": {"token": os.environ.get("TOKEN_GBYOUTUBER"), "category": "22", "tags": ["bhakti", "krishna", "motivation"], "style": f"wide angle cinematic, {ANATOMY_FILTER}", "hooks": ["श्री कृष्ण का सबसे बड़ा चमत्कार", "गीता का वह रहस्य जो कोई नहीं जानता", "महाभारत का सबसे गुप्त पात्र"]},
    "HEALTH_AYURVEDA": {"token": os.environ.get("TOKEN_HEALTH"), "category": "26", "tags": ["health", "ayurveda", "fitness"], "style": f"hyper-realistic nature, {ANATOMY_FILTER}", "hooks": ["आयुर्वेद का 1 गुप्त नियम", "गर्म पानी पीने के असली फायदे", "रात को दही खाने का सच"]},
    "SUCCESS_BUSINESS": {"token": os.environ.get("TOKEN_SUCCESS"), "category": "27", "tags": ["business", "motivation", "success"], "style": f"professional corporate photography, {ANATOMY_FILTER}", "hooks": ["रतन टाटा की सफलता का राज", "चाणक्य नीति के कड़वे सच", "अमीर बनने का गुप्त फॉर्मूला"]},
    "SANATAN_RAHASYA": {"token": os.environ.get("TOKEN_SANATAN"), "category": "24", "tags": ["rahasya", "mythology", "history"], "style": f"dark mysterious cinematic, {ANATOMY_FILTER}", "hooks": ["कैलाश पर्वत का अनसुलझा रहस्य", "समुद्र मंथन का असली सच", "पाताल लोक का द्वार"]},
    "BOOK_SUMMARIES": {"token": os.environ.get("TOKEN_BOOK"), "category": "27", "tags": ["books", "summary", "learning"], "style": f"cinematic inspiring environment, {ANATOMY_FILTER}", "hooks": ["Atomic Habits की सबसे बड़ी सीख", "Rich Dad Poor Dad का कड़वा सच", "Psychology of Money का जादू"]}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_scene_script(channel_name, hook_theme, is_long_video=False):
    print(f"\n📝 {channel_name} के लिए वायरल स्क्रिप्ट तैयार हो रही है...")
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rand_id = random.randint(100000, 999999)
    
    word_limit = "400 to 550" if is_long_video else "65 to 95"
    scene_count = 15 if is_long_video else 5

    # 🟢 मास्टर प्रॉम्प्ट: जो वीडियो को वायरल और सटीक बनाएगा
    prompt = f"""[SYSTEM SEED: {current_time_str} - {rand_id}]
तुम एक वर्ल्ड-क्लास YouTube Shorts और Documentary स्क्रिप्ट राइटर हो। तुम्हारा काम '{channel_name}' चैनल के लिए एक ऐसी कहानी लिखना है जो पहले 3 सेकंड में ही दर्शक को पकड़ ले।
विषय (Theme): "{hook_theme}"

सख्त निर्देश:
1. कहानी: रहस्यमयी या इमोशनल कहानी सुनाओ। शुरुआत एक बड़े सवाल या चौंकाने वाले सच से करें।
2. आवाज़: 'text' फील्ड में देवनागरी हिंदी का प्रयोग करें। हर वाक्य के बाद कॉमा (,) लगाएं ताकि आवाज प्राकृतिक लगे।
3. इमेज मैचिंग: 'prompt' फील्ड में वर्णन केवल ENGLISH में करें। किरदार का नाम (e.g. Lord Krishna, Ratan Tata) साफ लिखें। इमेज में कोई टेक्स्ट न हो।
4. कैप्शन: 'caption' में केवल 2-3 शब्द लिखें।
5. शब्द सीमा: पूरी कहानी {word_limit} शब्दों के बीच होनी चाहिए।

JSON STRUCTURE:
{{
  "title": "Viral Hindi Title",
  "scenes": [
    {{"text": "हिंदी कहानी यहाँ लिखे...", "caption": "कैप्शन", "prompt": "Detailed English visual prompt..."}}
  ]
}}
कुल दृश्य: {scene_count}. अंत में 'ऐसी ही अद्भुत जानकारी के लिए चैनल को अभी सब्सक्राइब करें।' अनिवार्य है।"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    
    for _ in range(5):
        try:
            res = requests.post(url, headers=headers, json=data, timeout=60)
            if res.status_code == 200:
                parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
                if parsed.get('scenes'): 
                    full_text = " ".join([s.get('text', '') for s in parsed['scenes']])
                    word_count = len(full_text.split())
                    # फ्लेक्सिबल वैलिडेशन ताकि रिजेक्शन लूप न बने
                    min_w = 300 if is_long_video else 45
                    max_w = 650 if is_long_video else 120
                    if word_count < min_w or word_count > max_w:
                        print(f"⚠️ [रिजेक्ट] शब्द सीमा ({word_count}) बाहर है। दोबारा प्रयास...")
                        time.sleep(5); continue
                    return parsed
            time.sleep(5)
        except: time.sleep(5)
    raise Exception("AI Scripting Failed")

def download_single_image(idx, p, style_filter, w, h):
    seed = random.randint(1000000, 9999999)
    enhanced_prompt = f"{p}, {style_filter}"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}?width={w}&height={h}&nologo=true&enhance=true&seed={seed}"
    fname = f"scene_{idx}.jpg"
    for _ in range(4):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            if r.status_code == 200 and len(r.content) > 10000:
                with open(fname, "wb") as f: f.write(r.content)
                Image.open(fname).verify(); return fname
        except: pass
        time.sleep(2)
    return None

def fetch_all_images_safe(scenes, style_filter, is_long_video):
    print("🎨 कहानी से मैच करती हुई तस्वीरें जनरेट हो रही हैं...")
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    valid_images, valid_scenes = [], []
    for i, s in enumerate(scenes):
        img_path = download_single_image(i, s.get('prompt', 'Cinematic background'), style_filter, w, h)
        if img_path:
            valid_images.append(img_path)
            valid_scenes.append(s)
    if not valid_images: raise Exception("Image Generation Failed")
    return valid_images, valid_scenes

def create_human_voice(text, filename):
    print("🎙️ मधुर और स्पष्ट हिंदी आवाज़ तैयार हो रही है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+0%", volume="+50%") 
        await communicate.save(filename)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def create_text_clip(caption_text, duration, is_long_video):
    w, h = (1920, 1080) if is_long_video else (1080, 1920)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fsize = 100 if is_long_video else 150
    try: font = ImageFont.truetype(font_path, fsize)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(caption_text, width=30 if is_long_video else 15)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    
    x, y = (w - tw) // 2, int(h * 0.8) if is_long_video else int(h * 0.65)
    # टेक्स्ट शैडो और बॉर्डर के साथ
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", align='center')
    
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_video(image_files, scenes, output_vid, audio_file, is_long_video):
    print(f"🎬 वीडियो रेंडरिंग शुरू: {'LONG' if is_long_video else 'SHORTS'}")
    main_audio = AudioFileClip(audio_file)
    dur_per_scene = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        base = ImageClip(img_path).set_duration(dur_per_scene).set_position('center')
        # हल्का ज़ूम इफ़ेक्ट (Ken Burns)
        zoom = base.resize(lambda t: 1 + 0.03 * (t/dur_per_scene))
        txt = create_text_clip(scenes[i].get('caption', 'WATCH NOW'), dur_per_scene, is_long_video)
        clips.append(CompositeVideoClip([zoom, txt.set_position(('center', 'center'))]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(output_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    main_audio.close(); final.close()

def upload_video(token, filename, title, description, tags, category):
    print(f"🚀 YouTube पर धमाका करने के लिए तैयार: {title}")
    try:
        creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
        youtube = build("youtube", "v3", credentials=creds)
        request = youtube.videos().insert(
            part="snippet,status",
            body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public"}},
            media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
        )
        request.execute()
        print("✅ सफलता! वीडियो लाइव हो गया है।")
    except Exception as e: print(f"❌ अपलोड फेल: {e}")

def run_network():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    is_long = True if ist_now.hour in [18, 19, 20] else False # शाम को लॉन्ग वीडियो
    
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    
    for ch_name in channels:
        cfg = CHANNELS_CONFIG[ch_name]
        try:
            data = get_scene_script(ch_name, random.choice(cfg['hooks']), is_long)
            imgs, valid_scenes = fetch_all_images_safe(data['scenes'], cfg['style'], is_long)
            
            full_txt = " ".join([s.get('text', '') for s in valid_scenes])
            create_human_voice(full_txt, "v.mp3")
            
            out = f"{ch_name}_final.mp4"
            assemble_video(imgs, valid_scenes, out, "v.mp3", is_long)
            
            title = data.get('title', 'Viral Video') if is_long else f"{data.get('title', 'Viral')[:70]} #shorts"
            desc = f"{full_txt}\n\n🔥 Best Deals: https://www.amazon.in/?tag=girishbhut07-21"
            
            upload_video(cfg['token'], out, title, desc, cfg['tags'], cfg['category'])
            time.sleep(20) # रेट लिमिट से बचाव
        except Exception as e: print(f"🛑 {ch_name} में गड़बड़: {e}")

if __name__ == "__main__": 
    run_network()

