import codecs
import re

with codecs.open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace fonts link using regex to avoid newline issues
new_fonts = '<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Pacifico&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">'
content = re.sub(r'<link\s+href="https://fonts\.googleapis\.com/css2\?family=[^"]+"\s+rel="stylesheet">', new_fonts, content)

# Fix CSS rules that didn't get updated in the previous run
content = content.replace("'Orbitron'", "'Alfa Slab One'")
content = content.replace("'Russo One'", "'Alfa Slab One'")
content = content.replace("'Poppins'", "'Outfit'")
content = content.replace("'Dancing Script'", "'Pacifico'")

# Ensure body uses Outfit
content = re.sub(r'body\s*{[^}]*font-family:\s*[^;]+;', "body {\n            font-family: 'Outfit', sans-serif;", content)

# Fix music button
old_yt = r'<!-- YouTube Player \(Hidden\) -->.*?</script>\s*</script>'
new_yt = """<!-- YouTube Player (Fallback to standard iframe for file:// support) -->
    <iframe id="yt-player-iframe" width="10" height="10" style="position: absolute; top: 0; left: 0; opacity: 0; pointer-events: none;" src="" frameborder="0" allow="autoplay; encrypted-media"></iframe>
    <script>
        let isMusicPlaying = false;
        const ytIframe = document.getElementById('yt-player-iframe');
        const btn = document.getElementById('music-btn');
        
        if(btn) {
            btn.addEventListener('click', () => {
                if (isMusicPlaying) {
                    ytIframe.src = "";
                    isMusicPlaying = false;
                    btn.classList.remove('playing');
                    btn.innerHTML = '🎵 Para más placer (Musiquita)';
                } else {
                    // Load the lyric video with autoplay
                    ytIframe.src = "https://www.youtube.com/embed/q6j74Wd9Zt0?autoplay=1&loop=1&playlist=q6j74Wd9Zt0";
                    isMusicPlaying = true;
                    btn.classList.add('playing');
                    btn.innerHTML = '⏸️ Pausar musiquita';
                }
            });
        }
    </script>"""

content = re.sub(old_yt, new_yt, content, flags=re.DOTALL)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
