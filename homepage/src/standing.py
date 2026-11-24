# -*- coding: utf-8 -*-
"""IBM and SAP credentials strip, shared by both home page versions. Kept quiet on purpose (Mac, 21 Nov 2026):
certifications and accolades only, no big headline, no approach steps.
Sources (Prolifics' own published claims, read 20 Nov 2026):
  IBM: https://prolifics.ai/partnerships/ibm (Platinum Business Partner, IBM Partner Plus, original watsonx beta partner);
       awards from https://prolifics.ai/about-us (2025 IBM North America Sustainability Award, 2019 IBM Beacon Award)
  SAP: https://prolifics.ai/sap (SAP Center of Excellence, RISE with SAP and GROW with SAP); Castaliaz as SAP Gold
       Partner from the 2025 acquisition announcement (dbta.com)."""
import html
E = lambda s: html.escape(s, quote=True)

IBM = {"logo": "ibm.svg", "name": "IBM", "items": [
    ("cert", "IBM Platinum Business Partner"),
    ("cert", "IBM Partner Plus"),
    ("cert", "Original watsonx beta partner"),
    ("award", "IBM North America Sustainability Award", "2025"),
    ("award", "IBM Beacon Award, Outstanding Analytics Solution", "2019"),
]}
SAP = {"logo": "sap.svg", "name": "SAP", "items": [
    ("cert", "SAP Gold Partner, through Castaliaz"),
    ("cert", "SAP Center of Excellence"),
    ("cert", "RISE with SAP and GROW with SAP"),
]}

ICON = {
    "cert": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="10" r="6.5"/><path d="M9.2 10.1l2 2 3.7-3.9M8.6 15.6L7.5 21l4.5-2.3 4.5 2.3-1.1-5.4"/></svg>',
    "award": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h10v4a5 5 0 0 1-10 0V4zM7 6H4v1.5A3.5 3.5 0 0 0 7.5 11M17 6h3v1.5a3.5 3.5 0 0 1-3.5 3.5M12 13v4M8.5 20.5h7M9.5 17h5v3.5h-5z"/></svg>',
}

def _panel(p, awards=True):
    lis = []
    for it in p["items"]:
        if it[0] == "award" and not awards:
            continue
        year = '<b>%s</b>' % it[2] if it[0] == "award" else ""
        lis.append('<li class="%s">%s<span>%s</span>%s</li>' % (it[0], ICON[it[0]], E(it[1]), year))
    return ('<div class="sd"><img class="sd-lg" src="assets/partners/%s" alt="%s"><ul>%s</ul></div>'
            % (p["logo"], E(p["name"]), "".join(lis)))

def section(img, arrow, label_html, variant="v1"):
    """img and arrow are unused now; kept so both builders call it the same way.
    Version 2 ("k") leaves the IBM awards out: its Industry recognition section right below already lists them."""
    awards = variant != "k"
    return ('<section class="stand %s" id="ibm-sap"><div class="wrap"><div class="sd-in" data-r>'
            '<div class="sd-head">%s<h2>Recognized by IBM and SAP</h2></div>'
            '<div class="sd-g">%s%s</div></div></div></section>'
            % (variant, label_html, _panel(IBM, awards), _panel(SAP, awards)))
