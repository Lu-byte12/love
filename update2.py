import codecs
import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Update Google Fonts
new_fonts = '<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Pacifico&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">'
content = re.sub(r'<link\s+href="https://fonts.googleapis.com/css2\?family=.*?rel="stylesheet">', new_fonts, content, flags=re.DOTALL)

# 2. Replace fonts in CSS
# Replace 'Nunito' and 'Russo One' with 'Alfa Slab One' for headers
content = content.replace("'Nunito', sans-serif;", "'Alfa Slab One', cursive;")
content = content.replace("'Russo One', sans-serif;", "'Alfa Slab One', cursive;")
content = content.replace("font-family: 'Nunito'", "font-family: 'Outfit'") # Fix body back to Outfit
content = content.replace("font-family: 'Outfit', cursive;", "font-family: 'Outfit', sans-serif;") # Fix any mishap

# Replace 'Dancing Script' with 'Pacifico'
content = content.replace("'Dancing Script', cursive;", "'Pacifico', cursive;")

# Make sure body is Outfit for readability
content = re.sub(r'body\s*{[^}]*font-family:\s*[^;]+;', "body {\n            font-family: 'Outfit', sans-serif;", content)

# 3. Refine spacing and padding (Responsiveness)
# Increase section gaps slightly for breathing room
content = content.replace('--section-gap: clamp(60px, 8vw, 120px);', '--section-gap: clamp(80px, 10vw, 150px);')
content = content.replace('padding: clamp(24px, 4vw, 48px);', 'padding: clamp(32px, 6vw, 64px);')
content = content.replace('padding: clamp(32px, 5vw, 60px) clamp(40px, 8vw, 100px);', 'padding: clamp(40px, 6vw, 80px) clamp(30px, 5vw, 60px);')
content = content.replace('gap: clamp(16px, 3vw, 32px);', 'gap: clamp(24px, 4vw, 48px);')

# Fix nav button for mobile
nav_css = """
        .nav-inner {
            display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;
"""
content = content.replace('.nav-inner {\n            display: flex;\n            align-items: center;\n            justify-content: space-between;', nav_inner_clean := '.nav-inner {\n            display: flex;\n            align-items: center;\n            justify-content: space-between;\n            flex-wrap: wrap;\n            gap: 12px;')

music_btn_css = """
            margin-left: 20px;
            margin-right: auto;
"""
# Make the music button look better on mobile (no huge margins)
content = content.replace(music_btn_css, "            margin: 0 10px;\n")

# 4. Fix YouTube Player (change ID to lyric video which is embeddable, and fix styles)
# Replace the old YT script
yt_old_start = '<!-- YouTube Player (Hidden) -->'
yt_old_end = '</script>'
# We will use regex to replace the entire old yt block
yt_new = """<!-- YouTube Player (Hidden) -->
    <div id="yt-player" style="position: absolute; top: 0; left: 0; width: 1px; height: 1px; opacity: 0; pointer-events: none;"></div>
    <script src="https://www.youtube.com/iframe_api"></script>
    <script>
        let ytPlayer;
        let isMusicPlaying = false;
        
        function onYouTubeIframeAPIReady() {
            ytPlayer = new YT.Player('yt-player', {
                height: '100',
                width: '100',
                videoId: 'q6j74Wd9Zt0', // Zoé - Luna Lyric Video (More likely to allow embedding)
                playerVars: {
                    'autoplay': 0,
                    'controls': 0,
                    'showinfo': 0,
                    'rel': 0,
                    'loop': 1,
                    'playlist': 'q6j74Wd9Zt0'
                },
                events: {
                    'onReady': function(event) {
                        const btn = document.getElementById('music-btn');
                        if(btn) {
                            btn.addEventListener('click', () => {
                                if (isMusicPlaying) {
                                    ytPlayer.pauseVideo();
                                    isMusicPlaying = false;
                                    btn.classList.remove('playing');
                                    btn.innerHTML = '🎵 Para más placer (Musiquita)';
                                } else {
                                    ytPlayer.playVideo();
                                    isMusicPlaying = true;
                                    btn.classList.add('playing');
                                    btn.innerHTML = '⏸️ Pausar musiquita';
                                }
                            });
                        }
                    },
                    'onError': function(event) {
                        console.error('YouTube Player Error:', event.data);
                        // Fallback to another video if blocked
                        if(event.data === 101 || event.data === 150) {
                            ytPlayer.loadVideoById('k-V3yN22v8g'); // Studio version
                        }
                    }
                }
            });
        }
    </script>"""

content = re.sub(r'<!-- YouTube Player \(Hidden\) -->.*?<\/script>\s*<\/script>', yt_new, content, flags=re.DOTALL)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
