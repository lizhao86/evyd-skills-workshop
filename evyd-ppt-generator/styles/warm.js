/**
 * warm — Coral orange + amber on deep espresso
 *
 * Warm-toned palette with coral and amber accents on a rich dark brown base.
 * Energetic, approachable, human. Good for education, healthcare patient-facing,
 * training materials, and lifestyle brands.
 *
 * Inspired by: 暖色调系 — 珊瑚橙 · 暖黄色 · 奶油白 (Kimi style reference)
 */

module.exports = {
  name: "warm",
  description: "Coral + amber on deep espresso. Energetic, approachable, human.",

  colors: {
    bg_primary:   "2C1810",   // deep espresso — cover & ending
    bg_content:   "3D2418",   // warm dark brown — content slides
    bg_white:     "FFFAF5",   // 奶油白 cream — light slides
    bg_row:       "FFF3E8",   // warm light orange tint row
    bg_card:      "FFFFFF",

    accent_orange: "E8622A",  // 珊瑚橙 coral — primary accent
    accent_teal:   "F0A830",  // 暖黄色 amber — secondary accent
    accent_dark2:  "1E1008",  // very dark espresso for tag backgrounds

    header_bg:    "2C1810",
    header_sep:   "5A3020",

    text_white:   "FFFFFF",
    text_primary: "F5E8D8",   // warm cream on dark backgrounds
    text_muted:   "A07858",
    text_navy:    "2C1810",   // on light slides
    text_mid:     "6A4030",
    text_blue_lt: "D4AA88",
    text_dim:     "987060",
    text_example: "885040",

    slide_num:    "5A3020",
    slide_num_lt: "AAAAAA",
    warning_bg:   "1E1008",
  },

  fonts: {
    heading: "Aptos",
    body:    "Aptos",
  },

  motifs: {
    left_bar_colors: ["E8622A", "F0A830"],
    header_tag_color: "E8622A",
    bullet_dot_color: "E8622A",
    number_color:     "F0A830",
    row_border_color: "E8622A",
    quote_mark_color: "F0A830",
    divider_color:    "E8622A",
    tier_dot_size:    14,
  },
};
