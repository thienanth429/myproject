---
name: edit-video-1
description: Dựng video dọc 9:16 kiểu talking-head + motion text theo từng từ + B-roll lớp phủ (4 preset rút ra từ 4 video mẫu - editorial tối giản, kinetic BĐS, creator phòng tối, premium kiểu Iman Gadzhi). Dùng khi người dùng muốn edit/dựng video nói trước máy, làm caption động từng từ, keyword glow/highlight, chèn B-roll dạng thẻ ảnh/tem/cảnh đồ hoạ, hoặc nhắc tới "edit video_1", "style video_1", "caption từng từ", "kinetic text", "chữ sau lưng người".
---

# edit-video-1

Skill dựng video dọc (1080×1920) theo trường phái: **người nói trước máy (A-roll) + chữ chạy theo từng từ được nói + B-roll đặt như lớp phủ**. Mọi thông số (số frame, màu, easing) lấy từ phân tích frame-by-frame 4 video mẫu — xem `references/styles.md`.

## Khi nào dùng preset nào

| Preset | Gốc | Cảm giác | Hợp với |
|---|---|---|---|
| `v1_editorial` | Phỏng vấn thương hiệu POTR | Tối giản, bình tĩnh | Phỏng vấn, brand story, video dài 60–120 s |
| `v2_kinetic` | Môi giới BĐS | Năng lượng cao, nhiều màu | Bán hàng, local business, 20–40 s |
| `v3_creator` | Creator phòng tối | Kể chuyện, nhấn cảm xúc | Storytelling cá nhân, 10–40 s |
| `v4_premium` | Style Iman Gadzhi | Cao cấp, sạch | Giáo dục, coaching, thương hiệu cá nhân |

Không chắc thì hỏi người dùng 1 câu: "Video này muốn cảm giác tối giản, năng lượng cao, kể chuyện hay cao cấp?"

## Quy trình

1. **Kiểm tra đầu vào** – `ffprobe` video A-roll (độ phân giải, fps, thời lượng). Nếu không phải 9:16, `render.py` sẽ crop giữa về 1080×1920.
2. **Lấy timestamp từng từ** – `python3 scripts/transcribe.py input.mp4 -o work/words.json` (cần `faster-whisper` hoặc `openai-whisper`; script báo cách cài nếu thiếu). Nếu người dùng đã có SRT/word timestamps thì chuyển sang định dạng `words.json` (xem `templates/words.example.json`).
3. **Lập edit plan** – copy `templates/plan.example.json` thành `work/plan.json`, điền:
   - `style`: một trong 4 preset.
   - `keywords`: từ cần nhấn (số liệu, nỗi đau, kết luận, danh từ chính). Quy tắc: **tối đa 1 keyword mỗi cụm 3–6 từ**. Nếu để trống, script tự chọn (ưu tiên số, từ viết hoa, từ dài nhất cụm).
   - `negatives`: từ phủ định (never/không/chưa) → nét chém (chỉ v2).
   - `broll`: danh sách `{file, start, end, mode}`; `mode` = `card` (thẻ đè lên thân, chừa mặt), `stamp` (tem nhỏ viền trắng cạnh keyword), `slide` (asset đặt giữa nền phẳng, kiểu cảnh đồ hoạ v3), `full` (cắt hẳn sang cảnh/ảnh toàn màn). Với `slide`/`full`, caption tự lên trên khung và cụm chữ tự ngắt tại điểm cắt. Đặt B-roll **đúng lúc danh từ tương ứng được nói**, giữ 1.5–2.5 s; montage liệt kê thì mỗi ảnh 0.28 s.
   - Đọc transcript và đề xuất B-roll cho người dùng nếu họ chưa có — mô tả ảnh cần tìm cho từng mốc thời gian.
4. **Sinh caption động** – `python3 scripts/make_captions.py work/plan.json -o work/captions.ass`. File ASS chứa animation (blur-in, fade, glow, highlight bar, flicker) theo preset.
5. **Render** – `python3 scripts/render.py work/plan.json -o out.mp4` (ghép B-roll + burn caption, caption luôn nằm trên B-roll). Thêm `--preview 0:10` để render nhanh 10 s đầu.
6. **Kiểm tra** – trích vài frame tại các keyword và mốc B-roll (`ffmpeg -ss T -i out.mp4 -frames:v 1 f.png`) rồi xem lại: chữ có che mặt không, keyword có đúng lúc nói không, B-roll có lệch nhịp không. Sửa plan → render lại.
7. **Phần làm tay** – các hiệu ứng ffmpeg/ASS không làm tốt được liệt kê ở `references/manual-effects.md` (chữ sau lưng người, tem lật, whip, light leak, icon 3D…). Ghi rõ cho người dùng mốc thời gian nên thêm chúng trong CapCut/AE.

## Nguyên tắc bắt buộc (DNA chung)

- Chữ chỉ xuất hiện **khi từ được nói**, cộng dồn thành cụm; không hiện cả câu trước.
- Hai tầng cỡ chữ: từ nối nhỏ/mảnh, keyword to/đậm/có màu (tỷ lệ ~1:3).
- Vào nhanh 2–6 frame, ease-out mạnh; thoát cắt cứng khi hết cụm (trừ v2).
- Mỗi cụm một điểm nhấn màu, còn lại trắng/xám.
- B-roll là lớp phủ, chừa mặt người nói; caption luôn trên cùng.
- Chuyển cảnh chủ yếu là cut đúng nhịp từ; whip/light leak tối đa 1–2 lần/video.
- SFX chỉ cho keyword và đồ hoạ lớn (ding/shimmer, whoosh), không cho từng từ.

## File trong skill

- `references/styles.md` – thông số chi tiết 4 preset (font, màu hex, keyframe theo frame).
- `references/manual-effects.md` – công thức AE/Premiere/CapCut cho hiệu ứng làm tay.
- `scripts/transcribe.py` – video → `words.json`.
- `scripts/make_captions.py` – plan + words → `captions.ass`.
- `scripts/render.py` – plan → video hoàn chỉnh (ffmpeg).
- `scripts/presets.py` – toàn bộ thông số preset; **chỉnh style ở đây**.
- `templates/` – mẫu `plan.json`, `words.json`.
