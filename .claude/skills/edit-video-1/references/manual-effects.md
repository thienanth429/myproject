# Hiệu ứng làm tay (script ffmpeg/ASS chưa làm được)

Khi render xong, liệt kê cho người dùng mốc thời gian nên thêm các hiệu ứng dưới đây.

| Hiệu ứng | After Effects / Premiere | CapCut |
|---|---|---|
| Chữ sau lưng người (v2) | Nhân đôi A-roll, Roto Brush bản trên, layer chữ kẹp giữa | Nhân đôi clip → Remove background bản trên, track chữ ở giữa |
| Flash bóng người trắng 3f đầu video (v2) | Dùng matte Roto, Fill trắng, 3 frame | Clip tách nền + filter trắng/độ sáng max, 0.1 s |
| Chữ bay tản ra (v2) | Mỗi từ Position lệch 80–150 px một hướng trong 4–5f + Opacity→0, bật Motion Blur | Animation Out: Slide/Blur out 0.15 s, mỗi từ một hướng |
| Tem lật ra (v2) | Precomp ảnh + matte răng cưa + viền nét đứt + drop shadow; Scale X 0→100% (3f, anchor giữa), ảnh Opacity 0→100% (2–3f); wiggle nhẹ | Overlay + PNG khung tem, keyframe scale ngang hoặc animation Flip |
| Ô tick bay vào (v2) | Position + Rotation −30°→0° trong 9f, tick Trim Paths 2f | Sticker tick + keyframe vị trí/xoay |
| Whip ngang | Transform (position + shutter angle cao) 2–3f | Transition Pull in / Swipe 0.1 s |
| Light leak | Stock light leak chế độ Screen + Exposure tăng, cắt khi trắng | Transition Light leak / Flash |
| Nét cong vẽ dần (v3) | Shape stroke dày round cap, Trim Paths End 0→100% ~10f | Overlay video nét vẽ |
| Asset trôi lên chậm (v3) | Position Y −3% trong 1–2 s, linear | Keyframe vị trí |
| Icon 3D (v4) | PNG icon, Gaussian Blur + Opacity 4f | Sticker 3D, animation Blur in |
| Chân dung tách nền + vòng tròn đỏ (v4) | Cutout trên nền gradient, Lens Blur 40→0 10f, circle Scale 90→100 | Remove background + shape, keyframe blur |
| Nền bóp méo như lụa (v1) | Turbulent Displace chỉ trên nền (mask người) | Effect "Wave/Liquid" trên clip nền + clip người tách nền phía trên |
| Punch-in cùng take (v1) | Scale 120–150% tại điểm cắt | Cắt clip + keyframe scale |
| Texture giấy nhàu khi montage (v1) | Overlay ảnh giấy, blend Multiply/Overlay | Overlay + blend mode |

SFX: chỉ cho keyword lớn (ding/shimmer) và đồ hoạ/chuyển cảnh (whoosh, pop). Không gắn cho từng từ.
