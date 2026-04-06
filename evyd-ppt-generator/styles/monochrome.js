/**
 * monochrome — Black, white, and grey
 *
 * Pure black/white/grey palette. Minimal, editorial, high-end.
 * Let content and layout do the talking. Good for fashion, art, executive
 * briefings, and any context where colour would be a distraction.
 *
 * Inspired by: 无色系 — 纯黑 · 炭灰 · 中灰 · 浅灰 · 纯白 (Kimi style reference)
 */

module.exports = {
  name: "monochrome",
  description: "Black, white, and grey — minimal, editorial, high-end.",

  colors: {
    bg_primary:   "111111",   // near-black — cover & ending
    bg_content:   "1E1E1E",   // dark charcoal — content slides
    bg_white:     "FAFAFA",   // near-white — light slides
    bg_row:       "F0F0F0",   // light grey row
    bg_card:      "FFFFFF",

    accent_orange: "EEEEEE",  // bright white-grey — primary accent (tags, dots)
    accent_teal:   "888888",  // mid grey — secondary accent
    accent_dark2:  "080808",  // deepest black for tag backgrounds

    header_bg:    "111111",
    header_sep:   "333333",

    text_white:   "FFFFFF",
    text_primary: "E8E8E8",   // near-white on dark backgrounds
    text_muted:   "777777",
    text_navy:    "111111",   // on light slides
    text_mid:     "444444",
    text_blue_lt: "BBBBBB",
    text_dim:     "666666",
    text_example: "888888",

    slide_num:    "444444",
    slide_num_lt: "AAAAAA",
    warning_bg:   "080808",
  },

  fonts: {
    heading: "Aptos",
    body:    "Aptos",
  },

  motifs: {
    left_bar_colors: ["EEEEEE", "888888"],
    header_tag_color: "DDDDDD",
    bullet_dot_color: "EEEEEE",
    number_color:     "AAAAAA",
    row_border_color: "AAAAAA",
    quote_mark_color: "888888",
    divider_color:    "555555",
    tier_dot_size:    14,
  },
};
