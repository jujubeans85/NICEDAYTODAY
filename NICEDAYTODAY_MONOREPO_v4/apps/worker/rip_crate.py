# Batch ripper for CrateJuice
import os, subprocess

urls_file = 'urls.txt'
outdir = 'tracks'
os.makedirs(outdir, exist_ok=True)

if not os.path.exists(urls_file):
    print("Add your links to urls.txt, one per line.")
    exit(1)

with open(urls_file) as f:
    urls = [l.strip() for l in f if l.strip()]

for url in urls:
    print("Ripping:", url)
    cmd = ['yt-dlp','-x','--audio-format','mp3','-o',f'{outdir}/%(title)s.%(ext)s',url]
    subprocess.run(cmd)
