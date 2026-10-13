#!/usr/bin/env python3
"""plan.json + words.json -> captions.ass (caption động theo preset).

Dùng: python3 make_captions.py work/plan.json -o work/captions.ass
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from presets import PRESETS, W, H, ass_color  # noqa: E402

PUNCT_END = re.compile(r"[.,!?;:…]$")


def norm(w):
    return re.sub(r"[^\w$%]", "", w.lower())


def esc(text):
    return text.replace("{", "(").replace("}", ")").replace("\\", "/")


def ts(t):
    t = max(t, 0)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def load_words(path):
    data = json.load(open(path, encoding="utf-8"))
    words = data["words"] if isinstance(data, dict) else data
    out = [{"word": w["word"].strip(), "start": float(w["start"]), "end": float(w["end"])}
           for w in words if w["word"].strip()]
    return out


def chunk_words(words, max_words, gap=0.35, cuts=()):
    """Tách cụm: đủ số từ, ngắt nghỉ > gap, hết câu, hoặc có cảnh B-roll toàn màn bắt đầu."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cut_between = cur and any(cur[-1]["start"] < c <= w["start"] for c in cuts)
        if cur and (len(cur) >= max_words or w["start"] - cur[-1]["end"] > gap
                    or PUNCT_END.search(cur[-1]["word"]) or cut_between):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def pick_keyword(chunk, wanted, auto):
    for i, w in enumerate(chunk):
        if norm(w["word"]) in wanted:
            return i
    if not auto or len(chunk) < 2:
        return 0 if (auto and len(chunk) == 1) else None

    def score(w):
        t = w["word"]
        return (3 if re.search(r"\d", t) else 0) + (2 if t[:1].isupper() and t.upper() == t and len(t) > 1 else 0) \
            + min(len(norm(t)), 10) / 3
    best = max(range(len(chunk)), key=lambda i: score(chunk[i]))
    return best if len(norm(chunk[best]["word"])) >= 4 or re.search(r"\d", chunk[best]["word"]) else None


class Ass:
    def __init__(self):
        self.styles, self.events = [], []

    def style(self, name, font, size, color, bold=False, italic=False, outline=0, outline_color="#000000",
              border_style=1, shadow=0, back="#000000", back_alpha=160):
        self.styles.append(
            f"Style: {name},{font},{size},{ass_color(color)},{ass_color(color)},{ass_color(outline_color)},"
            f"{ass_color(back, back_alpha)},{-1 if bold else 0},{-1 if italic else 0},0,0,100,100,0,0,"
            f"{border_style},{outline},{shadow},5,0,0,0,1")

    def ev(self, start, end, text, style="Default", layer=1):
        if end - start < 0.01:
            return
        self.events.append(f"Dialogue: {layer},{ts(start)},{ts(end)},{style},,0,0,0,,{text}")

    def dump(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nWrapStyle: 2\n"
                    "ScaledBorderAndShadow: yes\n\n" % (W, H))
            f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
                    "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, "
                    "Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
            f.write("\n".join(self.styles) + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, "
                    "MarginR, MarginV, Effect, Text\n")
            f.write("\n".join(self.events) + "\n")


def entry_tags(in_ms, blur, scale=100):
    """Tag animation vào: alpha 0->100%, blur->0, scale->100."""
    if in_ms <= 0:
        return ""
    t = f"\\alpha&HFF&\\blur{blur}"
    end = "\\alpha&H00&\\blur0"
    if scale != 100:
        t += f"\\fscx{scale}\\fscy{scale}"
        end += "\\fscx100\\fscy100"
    return f"{t}\\t(0,{in_ms},0.5,{end})"  # accel 0.5 = ease-out


def flicker_tags():
    # bật 80ms, tắt 40ms ×3 rồi giữ (đo từ V4: ~320ms)
    seq, t, on = "\\alpha&H00&", 0, True
    for d in (80, 40, 80, 40, 40, 40):
        t += d
        on = not on
        seq += f"\\t({t},{t + 1},\\alpha&H{'00' if on else 'FF'}&)"
    return seq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("-o", "--out", default="captions.ass")
    a = ap.parse_args()

    plan = json.load(open(a.plan, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.plan))
    P = PRESETS[plan["style"]]
    P = {**P, **plan.get("overrides", {})}
    words = load_words(os.path.join(base, plan["words"]))
    wanted = {norm(k) for k in plan.get("keywords", [])}
    negatives = {norm(k) for k in plan.get("negatives", ["never", "không", "chưa", "no", "not"])}
    full_broll = [(b["start"], b["end"]) for b in plan.get("broll", []) if b.get("mode") in ("full", "slide")]

    ass = Ass()
    italic = P.get("italic", False)
    if P["mode"] == "chunk":
        ass.style("Cap", P["font"], P["size"], P["color"], border_style=3, outline=10,
                  outline_color=P["box"], shadow=0)
    else:
        ass.style("Cap", P["font"], P["size"], P["color"], bold=P.get("bold", False), italic=italic, shadow=1)
    K = P.get("keyword")
    if K:
        ass.style("Kw", K["font"], K["size"], K["colors"][0], bold=K.get("bold", True), italic=K.get("italic", False))
        ass.style("Bar", "Arial", 20, K.get("highlight", "#FFFFFF"))
    nt = P.get("name_title")
    if nt:
        ass.style("Name", nt["font"], nt["size"], nt["color"], bold=True)
        ass.style("Role", nt["font"], nt["sub_size"], nt["color"])

    cuts = [t for se in full_broll for t in se]
    chunks = chunk_words(words, P["max_words"], cuts=cuts)
    cx = W // 2
    kw_count = 0
    for ci, ch in enumerate(chunks):
        c_end = ch[-1]["end"] + 0.25
        if ci + 1 < len(chunks):
            c_end = min(c_end, chunks[ci + 1][0]["start"])
        on_broll = any(s <= ch[0]["start"] < e for s, e in full_broll)

        if P["mode"] == "chunk":
            text = esc(" ".join(w["word"] for w in ch))
            ass.ev(ch[0]["start"], c_end, f"{{\\an5\\pos({cx},{int(H * P['y'])})}}{text}", "Cap")
            continue

        ki = pick_keyword(ch, wanted, plan.get("auto_keywords", True)) if K else None
        y = P["y"]
        if K and K.get("positions") and ki is not None:
            y = K["positions"][kw_count % len(K["positions"])]
        if on_broll:
            y = 0.12
        color_over = f"\\c{ass_color(P['broll_text_color'])}" if on_broll and P.get("broll_text_color") else ""
        kcolor = K["colors"][kw_count % len(K["colors"])] if (K and ki is not None) else None
        if ki is not None:
            kw_count += 1

        ky = int(H * y)
        lead_y = ky - int(K["size"] * 0.62) if ki is not None else ky
        tail_y = ky + int(K["size"] * 0.55) if ki is not None else ky

        for wi, w in enumerate(ch):
            t0 = w["start"]
            t1 = ch[wi + 1]["start"] if wi + 1 < len(ch) else c_end
            if t1 <= t0:
                continue
            visible = ch[: wi + 1]
            groups = {"lead": [], "tail": []}
            for vi, vw in enumerate(visible):
                if ki is None or vi < ki:
                    groups["lead"].append((vi, vw))
                elif vi > ki:
                    groups["tail"].append((vi, vw))
            for gname, gy in (("lead", lead_y), ("tail", tail_y)):
                g = groups[gname]
                if not g:
                    continue
                parts = []
                for vi, vw in g:
                    tag = entry_tags(P["in_ms"], P["blur_in"]) if vi == wi else ""
                    parts.append(f"{{{tag}}}{esc(vw['word'])}{{\\r}}" if tag else esc(vw["word"]))
                ass.ev(t0, t1, f"{{\\an5\\pos({cx},{gy}){color_over}}}" + " ".join(parts), "Cap")

            if ki is not None and wi >= ki:
                kw = ch[ki]["word"]
                up = K.get("uppercase")
                if up is True or (up == "auto" and len(norm(kw)) <= 6):
                    kw = kw.upper()
                is_new = wi == ki
                single = len(ch) == 1
                if is_new and single and K.get("flicker_emotion"):
                    anim = flicker_tags()
                elif is_new:
                    anim = entry_tags(K["in_ms"], K["blur_in"], K.get("scale_in", 100))
                else:
                    anim = ""
                kc = ass_color(kcolor)
                ass.ev(t0, t1, f"{{\\an5\\pos({cx},{ky})\\c{kc}{anim}}}{esc(kw)}", "Kw", layer=3)
                if K.get("glow"):
                    g_anim = f"\\alpha&HFF&\\t(0,{K['in_ms'] * 2},\\alpha&H60&)" if is_new else "\\alpha&H60&"
                    ass.ev(t0, t1, f"{{\\an5\\pos({cx},{ky})\\1a&HFF&\\bord{K['glow_bord']}\\3c{kc}"
                                   f"\\blur{K['glow_blur']}{g_anim}}}{esc(kw)}", "Kw", layer=2)
                if K.get("highlight"):
                    # thanh dạ quang nửa dưới chữ, quét từ trái (clip động), đi trước chữ ~2 frame
                    tw = int(len(kw) * K["size"] * 0.58)
                    bh = int(K["size"] * 0.42)
                    x0, yb = cx - tw // 2 - 12, ky - bh // 2 + int(K["size"] * 0.12)
                    draw = f"m 0 0 l {tw + 24} 0 l {tw + 24} {bh} l 0 {bh}"
                    clip = f"\\clip({x0},{yb},{x0 + 1},{yb + bh})\\t(0,120,0.5,\\clip({x0},{yb},{x0 + tw + 24},{yb + bh}))" \
                        if is_new else ""
                    ass.ev(max(t0 - 0.07, 0) if is_new else t0, t1,
                           f"{{\\an7\\pos({x0},{yb})\\bord0\\shad0\\c{ass_color(K['highlight'])}{clip}\\p1}}{draw}",
                           "Bar", layer=1)
                if P.get("negative_slash") and norm(ch[ki]["word"]) in negatives:
                    tw = int(len(kw) * K["size"] * 0.6)
                    x0 = cx - tw // 2 - 20
                    draw = f"m 0 {int(K['size'] * 0.35)} l {tw + 40} 0 l {tw + 40} 6 l 0 {int(K['size'] * 0.35) + 6}"
                    clip = f"\\clip({x0},0,{x0 + 1},{H})\\t(0,100,\\clip({x0},0,{x0 + tw + 40},{H}))" if is_new else ""
                    ass.ev(t0, t1, f"{{\\an7\\pos({x0},{ky - int(K['size'] * 0.2)})\\bord0\\shad0\\c&HFFFFFF&{clip}\\p1}}"
                                   f"{draw}", "Bar", layer=4)

    if nt and plan.get("name_title"):
        n = plan["name_title"]
        x, yy = int(W * nt["x"]), int(H * nt["y"])
        ass.ev(n["start"], n["end"], f"{{\\an7\\pos({x},{yy})}}{esc(n['name'])}", "Name")
        if n.get("role"):
            ass.ev(n["start"] + nt["sub_delay_ms"] / 1000, n["end"],
                   f"{{\\an7\\pos({x},{yy + nt['size'] + 6})}}{esc(n['role'])}", "Role")

    ass.dump(a.out)
    print(f"wrote {a.out}: {len(chunks)} cụm, {kw_count} keyword, {len(ass.events)} event")


if __name__ == "__main__":
    main()
