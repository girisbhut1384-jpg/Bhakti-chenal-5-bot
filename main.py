def create_centered_text_clip(text, duration):
    # कैप्शन्स के लिए एक सही चौड़ाई और ऊंचाई का पारदर्शी कैनवास बनाना
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try: 
        font = ImageFont.truetype("Roboto-Black.ttf", 110) # बोल्ड और साफ़ विज़िबिलिटी के लिए बड़ा फॉन्ट साइज़
    except: 
        font = ImageFont.load_default()
        
    # Alex Hormozi स्टाइल में शब्दों को छोटा और पंची रखने के लिए रैपिंग चौड़ाई कम की है
    wrapped_text = textwrap.fill(text.upper(), width=16) 
    
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped_text, font=font)
        
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    
    # चमकदार पीला रंग (#FFE81F) और बाहरी भारी काला स्ट्रोक (Outline) जोड़ना
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=14, stroke_fill="black", align='center')
    
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    
    return ImageClip(temp_filename).set_duration(duration)


def make_video(image_files, captions, final_vid, audio_file):
    print("🎬 Alex Hormozi स्टाइल में तेज़ और स्मूथ वीडियो रेंडर हो रहा है...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    
    # ⏱️ रफ़्तार नियम: हर तस्वीर स्क्रीन पर अधिकतम 2 सेकंड ही दिखेगी
    img_duration = 2.0 
    clips = []
    current_time = 0.0
    idx = 0
    
    # 🔄 लूपिंग लॉजिक: जब तक ऑडियो की अवधि पूरी नहीं होती, तस्वीरें बदलती और रिपीट होती रहेंगी
    while current_time < audio_duration:
        img_path = image_files[idx % len(image_files)]
        fixed_img_path = f"fixed_{idx}.jpg"
        process_image_for_video(img_path, fixed_img_path)
        
        # अंतिम क्लिप के लिए बची हुई अवधि की गणना करना ताकि वीडियो ऑडियो से लंबा न हो
        remaining_time = audio_duration - current_time
        current_clip_duration = min(img_duration, remaining_time)
        
        base_clip = ImageClip(fixed_img_path).set_duration(current_clip_duration)
        
        # 📈 ज़ूम इफ़ेक्ट: स्लाइडशो को डायनामिक बनाने के लिए निरंतर हल्का ज़ूम मोशन
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.06 * t)
        
        # सही कैप्शन चुनना और उसे रेंडर करना
        cap_text = captions[idx % len(captions)] if captions else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, current_clip_duration)
                # 📍 पोजीशन नियम: सबटाइटल्स को स्क्रीन के नीचे के हिस्से ('center', 0.8) पर सेट करना
                txt_clip = txt_clip.set_position(('center', 0.8), relative=True)
                
                final_clip = CompositeVideoClip(
                    [zoomed_clip.set_position(('center', 'center')), txt_clip], 
                    size=(1080, 1920)
                ).set_duration(current_clip_duration)
            except:
                final_clip = zoomed_clip
        else:
            final_clip = zoomed_clip
            
        # ✨ ट्रांज़िशन नियम: पहले क्लिप के बाद आने वाले सभी कट्स के बीच स्मूथ 'Crossfade' इफेक्ट लगाना
        if idx > 0:
            final_clip = final_clip.crossfadein(0.3)
            
        clips.append(final_clip)
        current_time += current_clip_duration
        idx += 1
        
    # सभी क्लिप्स को पैडिंग (Overlap) के साथ जोड़ना ताकि क्रॉसफ़ेड ट्रांज़िशन सही से काम करे
    video = concatenate_videoclips(clips, padding=-0.3, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    
    # 30 FPS पर वीडियो को एक्सपोर्ट करना ताकि विज़ुअल्स और कट्स एकदम मक्खन जैसे प्रोफेशनल लगें
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    
    # मेमोरी क्लीनअप करना
    main_audio.close()
    video.close()
    final.close()
