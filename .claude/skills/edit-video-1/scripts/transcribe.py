#!/usr/bin/env python3
"""Video/audio -> words.json (timestamp từng từ).

Dùng: python3 transcribe.py input.mp4 -o work/words.json [--model small] [--lang vi]
Cần một trong hai: pip install faster-whisper  |  pip install openai-whisper
"""
import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("-o", "--out", default="words.json")
    ap.add_argument("--model", default="small")
    ap.add_argument("--lang", default=None, help="vd: vi, en (bỏ trống = tự nhận)")
    a = ap.parse_args()

    words = []
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(a.model, compute_type="int8")
        segs, _ = model.transcribe(a.media, word_timestamps=True, language=a.lang)
        for s in segs:
            for w in s.words:
                words.append({"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
    except ImportError:
        try:
            import whisper
        except ImportError:
            sys.exit("Thiếu thư viện. Cài: pip install faster-whisper  (hoặc openai-whisper)")
        model = whisper.load_model(a.model)
        res = model.transcribe(a.media, word_timestamps=True, language=a.lang)
        for s in res["segments"]:
            for w in s.get("words", []):
                words.append({"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)})

    json.dump({"words": words}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {a.out}: {len(words)} từ")


if __name__ == "__main__":
    main()
