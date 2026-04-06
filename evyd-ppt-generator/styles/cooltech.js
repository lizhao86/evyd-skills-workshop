/**
 * cooltech — Deep space blue + tech cyan + electric purple
 *
 * Cool tech palette. Dark navy base with bright cyan primary accent
 * and electric purple secondary. Good for SaaS, AI, healthcare tech decks.
 *
 * Inspired by: 深空蓝 + 科技青 + 电光紫 (Kimi style reference)
 */

module.exports = {
  name: "cooltech",
  description: "Deep space navy with tech cyan + electric purple. Futuristic, confident.",

  colors: {
    bg_primary:   "0D1B2A",   // deep space navy (cover & ending)
    bg_content:   "14304A",   // dark blue content background
    bg_white:     "FFFFFF",
    bg_row:       "EBF4FA",   // very light blue row on white slides
    bg_card:      "FFFFFF",

    accent_orange: "00C9C8",  // 科技青 tech cyan — primary accent
    accent_teal:   "7B61FF",  // 电光紫 electric purple — secondary accent
    accent_dark2:  "091523",  // deeper bg for tag/badge backgrounds

    header_bg:    "0D1B2A",
    header_sep:   "1E4060",

    text_white:   "FFFFFF",
    text_primary: "C8E8F8",   // light blue-white on dark backgrounds
    text_muted:   "5A8AAA",
    text_navy:    "0D1B2A",   // on white slides
    text_mid:     "2A5070",
    text_blue_lt: "80CCEE",
    text_dim:     "4A7A99",
    text_example: "5599BB",

    slide_num:    "1E4060",
    slide_num_lt: "AAAAAA",
    warning_bg:   "0A2030",
  },

  fonts: {
    heading: "Aptos",
    body:    "Aptos",
  },

  motifs: {
    left_bar_colors: ["00C9C8", "7B61FF"],
    header_tag_color: "00C9C8",
    bullet_dot_color: "00C9C8",
    number_color:     "7B61FF",
    row_border_color: "00C9C8",
    quote_mark_color: "7B61FF",
    divider_color:    "00C9C8",
    tier_dot_size:    14,
  },
};
