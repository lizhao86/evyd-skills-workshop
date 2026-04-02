/**
 * dark_navy — Deep navy + teal + orange
 *
 * Premium dark theme. High contrast, confident. Good for internal
 * strategy decks, external pitches, and course/research presentations.
 *
 * To add a new style: copy this file, change the exports, and name
 * the file after your style (e.g. cyberpunk.js, red_line.js).
 */

module.exports = {
  name: "dark_navy",
  description: "Deep navy background, teal + orange accents. Premium look.",

  // ── Core palette (no # prefix — PptxGenJS requirement)
  colors: {
    bg_primary:   "0B1F3A",   // cover & ending background
    bg_content:   "1A5276",   // main content slide background
    bg_white:     "FFFFFF",   // light slide background (slide 3 style)
    bg_row:       "F4F6F8",   // row/card background on white slides
    bg_card:      "FFFFFF",   // card background (transparency applied in renderer)

    accent_orange: "E87722",  // primary accent — tags, dots, section labels
    accent_teal:   "17A589",  // secondary accent — borders, dividers, numbers
    accent_dark2:  "102740",  // darker navy for tag backgrounds

    header_bg:    "0B1F3A",   // slide header strip background
    header_sep:   "3A5570",   // header separator line

    text_white:   "FFFFFF",
    text_primary: "D8E8F4",   // body text on dark backgrounds
    text_muted:   "6B8BA4",   // muted/subtitle text
    text_navy:    "1C2B3A",   // body text on white backgrounds
    text_mid:     "3D5166",   // secondary text on white
    text_blue_lt: "7AAABF",   // light blue subtitle on blue slides
    text_dim:     "9BBFD4",   // dimmed text in cards
    text_example: "6899AA",   // italic example text in tier rows

    slide_num:    "3A5570",   // slide number color (dark slides)
    slide_num_lt: "BBBBBB",   // slide number color (light slides)

    warning_bg:   "1C3A52",   // bottom warning bar background
  },

  // ── Typography
  fonts: {
    heading: "Georgia",      // serif — cover title, large numbers, quote mark
    body:    "Calibri",      // sans — all body text, labels, bullets
  },

  // ── Visual motifs (used by renderer for consistent decoration)
  motifs: {
    left_bar_colors: ["E87722", "17A589"],   // cover gradient bar: [top, bottom]
    header_tag_color: "E87722",              // section tag text color
    bullet_dot_color: "E87722",              // bullet point dot color
    number_color:     "17A589",              // numbered row accent color
    row_border_color: "17A589",              // teal left border on rows
    quote_mark_color: "17A589",              // large quote mark color
    divider_color:    "17A589",              // horizontal divider lines
    tier_dot_size:    14,                    // colored dot size (pt) in tier rows
  },
};
