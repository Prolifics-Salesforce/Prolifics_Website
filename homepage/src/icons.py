# -*- coding: utf-8 -*-
"""Prolifics line icon set.
Motif taken from the Prolifics wordmark: a forward lean (every glyph is skewed -8 degrees, like the
italic logo) and a short cyan "speed bar" (the horizontal stroke across the top of the P and r),
drawn as the accent stroke in each icon. 24 x 24 grid, 1.6 stroke, miter joins, butt caps.
Usage: icon("agent") returns inline <svg>. Colors come from CSS: .ic { color: navy } .ic .a { stroke: cyan }"""

# each entry: (main paths, accent path). Paths are drawn upright, the skew is applied by the wrapper.
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # project root, so the codebase runs from any folder
I = {
 "agent":      ('<rect x="5" y="7" width="14" height="11" rx="1"/><path d="M9 12h.01M15 12h.01M9.5 15h5M12 7V4"/>', '<path d="M8 4h8"/>'),
 "spark":      ('<path d="M12 4l1.8 5.2L19 11l-5.2 1.8L12 18l-1.8-5.2L5 11l5.2-1.8z"/>', '<path d="M16 19h5"/>'),
 "cloud":      ('<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.2 11 3.5 3.5 0 0 0 7 18z"/>', '<path d="M4 21h9"/>'),
 "quote":      ('<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 15h7M9 18h4"/>', '<path d="M2 8h5"/>'),
 "revenue":    ('<path d="M4 19V5M4 19h16"/><path d="M7 15l4-4 3 3 5-6"/>', '<path d="M15 6h5"/>'),
 "molecule":   ('<circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="9" r="2.5"/><circle cx="10" cy="17" r="2.5"/><path d="M9.3 8.1l5.3.6M8 9.3l1.4 5.3M15.4 11l-3.6 4"/>', '<path d="M15 20h6"/>'),
 "bank":       ('<path d="M3 9l9-5 9 5M5 9v9M9.7 9v9M14.3 9v9M19 9v9M3 18h18"/>', '<path d="M3 21h18"/>'),
 "shield":     ('<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>', '<path d="M2 6h4"/>'),
 "risk":       ('<path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17h.01"/>', '<path d="M15 4h6"/>'),
 "compliance": ('<rect x="5" y="4" width="14" height="17" rx="1"/><path d="M9 4V2.5h6V4M8.5 12l2.2 2.2L15.5 9.5M8.5 18h7"/>', '<path d="M1 9h4"/>'),
 "workflow":   ('<rect x="3" y="4" width="6" height="5" rx="1"/><rect x="15" y="4" width="6" height="5" rx="1"/><rect x="9" y="15" width="6" height="5" rx="1"/><path d="M9 6.5h6M6 9v3.5h6V15M18 9v3.5h-6"/>', '<path d="M2 22h8"/>'),
 "gear":       ('<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>', '<path d="M17 21h5"/>'),
 "data":       ('<ellipse cx="12" cy="6" rx="7" ry="2.5"/><path d="M5 6v12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V6M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>', '<path d="M1 3h5"/>'),
 "integration":('<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.3 11l7.4-4M8.3 13l7.4 4"/>', '<path d="M2 21h7"/>'),
 "team":       ('<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9.5" r="2.3"/><path d="M3.5 19c.6-3.3 2.7-5 5.5-5s4.9 1.7 5.5 5M15 14.3c2.6-.5 4.8.9 5.5 4.7"/>', '<path d="M3 3h6"/>'),
 "engineer":   ('<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.8 3.6-6 7-6s6.2 2.2 7 6M8.5 5.5h7"/>', '<path d="M16 2.5h5"/>'),
 "deploy":     ('<path d="M12 3c3 2 5 5.5 5 9.5L15 16H9l-2-3.5C7 8.5 9 5 12 3z"/><circle cx="12" cy="10" r="1.6"/><path d="M9 16l-1.5 4M15 16l1.5 4"/>', '<path d="M2 20h5"/>'),
 "chart":      ('<path d="M4 20V10M9.3 20V5M14.6 20v-7M20 20V8"/>', '<path d="M2 22h8"/>'),
 "globe":      ('<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.5 3.6 5.3 3.6 8.5s-1.1 6-3.6 8.5c-2.5-2.5-3.6-5.3-3.6-8.5S9.5 6 12 3.5z"/>', '<path d="M16 2h6"/>'),
 "legacy":     ('<circle cx="12" cy="13" r="7.5"/><path d="M12 9v4.5l3 2"/>', '<path d="M7 2.5h10"/>'),
 "handshake":  ('<path d="M3 12l3-3 4 2 3-2.5 3 .5 5 3M6 9l-3 6 4 4 2-1M16 9l3 6-6 4-4-3"/><path d="M10 14l2 2M12 12.5l2.5 2.5"/>', '<path d="M2 4h6"/>'),
 "insight":    ('<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5.5 5.5M8 10.5h5"/>', '<path d="M16 3h6"/>'),
 "lock":       ('<rect x="5" y="10" width="14" height="10" rx="1"/><path d="M8 10V7.5a4 4 0 0 1 8 0V10M12 14v2.5"/>', '<path d="M1 22h7"/>'),
 "health":     ('<rect x="4" y="4" width="16" height="16" rx="1"/><path d="M12 8v8M8 12h8"/>', '<path d="M16 1.5h6"/>'),
 "energy":     ('<path d="M13 3L5 13h6l-1 8 8-10h-6z"/>', '<path d="M16 21h6"/>'),
 "factory":    ('<path d="M3 20V10l5 3V10l5 3V10l5 3V5h3v15z"/><path d="M7 17h2M12 17h2M17 17h1"/>', '<path d="M1 2.5h7"/>'),
 "government": ('<path d="M4 9h16M12 3l8 6H4zM6 9v8M10 9v8M14 9v8M18 9v8M4 20h16"/>', '<path d="M2 22.5h8"/>'),
 "retail":     ('<path d="M3 5h2.5l2 10h10l2-7H7"/><circle cx="9.5" cy="19" r="1.4"/><circle cx="16" cy="19" r="1.4"/>', '<path d="M13 2.5h7"/>'),
 "insurance":  ('<path d="M3 11a9 9 0 0 1 18 0zM12 11v7a2 2 0 0 0 4 0"/>', '<path d="M2 3h6"/>'),
 "headset":    ('<path d="M5 14v-2a7 7 0 0 1 14 0v2"/><rect x="3.5" y="13" width="4" height="6" rx="1"/><rect x="16.5" y="13" width="4" height="6" rx="1"/><path d="M18.5 19c0 1.5-2 2.5-5 2.5"/>', '<path d="M2 3h6"/>'),
 "document":   ('<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 11h7M9 14h7M9 17h7"/>', '<path d="M1 21.5h4"/>'),
 "target":     ('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="M12 12l7-7"/>', '<path d="M16 4h5"/>'),
 "pod":        ('<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><path d="M17 13v8M13 17h8"/>', '<path d="M1 1h6"/>'),
 "code":       ('<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 4l-3 16"/>', '<path d="M15 22h6"/>'),
 "testing":    ('<path d="M9 3h6M10 3v6l-5 10a1.5 1.5 0 0 0 1.3 2h11.4A1.5 1.5 0 0 0 19 19l-5-10V3"/><path d="M7.5 15h9"/>', '<path d="M17 4h5"/>'),
 "managed":    ('<path d="M20 12a8 8 0 0 1-14.3 4.9M4 12A8 8 0 0 1 18.3 7.1"/><path d="M18.5 3v4.5H14M5.5 21v-4.5H10"/>', '<path d="M9 12h6"/>'),
 "augment":    ('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.8 3.4-6 6.5-6s5.7 2.2 6.5 6M19 8v6M16 11h6"/>', '<path d="M2 2.5h6"/>'),
 "compass":    ('<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>', '<path d="M15 2h6"/>'),
 "accelerator":('<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4.5-6"/>', '<path d="M2 21.5h20"/>'),
 "dashboard":  ('<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M8 9v11M11 13h7M11 16h5"/>', '<path d="M14 1.5h7"/>'),
 "pin":        ('<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>', '<path d="M15 22h6"/>'),
 "mail":       ('<rect x="3" y="5.5" width="18" height="13" rx="1"/><path d="M3 7l9 6 9-6"/>', '<path d="M1 21.5h7"/>'),
 "calendar":   ('<rect x="3.5" y="5" width="17" height="15" rx="1"/><path d="M3.5 10h17M8 3v4M16 3v4M8 14h3M13 14h3M8 17h3"/>', '<path d="M14 22.5h7"/>'),
 "mic":        ('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/>', '<path d="M17 3.5h5"/>'),
 "play":       ('<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M10 9l5 3-5 3z"/>', '<path d="M1 22h8"/>'),
 "arrow":      ('<path d="M4 12h15M13 6l6 6-6 6"/>', ''),
 "check":      ('<path d="M5 12.5l4.5 4.5L19 7.5"/>', ''),
 "plus":       ('<path d="M12 5v14M5 12h14"/>', ''),
 "people":     ('<circle cx="12" cy="7.5" r="3"/><circle cx="5.5" cy="10" r="2.2"/><circle cx="18.5" cy="10" r="2.2"/><path d="M7 19c.6-3 2.6-5 5-5s4.4 2 5 5M2 18c.3-2 1.6-3.3 3.5-3.3M22 18c-.3-2-1.6-3.3-3.5-3.3"/>', '<path d="M8 2h8"/>'),
 "layers":     ('<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.5l9 5 9-5M3 17l9 5 9-5"/>', '<path d="M17 2.5h5"/>'),
 "search":     ('<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5l5 5"/>', ''),
 "menu":       ('<path d="M3 7h18M3 12h18M3 17h18"/>', ''),
 "close":      ('<path d="M6 6l12 12M18 6L6 18"/>', ''),
 "linkedin":   ('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 10v7M8 7v.01M12 17v-4a2.5 2.5 0 0 1 5 0v4M12 10v7"/>', ''),
 "service":    ('<path d="M4 17h16M6 17a6 6 0 0 1 12 0M12 7.5V6M9 20h6"/>', '<path d="M2 3h6"/>'),
 "migrate":    ('<rect x="2.5" y="6" width="7" height="12" rx="1"/><rect x="14.5" y="6" width="7" height="12" rx="1"/><path d="M9.5 12h5M12.5 9.5l2.5 2.5-2.5 2.5"/>', '<path d="M8 2.5h8"/>'),
 "graduation": ('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c2 2 10 2 12 0v-5M22 9v6"/>', '<path d="M3 21h8"/>'),
 "legal":      ('<path d="M12 4v16M7 20h10M5 8h14M5 8l-2.5 6a2.5 2.5 0 0 0 5 0zM19 8l-2.5 6a2.5 2.5 0 0 0 5 0z"/>', '<path d="M9 2h6"/>'),
 "truck":      ('<path d="M2 6h12v10H2zM14 10h4l3 3v3h-7"/><circle cx="6" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>', '<path d="M1 3h7"/>'),
}

def icon(name, size=28, cls="ic"):
    main, acc = I[name]
    acc_g = ('<g class="a">%s</g>' % acc) if acc else ""
    return ('<svg class="%s" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linejoin="miter" stroke-linecap="butt" aria-hidden="true">'
            '<g transform="skewX(-8) translate(1.6 0)">%s%s</g></svg>') % (cls, size, size, main, acc_g)

def sheet():
    """Contact sheet for review and for the design brief."""
    cells = "".join('<div class="c">%s<span>%s</span></div>' % (icon(k, 40), k) for k in I)
    return ('<!doctype html><meta charset="utf-8"><title>Prolifics icon set</title><style>'
            'body{font-family:Inter,Arial,sans-serif;background:#fff;color:#001F5B;margin:40px}'
            'h1{font-size:22px}.g{display:grid;grid-template-columns:repeat(8,1fr);gap:18px}'
            '.c{border:1px solid #DCE4F2;border-radius:6px;padding:18px 8px;text-align:center}'
            '.c span{display:block;font-size:11px;margin-top:8px;color:#4A5878}.ic .a{stroke:#00AEEF}'
            '.dark{background:#001F5B;padding:24px;margin-top:24px;border-radius:8px;color:#fff}.dark .ic{color:#fff}'
            '</style><h1>Prolifics line icons, %d glyphs</h1><p>Forward lean and cyan speed bar from the wordmark.</p>'
            '<div class="g">%s</div><div class="dark g">%s</div>') % (len(I), cells, cells)

if __name__ == "__main__":
    open(ROOT + "/design-briefs/icon-sheet.html", "w").write(sheet())
    print(len(I), "icons")
