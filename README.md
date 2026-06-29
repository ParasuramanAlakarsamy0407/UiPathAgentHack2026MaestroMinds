# OmniQuote AI

### Powered by the A.U.R.A Framework — *Automated Underwriting \& Risk Architecture*

**UiPath Agentic AI Hackathon 2026 — Team MaestroMinds**

\---

## 1\. Repository \& Team

|||
|-|-|
|**Repository**|[https://github.com/ParasuramanAlakarsamy0407/UiPathAgentHack2026MaestroMinds](https://github.com/ParasuramanAlakarsamy0407/UiPathAgentHack2026MaestroMinds)|
|**Team Name**|MaestroMinds|
|**Team Members**|Guhan Eshwar, Parasuraman, Praison Thomas, Ainul Inayas|

\---

## 2\. Business Problem



Group employee-benefits underwriting (life, health, and stop-loss insurance) is one of the most manually intensive processes in commercial insurance. When a broker submits a Request for Proposal (RFP), an underwriting team must:



* Manually read and reconcile **census files, large claimant reports, and claims experience files** that arrive in inconsistent formats.
* Manually contact **multiple carriers** — some through modern APIs, many still through legacy web portals — to collect competing quotes.
* Manually cross-reference every carrier's pricing against the case's clinical and demographic risk profile.
* Manually apply underwriting guardrails (premium thresholds, prohibited industries, risk thresholds) before any quote can move forward.
* Manually assemble the final comparison and proposal document to send back to the broker.



This process is slow (often days), error-prone, inconsistent across underwriters, and offers no structured audit trail for compliance review. Brokers lose deals to carriers who can quote faster, and underwriters spend most of their time on data assembly rather than on judgment calls that actually require human expertise.



## 3\. Our Solution



**OmniQuote AI** automates the entire RFP-to-Proposal lifecycle end-to-end using a combination of **UiPath RPA, UiPath Maestro orchestration, and purpose-built AI Agents**, while keeping a licensed underwriter firmly in control of every risk decision through a structured **Human-in-the-Loop (HITL)** checkpoint in Action Center.

In short, OmniQuote AI turns a multi-day, multi-person manual workflow into a **3–4 minute automated pipeline** that ends with the underwriter reviewing AI-generated risk reasoning instead of raw spreadsheets — and a broker receiving a polished, carrier-compared proposal PDF directly in their inbox.



### What makes it "agentic" rather than just "RPA"



The solution does not simply automate clicks. Three distinct AI Agents perform genuine reasoning at different stages of the pipeline:



|Agent|Role|
|-|-|
|**Intake Agent (LLM)**|Reads census, large claimant, and claims experience files; extracts broker/client metadata and demographic composition; produces one standardized "golden record" JSON payload.|
|**Risk Agent (Multimodal LLM)**|Ingests every carrier's quote PDF directly (no manual data entry); evaluates each carrier's pricing against clinical and demographic risk signals; produces a risk score, confidence level, and a clinical reasoning narrative per carrier.|
|**Proposal Agent (LLM)**|Synthesizes every underwriter-approved quote into an executive-ready broker proposal — summary narrative, market comparison table, and pros/cons — exported as a final PDF.|



These agents work alongside a **deterministic Business Rules Engine** (hard guardrails that are never left to AI judgment — premium ceilings, NAICS industry blacklist, risk thresholds) and a **mandatory human underwriter checkpoint**, so AI accelerates the process without ever bypassing governance.

\---

## 4\. End-to-End Architecture (10 Stages)



> A full animated walkthrough of this architecture is included in the repo: 

(https://github.com/ParasuramanAlakarsamy0407/UiPathAgentHack2026MaestroMinds/blob/main/OmniQuoteAI\_\_Animated\_ArchitectureFlow.html) — open it in any browser and use the arrow keys / nav buttons to step through.



|#|Stage|What Happens|
|-|-|-|
|1|**Trigger \& Inbound Ingestion**|Unattended UiPath bot monitors the mailbox 24/7, matches RFP emails by subject keyword, downloads attachments into a secure runtime directory.|
|2|**Structured Extraction — Intake Agent**|LLM agent extracts metadata and builds the standardized JSON "golden record" from the census/claims files.|
|3|**Parallel Carrier Orchestration**|UiPath Orchestrator fans out simultaneously to (3a) modern API-based carriers via FastAPI endpoints and (3b) legacy carrier portals via RPA browser automation. A `JOIN` node waits for both branches to complete.|
|4|**Raw Batch Assembly**|Verifies all carrier quote PDFs arrived and assembles them into a single batch with a file pointer array.|
|5|**Risk Agent Analysis**|Multimodal LLM reads every quote PDF directly and scores carrier pricing against clinical/demographic risk, with reasoning.|
|6|**Deterministic Guardrails \& Auto-Tagging**|A rules engine applies non-negotiable business rules and tags every quote with a review status.|
|7|**Supervisory Suspension**|The Maestro process suspends; a structured task is created in Action Center and routed to the underwriting queue with SLA timers.|
|8|**Underwriter HITL Validation**|The underwriter self-assigns the task, reviews AI reasoning, **bulk-accepts** low-risk auto-recommended items, and individually **accepts/overrides/rejects** flagged high-risk items. All items must be dispositioned before the process can continue.|
|9|**Consolidation — Proposal Agent**|LLM synthesizes all approved quotes into an executive narrative, comparison table, and pros/cons, rendered as the final Proposal PDF.|
|10|**Delivery \& Compliance Logging**|UiPath robot emails the final proposal back to the broker and writes a full immutable audit trail (approvals, overrides, AI reasoning) to the audit log store.|



**Persistent platform layers (active throughout):**



* **Data \& Storage:** Storage Bucket, Data Fabric, Audit \& Log Store (immutable)
* **Controls \& Governance:** Business Rules \& Guardrails, Policy \& Risk Libraries, Access Control (RBAC), Audit/Logging/Traceability, Compliance alignment (HIPAA, SOC2)

\---



## 5\. UiPath Components in This Repo

As published in Orchestrator:

|Name|Type|Entry Point|Description|
|-|-|-|-|
|`GetEmail`|RPA|`Main.xaml`|Monitors inbox, matches RFP emails, downloads attachments|
|`ReadStorageDocument`|RPA|`Main.xaml`|Reads the census / claimant / claims experience documents from storage|
|`ReadStoragePDF`|RPA|`Main.xaml`|Reads carrier quote PDFs from storage|
|`DownloadStorageFiles`|RPA|`Main.xaml`|Retrieves files from the Storage Bucket for downstream steps|
|`QuotationBOT'|RPA|`Main.xaml`|Legacy carrier portal automation — logs in, submits census, downloads quote PDF|
|`Batch.Assembely`|RPA|`Main.xaml`|Assembles carrier quote PDFs into a single batch for the Risk Agent|
|`Business.Rule.Engine`|RPA|`Main.xaml`|Applies deterministic underwriting guardrails and tags review status|
|`RespondEmail`|RPA|`Main.xaml`|Sends the final proposal PDF back to the broker; writes audit log|
|`Intake Agent`|Agent|`content/agent.json`|Extracts metadata and builds the standardized golden-record JSON|
|`RiskAgent`|Agent|`content/agent.json`|Multimodal risk scoring across all carrier quote PDFs|
|`Consolidation Agent`|Agent|`content/agent.json`|Synthesizes approved quotes into the final broker proposal PDF|
|`OmniquoteAI`|Maestro (BPMN)|—|Single Maestro process orchestrating the full 10-stage pipeline end-to-end (no split sub-processes)|



**Workflow count note:** 8 RPA processes are published in Orchestrator above; `QuotationBOT` itself contains the legacy-portal logic across multiple internal `.xaml` files, which together with the other 6 single-file RPA processes make up the **7 `.xaml` workflows** referenced in the submission.



**LLM connections used:** Mixed model providers across agents (Anthropic Claude and OpenAI), configured at the Agent Builder connection level — no LLM-specific configuration is required from the runner.



**External dependencies:**

* No NuGet packages beyond standard UiPath activity packages.
* Python is used **only inside the external carrier-quoting API** (not inside any UiPath workflow).
* External REST API endpoints simulate modern carrier quoting (rating engine + PDF generation) — fully hosted, no local setup required.

\---

## 6\. Setup Instructions



This solution is designed to be judged with **zero local configuration**. Everything (the carrier APIs, mock carrier portals, and the agents) is already hosted and reachable from any machine that can run the UiPath workflows.



### Step 1 — Get Access



1. Clone or download this repository:

```bash
   git clone https://github.com/ParasuramanAlakarsamy0407/UiPathAgentHack2026MaestroMinds.git
   ```

2. Open the project in **UiPath Studio**, connected to the same Orchestrator tenant used for this submission (UiPath Automation Cloud — Staging):

```
   https://staging.uipath.com/hackathon26\\\_695/DefaultTenant
   ```

*(If judging from a different tenant, simply publish the included Maestro process to your own tenant — no Orchestrator Assets or Queues need to be pre-created, and no `project.json`/config values need to be edited, since all endpoints are fully hosted and self-contained , Recheck on the Shared files updated as expected)*



*3. Retrieve the Microsoft Edge download directory. Then extract and return only the parent directory by removing the Downloads folder from the path.*



*Examples:*

*If the download path is C:\\Users\\jhsjm\\Downloads\\, return C:\\Users\\jhsjm\\*

*If the download path is D:\\Downloads\\, return D:\\*

*If the download path is E:\\MyFiles\\Downloads\\, return E:\\MyFiles\\*



*Return only the path as plain text, without any additional text or formatting. Then pass the returned value into the Maestro BPMN flow argument named MachineDownloadPath.*



### Step 2 — Confirm the Maestro Process is Running

1. In Orchestrator, navigate to **Maestro → Processes**.
2. Confirm the **`OmniquoteAI`** BPMN process is active and the `GetEmail` trigger listener (mail monitoring) is running as an **unattended** job.



   ### Step 3 — Prepare the Sample RFP Email

   Sample input files are already included in this repository under the **`/Sample`** folder, ready to attach as-is:

* A **Census file** (filename/content must contain the keyword `Census`)
* A **Large Claimant file**
* A **Claims Experience file**



  ### Step 4 — Trigger the Demo

  Send an email (using the sample files from `/Sample`, unmodified) to:

  ```
To:      Parasuraman.a@firstsource.com

  To:      Parasuraman.a@firstsource.com
Subject: RFP Submission
Attach:  Census file, Large Claimant file, Claims Experience file

  ```

  The unattended bot polls the mailbox, detects the subject keyword `RFP Submission`, validates the three attachments, and kicks off the Maestro process automatically. \*\*No manual file drop, SFTP path, or folder placement is required\*\* — this is a pure email trigger.

 **Step 5 — Watch the Pipeline Run**

  End-to-end, fully automated stages (1–6 and 9–10) complete in roughly \*\*4 to 5 minutes\*\* for the sample census file, covering: ingestion → intake extraction → parallel carrier quoting (API + RPA portals) → batch assembly → AI risk analysis → guardrail tagging.

  ### Step 6 — Human-in-the-Loop Review (Action Center)

1. Log in to \*\*Action Center\*\* under the \*\*Underwriting Assistant\*\* app.
2. Locate the task in the \*\*Unassigned\*\* queue and \*\*self-assign\*\* it to yourself (no special role/permission beyond standard Action Center access is required).
3. Review the AI Risk Agent's reasoning for each carrier quote:

   \* \*\*Auto-Recommended (Low Risk):\*\* verify reasoning, then \*\*Bulk Accept\*\* in one click.
   \* \*\*Flagged (High Risk / Exceptions):\*\* review reasoning individually, then click \*\*Accept (override) only\*\*.
4. All items must be dispositioned before the process can resume — this is enforced by design.

   ### Step 7 — Receive the Output

   Once every item is dispositioned, the Consolidation/Proposal Agent generates the final comparison proposal, and the UiPath robot automatically \*\*emails the Proposal PDF back to the address that originally sent the RFP\*\* (no SharePoint or shared drive step — the response goes straight to the requester's inbox). A full audit trail (every approval, override, and the underlying AI reasoning) is written to the immutable audit log store for compliance review.

   > \\\*\\\*Demo mode:\\\*\\\* Not required. All carrier APIs and the mock legacy carrier portals are publicly hosted, so the entire pipeline runs identically on any machine without local mocks or live carrier credentials.

   \\---

   ## 7\\. Repository Structure

   ```

  UiPathAgentHack2026MaestroMinds/
├── OmniQuoteAI\_\_Animated\_ArchitectureFlow/                      #  Interactive architecture walkthrough
├── SampleInputs/                         			    # Sample RFP email + 3 input files for the demo
│   ├── File 01
│   ├── File 02
│   └── File 03 \& Email Template
├── UiPathMaestro/                        # 1 published BPMN process
└── README.md```   
   \\---

   ## 8\\. Key Outcomes

\* \*\*Faster Turnaround\*\* — multi-day manual underwriting reduced to a \\\~ 8 to 10 minutes automated pipeline
\* \*\*AI-Powered Risk Insights\*\* — multimodal risk scoring directly from carrier PDFs, with full reasoning
\* \&#x20;\*\*Human Governance Preserved\*\* — every quote is dispositioned by a licensed underwriter before delivery
\* \&#x20;\*\*Compliance by Design\*\* — immutable audit trail of every AI decision and human override
\* \&#x20;\*\*Zero Manual File Parsing\*\* — census, claimant, and claims data extracted automatically
\* \&#x20;\*\*100% Data Integrity\*\* — deterministic guardrails enforce non-negotiable underwriting rules regardless of AI output

  \\---

  ## 9\\. Tech Stack

\* \*\*UiPath Orchestrator + Maestro\*\* — process orchestration, parallel carrier outreach, supervisory suspension/resume
\* \*\*UiPath Studio\*\* — 7 RPA workflows (mail automation, legacy carrier portal automation, file assembly, delivery, audit logging)
\* \*\*UiPath Agent Builder\*\* — 3 LLM-powered agents (Intake, Risk, Proposal), using a mix of Anthropic Claude and OpenAI models
\* \*\*UiPath Action Center\*\* — Underwriting Assistant app for human-in-the-loop review
\* \*\*Python + REST APIs\*\* — externally hosted carrier rating/quoting service (outside the UiPath workflows)
\* \*\*HTML + JS\*\* - Create Mock up Carrier Applications
\* \*\*UiPath Data Fabric\*\* - to store Real time data's
\* \*\*UiPath Storage Bucket\*\* - Stores all the input and output files

\* \*\*UiPath Integration Services\*\* - Email integrations

&#x20;\*\*UiPath Apps\*\* - Create Human In the Loop

  \\---


  \## 10\\. Coding Agent Acceleration 



  To maximize our time spent inside UiPath Studio and Maestro, we utilized Codex as our primary developer coding agent to rapidly generate the external testing ecosystem. Specific Codex contributions include:



  Mock Application Generation: Completely generated the HTML/JS frontend for the legacy carrier portal that our RPA bot scrapes.



  API Backend: Architected the Python/FastAPI routing structure to simulate the modern carrier rating engine.



  Data Schemas: Iterated and formatted the strict JSON payloads required for UiPath deserialization.



  By using Codex to build the surrounding environment, we were able to dedicate 100% of our engineering focus to perfecting the Maestro BPMN orchestration and UiPath Agent Builder logic.

  
  ## 11\\. Contact

  For questions about this submission, please reach out to any team member listed above or open an issue on the (https://github.com/ParasuramanAlakarsamy0407/UiPathAgentHack2026MaestroMinds).


