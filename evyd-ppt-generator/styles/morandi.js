/**
 * morandi — Muted grey-toned pastels
 *
 * Low-saturation, grey-shifted palette: slate blue, dusty rose, sage green,
 * warm beige. Calm, refined, artistic. Good for culture, lifestyle, brand
 * handbook, and upscale internal reports.
 *
 * Inspired by: 莫兰迪色系 — 雾霾蓝 #B3CDE0 · 灰粉色 #E7CBCB · 燕麦色 #D8CBBE
 *              豆沙绿 #B5CAA0 · 烟灰色 #C2C2C2 (Kimi style reference)
 */

module.exports = {
  name: "morandi",
  description: "Muted grey-toned pastels — slate, dusty rose, sage. Calm and refined.",

  colors: {
    bg_primary:   "5C7080",   // 雾霾蓝 deeper — cover & ending
    bg_content:   "6B8090",   // slate blue-grey — content slides
    bg_white:     "FAF7F2",   // 燕麦色 warm off-white — light slides
    bg_row:       "F0EBE3",   // warm light row background
    bg_card:      "FFFFFF",

    accent_orange: "C4857A",  // 灰粉色 dusty rose — primary accent
    accent_teal:   "8FAF9F",  // 豆沙绿 sage green — secondary accent
    accent_dark2:  "4A5F6A",  // darker slate for tag backgrounds

    header_bg:    "5C7080",
    header_sep:   "7A90A0",

    text_white:   "FFFFFF",
    text_primary: "EDE8E2",   // warm white on dark backgrounds
    text_muted:   "A8BCCA",
    text_navy:    "3A4A52",   // dark slate on light slides
    text_mid:     "5A7080",
    text_blue_lt: "B8CCDA",
    text_dim:     "9AACBA",
    text_example: "8899AA",

    slide_num:    "7A90A0",
    slide_num_lt: "AAAAAA",
    warning_bg:   "485D6A",
  },

  fonts: {
    heading: "Aptos",
    body:    "Aptos",
  },

  motifs: {
    left_bar_colors: ["C4857A", "8FAF9F"],
    header_tag_color: "C4857A",
    bullet_dot_color: "C4857A",
    number_color:     "8FAF9F",
    row_border_color: "8FAF9F",
    quote_mark_color: "C4857A",
    divider_color:    "8FAF9F",
    tier_dot_size:    14,
  },
};
