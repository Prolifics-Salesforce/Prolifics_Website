# -*- coding: utf-8 -*-
"""Home page content. Menu items and paths are taken from https://prolifics-website.vercel.app (19 November 2026).
Company figures are Prolifics' own published numbers; each carries its source. Case study metrics come from
Prolifics and group company case studies (gtm/sites/content/shared.json). House rules: no em or en dashes,
no exclamation marks, no pricing."""

PRACTICES = [
    {"k": "ai", "name": "AI & Data", "icon": "data", "img": "p_ai", "href": "/services/ai-services",
     "desc": "Strategy, platforms and operations that turn data into production AI.",
     "long": "AI-ready data platforms, analytics, MLOps and governance, with responsible AI built in from day one.",
     "groups": [
         ("AI Services", [("AI Maturity & Readiness", "/services/ai-maturity"), ("Generative AI", "/services/generative-ai"),
                          ("AI as a Service (AIaaS)", "/services/aiaas"), ("Custom AI Development", "/services/custom-ai")]),
         ("Data", [("Data Assessment", "/services/data-assessment"), ("Data Engineering", "/services/data-engineering"),
                   ("Data Management", "/services/data-management"), ("Analytics", "/services/analytics")]),
         ("Operate & Govern", [("MLOps", "/services/mlops"), ("Data & AI Governance", "/services/data-governance"),
                               ("Data & AI Managed Services", "/services/data-managed")]),
     ], "start": ("Data & AI Maturity Assessment", "/services/ai-maturity")},
    {"k": "fde", "name": "FDE AI Engineering", "icon": "pod", "img": "p_fde", "href": "/services/fde-ai-engineering",
     "desc": "Forward deployed pods that take AI from pilot to production inside your teams.",
     "long": "Small senior pods embed with the business owner, ship one workflow at a time and stay accountable for the result in production.",
     "groups": [
         ("Pods", [("AI & Data Pod", "/services/fde-ai-engineering"), ("Salesforce & Agentforce Pod", "/services/fde-ai-engineering"),
                   ("ServiceNow Pod", "/services/fde-ai-engineering"), ("SAP & ERP Pod", "/services/fde-ai-engineering"),
                   ("Integration & Automation Pod", "/services/fde-ai-engineering"), ("Quality & Testing for AI Pod", "/services/fde-ai-engineering")]),
         ("Engage", [("Advisory", "/services/fde-ai-engineering"), ("Co-delivery", "/services/fde-ai-engineering"),
                     ("Build-operate-transfer", "/services/fde-ai-engineering"), ("Fully managed", "/services/fde-ai-engineering")]),
     ], "start": ("Talk to an FDE Expert", "/contact")},
    {"k": "sf", "name": "Salesforce", "icon": "cloud", "img": "p_sf", "href": "/services/salesforce",
     "desc": "Agentforce 360, Data 360 and the core clouds, implemented and governed for the agentic enterprise.",
     "long": "Agentforce, Data 360 and the core clouds, from first agent to managed operations, with the integration depth agents need to act.",
     "groups": [
         ("Agentic AI", [("Agentforce Implementation", "/services/agentforce"), ("Agentforce Training", "/services/agentforce-training"),
                         ("AIforce: Claude, Slack & Coworker", "/services/sf-aiforce"), ("Agent Governance & Trust", "/services/sf-agent-governance")]),
         ("Platform & Clouds", [("Data 360", "/services/sf-data360"), ("Sales, Service & Marketing Cloud", "/services/sf-clouds"),
                                ("Industry Clouds", "/services/sf-industries")]),
         ("Services", [("Implementation & Migration Services", "/services/sf-implementation"),
                       ("Integration & Automation Services", "/services/sf-integration"),
                       ("Optimization & Managed Services", "/services/sf-optimisation")]),
     ], "start": ("Agentforce Readiness Assessment", "/services/agentforce")},
    {"k": "sn", "name": "ServiceNow", "icon": "workflow", "img": "p_sn", "href": "/services/servicenow",
     "desc": "Governed AI agents and workflows across IT, employee, customer, security and risk.",
     "long": "Now Assist, AI Control Tower and the core workflows, connected to the systems agents need and governed from the first release.",
     "groups": [
         ("AI Platform", [("Now Assist & AI Specialists", "/services/sn-ai-agents"), ("ServiceNow Otto", "/services/sn-otto"),
                          ("Action Fabric & MCP", "/services/sn-action-fabric"), ("AI Control Tower", "/services/sn-ai-control-tower")]),
         ("Workflows", [("ITSM, ITOM & AIOps", "/services/sn-itsm"), ("HR Service Delivery & Employee", "/services/sn-employee"),
                        ("Autonomous CRM & CSM", "/services/sn-crm"), ("Security & Risk", "/services/sn-security")]),
         ("Build & Run", [("App Engine & Build Agent", "/services/sn-build"),
                          ("Implementation, Upgrades & Managed Services", "/services/sn-implementation")]),
     ], "start": ("ServiceNow Platform & AI Readiness", "/services/servicenow")},
    {"k": "sap", "name": "SAP & ERP", "icon": "layers", "img": "p_sap", "href": "/services/sap",
     "desc": "S/4HANA migration, clean-core extensions and SAP Business AI, delivered with Castaliaz.",
     "long": "A clear path off ECC, clean-core extensions on BTP and Joule in the processes that matter, delivered with Castaliaz.",
     "groups": [
         ("Migrate", [("S/4HANA Implementation & Migration", "/services/s4hana"), ("ERP Modernization", "/services/erp-modernization")]),
         ("Innovate", [("SAP BTP & Integration", "/services/sap-btp"), ("Joule & SAP Business AI", "/services/sap-ai")]),
         ("Run", [("SAP Testing & Managed Services", "/services/sap-testing"), ("SAP", "/services/sap")]),
     ], "start": ("S/4HANA Readiness Check", "/services/s4hana")},
    {"k": "app", "name": "Application & Cloud", "icon": "code", "img": "p_app", "href": "/services/app-services",
     "desc": "Modern applications on secure, scalable cloud platforms, connected and automated so AI can act across the enterprise.",
     "long": "Modern applications, cloud platforms, integration and automation, so AI can act across the enterprise.",
     "groups": [
         ("Application Services", [("Modernize Legacy Apps", "/services/legacy-modernisation"), ("Application Management", "/services/app-management"),
                                   ("Microservices Architecture", "/services/microservices"), ("Application Security", "/services/appsec")]),
         ("Cloud & Infrastructure", [("Cloud Migration & Integration", "/services/cloud-migration"), ("Platform Engineering", "/services/platform-engineering"),
                                     ("Database Migration", "/services/database-migration")]),
         ("Digital Engineering", [("DevOps & Platform Engineering", "/services/devops-platform"), ("SDLC Automation", "/services/sdlc-automation"),
                                  ("DevOps", "/services/devops")]),
         ("Integration", [("Integration Strategy", "/services/integration-strategy"), ("API Development & Management", "/services/api-dev"),
                          ("API Managed Services", "/services/api-managed")]),
         ("Automation", [("Business Process Automation", "/services/bpa"), ("Maturity Assessments", "/services/maturity-assessments")]),
     ], "start": ("Maturity Assessments", "/services/maturity-assessments")},
    {"k": "bt", "name": "Business Transformation", "icon": "compass", "img": "p_bt", "href": "/services/business-transformation",
     "desc": "Prove value quickly, then redesign operations around AI.",
     "long": "Prove value on one process with a proof of value, then redesign operations around what worked.",
     "groups": [
         ("Transform", [("AI-Led Operations", "/services/ai-led-ops"), ("Process Optimization", "/services/process-optimisation")]),
         ("Innovate", [("Innovation as a Service", "/services/innovation-aas"), ("PoV / PoC / PoT", "/services/pov-poc-pot")]),
     ], "start": ("PoV / PoC / PoT", "/services/pov-poc-pot")},
    {"k": "qe", "name": "Quality Engineering", "icon": "testing", "img": "p_qe", "href": "/services/qa",
     "desc": "AI-driven testing that improves quality while accelerating releases.",
     "long": "AI test automation for enterprise platforms, and testing for AI itself: evaluation, red teaming and regression from week one.",
     "groups": [
         ("Testing", [("AI Test Automation", "/services/ai-test-automation"), ("Performance Engineering", "/services/performance-engineering"),
                      ("Testing for AI", "/services/testing-for-ai")]),
         ("Assurance", [("Accessibility & Compliance", "/services/accessibility"), ("Managed Testing Services", "/services/managed-testing")]),
     ], "start": ("Testing for AI", "/services/testing-for-ai")},
]

TECH = [
    ("CRM & Service", ["Salesforce", "Agentforce", "Data 360", "MuleSoft", "Tableau", "ServiceNow"]),
    ("ERP & Business Apps", ["SAP S/4HANA", "SAP BTP", "Microsoft Dynamics 365", "Power Platform"]),
    ("Cloud", ["AWS", "Microsoft Azure", "Google Cloud", "Kubernetes", "Red Hat OpenShift"]),
    ("AI & Integration", ["IBM watsonx", "IBM Cloud Pak for Integration", "Azure OpenAI", "Amazon Bedrock", "Google Vertex AI"]),
    ("Prolifics Tools", ["JAM/Panther", "Prolifics Testing"]),
]

SOLUTIONS = [
    ("Agentic Enterprise", [
        ("Agentic AI Starter", "Your first AI agent in production, measured against a baseline.", "/solutions/agentic-starter", "agent", "6 to 8 weeks"),
        ("AI Governance & Agent Control", "Inventory, govern and secure every model and agent.", "/solutions/ai-governance", "shield", "4 to 6 weeks to operating model"),
        ("Enterprise Knowledge Assistant", "Grounded answers from your documents, tickets and systems.", "/solutions/knowledge-assistant", "search", None)]),
    ("Customer & Revenue", [
        ("Customer 360 with Agentforce", "Unified customer data that powers agents, service and marketing.", "/solutions/customer-360", "people", "8 to 12 weeks"),
        ("Intelligent Contact Center", "AI and voice agents working alongside your service teams.", "/solutions/contact-center", "headset", None)]),
    ("Operations & Service", [
        ("Autonomous IT Service Desk", "AI specialists that resolve IT requests end to end.", "/solutions/service-desk", "service", "6 to 8 weeks"),
        ("Intelligent Document Processing", "Extract, classify and act on documents automatically.", "/solutions/idp", "document", None),
        ("Process Automation with Agents", "Agents and workflows that complete multi-step processes across systems.", "/solutions/process-agents", "workflow", None)]),
    ("Modernize", [
        ("ECC to S/4HANA Fast-Track", "A clear, low-risk path off ECC before the 2027 deadline.", "/solutions/s4-fasttrack", "migrate", "6 week readiness, then phased migration"),
        ("AI-Assisted Legacy Modernization", "Use AI to understand and modernize legacy code faster.", "/solutions/legacy-ai", "legacy", "4 week assessment, then waves"),
        ("Data Platform Modernization", "An AI-ready lakehouse that replaces legacy warehouses.", "/solutions/data-platform", "data", None)]),
    ("Assure", [
        ("AI Test Automation for Enterprise Platforms", "Automated regression for Salesforce, SAP and ServiceNow releases.", "/solutions/ai-testing", "testing", None),
        ("Responsible AI & EU AI Act Readiness", "Meet AI regulation without slowing innovation.", "/solutions/eu-ai-act", "compliance", None)]),
    ("Industry Solutions", [
        ("Wildfire Risk Mitigation AI", "AI decision support for wildfire prevention.", "/solutions/wildfire", "risk", None),
        ("Real-Time Fraud Detection", "Spot fraud and anomalies as transactions happen.", "/solutions/fraud", "lock", None),
        ("Connected Patient & Member Engagement", "Personalized engagement on secure, interoperable data.", "/solutions/patient", "health", None)]),
]

INDUSTRIES = [
    ("Banking & Finance", "Streamline operations and boost performance with data-driven financial strategies.", "/industries/banking", "bank", "i_bank"),
    ("Healthcare & Life Sciences", "Innovative AI solutions for better patient outcomes and operational efficiency.", "/industries/healthcare", "health", "i_hosp_arch_4"),
    ("Retail, CPG & Logistics", "Optimize supply chains and personalize customer experiences.", "/industries/retail", "retail", "i_aerial_port_2"),
    ("Energy & Utilities", "Digital transformation for smarter energy management and distribution.", "/industries/energy", "energy", "i_powerlines_1"),
    ("Government & Public Sector", "Innovation for public services to improve citizen engagement and trust.", "/industries/government", "government", "i_columns_5"),
    ("Legal Sector", "Secure, AI-assisted workflows for legal teams and firms.", "/industries/legal", "legal", "i_dome_5"),
    ("Higher Education", "AI and data solutions for student success and efficient campus operations.", "/industries/higher-ed", "graduation", "i_edu"),
    ("Emerging Markets", "Tailored strategies for growing global markets.", "/industries/emerging-markets", "globe", "i_emerging"),
]

ABOUT = [
    ("Company", [("Overview", "Our mission, story and values", "/about"), ("Leadership", "The team leading Prolifics", "/about/leadership"), ("Group companies", "Enable, Castaliaz, Prolifics Testing, Tier 2", "/group"),
                 ("Careers", "Join 2,000+ experts worldwide", "/about/careers"), ("Social Impact", "Technology that serves people", "/about/social-impact"),
                 ("ESG Vision", "Sustainable, responsible technology", "/about/esg")]),
    ("Connect", [("Contact", "Talk to our experts", "/contact"), ("Locations", "North America, Europe, India, UAE", "/about/locations"),
                 ("Partnerships", "IBM, Salesforce, ServiceNow, SAP and more", "/partnerships"),
                 ("Resource Center", "Blogs, news, events and case studies", "/resources")]),
]

# Resources menu (27 Nov 2026): the library types open the live library on /resources already filtered; Happenings
# moved here from the main menu. Every item opens a page on this site; the content behind each comes from HubSpot.
RESOURCES_MENU = [
    ("Library", [("Resource Center", "Guides, library and case studies in one place", "/resources"), ("Blogs", "Practical thinking on AI, data and platforms", "/resources?type=blog#library"),
                 ("Case Studies", "Published client results", "/resources?type=case-study#library"), ("News", "Partner and company news", "/resources?type=news#library"),
                 ("One Pagers", "Short overviews of what we offer", "/resources?type=one-pager#library")]),
    ("Events and more", [("Events", "Events, webinars and campaigns", "/events"), ("Planning Guides", "Questions to answer before you start", "/resources?type=planning-guide#library"),
                         ("Videos", "Watch Prolifics videos", "/resources?type=video#library")]),
]

PARTNERS = ["IBM", "Salesforce", "ServiceNow", "SAP", "Microsoft", "Boomi", "AWS", "MuleSoft", "Databricks", "Red Hat",
            "Snowflake", "Google Cloud", "EDB", "Tricentis"]

STATS = [
    ("48", "Years of enterprise delivery", "Founded in New York, still making complex systems work", "prolifics.ai/about-us", "https://prolifics.ai/about-us"),
    ("2,000+", "Global experts", "Engineers, architects and consultants across the group", "prolifics.ai", "https://prolifics.ai/"),
    ("150+", "Fortune 1000 clients", "Across regulated and asset-intensive industries", "prolifics.ai", "https://prolifics.ai/"),
    ("13", "Offices in 6 countries", "United States, Canada, United Kingdom, Germany, UAE and India", "prolifics.ai/locations", "https://prolifics.ai/locations"),
]

# Published case studies (Prolifics and group companies). logo file names from gtm/assets/clients.
STORIES = [
    ("horizon-bcbs-nj.png", "Horizon Blue Cross Blue Shield of New Jersey", "60M", "claims a year flowing through automated handling",
     "Claims handling automated at payer scale", "Health insurance", "Prolifics",
     "https://www.casestudies.com/company/prolifics/case-study/horizon-improves-the-health-of-claims-processes-with-bpm"),
    ("rac.svg", "RAC", "680+", "point to point interfaces rationalized",
     "An integration layer agents can actually use", "Roadside and insurance", "Prolifics",
     "https://www.casestudies.com/company/prolifics/case-study/rac-customer-case-study"),
    ("broadridge.svg", "Broadridge Financial Solutions", "75%", "less manual transaction matching",
     "Process automation in financial operations", "Financial services", "Prolifics",
     "https://www.casestudies.com/company/prolifics/case-study/process-automation-enhances-broadridge-bpo-business-potentia"),
    ("insolvency-service.svg", "The Insolvency Service", "50%", "annual cost reduction reported",
     "Integration modernized for a UK government agency", "UK government", "Prolifics",
     "https://prolifics.ai/resource-center/case-studies/azure-integration-modernization"),
    ("mckesson.svg", "McKesson", "99%+", "defect removal efficiency on an SAP S/4HANA migration",
     "Test automation that scales with change", "Healthcare distribution", "Prolifics Testing",
     "https://www.prolifics-testing.com/case-studies/test-automation/transforming-business-with-scriptless-test-automation-mckesson"),
    ("teradyne.svg", "Teradyne", "10x", "faster firmware transfer for customers",
     "Customer and partner portals rebuilt", "Semiconductor test", "Prolifics",
     "https://www.casestudies.com/company/prolifics/case-study/teradyne-customer-case-study"),
]

LOGOS = ["mastercard.svg", "mckesson.svg", "gsk.svg", "broadridge.svg", "horizon-bcbs-nj.png", "emblemhealth.png", "teradyne.svg",
         "zions-bancorporation.svg", "rac.svg", "nutrien.svg", "american-bureau-of-shipping.svg", "intuitive-surgical.svg",
         "intealth.svg", "queen-mary-university-of-london.svg", "insolvency-service.svg", "cancer-research-uk.svg",
         "motability-operations.svg", "watts-water-technologies.png", "cmc-energy-services.png"]

GROUP = [
    ("Prolifics", "Integration, data, AI, application and cloud engineering since 1978.", "layers"),
    ("Enable Consulting", "The Salesforce practice: a Salesforce partner since 2002, part of Prolifics since September 2023.", "cloud"),
    ("Castaliaz", "SAP S/4HANA, BTP and SAP Business AI delivery, part of Prolifics since 2025.", "factory"),
    ("Prolifics Testing", "Test automation, performance engineering and testing for AI, with its own published case studies.", "testing"),
    ("Tier 2 Consulting", "Custom software, container platforms and integration in the UK, a Red Hat business partner, part of Prolifics since July 2022.", "code"),
]
# Group company logos (src/brand/group, sources in sources.json there)
GROUP_LOGO = {"Prolifics": "prolifics.png", "Enable Consulting": "enable-consulting.webp", "Castaliaz": "castaliaz.png",
              "Prolifics Testing": "prolifics-testing.png", "Tier 2 Consulting": "tier-2-consulting.png"}

# Client wall by industry (23 Nov 2026, Mac: industry-wise logos, 10 to 12 key ones, then "150+ more").
# "group/..." files are clients published by Prolifics Testing (src/brand/clients/group/sources.json).
WALL = [
    ("featured", "Featured", ["mastercard.svg", "mckesson.svg", "gsk.svg", "group/santander.png", "group/nhs.png", "group/aviva.png",
                              "group/sky.png", "group/fujitsu.png", "broadridge.svg", "horizon-bcbs-nj.png", "group/asos.png"]),
    ("finance", "Banking and insurance", ["mastercard.svg", "broadridge.svg", "zions-bancorporation.svg", "group/santander.png", "group/aviva.png",
                                         "group/close-brothers.png", "group/bank-leumi.png", "group/icbc.png", "rac.svg"]),
    ("health", "Healthcare and life sciences", ["horizon-bcbs-nj.png", "emblemhealth.png", "mckesson.svg", "gsk.svg", "intuitive-surgical.svg", "intealth.svg",
                                                "cancer-research-uk.svg", "group/nhs.png", "group/bmi-healthcare.png", "group/public-health-england.png"]),
    ("public", "Public sector and education", ["insolvency-service.svg", "group/bristol-city-council.png", "queen-mary-university-of-london.svg",
                                              "group/royal-museums-greenwich.png", "motability-operations.svg", "group/public-health-england.png"]),
    ("industry", "Retail, industrial and energy", ["group/asos.png", "nutrien.svg", "american-bureau-of-shipping.svg", "watts-water-technologies.png",
                                                  "cmc-energy-services.png", "teradyne.svg", "group/wates.png"]),
    ("tech", "Technology and services", ["group/sky.png", "group/fujitsu.png", "group/deloitte.png", "teradyne.svg"]),
]
WALL_NOTE = "Clients of Prolifics and its group companies: Enable Consulting, Castaliaz, Prolifics Testing and Tier 2 Consulting."

OFFICES = [
    ("North America", "New York, Westbury, Trevose, Orlando, Toronto"),
    ("United Kingdom & Europe", "London, Borehamwood, Stevenage, Hamburg"),
    ("Middle East", "Dubai"),
    ("India", "Hyderabad, Pune: engineering and delivery centers"),
]

GUIDES = [
    ("Forward deployed AI engineering, consulting or staff augmentation?",
     "Compare delivery models by responsibility, team model, prerequisites and operational ownership.",
     "/resources/forward-deployed-ai-vs-consulting", "g_rowing"),
    ("Is your enterprise data ready for an AI use case?",
     "Assess relevance, quality, access, traceability, freshness and ownership before choosing a platform or model.",
     "/resources/ai-data-readiness", "g_catalog"),
    ("How to evaluate an enterprise AI agent before release",
     "Plan for task success, data permissions, tool actions, human escalation, operating cost and monitoring.",
     "/resources/enterprise-ai-evaluation", "g_knot"),
]

SPRINT = [("Week 0", "Baseline", "Use case, data access and a signed success measure."),
          ("Weeks 1 to 4", "Build", "Weekly demos in your environment, on your platforms."),
          ("Week 5", "Evaluate", "Evaluation sets, red teaming, approvals and guardrails."),
          ("Week 6", "Go live", "In production, measured against the baseline, then handed over or run.")]

ENGAGE = [("Advisory", "Architecture, roadmap and use case selection with the people who will build it.", "compass"),
          ("Co-delivery", "Our pod works beside your engineers, sharing the backlog and the result.", "people"),
          ("Build-operate-transfer", "We build and run the capability, then transfer the team and the know-how.", "handshake"),
          ("Fully managed", "We own operations: monitoring, evaluation, cost and change, on agreed service levels.", "managed")]

FOOTER = [
    ("Services", [(p["name"], p["href"]) for p in PRACTICES] + [("Agentforce Implementation", "/services/agentforce"), ("S/4HANA Migration", "/services/s4hana")]),
    ("Group", [("Group companies", "/group"), ("Enable Consulting", "/group/enable-consulting"), ("Castaliaz", "/group/castaliaz"),
               ("Prolifics Testing", "/group/prolifics-testing"), ("Tier 2 Consulting", "/group/tier-2-consulting"), ("Partnerships", "/partnerships")]),
    ("Industries", [("All industries", "/industries")] + [(i[0], i[2]) for i in INDUSTRIES]),
    ("Company", [("About Us", "/about"), ("Leadership", "/about/leadership"), ("Careers", "/about/careers"), ("Locations", "/about/locations"),
                 ("Resource Center", "/resources"), ("Events", "/events"), ("Contact", "/contact")]),
]
LEGAL = [("Legal Notice", "/legal-notice"), ("Privacy Policy", "/privacy-policy"), ("Cookie Policy", "/cookie-policy")]   # pages on this site

SOL_IMG = {"Agentic Enterprise": "s_agentic", "Customer & Revenue": "s_customer", "Operations & Service": "s_ops",
           "Modernize": "s_modern", "Assure": "s_assure", "Industry Solutions": "s_industry"}

# The 48 year story. Sources: prolifics.ai/about-us (1978, 1985, 2025 award, Castaliaz), research-acquisitions.md
# (Stream Integration Feb 2015, e-testing Nov 2017, Tier 2 Consulting Jul 2022, Enable Consulting Sep 2023, Castaliaz Sep 2025).
ERAS = [
    ("1978", "Founded", "Founded in New York", "JYACC starts building tools for enterprise application developers.", "n1978"),
    ("1985", "Dev tools", "JAM and Panther", "Application development tools that enterprise teams build and modernize with. Still in the Prolifics toolset.", "n1985"),
    ("2000s", "Integration", "Integration at scale", "Integration, process automation and data work for health plans, banks, insurers, states and retailers, as a long standing IBM partner.", "e2000"),
    ("2015", "Data", "Data and analytics", "Stream Integration joins, bringing information management and analytics.", "e2015"),
    ("2017", "Quality", "Quality engineering", "e-testing joins in the UK, followed by Tier 2 Consulting in 2022.", "n2017"),
    ("2023", "Salesforce", "Salesforce practice", "Enable Consulting, a Salesforce partner since 2002, becomes part of Prolifics.", "e2023"),
    ("2025", "SAP", "SAP and Prolifics 2.0", "Castaliaz joins for SAP. Prolifics receives the 2025 IBM North America Sustainability Award.", "e2025"),
    ("Today", "AI", "AI in production", "Forward deployed engineering pods put AI to work inside the platforms clients already run.", "n2026"),
]

# one abstract image per solution card, in SOLUTIONS order
SOL_CARD_IMG = ["r01", "r02", "r03", "r04", "r05", "r06", "r07", "r08", "r09", "r10", "r11", "r12", "r13", "r14", "r15", "r16"]

# Case studies, Sarvam style: three featured, then two rows of three. Figures as published in case studies.
CASES = [
    ("horizon-bcbs-nj.png", "Horizon Blue Cross Blue Shield of New Jersey", "Health insurance", "Prolifics",
     "Claims handling automated at payer scale",
     "Prolifics rebuilt claims handling on business process management, so routine claims move through automated rules and examiners spend their time on the exceptions.",
     "60M", "claims a year through automated handling", "cs_horizon",
     "https://www.casestudies.com/company/prolifics/case-study/horizon-improves-the-health-of-claims-processes-with-bpm"),
    ("rac.svg", "RAC", "Roadside and insurance", "Prolifics",
     "One integration layer instead of hundreds of links",
     "Prolifics replaced a web of point to point connections with a governed integration layer, so new channels and services connect once and run the same way everywhere.",
     "680+", "point to point interfaces rationalized", "cs_rac",
     "https://www.casestudies.com/company/prolifics/case-study/rac-customer-case-study"),
    ("mckesson.svg", "McKesson", "Healthcare distribution", "Prolifics Testing",
     "Test automation for an SAP S/4HANA migration",
     "Prolifics Testing built scriptless test automation for the move to SAP S/4HANA, catching defects before release while the program kept changing.",
     "99%+", "defect removal efficiency", "cs_mckesson",
     "https://www.prolifics-testing.com/case-studies/test-automation/transforming-business-with-scriptless-test-automation-mckesson"),
    ("broadridge.svg", "Broadridge Financial Solutions", "Financial services", "Prolifics",
     "Process automation in financial operations",
     "Automated matching took repetitive manual work out of business process outsourcing operations.",
     "75%", "less manual transaction matching", "cs_broadridge",
     "https://www.casestudies.com/company/prolifics/case-study/process-automation-enhances-broadridge-bpo-business-potentia"),
    ("insolvency-service.svg", "The Insolvency Service", "UK government", "Prolifics",
     "Integration modernized for a UK government agency",
     "Prolifics modernized the agency's integration estate on Azure, cutting annual running costs while keeping public services online.",
     "50%", "annual cost reduction reported", "cs_insolvency",
     "https://prolifics.ai/resource-center/case-studies/azure-integration-modernization"),
    ("teradyne.svg", "Teradyne", "Semiconductor test", "Prolifics",
     "Customer and partner portals rebuilt",
     "Rebuilt portals give customers and partners faster access to firmware and support.",
     "10x", "faster firmware transfer for customers", "cs_teradyne",
     "https://www.casestudies.com/company/prolifics/case-study/teradyne-customer-case-study"),
    ("american-bureau-of-shipping.svg", "American Bureau of Shipping", "Maritime classification", "Prolifics",
     "Data governance for GDPR and CCPA",
     "One privacy and data governance model applied across a global maritime organization.",
     "70", "countries under one governance model", "cs_abs",
     "https://prolifics.ai/resource-center/case-studies/the-american-bureau-of-shipping-navigates-data-privacy"),
    ("intealth.svg", "Intealth", "Healthcare credentialing", "Enable Consulting",
     "A Salesforce platform rescued and delivered",
     "Enable architected and deployed a Salesforce platform with Communities and Lightning Components for physicians, educators and institutions.",
     "2", "previous vendors had failed before Enable took over", "cs_intealth",
     "https://prolifics.ai/resource-center/case-studies/salesforce-implementation-success"),
    ("cmc-energy-services.png", "CMC Energy Services", "Utility energy programs", "Enable Consulting",
     "Utility programs moved onto Salesforce",
     "A Salesforce proof of concept, then the full move from legacy systems, so utility efficiency programs run on one CRM.",
     "1", "CRM for utility efficiency programs", "cs_cmc",
     "https://prolifics.ai/resource-center/case-studies/salesforce-crm-transformation-case-study"),
]

SPRINT_IMG = ["sp_base", "sp_build", "sp_eval", "sp_live"]
