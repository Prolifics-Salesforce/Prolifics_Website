# -*- coding: utf-8 -*-
"""Copy for the first inner pages (22 Nov 2026), for Mac's approval before the full revamp.
Base copy is the reference site, prolifics-website.vercel.app (pages /services/salesforce, /services/agentforce,
/industries, /industries/healthcare, read 22 Nov 2026). Additions come only from sourced material already in
content.py: company figures (prolifics.ai), group companies, engagement models, the sprint, and published case
studies. House rules: no em or en dashes, no exclamation marks, no pricing, no invented numbers."""

# ---------------------------------------------------------------- Services landing
SVC_CATS = [
    ("ai-engineering", "AI and engineering", "Put AI into production on data you can trust.", ["ai", "fde"]),
    ("platforms", "Enterprise platforms", "Make the platforms you already run ready for agents.", ["sf", "sn", "sap"]),
    ("modernize", "Modernize and assure", "Modern applications, redesigned operations and quality at every release.", ["app", "bt", "qe"]),
]

SVC_HERO = {
    "kick": "Services",
    "h1": "Engineering that takes enterprise AI from pilot to production",
    "lead": ("Eight practices, one delivery standard: a scoped first step, a baseline agreed before we build, and a team that "
             "stays accountable for the result in production. Built on 48 years of enterprise engineering and more than 2,000 experts."),
    "card": ("150+", "Fortune 1000 clients across regulated and asset-intensive industries"),
}

PRINCIPLES = [
    ("Scope first", "Every engagement starts with one defined process, its data, its owners and a measure the business signs off."),
    ("Measure always", "We record a baseline before release and compare like for like afterward, with your process owners."),
    ("Build inside your teams", "Forward deployed pods work in your environment and on your platforms, not in a separate lab."),
    ("Stay for operations", "Ownership of monitoring, evaluation and change is agreed before go live, not after."),
]

# ---------------------------------------------------------------- Salesforce practice
SF = {
    "kick": "Salesforce practice",
    "h1": "Salesforce consulting and Agentforce implementation",
    "lead": ("Prolifics helps enterprises implement, integrate and improve Salesforce across sales, service and customer operations, "
             "combining CRM configuration, data migration, integration and Agentforce engineering."),
    "card": ("2002", "Enable Consulting, our Salesforce practice, has been a Salesforce partner since 2002"),
    "who": ("For Salesforce owners planning a new implementation, replacing a legacy CRM, improving an existing org or introducing "
            "AI agents into a defined sales or service process."),
    "pillars": [
        ("CRM foundations", "Processes, data model, access controls and migration done properly, so automation has something solid to stand on."),
        ("Governed AI", "Agents with bounded tasks, approved data and permitted actions, tested before they reach live users."),
        ("Integration depth", "CRM connected to ERP, service and data platforms, with identity, synchronization and error handling designed in."),
    ],
    "caps": [
        ("Implementation and migration", "Design processes, the data model and access controls. Configure the selected clouds, map and reconcile migrated records, test the user journey and plan cutover and adoption.", "/services/sf-implementation"),
        ("Agentforce design and evaluation", "Select a bounded workflow, define the agent's permitted actions and connect approved information. Test task completion, escalation and data access before introducing the agent to live users.", "/services/agentforce"),
        ("Customer data and integration", "Connect CRM to customer data and enterprise systems. Establish identity, synchronization and error handling rules so automation uses the right context and records remain consistent.", "/services/sf-integration"),
        ("Optimization and managed services", "Review configuration, technical debt, adoption and release impact. Prioritize improvements and maintain regression coverage as processes and platform capabilities change.", "/services/sf-optimisation"),
    ],
    "steps": [
        ("Assess the org and process", "Map the user journey, required records, integrations and reporting needs. Review permission sets, sharing, data quality and technical debt before expanding automation."),
        ("Define a release scope", "Agree the target process, acceptance criteria and dependencies. Confirm product entitlements and identify which decisions require human approval, especially where an agent updates records or invokes external systems."),
        ("Configure, integrate and test", "Implement in an appropriate development environment, validate migrated data and test integrations, including functional regression, permission boundaries, agent evaluation and user acceptance testing."),
        ("Roll out and measure", "Plan deployment, enablement and support. Compare results with a pre-release baseline and prioritize improvements using observed behavior rather than demonstration results."),
    ],
    "readiness": ("Confirm the task, process owner, data sources, users, licenses and action permissions before choosing an agent design. "
                  "A CRM-grounded use case may have different data needs from one spanning multiple systems, and integration access and "
                  "platform entitlements must be checked for your org."),
    "example": ("An illustrative service workflow could retrieve approved knowledge, prepare a response and propose a next action for a case. "
                "The team would decide which steps need approval and how unresolved cases reach a person. Evaluation would cover answer "
                "support, sharing rules and accurate record updates."),
    "measures": [
        ("Service outcomes", "Resolution time and quality, tracked with case mix and reopen rates."),
        ("User adoption", "Use of the intended workflow and feedback from sales or service teams."),
        ("Agent task completion", "Correct completion, escalation and prevention of unauthorized actions."),
        ("Integration reliability", "Record reconciliation, failed transactions and recovery handling."),
    ],
    "faq": [
        ("What does Salesforce implementation include?", "Scope can include process design, configuration, data migration, integrations, testing, deployment and user enablement. A discovery phase determines which clouds, dependencies and delivery responsibilities apply to your organization."),
        ("Do we need a separate customer data platform for Agentforce?", "That depends on the workflow and where its required information resides. Confirm the grounding sources, identity requirements, permissions and entitlements before selecting the data architecture. A separate platform should solve an identified requirement."),
        ("How do you keep an agent inside its permissions?", "Define least-privilege access, approved actions, input checks and escalation rules. Evaluate the agent with representative and adversarial tasks, then monitor its behavior. Permissions and integration controls should be enforced by the underlying systems, not only by prompts."),
        ("Can Salesforce connect to ServiceNow or ERP systems?", "Integration can connect CRM with service and ERP processes where suitable APIs, connectors and entitlements are available. The design needs identity, data mapping, transaction handling and clear ownership of errors and approvals."),
        ("How are scope, timeline and cost agreed?", "They depend on the selected clouds, data quality, migration volume, integrations, customizations and testing needs. We define a scoped engagement after discovery rather than promising the same duration for every org."),
    ],
    "cases": ["intealth.svg", "cmc-energy-services.png", "rac.svg"],
    "related": [
        ("Data 360", "Unified customer data that grounds agents, service and marketing.", "/services/sf-data360"),
        ("Agent Governance and Trust", "Inventory, permissions and evaluation for every agent in the org.", "/services/sf-agent-governance"),
        ("Salesforce and Agentforce Pod", "A forward deployed pod that ships one workflow at a time.", "/services/fde-ai-engineering"),
        ("Is your data ready for an AI use case?", "A planning guide to relevance, quality, access and ownership.", "/resources/ai-data-readiness"),
    ],
}

# ---------------------------------------------------------------- Agentforce service detail
AF = {
    "kick": "Agentforce Implementation",
    "h1": "Agentforce implementation and governed delivery",
    "lead": ("Prolifics helps Salesforce teams implement Agentforce for a defined sales or service workflow, connecting use case selection, "
             "approved CRM data, action design, integrations, evaluation and release controls."),
    "who": ("For Salesforce owners who need hands-on agent delivery and production readiness. Teams looking for role-based learning can use "
            "the separate Agentforce Training and Enablement service."),
    "work": [
        ("Workflow and architecture", "Choose a bounded task and define the information, decisions and actions it needs. Identify data and integration constraints before selecting the implementation scope."),
        ("Grounding and data access", "Map the approved CRM and customer information an agent may use. Review sharing, source freshness and any additional data platform requirements for the workflow."),
        ("Actions and integration", "Connect permitted actions to business systems with explicit inputs, approvals and failure handling. Enforce permissions in the underlying services as well as the agent design."),
        ("Evaluation and release", "Test task completion, answer support, action correctness and escalation. Agree rollout, monitoring, incident handling and ownership of later changes."),
    ],
    "steps": [
        ("Establish the baseline", "Review representative work with sales or service users. Document current effort, quality and exception paths, then agree a useful measure of improvement and a realistic acceptance decision."),
        ("Confirm access and entitlements", "Assess the org, roles, data and interfaces the workflow needs. Check product availability and licensing for your actual environment before promising a capability or date."),
        ("Build and challenge the behavior", "Implement in an appropriate environment and test normal, ambiguous and unauthorized requests. Validate records and external actions, including partial failures and safe handoff to a person."),
        ("Release with operational ownership", "Agree a controlled rollout, user guidance, monitoring and rollback decisions. Define who reviews evaluations and authorizes changes when processes, models or knowledge sources change."),
    ],
    "bring": ["A process owner and a Salesforce technical counterpart", "Example requests from real sales or service work",
              "Your current access model and permission sets", "The systems an agent may read or update",
              "The decisions that must stay with a person"],
    "example": ("An illustrative agent could retrieve approved case context, prepare a response and propose a permitted update. Tests would verify "
                "the evidence behind the response, the user's access and the correctness of the update. Cases outside scope would reach a service agent."),
    "measures": [
        ("Correct task completion", "Accepted outcomes across the agreed task set and representative case types."),
        ("Permission boundaries", "Prevention of restricted data access and unauthorized actions."),
        ("Human handoff", "Appropriate escalation with enough context for a person to continue."),
        ("Operating performance", "Response time, cost and error patterns under the agreed workload."),
    ],
    "faq": [
        ("Is this an implementation service or a training course?", "This page describes hands-on implementation and production delivery. Agentforce Training and Enablement is a separate service for role-based learning, guided practice and team adoption."),
        ("Can we begin without a complete enterprise data program?", "A limited workflow may use approved CRM data, while others need additional data preparation or integration. Assess the selected task and its permissions before deciding which dependencies are necessary."),
        ("How are agent actions governed?", "Define approved actions, least-privilege access, validation, approvals and recovery. Enforce these controls in connected systems and evaluate how the agent handles ambiguous or out-of-scope instructions."),
        ("How long does implementation take?", "Timing depends on scope, data readiness, integrations, entitlements and approvals. Discovery separates feasibility testing, implementation, release evaluation and operational handover into realistic milestones."),
        ("Who maintains the agent after launch?", "Operational ownership is agreed before release. The plan covers incidents, knowledge updates, monitoring, evaluations and approval of model, prompt or tool changes."),
    ],
    "related": [
        ("Agentforce Training", "Role-based learning and guided practice for the teams who will run agents.", "/services/agentforce-training"),
        ("Salesforce and Agentforce Pod", "A forward deployed pod that puts one Agentforce workflow into production at a time.", "/services/fde-ai-engineering"),
        ("How to evaluate an enterprise AI agent before release", "A planning guide to task success, permissions, escalation and cost.", "/resources/enterprise-ai-evaluation"),
    ],
}

# ---------------------------------------------------------------- Industries
IND_HERO = {
    "kick": "Industries",
    "h1": "Industry expertise, connected to enterprise delivery",
    "lead": ("AI, data and enterprise platform engineering applied to the workflows each industry actually runs, with the security, "
             "compliance and integration depth regulated organizations need."),
}

# industry slug -> published case studies (file names from CASES) shown on the industries page
IND_WORK = [
    ("Healthcare & Life Sciences", "/industries/healthcare", ["horizon-bcbs-nj.png", "mckesson.svg", "intealth.svg"]),
    ("Banking & Finance", "/industries/banking", ["broadridge.svg"]),
    ("Government & Public Sector", "/industries/government", ["insolvency-service.svg"]),
    ("Energy & Utilities", "/industries/energy", ["cmc-energy-services.png"]),
    ("Retail, CPG & Logistics", "/industries/retail", ["american-bureau-of-shipping.svg", "teradyne.svg"]),
]

HC = {
    "kick": "Healthcare and life sciences",
    "h1": "Connected data and governed AI for healthcare and life sciences",
    "lead": ("AI solutions for better patient outcomes and operational efficiency, built on secure interoperability frameworks and "
             "compliance-ready architectures, for payers, providers, distributors and life sciences companies."),
    "help": [
        ("Interoperability", "Secure data exchange across clinical, claims and member systems, with governance that keeps every record traceable.", "integration"),
        ("Patient and member centric", "Predictive, personalized engagement on interoperable data, across service, care and outreach.", "people"),
        ("Compliance ready", "HIPAA-aligned governance, privacy controls and continuous monitoring designed in from the start.", "shield"),
        ("Faster research", "AI-enabled research analytics and regulated data platforms for life sciences teams.", "data"),
    ],
    "challenges": [
        ("Fragmented health systems", "Interoperability frameworks and governance models for secure data exchange between payers, providers and partners."),
        ("Life sciences innovation demands", "Regulated data platforms and lifecycle systems that shorten the path from research to market."),
        ("Fragmented data environments", "Governed analytics and AI-powered insight on data that was never designed to work together."),
        ("Security and compliance", "Privacy controls, access governance and continuous monitoring across every system an agent can touch."),
    ],
    "cases": ["horizon-bcbs-nj.png", "mckesson.svg", "intealth.svg"],
    "logos": ["horizon-bcbs-nj.png", "mckesson.svg", "gsk.svg", "group/nhs.png", "emblemhealth.png", "intuitive-surgical.svg", "group/bmi-healthcare.png",
              "cancer-research-uk.svg", "group/public-health-england.png", "intealth.svg"],
    "services": [
        ("Data & AI Governance", "/services/data-governance", "AI & Data"),
        ("Data Engineering", "/services/data-engineering", "AI & Data"),
        ("Industry Clouds", "/services/sf-industries", "Salesforce"),
        ("Agentforce Implementation", "/services/agentforce", "Salesforce"),
        ("Integration Strategy", "/services/integration-strategy", "Application & Cloud"),
        ("Business Process Automation", "/services/bpa", "Application & Cloud"),
        ("Testing for AI", "/services/testing-for-ai", "Quality Engineering"),
        ("Accessibility & Compliance", "/services/accessibility", "Quality Engineering"),
    ],
    "solution": ("Connected Patient & Member Engagement", "Personalized engagement on secure, interoperable data.", "/solutions/patient", "10 to 12 weeks"),
}

# ---------------------------------------------------------------- Salesforce page v2 (22 Nov 2026, after Mac's review:
# more clients, more capability depth, industries served, more impact). Services, industries, stats and "what agents
# change" come from sf_data.json (copied from the Salesforce GTM microsite content). Stories are prolifics.ai case studies.
import json as _json, os as _os
SFD = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "sf_data.json"), encoding="utf-8"))

SF2 = {
    "kick": "Salesforce practice",
    "h1": "Agents only work when they reach the systems they act on",
    "lead": ("Salesforce consulting and Agentforce implementation from Prolifics: certified Salesforce engineers on your team, forward "
             "deployed pods beside your business owners, and the integration depth that moves Agentforce from pilot to production."),
    "cards": [("Since 2002", "Salesforce partner, through Enable Consulting"), ("6 weeks", "from Agentforce pilot to production with a forward deployed pod")],
    "img": "r09",
}

CS = "https://prolifics.ai/resource-center/case-studies/"
# (client, industry, title, brief, metric, metric label, image, logo file or None, delivered by, url)
SF_WORK = [
    ("Intealth", "Healthcare credentialing", "A Salesforce platform rescued and delivered",
     "Enable architected and deployed a Salesforce platform with Communities and Lightning Components for physicians, educators and institutions.",
     "2", "previous vendors had failed before Enable took over", "cs_intealth", "intealth.svg", "Enable Consulting", CS + "salesforce-implementation-success"),
    ("Wealth Hub", "Wealth and trust management", "A Salesforce native trust management platform",
     "Custom objects and workflows for trusts, clients, accounts and legal provisions in one view, with approval workflows and dashboards built for compliance.",
     None, None, "r15", None, "Prolifics", CS + "salesforce-trust-management"),
    ("An energy solutions company", "Energy and manufacturing", "Three Salesforce orgs consolidated into one",
     "Three separate Salesforce CRMs merged into one platform, with sales and marketing workflows standardized across business units.",
     "3 to 1", "Salesforce orgs consolidated", "r10", None, "Prolifics", CS + "salesforce-crm-consolidation"),
    ("CMC Energy Services", "Utility energy programs", "Utility programs moved onto Salesforce",
     "A Salesforce proof of concept, then the full move from legacy systems, so utility efficiency programs run on one CRM.",
     None, None, "cs_cmc", "cmc-energy-services.png", "Enable Consulting", CS + "salesforce-crm-transformation-case-study"),
    ("Exalt", "Nonprofit", "Donor management on Nonprofit Success Pack",
     "A phased Salesforce NPSP implementation that brought donors, funders, volunteers and campaigns into one governed CRM.",
     None, None, "team2", None, "Prolifics", CS + "salesforce-npsp-implementation"),
    ("A global life sciences leader", "Life sciences", "A vendor-neutral CRM decision to replace Siebel",
     "ROI and cost modeling, weighted requirements scoring and scenario demos gave IT and the business one evidence-based choice.",
     None, None, "r01", None, "Prolifics with Enable Consulting", CS + "data-driven-crm-transformation-life-sciences"),
]
# industry slug prefix -> index into SF_WORK used as proof on the industry tile
SF_PROOF = {"banking": 1, "health": 0, "manufacturing": 2, "life": 5, "public": 4}
SF_QUOTE = ("Prolifics turned a complex CRM decision into a confident, strategic choice.",
            "Client, a global life sciences leader", CS + "data-driven-crm-transformation-life-sciences")

# ---------------------------------------------------------------- Group companies (23 Nov 2026, Mac: "start also building the
# group companies offerings"). Read from each company's live site on 23 Nov 2026; every claim carries its source URL.
# Partner tiers and certification counts are left out on purpose (house rule), even where a site states them.
GROUP_PAGES = {
 "enable-consulting": dict(
    name="Enable Consulting", logo="enable-consulting.webp", img="p_sf", practice=("Salesforce", "/services/salesforce"), form="sf",
    kick="Salesforce, a Prolifics group company",
    h1="Salesforce consulting, implementation and long-term support",
    lead="Enable Consulting brings Salesforce strategy, implementation, customization and ongoing support to the Prolifics group, delivered through a hybrid model of US consultants and offshore teams.",
    facts=[("Joined Prolifics", "September 2023", "https://india.entrepreneur.com/news-and-trends/prolifics-acquires-enable-consulting-to-strengthen/459072"),
           ("Today", "Operates as the Prolifics Salesforce practice", "https://www.enableconsulting.com/"),
           ("Listing", "Prolifics + Enable on Salesforce AppExchange", "https://appexchange.salesforce.com/appxConsultingListingDetail?listingId=a0N3000000B53k0EAB")],
    offers=[("Salesforce strategy", "Roadmaps and design for Sales, Service and Marketing Cloud programs."),
            ("Implementation and customization", "Sales Cloud, Service Cloud, CPQ, Field Service, Experience Cloud and Marketing Cloud."),
            ("Data and analytics", "Data Cloud and Tableau, connected to the CRM."),
            ("Integration", "MuleSoft and IoT integration with the systems Salesforce has to work with."),
            ("Agentic AI", "Agentforce use cases built on governed CRM data."),
            ("Long-term support", "Ongoing administration, enhancements and support after go-live.")],
    offers_src="https://appexchange.salesforce.com/appxConsultingListingDetail?listingId=a0N3000000B53k0EAB",
    sectors=["Manufacturing", "Healthcare", "Financial services", "Nonprofit"],
    creds=[], cases=["intealth", "cmc", "wealthhub"], logos=["intealth.svg", "cmc-energy-services.png"], site=None),
 "castaliaz": dict(
    name="Castaliaz", logo="castaliaz.png", img="p_sap", practice=("SAP & ERP", "/services/sap"), form="sap",
    kick="SAP, a Prolifics group company",
    h1="SAP S/4HANA implementation, migration and managed support",
    lead="Castaliaz has implemented and run SAP for Indian enterprises since 2008, with industry solutions for pharma, chemicals, discrete manufacturing and consumer goods. It joined Prolifics in September 2025.",
    facts=[("Founded", "2008, Mumbai, with an office in Bengaluru", "https://www.castaliaz.co.in/idea-behind-castaliaz/"),
           ("Joined Prolifics", "September 2025", "https://www.prnewswire.com/in/news-releases/prolifics-strengthens-global-sap-capabilities-with-castaliaz-acquisition-302564130.html"),
           ("At the time of joining", "More than 140 SAP specialists and over 30 S/4HANA transformations", "https://www.prnewswire.com/in/news-releases/prolifics-strengthens-global-sap-capabilities-with-castaliaz-acquisition-302564130.html")],
    offers=[("Greenfield S/4HANA implementation", "A new S/4HANA system run in six phases: prepare, design, build, test, train and go-live."),
            ("Brownfield conversion, ECC to S/4HANA", "Keeps existing configuration, with pre-checks, readiness checks and the SAP conversion tools."),
            ("Application maintenance and support", "Basic, Business and Enterprise plans; the Enterprise plan adds a 24 hour service window and a dedicated account manager."),
            ("Enhancements", "Continuous improvement projects on a live SAP estate."),
            ("SAP SuccessFactors", "Core HR and payroll, talent management, employee experience and HR analytics."),
            ("Add-on applications", "Fiori, SAP Analytics Cloud, Digital Compliance, Concur, warehouse handheld, labeling and gate entry apps.")],
    offers_src="https://www.castaliaz.co.in/",
    sectors=["Pharma (CastaLife)", "Chemicals (CastaChem)", "Discrete manufacturing (CastaIndus)", "Consumer packaged goods (CastaCPG)", "Automotive components", "Retail"],
    creds=[("SAP Gold Partner", "https://www.castaliaz.co.in/idea-behind-castaliaz/"), ("Authorized SAP license provider", "https://www.castaliaz.co.in/idea-behind-castaliaz/"),
           ("CastaChem and CastaLife, industry solutions certified by SAP SE", "https://www.castaliaz.co.in/sap-chemical-industry-solution-castachem/")],
    cases=["chemicals", "agro", "wine", "pharma-sap"], logos=[], site="https://www.castaliaz.co.in/"),
 "prolifics-testing": dict(
    name="Prolifics Testing", logo="prolifics-testing.png", img="p_qe", practice=("Quality Engineering", "/services/qa"), form="qe",
    kick="Quality engineering, a Prolifics group company",
    h1="AI-led software testing and quality engineering since 1999",
    lead="Prolifics Testing is the UK quality engineering arm of Prolifics. It uses AI agents to test faster, and it tests the AI that clients build or buy.",
    facts=[("Established", "1999", "https://www.prolifics-testing.com/about-us"),
           ("In the group", "The UK quality engineering arm of Prolifics", "https://www.prolifics-testing.com/"),
           ("Quality system", "ISO 9001:2015, accredited since 2003", "https://www.prolifics-testing.com/about-us/accreditations")],
    offers=[("Load and performance testing", "Performance engineering for business-critical platforms."),
            ("Test automation", "Including SAP test automation and accelerators."),
            ("Functional, integration and acceptance testing", "System integration and user acceptance testing."),
            ("Security, penetration and accessibility testing", "Assurance for public-facing and regulated services."),
            ("Platform testing", "Salesforce, Workday, Microsoft 365 and Copilot, Ellucian Banner and Tribal SITS."),
            ("Testing generative AI", "Quality engineering for the AI applications clients build or buy."),
            ("Managed testing", "Managed testing service, team staffing and offshore testing."),
            ("QA consultancy and training", "Testing health checks and ISTQB training.")],
    offers_src="https://www.prolifics-testing.com/",
    sectors=["Legal and professional services", "Higher education", "Public sector", "Banking and finance", "Healthcare", "Logistics", "Utilities", "Retail", "Telecoms"],
    creds=[("ISO 9001:2015 and ISO 27001", "https://www.prolifics-testing.com/about-us/accreditations"), ("G-Cloud 13 framework supplier, since 2014", "https://www.prolifics-testing.com/about-us/accreditations"),
           ("Digital Outcomes and Specialists framework", "https://www.prolifics-testing.com/about-us/accreditations"), ("FSQS approved supplier", "https://www.prolifics-testing.com/about-us/accreditations"),
           ("BS7858:2012 security screening, clearance up to SC", "https://www.prolifics-testing.com/about-us/accreditations"),
           ("Technology partners: Tricentis, OpenText, RadView, Ellucian, Tribal, Aderant", "https://www.prolifics-testing.com/about-us/partners")],
    work=[("McKesson", "Scriptless test automation", "over £1.7 million in cost savings"), ("McKesson", "SAP S/4HANA migration testing", "over 99% defect removal efficiency"),
          ("NHS", "COVID-19 vaccine booking portal", "stress testing before launch"), ("University of Bristol", "Application migration", "800 applications migrated"),
          ("Cancer Research UK", "Testing", "a managed testing service"), ("Bank Leumi", "Testing", "testing as a service")],
    work_src="https://www.prolifics-testing.com/about-us/case-studies",
    cases=["mckesson", "aderant", "perf-legal"], logos=["group/nhs.png", "group/santander.png", "group/aviva.png", "group/sky.png", "group/fujitsu.png", "group/asos.png",
                                                    "mckesson.svg", "gsk.svg", "group/deloitte.png", "cancer-research-uk.svg", "group/bank-leumi.png", "group/bristol-city-council.png"],
    site="https://www.prolifics-testing.com/"),
 "tier-2-consulting": dict(
    name="Tier 2 Consulting", logo="tier-2-consulting.png", img="p_app", practice=("Application & Cloud", "/services/app-services"), form="app",
    kick="Custom software, a Prolifics group company",
    h1="Custom software on open source and cloud native technology",
    lead="Tier 2 Consulting designs, builds and supports custom software for UK organizations, delivered in an agile way on open source and cloud native platforms, with deep Red Hat expertise.",
    facts=[("Founded", "2002, Stevenage, Hertfordshire", "https://tier2consulting.com/software-development-company/"),
           ("Joined Prolifics", "July 2022", "https://benzinga.com/z/27944107"),
           ("Today", "A wholly owned subsidiary of Prolifics Application Services Inc.", "https://tier2consulting.com/software-development-company/")],
    offers=[("Application modernisation", "Move legacy applications onto modern, supportable platforms."),
            ("Custom application development", "Bespoke software built with the client, from discovery to delivery."),
            ("Integration", "Connect applications and data across the estate."),
            ("Cloud migration", "Replatform from data centres to cloud, including OpenShift."),
            ("Support and maintenance", "Ongoing support for the applications Tier 2 builds and inherits."),
            ("Red Hat technology", "OpenShift, Ansible, RHEL, Application Foundations, subscriptions and licensing.")],
    offers_src="https://www.tier2consulting.com/",
    sectors=["Insurance broking", "Life sciences", "UK public services"],
    creds=[("Red Hat partner", "https://tier2consulting.com/software-development-company/"), ("Crown Commercial Service Digital Outcomes and Specialisms supplier", "https://tier2consulting.com/software-development-company/"),
           ("Scrum Alliance certified", "https://tier2consulting.com/software-development-company/")],
    work=[("GSK", "Compound data repository", "a searchable repository of studies, genotoxic hazards and structures, delivered in phases"),
          ("Motability Operations", "Cloud replatforming", "a year-long move from on-premise data centres to AWS on OpenShift and Red Hat Fuse, on time and within budget")],
    work_src="https://tier2consulting.com/our-resources/case-study/",
    cases=[], logos=["gsk.svg", "motability-operations.svg"], site="https://www.tier2consulting.com/"),
}
