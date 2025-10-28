# Simple yt-dlp ripper script (CLI)
import sys, os, subprocess

if len(sys.argv)<2:
    print("Usage: python rip_crate.py <url>")
    sys.exit(1)

url=sys.argv[1]
outdir='out'
os.makedirs(outdir,exist_ok=True)
cmd=['yt-dlp','-x','--audio-format','mp3','-o',f'{outdir}/%(title)s.%(ext)s',url]
subprocess.run(cmd)
