#!/usr/bin/env python3
"""plan.json -> video 1080x1920: A-roll + B-roll lớp phủ + caption động (ffmpeg/libass).

Dùng: python3 render.py work/plan.json -o out.mp4 [--preview 10] [--dry-run]
Caption được sinh lại mỗi lần render (gọi make_captions.py).
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from presets import PRESETS, W, H  # noqa: E402

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("-o", "--out", default="out.mp4")
    ap.add_argument("--preview", type=float, help="chỉ render N giây đầu")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true", help="in lệnh ffmpeg, không chạy")
    a = ap.parse_args()

    plan = json.load(open(a.plan, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.plan))
    P = {**PRESETS[plan["style"]], **plan.get("overrides", {})}
    path = lambda p: p if os.path.isabs(p) else os.path.join(base, p)  # noqa: E731

    ass_path = os.path.join(base, "captions.ass")
    subprocess.run([sys.executable, os.path.join(HERE, "make_captions.py"), a.plan, "-o", ass_path], check=True)

    cmd = ["ffmpeg", "-hide_banner", "-y", "-i", path(plan["video"])]
    fc = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={a.fps}[v0]"]
    last = "v0"
    card = P.get("broll_card", {"width": 0.8, "cy": 0.5})
    bg = P.get("broll_bg", "#D8D8D8").lstrip("#")

    for i, b in enumerate(plan.get("broll", [])):
        s, e = float(b["start"]), float(b["end"])
        dur = e - s
        src = path(b["file"])
        if os.path.splitext(src)[1].lower() in IMG_EXT:
            cmd += ["-loop", "1", "-t", f"{dur:.3f}", "-i", src]
        else:
            cmd += ["-ss", str(b.get("from", 0)), "-t", f"{dur:.3f}", "-i", src]
        n = i + 1
        mode = b.get("mode", "card")
        shift = f"setpts=PTS-STARTPTS+{s:.3f}/TB"
        if mode == "full":
            fc.append(f"[{n}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,{shift}[b{n}]")
            pos = "0:0"
        elif mode == "slide":   # ảnh/asset đặt giữa nền phẳng (V3: nền giấy xám)
            bw = int(W * 0.72)
            fc.append(f"[{n}:v]scale={bw}:{int(H * 0.45)}:force_original_aspect_ratio=decrease,"
                      f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0x{bg},setsar=1,{shift}[b{n}]")
            pos = "0:0"
        elif mode == "stamp":   # V2: tem có viền trắng (mép răng cưa/viền đứt làm tay)
            bw = int(W * b.get("width", 0.42))
            fc.append(f"[{n}:v]scale={bw}:-2,pad=iw+28:ih+28:14:14:color=white,setsar=1,{shift}[b{n}]")
            cy = b.get("cy", card["cy"])
            pos = f"(W-w)/2:{int(H * cy)}-h/2"
        else:                   # card: thẻ đè lên thân, chừa mặt
            bw = int(W * b.get("width", card["width"]))
            fc.append(f"[{n}:v]scale={bw}:{int(H * 0.5)}:force_original_aspect_ratio=decrease,setsar=1,{shift}[b{n}]")
            cy = b.get("cy", card["cy"])
            pos = f"(W-w)/2:{int(H * cy)}-h/2"
        fc.append(f"[{last}][b{n}]overlay={pos}:eof_action=pass:enable='between(t,{s:.3f},{e:.3f})'[v{n}]")
        last = f"v{n}"

    ass_esc = ass_path.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    fc.append(f"[{last}]ass='{ass_esc}'[vout]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "0:a?",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k"]
    if a.preview:
        cmd += ["-t", str(a.preview)]
    cmd.append(a.out)

    if a.dry_run:
        print(" ".join(f"'{c}'" if " " in c or ";" in c else c for c in cmd))
        return
    subprocess.run(cmd, check=True)
    print(f"rendered {a.out}")


if __name__ == "__main__":
    main()
