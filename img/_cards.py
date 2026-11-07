# Card images for k-kolovos.github.io: one big number, one line, a simple bar chart. Greek and English. pycairo.
import cairo, os, unicodedata
def caps(t): return ''.join(ch for ch in unicodedata.normalize('NFD', t.upper()) if unicodedata.category(ch) != 'Mn')
OUT = os.path.dirname(os.path.abspath(__file__))
W, H, S = 1200, 675, 2
RED, NAVY, GREY, TXT, SUB = "#C0392B", "#2C3E50", "#B8BEC4", "#1D2733", "#5B6673"
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
def txt(c, s, x, y, size, col=TXT, bold=False, align="left", serif=False):
    c.select_font_face("DejaVu Serif" if serif else "DejaVu Sans", 0, 1 if bold else 0); c.set_font_size(size)
    e = c.text_extents(s)
    if align == "right": x -= e.x_advance
    if align == "center": x -= e.x_advance / 2
    c.set_source_rgb(*rgb(col)); c.move_to(x, y); c.show_text(s); return e.x_advance
def new():
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W * S, H * S); c = cairo.Context(s); c.scale(S, S)
    c.set_source_rgb(1, 1, 1); c.paint(); c.set_source_rgb(*rgb(RED)); c.rectangle(0, 0, W, 10); c.fill(); return s, c
def bar(c, x, y, w, h, col): c.set_source_rgb(*rgb(col)); c.rectangle(x, y, w, h); c.fill()

def card(name, lang, kicker, big, line, bars, note, unit=""):
    s, c = new()
    txt(c, caps(kicker), 70, 92, 24, SUB, bold=True)
    txt(c, big, 66, 250, 150, RED, bold=True)
    y = 312
    for ln in line: txt(c, ln, 70, y, 32, TXT); y += 44
    # bars: list of (label, value, colour, text)
    mx = max(v for _, v, _, _ in bars); x0, bw = 70, 640; yb = 450
    for lab, v, col, t in bars:
        txt(c, lab, x0, yb + 6, 24, SUB)
        w = bw * v / mx; bar(c, x0 + 250, yb - 22, w, 36, col)
        txt(c, t, x0 + 250 + w + 14, yb + 6, 26, col if col != GREY else SUB, bold=True)
        yb += 62
    txt(c, note, 70, H - 36, 19, SUB)
    s.write_to_png(os.path.join(OUT, f"card-{name}-{lang}.png"))

f = lambda v, d=1: f"{v:.{d}f}".replace('.', ',')
# inflation
card("inflation", "el", "Πληθωρισμός · Σεπτέμβριος 2026", "4,8% · 5,0%",
     ["σχεδόν ίδιος για φτωχότερους και πλουσιότερους,", "αλλά από άλλη πόρτα: πόσες μονάδες από τη στέγαση"],
     [("φτωχότερο 20%", 3.3, RED, "3,3 μον."), ("πλουσιότερο 20%", 1.7, NAVY, "1,7 μον.")],
     "Πηγή: ΕΛΣΤΑΤ (ΔΤΚ, ΕΟΠ 2025), δικός μας υπολογισμός")
card("inflation", "en", "Inflation · September 2026", "4.8% · 5.0%",
     ["almost the same for poorer and richer households,", "but through a different door: points from housing"],
     [("poorest 20%", 3.3, RED, "3.3 pts"), ("richest 20%", 1.7, NAVY, "1.7 pts")],
     "Source: ELSTAT (CPI, HBS 2025), own calculation")
# holidays
card("holidays", "el", "Διακοπές · 2025", "46,6%",
     ["των κατοίκων της Ελλάδας δεν μπορεί να αντέξει", "μία εβδομάδα διακοπών τον χρόνο"],
     [("Ελλάδα", 46.6, RED, "46,6%"), ("ΕΕ", 27.5, GREY, "27,5%")],
     "Πηγή: Eurostat, EU-SILC 2025")
card("holidays", "en", "Holidays · 2025", "46.6%",
     ["of residents of Greece cannot afford", "one week of holiday a year"],
     [("Greece", 46.6, RED, "46.6%"), ("EU", 27.5, GREY, "27.5%")],
     "Source: Eurostat, EU-SILC 2025")
# school 2030
card("school", "el", "Δημοτικό σχολείο · 2030", "−14%",
     ["μαθητές δημοτικού ως το 2029/30,", "από παιδιά που έχουν ήδη γεννηθεί"],
     [("2023/24", 566.7, GREY, "567.000"), ("2029/30", 487.1, RED, "487.000")],
     "Πηγή: Eurostat (γεννήσεις, εγγραφές), δική μας εκτίμηση")
card("school", "en", "Primary school · 2030", "−14%",
     ["primary pupils by 2029/30,", "from children already born"],
     [("2023/24", 566.7, GREY, "567,000"), ("2029/30", 487.1, RED, "487,000")],
     "Source: Eurostat (births, enrolments), own estimate")
# demographics
card("demographics", "el", "Δημογραφικό · γονιμότητα", "1,24",
     ["παιδιά ανά γυναίκα το 2024: κάτω από το 2,1", "της αναπλήρωσης κάθε χρονιά από το 1981"],
     [("1980", 2.23, GREY, "2,23"), ("2008", 1.50, GREY, "1,50"), ("2024", 1.24, RED, "1,24")],
     "Πηγή: Eurostat (demo_find)")
card("demographics", "en", "Demographics · fertility", "1.24",
     ["children per woman in 2024: below the 2.1", "replacement level every year since 1981"],
     [("1980", 2.23, GREY, "2.23"), ("2008", 1.50, GREY, "1.50"), ("2024", 1.24, RED, "1.24")],
     "Source: Eurostat (demo_find)")
print("ok")
