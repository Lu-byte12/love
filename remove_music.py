import codecs
import re

with codecs.open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Remove music-btn HTML
content = re.sub(r'\s*<button id="music-btn"[^>]*>.*?</button>', '', content)

# 2. Remove music-btn CSS
# Match from .music-btn { to the end of the @keyframes pulse-soft block
css_pattern = r'\s*\.music-btn\s*\{.*?\s*\}\s*\.music-btn:hover\s*\{.*?\s*\}\s*\.music-btn\.playing\s*\{.*?\s*\}\s*@keyframes\s*pulse-soft\s*\{.*?\s*\}'
content = re.sub(css_pattern, '', content, flags=re.DOTALL)

# 3. Remove YouTube Player HTML and Script
# Because the user format could vary (Iframe API or the fallback I added), 
# I will match anything from <!-- YouTube Player to the end of that script.
yt_pattern = r'\s*<!-- YouTube Player.*?</script>\s*</script>'
content = re.sub(yt_pattern, '', content, flags=re.DOTALL)
yt_pattern_single = r'\s*<!-- YouTube Player.*?</script>'
content = re.sub(yt_pattern_single, '', content, flags=re.DOTALL)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Button and scripts removed")
