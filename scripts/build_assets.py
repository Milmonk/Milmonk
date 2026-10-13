#!/usr/bin/env python3
"""Build the SVG graphics used by the profile README.

GitHub shows README images in a sandbox that cannot load web fonts, so every
piece of text is converted to outlines here. Each graphic is written twice,
once per colour theme, and the README picks the right one with <picture>.

    pip install fonttools uharfbuzz
    python scripts/build_assets.py

Fonts (Newsreader, IBM Plex Sans, IBM Plex Mono, all SIL OFL) are downloaded
into scripts/.fonts on the first run.
"""
import io
import pathlib
import urllib.parse
import urllib.request

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = pathlib.Path(__file__).resolve().parent / ".fonts"
OUT_DIR = ROOT / "assets"
FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONT_FILES = {
    "Newsreader.ttf": "newsreader/Newsreader[opsz,wght].ttf",
    "Newsreader-Italic.ttf": "newsreader/Newsreader-Italic[opsz,wght].ttf",
    "PlexSans.ttf": "ibmplexsans/IBMPlexSans[wdth,wght].ttf",
    "PlexMono-Regular.ttf": "ibmplexmono/IBMPlexMono-Regular.ttf",
    "PlexMono-Medium.ttf": "ibmplexmono/IBMPlexMono-Medium.ttf",
}

# One accent, one context gray, warm neutrals. The dark column is stepped for
# GitHub's dark page (#0d1117), not an inversion of the light one.
THEMES = {
    "light": dict(
        page="#ffffff", panel="#faf9f6", line="#dedbd3", cell="#efede7",
        ink="#1b1a17", ink2="#5c5a55", accent="#cc3317", context="#8e8b84",
    ),
    "dark": dict(
        page="#0d1117", panel="#11161d", line="#2a303a", cell="#171c24",
        ink="#ece9e1", ink2="#a6a39a", accent="#f0603f", context="#6b7280",
    ),
}


def fetch_fonts():
    FONT_DIR.mkdir(exist_ok=True)
    for name, path in FONT_FILES.items():
        target = FONT_DIR / name
        if not target.exists():
            urllib.request.urlretrieve(FONT_BASE + urllib.parse.quote(path), target)


class Face:
    """A font pinned to one style, able to shape text and hand out outlines."""

    def __init__(self, key, filename, axes=None):
        font = TTFont(FONT_DIR / filename)
        if axes:
            font = instancer.instantiateVariableFont(font, axes)
        buf = io.BytesIO()
        font.save(buf)
        data = buf.getvalue()
        self.key = key
        self.tt = TTFont(io.BytesIO(data))
        self.hb = hb.Font(hb.Face(data))
        self.upm = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf)
        return [(i.codepoint, p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def outline(self, gid):
        pen = SVGPathPen(self.glyphs, ntos=lambda v: "%g" % round(v))
        self.glyphs[self.tt.getGlyphName(gid)].draw(pen)
        return pen.getCommands()

    def width(self, text, size, tracking=0.0):
        units = sum(adv + tracking * self.upm for _, adv, _, _ in self.shape(text))
        return (units - tracking * self.upm) * size / self.upm


def n(value):
    return "%g" % round(value, 2)


class SVG:
    def __init__(self, width, height, title):
        self.width, self.height, self.title = width, height, title
        self.defs, self.body, self.css = {}, [], ""

    def add(self, markup):
        self.body.append(markup)

    def text(self, face, string, x, y, size, fill, anchor="start", tracking=0.0, cls=None):
        """Draw outlined text with its baseline at (x, y); returns the width."""
        width = face.width(string, size, tracking)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        pen_x, uses = 0.0, []
        for gid, adv, dx, dy in face.shape(string):
            d = face.outline(gid)
            if d:
                ref = self.defs.setdefault((face.key, gid), (f"{face.key}{gid}", d))[0]
                pos = f' x="{n(pen_x + dx)}"' if pen_x + dx else ""
                pos += f' y="{n(dy)}"' if dy else ""
                uses.append(f'<use href="#{ref}"{pos}/>')
            pen_x += adv + tracking * face.upm
        k = size / face.upm
        attr = f' class="{cls}"' if cls else ""
        self.add(f'<g{attr} transform="translate({n(x)} {n(y)}) scale({k:.5f} {-k:.5f})" '
                 f'fill="{fill}">{"".join(uses)}</g>')
        return width

    def render(self):
        defs = "".join(f'<path id="{ref}" d="{d}"/>' for ref, d in self.defs.values())
        style = f"<style>{self.css}</style>" if self.css else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
                f'width="{self.width}" height="{self.height}" role="img">'
                f"<title>{self.title}</title>{style}<defs>{defs}</defs>{''.join(self.body)}</svg>\n")


def rounded_route(points, radius):
    """Path through right-angled waypoints with the corners rounded off."""
    d = [f"M{n(points[0][0])} {n(points[0][1])}"]
    for prev, here, nxt in zip(points, points[1:], points[2:]):
        ax, ay = (prev[0] - here[0], prev[1] - here[1])
        bx, by = (nxt[0] - here[0], nxt[1] - here[1])
        la, lb = abs(ax) + abs(ay), abs(bx) + abs(by)
        d.append(f"L{n(here[0] + ax / la * radius)} {n(here[1] + ay / la * radius)}")
        d.append(f"Q{n(here[0])} {n(here[1])} {n(here[0] + bx / lb * radius)} {n(here[1] + by / lb * radius)}")
    d.append(f"L{n(points[-1][0])} {n(points[-1][1])}")
    return "".join(d)


def arrow(svg, points, color, radius=5):
    """Hairline connector ending in a small arrowhead."""
    (x0, y0), (x1, y1) = points[-2], points[-1]
    length = abs(x1 - x0) + abs(y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    d = rounded_route(points, radius) if len(points) > 2 else f"M{n(points[0][0])} {n(points[0][1])}L{n(x1)} {n(y1)}"
    svg.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.25"/>')
    bx, by = x1 - ux * 5.5, y1 - uy * 5.5
    svg.add(f'<path d="M{n(x1)} {n(y1)}L{n(bx - uy * 3.2)} {n(by + ux * 3.2)}'
            f'L{n(bx + uy * 3.2)} {n(by - ux * 3.2)}Z" fill="{color}"/>')


def figure(title, number, caption, t, F, height=252):
    """Shared plate for the project figures: panel, figure number, caption."""
    # 12px of clear space under the panel keeps text off it when the layout stacks on phones
    svg = SVG(400, height + 12, title)
    svg.add(f'<rect x=".5" y=".5" width="399" height="{height - 1}" rx="8" '
            f'fill="{t["panel"]}" stroke="{t["line"]}"/>')
    w = svg.text(F["mono_md"], f"FIG. {number}", 18, 30, 10, t["accent"], tracking=0.1)
    svg.text(F["mono"], caption, 18 + w + 12, 30, 10, t["ink2"], tracking=0.1)
    return svg


# ----------------------------------------------------------------- banner

GRID_COLS, GRID_ROWS, CELL, PITCH = 10, 8, 26, 30
HEAT = {  # (col, row): level 1-4
    (4, 0): 1, (3, 1): 3, (4, 1): 4, (2, 2): 1, (3, 2): 4, (4, 2): 2,
    (6, 4): 2, (7, 4): 4, (6, 5): 4, (7, 5): 3, (8, 5): 1, (7, 6): 1,
    (0, 5): 1, (1, 5): 2, (1, 6): 3, (2, 6): 1,
    (8, 1): 2, (9, 2): 1, (5, 6): 1,
}
ROUTE = [(0, 7), (3, 7), (3, 4), (5, 4), (5, 1), (7, 1), (7, 0), (9, 0)]
HEAT_OPACITY = {1: 0.2, 2: 0.42, 3: 0.68, 4: 1.0}


def banner(t, F):
    W, H = 846, 240
    svg = SVG(W, H, "Martin Duračka. Machine learning, computer vision and robotics.")
    svg.css = (
        ".route{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 2.2s cubic-bezier(.3,.1,.2,1) .25s both}"
        ".goal{animation:land .4s ease-out 2.3s both}"
        "@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
        "@keyframes land{from{opacity:0}to{opacity:1}}"
        "@media (prefers-reduced-motion:reduce){.route,.goal{animation:none}}"
        # README images shrink on phones; drop the grid and enlarge the name there.
        "@media (max-width:560px){.grid,.small{display:none}"
        ".id{transform:translate(0,-34px) scale(1.34)}}"
    )

    gx = W - (GRID_COLS * PITCH - (PITCH - CELL))
    gy = (H - (GRID_ROWS * PITCH - (PITCH - CELL))) / 2
    svg.add('<g class="grid">')
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            fade = min(1.0, 0.4 + 0.3 * col)
            x, y = gx + col * PITCH, gy + row * PITCH
            svg.add(f'<rect x="{n(x)}" y="{n(y)}" width="{CELL}" height="{CELL}" rx="3" '
                    f'fill="{t["cell"]}" opacity="{n(fade)}"/>')
            level = HEAT.get((col, row))
            if level:
                svg.add(f'<rect x="{n(x)}" y="{n(y)}" width="{CELL}" height="{CELL}" rx="3" '
                        f'fill="{t["accent"]}" opacity="{n(HEAT_OPACITY[level] * fade)}"/>')
    pts = [(gx + c * PITCH + CELL / 2, gy + r * PITCH + CELL / 2) for c, r in ROUTE]
    svg.add(f'<path class="route" pathLength="1" d="{rounded_route(pts, 9)}" fill="none" '
            f'stroke="{t["ink"]}" stroke-width="2" stroke-linecap="round"/>')
    (sx, sy), (ex, ey) = pts[0], pts[-1]
    svg.add(f'<circle cx="{n(sx)}" cy="{n(sy)}" r="5" fill="{t["page"]}" stroke="{t["ink"]}" stroke-width="2"/>')
    svg.add(f'<circle class="goal" cx="{n(ex)}" cy="{n(ey)}" r="6" fill="{t["ink"]}" '
            f'stroke="{t["page"]}" stroke-width="2"/>')
    svg.add("</g>")

    svg.add('<g class="small">')
    svg.add(f'<rect x="0" y="33" width="7" height="7" fill="{t["accent"]}"/>')
    svg.text(F["mono_md"], "TECHNICAL UNIVERSITY OF KOŠICE  ·  FEI", 17, 40, 10.5, t["ink2"], tracking=0.14)
    svg.add("</g>")
    svg.add('<g class="id">')
    svg.text(F["display"], "Martin Duračka", -3, 130, 70, t["ink"])
    svg.text(F["italic"], "Machine learning, computer vision & robotics", 0, 171, 24, t["ink2"])
    svg.add(f'<rect x="0" y="197" width="56" height="2" fill="{t["accent"]}"/>')
    svg.add("</g>")
    return svg


# ------------------------------------------------------------ fig. 1: BLEU

BLEU = [("German", 3.95, 1.11), ("French", 5.67, 2.25)]  # (language, translated, direct)


def fig_flamingo(t, F):
    svg = figure("BLEU on Multi30K test 2016: captions generated in English and translated "
                 "score 3.95 (German) and 5.67 (French); captions generated directly score 1.11 and 2.25.",
                 1, "BLEU ON MULTI30K TEST 2016", t, F, height=252)
    x = 18
    for color, label in ((t["accent"], "English, then translated"), (t["context"], "Generated directly")):
        svg.add(f'<rect x="{x}" y="47" width="10" height="10" rx="2" fill="{color}"/>')
        x += 16 + svg.text(F["sans"], label, x + 16, 56, 11.5, t["ink2"]) + 18

    x0, unit, top = 84, 44.0, 74
    for tick in (0, 2, 4, 6):
        gx = x0 + tick * unit
        svg.add(f'<rect x="{n(gx - 0.5)}" y="{top}" width="1" height="118" fill="{t["line"]}"/>')
        svg.text(F["mono"], str(tick), gx, top + 134, 10, t["ink2"], anchor="middle")
    for i, (language, translated, direct) in enumerate(BLEU):
        y = top + 12 + i * 54
        svg.text(F["sans_md"], language, 18, y + 21, 12, t["ink"])
        for j, (value, color) in enumerate(((translated, t["accent"]), (direct, t["context"]))):
            by, w = y + j * 18, value * unit
            # square at the baseline, 4px round at the data end
            svg.add(f'<path d="M{n(x0)} {by}h{n(w - 4)}a4 4 0 0 1 4 4v8a4 4 0 0 1 -4 4h{n(-(w - 4))}z" '
                    f'fill="{color}"/>')
            svg.text(F["sans_md"], f"{value:.2f}", x0 + w + 7, by + 12.2, 11.5, t["ink"])
    svg.text(F["sans"], "Translating scored 3.6× the direct result for German, 2.5× for French.",
             18, 232, 11, t["ink2"])
    return svg


# ---------------------------------------------------- fig. 2: architecture

def fig_autocena(t, F):
    svg = figure("AutoCena architecture: a React frontend on Azure Blob Storage calls a FastAPI backend "
                 "on Azure App Service, which uses PostgreSQL, a price model on AWS Lambda, the Gemini API "
                 "and SendGrid. A daily Azure Functions job checks price alerts.",
                 2, "WHAT RUNS WHERE", t, F, height=252)
    lx = 382
    for color, label in ((t["context"], "OTHER PROVIDERS"), (t["accent"], "AZURE")):
        lx -= F["mono"].width(label, 9, 0.1)
        svg.text(F["mono"], label, lx, 30, 9, t["ink2"], tracking=0.1)
        lx -= 9
        svg.add(f'<rect x="{n(lx)}" y="22" width="3" height="9" fill="{color}"/>')
        lx -= 14

    W, Hn = 104, 36
    nodes = {  # name: (x, y, title, host, on_azure)
        "chat": (268, 48, "Chat", "Gemini API", False),
        "web": (18, 96, "Frontend", "Blob Storage", True),
        "api": (140, 96, "Backend API", "App Service", True),
        "model": (268, 96, "Price model", "AWS Lambda", False),
        "mail": (268, 144, "Email", "SendGrid", False),
        "db": (140, 198, "Database", "PostgreSQL", True),
        "cron": (268, 198, "Daily alert job", "Functions", True),
    }
    edge = t["ink2"]
    mid = lambda k: nodes[k][1] + Hn / 2
    arrow(svg, [(18 + W, mid("web")), (140, mid("web"))], edge)
    # backend fans out to the three services on the right
    svg.add(f'<path d="M256 {n(mid("chat"))}V{n(mid("mail"))}" stroke="{edge}" stroke-width="1.25"/>')
    svg.add(f'<path d="M{140 + W} {n(mid("api"))}H256" stroke="{edge}" stroke-width="1.25"/>')
    for key in ("chat", "model", "mail"):
        arrow(svg, [(256, mid(key)), (268, mid(key))], edge)
    arrow(svg, [(140 + W / 2, 96 + Hn), (140 + W / 2, 198)], edge)
    arrow(svg, [(268, mid("cron")), (140 + W, mid("cron"))], edge)
    arrow(svg, [(268 + W / 2, 198), (268 + W / 2, 144 + Hn)], edge)
    arrow(svg, [(268 + W, mid("cron")), (382, mid("cron")), (382, mid("model")), (268 + W, mid("model"))], edge)

    svg.text(F["sans"], "Deployed on every push", 18, 213, 10.5, t["ink2"])
    svg.text(F["sans"], "by GitHub Actions.", 18, 227, 10.5, t["ink2"])

    for x, y, title, host, azure in nodes.values():
        svg.add(f'<rect x="{x + .5}" y="{y + .5}" width="{W - 1}" height="{Hn - 1}" rx="4" '
                f'fill="{t["page"]}" stroke="{t["line"]}"/>')
        svg.add(f'<path d="M{x + 4} {y}h-0a4 4 0 0 0 -4 4v{Hn - 8}a4 4 0 0 0 4 4z" '
                f'fill="{t["accent"] if azure else t["context"]}"/>')
        svg.text(F["sans_md"], title, x + 12, y + 15.5, 11.5, t["ink"])
        svg.text(F["sans"], host, x + 12, y + 29, 10.5, t["ink2"])
    return svg


# ------------------------------------------------------- fig. 3: MDMLP stats

def fig_mdmlp(t, F):
    svg = figure("MDMLP replication: 88.06% accuracy on CIFAR-10 with 0.57 million parameters, "
                 "trained from scratch.", 3, "CIFAR-10, TRAINED FROM SCRATCH", t, F, height=252)
    svg.text(F["sans_sb"], "88.06%", 16, 112, 50, t["ink"])
    svg.text(F["sans"], "accuracy", 18, 134, 12, t["ink2"])
    svg.add(f'<rect x="18" y="158" width="150" height="1" fill="{t["line"]}"/>')
    svg.text(F["sans_sb"], "0.57M", 17, 197, 26, t["ink"])
    svg.text(F["sans"], "parameters", 18, 217, 12, t["ink2"])

    # the paper's overlapping patch embedding: neighbouring windows share half their pixels
    ox, oy, pitch, px = 224, 58, 20, 18
    for row in range(8):
        for col in range(8):
            svg.add(f'<rect x="{ox + col * pitch}" y="{oy + row * pitch}" width="{px}" height="{px}" '
                    f'rx="2" fill="{t["cell"]}"/>')
    for step in (0, 2, 4):
        x, y, side = ox + step * pitch - 1, oy + step * pitch - 1, 4 * pitch
        svg.add(f'<rect x="{x - .25}" y="{y - .25}" width="{side + .5}" height="{side + .5}" rx="4" '
                f'fill="{t["accent"]}" fill-opacity=".2" stroke="{t["accent"]}" stroke-width="1.5"/>')
    svg.text(F["mono"], "OVERLAPPING PATCHES", ox + (8 * pitch - 2) / 2, 236, 9, t["ink2"],
             anchor="middle", tracking=0.1)
    return svg


def main():
    fetch_fonts()
    faces = {
        "display": Face("d", "Newsreader.ttf", {"opsz": 72, "wght": 500}),
        "italic": Face("i", "Newsreader-Italic.ttf", {"opsz": 24, "wght": 400}),
        "sans": Face("s", "PlexSans.ttf", {"wght": 400, "wdth": 100}),
        "sans_md": Face("m", "PlexSans.ttf", {"wght": 500, "wdth": 100}),
        "sans_sb": Face("b", "PlexSans.ttf", {"wght": 600, "wdth": 100}),
        "mono": Face("o", "PlexMono-Regular.ttf"),
        "mono_md": Face("p", "PlexMono-Medium.ttf"),
    }
    OUT_DIR.mkdir(exist_ok=True)
    graphics = {"banner": banner, "fig-flamingo": fig_flamingo,
                "fig-autocena": fig_autocena, "fig-mdmlp": fig_mdmlp}
    for name, build in graphics.items():
        for theme, tokens in THEMES.items():
            target = OUT_DIR / f"{name}-{theme}.svg"
            target.write_text(build(tokens, faces).render(), encoding="utf-8")
            print(f"{target.relative_to(ROOT)}  {target.stat().st_size / 1024:.1f} kB")


if __name__ == "__main__":
    main()
