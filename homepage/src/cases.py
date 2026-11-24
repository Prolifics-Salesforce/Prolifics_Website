# -*- coding: utf-8 -*-
"""Case study library for the full site (22 Nov 2026). Every entry is a published case study: the CASES list in
content.py (casestudies.com, prolifics.ai, prolifics-testing.com) plus prolifics.ai/resource-center/case-studies
pages read on 22 Nov 2026 (copies in ../ref/cs). Metrics appear only where the case study states them.
Practices: ai, fde, sf, sn, sap, app, bt, qe. Industries: banking, healthcare, retail, energy, government, legal,
higher-ed, emerging, other. ServiceNow has no case study claims by rule."""
from content import CASES
from pages_content import SF_WORK

PA = "https://prolifics.ai/resource-center/case-studies/"
# key: (client, sector label, title, brief, metric, metric label, image, logo, delivered by, url, practices, industries)
LIB = {}
def add(key, client, sector, title, brief, m, ml, im, logo, by, url, pr, ind):
    LIB[key] = dict(client=client, sector=sector, title=title, brief=brief, m=m, ml=ml, im=im, logo=logo, by=by, url=url, pr=pr, ind=ind)

# from content.CASES (casestudies.com, prolifics.ai, prolifics-testing.com)
_C = {c[0]: c for c in CASES}
def _from(f, key, pr, ind):
    _, client, sector, by, title, brief, m, ml, im, u = _C[f]
    add(key, client, sector, title, brief, m, ml, im, f, by, u, pr, ind)
_from("horizon-bcbs-nj.png", "horizon", ["bt", "app"], ["healthcare"])
_from("rac.svg", "rac", ["app"], ["other"])
_from("mckesson.svg", "mckesson", ["qe", "sap"], ["healthcare"])
_from("broadridge.svg", "broadridge", ["bt"], ["banking"])
_from("insolvency-service.svg", "insolvency", ["app"], ["government"])
_from("teradyne.svg", "teradyne", ["app"], ["other"])
_from("american-bureau-of-shipping.svg", "abs", ["ai"], ["retail"])
_from("intealth.svg", "intealth", ["sf"], ["healthcare"])
_from("cmc-energy-services.png", "cmc", ["sf"], ["energy"])

# Salesforce stories (pages_content.SF_WORK)
for i, k in enumerate(["intealth-sf", "wealthhub", "energy-orgs", "cmc-sf", "exalt", "ls-crm"]):
    client, sector, title, brief, m, ml, im, lg, by, u = SF_WORK[i]
    if k in ("intealth-sf", "cmc-sf"): continue
    add(k, client, sector, title, brief, m, ml, im, lg, by, u, ["sf"], {"wealthhub": ["banking"], "energy-orgs": ["energy"], "exalt": ["other"], "ls-crm": ["healthcare"]}[k])

# prolifics.ai case studies
add("rca-pharma", "A global pharmaceutical manufacturer", "Life sciences", "Root cause analysis with AI and a knowledge graph",
    "Manual, fragmented investigations became a faster, compliance-driven framework for a regulated manufacturing operation.",
    "60 to 80%", "less investigation effort", "r12", None, "Prolifics", PA + "ai-powered-root-cause-analysis-pharmaceutical", ["ai"], ["healthcare"])
add("rag-bank", "A global investment bank", "Investment banking", "Contact center intelligence with graph-powered RAG",
    "Accurate, compliant, context-aware answers drawn from large volumes of unstructured call transcripts.",
    "1.5M+", "calls a month in scope", "r05", None, "Prolifics", PA + "graph-powered-rag-contact-center-banking", ["ai"], ["banking"])
add("fraud-graph", "An investment bank", "Investment banking", "Fraud networks found with graph analytics",
    "Graph-based analytics that separate meaningful risk signals from normal-looking transactions at scale.",
    None, None, "g_chip", None, "Prolifics", PA + "ai-fraud-detection-banking", ["ai"], ["banking"])
add("inventory-ai", "A healthcare provider", "Healthcare", "Inventory forecasting with AI demand prediction",
    "Demand prediction that keeps stock balanced across facilities when demand shifts unexpectedly.",
    None, None, "r16", None, "Prolifics", PA + "ai-healthcare-inventory-forecasting-demand-prediction", ["ai"], ["healthcare"])
add("parking", "A leading US parking management company", "Parking and mobility", "Real-time data and AI for parking revenue",
    "Availability turned into a dynamic revenue opportunity as demand shifts with events, traffic and weather.",
    None, None, "r08", None, "Prolifics", PA + "ai-powered-parking-revenue-management", ["ai"], ["retail"])
add("auto-data", "A leading automotive manufacturer", "Automotive", "Data management modernized on Azure and Databricks",
    "A fragmented data estate across POS, supply chain and legacy repositories became one scalable cloud platform.",
    None, None, "r10", None, "Prolifics", PA + "automotive-data-platform-modernization", ["ai"], ["retail"])
add("truck-load", "A global sustainable packaging leader", "Logistics", "Truck load planning automated with AI",
    "A manual, expert-dependent planning process replaced with AI-powered automation across a complex supply chain.",
    None, None, "k_relay", None, "Prolifics", PA + "ai-powered-truck-load-planning", ["ai"], ["retail"])
add("lakehouse", "A retailer", "Retail", "A metadata driven lakehouse for retail data",
    "Disconnected systems and manual data work replaced by one automated platform with faster, consistent reporting.",
    None, None, "r13", None, "Prolifics", PA + "metadata-driven-lakehouse-retail-data-insights", ["ai"], ["retail"])
add("powerbi-legal", "A regulatory and compliance team", "Legal and compliance", "Self-service legal and compliance reporting on Power BI",
    "Complex legacy reporting replaced by self-service analytics that cut IT dependency for compliance teams.",
    None, None, "g_knot", None, "Prolifics", PA + "power-bi-self-service-analytics-compliance", ["ai"], ["legal"])
add("theatre-data", "A major theatre chain", "Entertainment", "Managed services for Azure data pipelines",
    "Reliable Azure Data Factory and Synapse pipelines behind ticket sales insight and operational reporting.",
    None, None, "e2015", None, "Prolifics", PA + "data-pipeline-managed-services-theatre-chain", ["ai"], ["retail"])
add("renewables", "A utility", "Energy and utilities", "Renewable energy integrated through API-led connectivity",
    "Distributed solar and wind assets connected to legacy distribution systems through an API-led architecture.",
    None, None, "i_powerlines_1", None, "Prolifics", PA + "api-led-renewable-energy-integration", ["app"], ["energy"])
add("mainframe", "A state Department of Human Services", "State government", "Mainframe applications retired to the cloud",
    "A mandated move off legacy mainframe applications, with zero downtime and full data validation.",
    "11x", "faster document search and retrieval", "i_columns_5", None, "Prolifics", PA + "mainframe-to-cloud-modernization", ["app"], ["government"])
add("rpg", "A wine and spirits distributor", "Distribution", "AI-assisted modernization of legacy RPG systems",
    "Critical RPG applications modernized with AI assistance, without disrupting day-to-day operations.",
    None, None, "r07", None, "Prolifics", PA + "ai-assisted-legacy-modernization-rpg", ["app", "ai"], ["retail"])
add("fin-apps", "One of the largest US financial institutions", "Banking", "Mission-critical internal applications modernized",
    "Years of technical debt, fragmented workflows and compliance challenges turned into a scalable application estate.",
    "110+", "mission-critical applications modernized", "i_bank", None, "Prolifics", PA + "legacy-application-modernization", ["app"], ["banking"])
add("water", "A national water utility in the Middle East", "Water utility", "Workforce platform rebuilt on an AI-ready architecture",
    "A maintenance-heavy legacy system replaced with an API-driven foundation for digital government services.",
    None, None, "i_emerging", None, "Prolifics", PA + "digital-transformation-in-water-utilities", ["app"], ["energy", "emerging"])
add("wms", "A home furnishings and kitchenware retailer", "Retail and logistics", "Warehouse operations moved to Manhattan WMS",
    "A move from legacy mainframe systems to Manhattan WMS across multiple distribution centers and hubs.",
    None, None, "i_aerial_port_2", None, "Prolifics", PA + "manhattan-wms-implementation-services", ["app"], ["retail"])
add("restaurants", "A global restaurant, bar and cafe operator", "Hospitality", "Workforce integration run as a managed service",
    "Prolifics Managed Services runs the MuleSoft integration behind SAP SuccessFactors people and benefits programs.",
    "38", "countries supported", "globe", None, "Prolifics", PA + "prolifics-managed-services", ["app"], ["retail"])
add("contracts", "A leading communications provider", "Communications", "Franchise contract management automated",
    "An automated system that keeps franchise agreements across the US organized, compliant and renewed on time.",
    None, None, "r11", None, "Prolifics", PA + "contract-management-automation", ["bt"], ["legal"])
add("courts", "Tennessee Administrative Office of the Courts", "State government", "Claims processing modernized for the courts",
    "Intelligent automation and a cloud-first platform brought real-time visibility to claims processing.",
    "Under 10 days", "claims processing, down from 45 days", "i_dome_5", None, "Prolifics", PA + "justice-delivery-automation", ["bt"], ["government", "legal"])
add("vital-records", "A state Department of Health", "State government", "Vital records services modernized for citizens",
    "Paper-heavy birth, death and marriage certificate processes moved to modern digital citizen services.",
    None, None, "r03", None, "Prolifics", PA + "citizen-services-modernization-public-sector", ["bt"], ["government"])
add("licensing", "A government healthcare authority in the Middle East", "Healthcare regulation", "Healthcare licensing transformed",
    "Slow, manual licensing for healthcare providers and facilities replaced with an automated, citizen-friendly platform.",
    "50%+", "of licensing processes automated", "i_hosp_arch_4", None, "Prolifics", PA + "intelligent-licensing-transformation-healthcare", ["bt"], ["healthcare", "government", "emerging"])
add("behavioral", "A digital behavioral health organization", "Behavioral health", "Platforms engineered for behavioral health",
    "Engineering that helps identify people who need behavioral care and connect patients, providers and payers.",
    None, None, "g_meeting", None, "Prolifics", PA + "engineering-behavioral-health-platforms", ["app"], ["healthcare"])
add("itam", "A leading IT asset management provider", "Technology", "Faster, more reliable releases for an ITAM platform",
    "Quality and workflow improvements that helped the platform scale and ship software releases faster.",
    None, None, "g_chip", None, "Prolifics", PA + "it-asset-management-modernization", ["qe", "app"], ["other"])
add("aderant", "A leading law firm", "Legal", "A seamless Aderant Expert go-live through managed testing",
    "Functional, integration and performance testing reduced implementation risk and delivered a stable launch.",
    None, None, "r06", None, "Prolifics Testing", PA + "aderant-expert-testing-services", ["qe"], ["legal"])
add("perf-legal", "A global law firm", "Legal", "Performance testing for a business-critical risk platform",
    "Testing maturity strengthened, geographic latency uncovered and a risk platform validated before rollout.",
    None, None, "sp_eval", None, "Prolifics Testing", PA + "enterprise-application-performance-testing-services", ["qe"], ["legal"])
add("sap-lowcode", "A leading American healthcare distributor", "Healthcare distribution", "SAP testing accelerated with low-code automation",
    "Automated validation of frequent SAP patches across 400+ interfaces, with zero disruption during patching.",
    "30%", "faster automation efforts", "g_catalog", None, "Prolifics", PA + "low-code-sap-test-automation", ["qe", "sap"], ["healthcare"])
add("chemicals", "A specialty chemicals manufacturer", "Specialty chemicals", "One SAP S/4HANA core across ten plants",
    "A unified SAP S/4HANA transformation across manufacturing units, warehouses and R&D centers in India.",
    None, None, "promo", None, "Prolifics", PA + "sap-s-4hana-chemical-industry", ["sap"], ["emerging", "retail"])
add("pharma-sap", "A life sciences enterprise", "Life sciences", "Pharma operations scaled on SAP",
    "Fragmented systems modernized and manual processes automated, with real-time insight across every function.",
    None, None, "cs_mckesson", None, "Prolifics", PA + "sap-s-4hana-in-pharma-transformation", ["sap"], ["healthcare"])
add("agro", "An agro manufacturer in Maharashtra", "Agro manufacturing", "Agro manufacturing digitized on SAP S/4HANA Cloud",
    "Sugar, spirits and renewable power operations moved from manual, siloed processes to one cloud ERP.",
    "50%", "faster approvals and reconciliations", "e2000", None, "Prolifics", PA + "sap-s4hana-cloud-agro-manufacturing-digitization", ["sap"], ["emerging"])
add("wine", "India's premier wine producer", "Food and beverage", "A legacy brand moved to SAP S/4HANA Cloud",
    "A cloud ERP for operations across 25 states, 70+ warehouses and 850 partner farms.",
    "40%", "improvement in operational efficiency", "sp_build", None, "Prolifics", PA + "sap-s4hana-cloud-digital-transformation", ["sap"], ["emerging"])
add("cpg-btp", "A global CPG enterprise", "Consumer goods", "Legacy SAP and EDI modernized on SAP BTP",
    "A composable, event-driven, API-first integration architecture for better vendor collaboration.",
    None, None, "r04", None, "Prolifics", PA + "sap-btp-legacy-modernization-in-cpg", ["sap"], ["retail"])

PRACTICE_CASES = {
    "ai": ["rca-pharma", "rag-bank", "abs", "auto-data", "truck-load", "fraud-graph"],
    "fde": [],
    "sf": ["intealth", "wealthhub", "energy-orgs", "cmc", "exalt", "ls-crm"],
    "sn": [],
    "sap": ["mckesson", "sap-lowcode", "wine", "agro", "cpg-btp", "chemicals"],
    "app": ["rac", "insolvency", "fin-apps", "mainframe", "renewables", "restaurants"],
    "bt": ["horizon", "broadridge", "courts", "licensing", "contracts", "vital-records"],
    "qe": ["mckesson", "sap-lowcode", "aderant", "perf-legal", "itam"],
}
INDUSTRY_CASES = {
    "banking": ["broadridge", "rag-bank", "fin-apps", "fraud-graph", "wealthhub"],
    "healthcare": ["horizon", "mckesson", "intealth"],
    "retail": ["wms", "truck-load", "cpg-btp", "lakehouse", "rpg", "auto-data"],
    "energy": ["cmc", "renewables", "water", "energy-orgs"],
    "government": ["insolvency", "courts", "mainframe", "vital-records", "licensing"],
    "legal": ["aderant", "perf-legal", "powerbi-legal", "contracts"],
    "higher-ed": [],
    "emerging": ["wine", "agro", "chemicals", "water", "licensing"],
}
