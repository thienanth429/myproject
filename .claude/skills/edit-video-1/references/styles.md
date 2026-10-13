# Thông số 4 preset (đo frame-by-frame từ video mẫu)

Báo cáo trực quan đầy đủ (dải frame + track keyframe): https://claude.ai/artifact/8DDPYiNNRL4eVDYpHrEwGR
Số frame tính theo fps gốc của video mẫu. Tên font là ước đoán theo hình dáng chữ.

## v1_editorial — phỏng vấn thương hiệu (25 fps, 106 s)
- Phông nền: studio liền màu cam `#F08848`, máy toàn thân, người ngồi ghế cao.
- Caption: hộp mint `#86D98E`, chữ gần đen, sans tròn (kiểu Plus Jakarta Sans) cỡ nhỏ; cụm 3–6 từ, giữ 1–2 s; **vào/ra 0 frame**; tắt khi người nói ngừng; vị trí cố định ~72% chiều cao; luôn nằm trên B-roll.
- Tên nhân vật: xanh lá tươi, góc trên-trái, hiện cứng ở 1.28 s; chức danh nhỏ hiện sau ~0.7 s.
- B-roll (~25% thời lượng): thẻ ảnh giữa khung che thân, chừa mặt; cắt cứng; montage liệt kê **7 frame/ảnh (0.28 s)**, mỗi ảnh lệch vị trí/cỡ như một xấp ảnh, nền phủ texture giấy nhàu; ảnh hero lên full màn 1–2 s.
- Xen punch-in cùng take (crop 120–150%) và góc máy phụ cận tay/sản phẩm.
- Hiệu ứng nền: khi nói về "patterns/textiles", nền bị bóp méo như lụa ~2 s, người vẫn nét (cần mask).

## v2_kinetic — môi giới BĐS (30 fps, 29 s)
- Từ nối: sans mảnh nghiêng trắng (kiểu Helvetica Neue Light Italic), trượt từ phải ~30 px + fade trong 3 frame.
- Keyword: grotesk siêu đậm (kiểu Helvetica Black), cỡ ~3.5× từ nối, glow cùng màu; blur ~30→0 + opacity + Y +15→0 trong **2–3 frame**.
- Màu xoay vòng: `#F8F808` vàng, `#C808F8` tím, `#F81818` đỏ, `#4888F8` xanh, `#D89838` vàng đồng, `#A02828` đỏ đô; vài từ gradient ngang 2 màu.
- **Chữ sau lưng người**: keyword luân phiên vùng trên đầu (bị đầu che) và vùng bụng.
- Thoát: mỗi từ bay một hướng 80–150 px + opacity→0 trong 4–5 frame có motion blur; cụm mới vào chồng 2–3 frame.
- Từ phủ định ("never"): vệt sáng trắng quét chéo (trim path 0→100% trong 3 frame), chữ hiện sau, vệt ở lại thành gạch chéo.
- B-roll "tem bưu chính": mép răng cưa, viền nét đứt trắng, đổ bóng, rộng ~40% khung; thẻ trắng Scale X 0→100% (3f, neo giữa) rồi ảnh opacity 0→100% (2–3f); minh hoạ đúng danh từ đang nói.
- UI: chip kính mờ có ✕ đỏ; ô tick xanh 3D bay vào từ trái-dưới xoay −30°→0° trong 9f, tick tự vẽ 2f, chip bị đẩy ra phải.
- Mở đầu: 3 frame bóng người tô trắng (từ mask) → hình thật.
- Chuyển cảnh: whip ngang 2–3f (chữ và tem trượt cùng khung); 1 lần light leak cháy sáng ~8f.
- SFX (suy từ phổ): whoosh/riser ở keyword lớn và icon.

## v3_creator — creator phòng tối (30 fps, 11.6 s)
- Caption: sans hình học đậm trắng (kiểu Poppins/Gilroy SemiBold), cộng dồn từng từ: opacity 0→100% + Y +10→0 trong **3 frame**, ease-out; cả dòng tự căn giữa lại; vị trí ngang ngực 55–62%; **thoát cắt cứng**.
- Keyword: đỏ `#F80A0A` + glow đỏ; blur 20→0 (4f), opacity (3f), glow tăng tới f7; dòng phụ font script/brush trắng vào f4–f8, chồng ~25% lên chân dòng chính.
- ~1 keyword mỗi 2–3 s (số tiền, nỗi đau, kết luận).
- B-roll (~43%): cảnh đồ hoạ nền xám `#D8D8D8` + lưới kẻ ô + bóng nắng rèm chéo; asset đen trắng đổ bóng mềm, hiện cứng rồi trôi lên ~3%; nét cong xám dày vẽ dần (trim path ~10f); caption lên trên đổi xám đậm; đổi asset bằng cut đúng từ khoá; vào bằng cut hoặc hoà 1–2f.
- SFX (suy từ phổ): "ding/shimmer" ở keyword.

## v4_premium — style Iman Gadzhi (25 fps gốc, 23 s)
- Từ nối nhỏ trắng (kiểu Inter), blur + opacity ~6f (240 ms), hiện lần lượt.
- Keyword trắng đậm trên **thanh highlight lime `#8CF80A`** cao ~55% chữ ở nửa dưới; thanh Scale X 0→100% từ trái, đi trước chữ 1–2f, kéo dài đón từ tiếp theo.
- Bố cục bậc thang chéo: từ dẫn trên-trái, keyword giữa, từ đuôi dưới-phải.
- Từ cảm xúc đứng một mình (lime nhạt `#C0F870`): flicker tắt/bật 3 lần trong ~320 ms.
- Icon 3D bóng (chìa khoá, não) chen giữa 2 dòng, blur+opacity 4f; chữ đè lên icon.
- Slide toàn màn: nền trắng chữ condensed đen gradient blur-in 250 ms; chân dung tách nền đen trắng blur ~40→0 trong 10f + vòng tròn đỏ `#A80808` (opacity 30→100, scale 90→100) + chấm đỏ nở 0→100; push-in chậm.
- Cảnh "sang": nền nâu đỏ rất tối, vòng cung viền vàng mảnh có hạt sáng chạy; chờ 1.35 s rồi tiêu đề blur-in 400 ms, phụ đề +0.5 s, căn trái.
- SFX (suy từ phổ): pop/whoosh ngắn cho mỗi đồ hoạ.

## Bảng nhịp nhanh
| Thông số | Giá trị |
|---|---|
| Vào caption thường | 2–4f (70–130 ms) |
| Vào keyword blur-in | 4–6f (130–240 ms) |
| Vào tiêu đề/slide sang | 10f (400 ms) |
| Thoát (v1, v3) | 0f cắt cứng |
| Keyword | 1 / cụm 3–6 từ |
| Giữ B-roll | 1.5–2.5 s; montage 7f/ảnh |
| Easing | Ease Out mạnh (influence 70–90%), không bounce (trừ icon) |
