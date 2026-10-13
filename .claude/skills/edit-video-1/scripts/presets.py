"""Thông số 4 preset, đo từ video mẫu (xem references/styles.md).

Đơn vị: px trên khung 1080x1920, thời gian ms. Chỉnh style tại đây.
Font: tên font phải cài trên máy render; libass tự fallback nếu thiếu.
"""

W, H = 1080, 1920

PRESETS = {
    # V1 – phỏng vấn thương hiệu: hộp mint, cắt cứng, không animation
    "v1_editorial": {
        "mode": "chunk",            # cả cụm hiện cùng lúc
        "max_words": 6,
        "font": "Plus Jakarta Sans",
        "size": 40,
        "color": "#111111",
        "box": "#86D98E",           # nền hộp caption
        "y": 0.72,                  # tâm caption theo chiều cao khung
        "in_ms": 0, "blur_in": 0,
        "keyword": None,            # V1 không nhấn keyword
        "name_title": {"font": "Plus Jakarta Sans", "size": 64, "color": "#3DDC84",
                       "sub_size": 26, "x": 0.08, "y": 0.10, "sub_delay_ms": 700},
        "broll_card": {"width": 0.88, "cy": 0.52},
    },
    # V2 – kinetic BĐS: từ nhỏ nghiêng mảnh + keyword siêu đậm glow, màu xoay vòng
    "v2_kinetic": {
        "mode": "word",
        "max_words": 5,
        "font": "Helvetica Neue",
        "italic": True,
        "size": 46,
        "color": "#FFFFFF",
        "y": 0.50,
        "in_ms": 100, "rise_px": 0, "slide_px": 30, "blur_in": 6,
        "keyword": {
            "font": "Helvetica Neue Black", "bold": True, "italic": False, "size": 170,
            "colors": ["#F8F808", "#C808F8", "#F81818", "#4888F8", "#D89838", "#A02828"],
            "glow": True, "glow_blur": 14, "glow_bord": 10,
            "in_ms": 70, "blur_in": 20, "scale_in": 110, "uppercase": "auto",
            "positions": [0.50, 0.17],   # luân phiên vùng bụng / trên đầu
        },
        "negative_slash": True,
        "broll_card": {"width": 0.42, "cy": 0.66},
    },
    # V3 – creator phòng tối: cộng dồn từng từ trắng + keyword đỏ glow + dòng script
    "v3_creator": {
        "mode": "word",
        "max_words": 5,
        "font": "Poppins SemiBold",
        "bold": True,
        "size": 68,
        "color": "#FFFFFF",
        "y": 0.60,
        "in_ms": 100, "rise_px": 10, "slide_px": 0, "blur_in": 0,
        "keyword": {
            "font": "Poppins ExtraBold", "bold": True, "size": 120,
            "colors": ["#F80A0A"],
            "glow": True, "glow_blur": 18, "glow_bord": 8,
            "in_ms": 130, "blur_in": 20, "scale_in": 100, "uppercase": False,
            "positions": None,
        },
        "broll_card": {"width": 0.72, "cy": 0.48},
        "broll_bg": "#D8D8D8",       # nền giấy xám cho cảnh B-roll full
        "broll_text_color": "#555555",
    },
    # V4 – premium: blur-in, keyword trắng trên thanh lime, từ nối nhỏ
    "v4_premium": {
        "mode": "word",
        "max_words": 5,
        "font": "Inter",
        "size": 44,
        "color": "#FFFFFF",
        "y": 0.55,
        "in_ms": 240, "rise_px": 0, "slide_px": 0, "blur_in": 12,
        "keyword": {
            "font": "Inter Display ExtraBold", "bold": True, "size": 110,
            "colors": ["#FFFFFF"],
            "highlight": "#8CF80A",     # thanh dạ quang sau keyword
            "glow": False,
            "in_ms": 160, "blur_in": 14, "scale_in": 100, "uppercase": False,
            "flicker_emotion": True,     # keyword đứng một mình -> flicker
            "positions": None,
        },
        "broll_card": {"width": 0.80, "cy": 0.50},
    },
}


def ass_color(hex_color, alpha=0):
    """#RRGGBB -> &HAABBGGRR (alpha 0 = đặc, 255 = trong suốt)."""
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()
