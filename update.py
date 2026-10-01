import codecs
import re

with codecs.open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace fonts
content = content.replace('Orbitron:wght@400;500;600;700;800;900&family=Russo+One&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400', 'Nunito:wght@400;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800')
content = content.replace("'Orbitron'", "'Outfit'")
content = content.replace("'Russo One'", "'Nunito'")
content = content.replace("'Poppins'", "'Nunito'")

# Soften borders
content = content.replace('--radius-sm: 8px;', '--radius-sm: 12px;')
content = content.replace('--radius-md: 16px;', '--radius-md: 20px;')
content = content.replace('--radius-lg: 24px;', '--radius-lg: 32px;')
content = content.replace('--radius-xl: 32px;', '--radius-xl: 48px;')

# Soften colors
content = content.replace('--hw-darker: #040810;', '--hw-darker: #0a111a;')
content = content.replace('--hw-dark: #070D1A;', '--hw-dark: #0f1926;')

# Add music button to nav
nav_replace = '<div class="nav-inner">\n                <a href="#" class="nav-logo">🏎️ HW × AMOR</a>\n                <button id="music-btn" class="music-btn">🎵 Para más placer (Musiquita)</button>'
content = re.sub(r'<div class="nav-inner">\s*<a href="#" class="nav-logo">.*?</a>', nav_replace, content)

# Add music button CSS
css_to_add = '''
        .music-btn {
            background: linear-gradient(135deg, rgba(0,102,255,0.2), rgba(0,229,255,0.2));
            border: 1px solid rgba(0,229,255,0.4);
            border-radius: 50px;
            padding: 8px 16px;
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
            margin-left: 20px;
            margin-right: auto;
        }
        .music-btn:hover {
            background: rgba(0,229,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,229,255,0.3);
        }
        .music-btn.playing {
            border-color: var(--hw-green-bright);
            box-shadow: 0 0 15px rgba(0,230,118,0.4);
            animation: pulse-soft 2s infinite;
        }
        @keyframes pulse-soft {
            0% { box-shadow: 0 0 10px rgba(0,230,118,0.4); }
            50% { box-shadow: 0 0 25px rgba(0,230,118,0.7); }
            100% { box-shadow: 0 0 10px rgba(0,230,118,0.4); }
        }
'''
content = content.replace('/* ============================================================', css_to_add + '\n        /* ============================================================', 1)

# Add YouTube API and div
yt_html = '''
    <!-- YouTube Player (Hidden) -->
    <div id="yt-player" style="position: absolute; top: -9999px; left: -9999px;"></div>
    <script src="https://www.youtube.com/iframe_api"></script>
    <script>
        let ytPlayer;
        let isMusicPlaying = false;
        
        function onYouTubeIframeAPIReady() {
            ytPlayer = new YT.Player('yt-player', {
                height: '10',
                width: '10',
                videoId: 'YtQS26joHWo', // Zoé - Luna MTV Unplugged
                playerVars: {
                    'autoplay': 0,
                    'controls': 0,
                    'showinfo': 0,
                    'rel': 0,
                    'loop': 1,
                    'playlist': 'YtQS26joHWo'
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
                    }
                }
            });
        }
    </script>
'''
content = content.replace('<!-- ============================================================', yt_html + '\n    <!-- ============================================================', 1)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
