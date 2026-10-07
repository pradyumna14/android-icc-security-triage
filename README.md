# Android ICC Security Triage

### LLM-Assisted Multi-Agent Framework for Context-Aware Android Inter-Component Communication Security Analysis

> **Research Paper:** [An LLM-Assisted Multi-Agent Framework for Context-Aware Triage of Android Inter-Component Communication Security Findings](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7233718)
>
> The research paper describing this framework is publicly available online. This repository contains the implementation and supporting code for the research prototype.

---

## Overview

Android applications rely heavily on **Inter-Component Communication (ICC)** to allow Activities, Services, Broadcast Receivers, and Content Providers to communicate with each other and with external applications.

Static Android security analysis tools can identify potentially risky ICC configurations, but rule-based analysis can produce a large number of findings that require manual verification. For security analysts, this creates a significant triage problem: not every flagged component represents an exploitable vulnerability.

This project explores an **LLM-assisted multi-agent approach to Android ICC security triage**.

The framework takes potentially suspicious Android component metadata, reasons about its security context using multiple specialized agents, and produces a structured assessment indicating whether a finding is:

* **Real Vulnerability**
* **False Positive**
* **Needs Manual Review**

The objective is not to replace security analysts, but to provide an intermediate reasoning layer that can reduce unnecessary manual investigation and prioritize findings that deserve deeper analysis.

---

## Research Contribution

The research investigates a collaborative multi-agent reasoning pipeline in which different agents approach the same security finding from different perspectives.

The overall research framework consists of three reasoning stages:

### 1. Risk Analysis

The first agent examines the Android component and identifies:

* Potential security risks
* Possible attack paths
* Attacker prerequisites
* Potential impact
* Severity

### 2. Verification

The second agent challenges the initial security assessment.

It considers:

* Android platform protections
* Intended component functionality
* Reasons exploitation may not work
* Potential false positives
* Evidence supporting or contradicting the initial assessment

### 3. Final Decision

The final agent acts as a skeptical security reviewer rather than simply accepting the previous analysis.

It:

* Reviews the component metadata
* Compares the risk and verification analyses
* Separates observed facts from assumptions
* Assigns an evidence level
* Determines what can and cannot be established from the available information
* Produces the final classification

This separation is important because an LLM should not automatically treat a potentially dangerous configuration as a confirmed vulnerability without sufficient evidence.

---

## High-Level Pipeline

```text
                    Android APK
                        │
                        ▼
               APK / Manifest Analysis
                        │
                        ▼
             ICC Component Extraction
                        │
                        ▼
              Potential ICC Findings
                        │
                        ▼
              ┌─────────────────────┐
              │   Risk Agent        │
              │                     │
              │ Attack paths        │
              │ Impact              │
              │ Severity            │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Verification Agent  │
              │                     │
              │ Android protections │
              │ Intended behavior   │
              │ False positives     │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Final Judge       │
              │                     │
              │ Evidence-based      │
              │ classification      │
              └──────────┬──────────┘
                         │
                         ▼
          ┌─────────────────────────────┐
          │ Real Vulnerability          │
          │ False Positive              │
          │ Needs Manual Review         │
          └─────────────────────────────┘
```

---

## Repository Structure

```text
android-icc-security-triage/
│
├── README.md
│
├── apk_analyzer.py
│   └── Extracts Android application/component information
│       from an APK using Androguard.
│
├── icc_detector.py
│   └── Performs rule-based identification of potentially
│       risky exported Android components.
│
├── security_report.py
│   └── Converts exported Activity metadata and intent
│       information into a structured ICC security report.
│
├── llm_analyzer.py
│   └── Sends ICC findings to an LLM for context-aware
│       security classification.
│
├── multi_agent_analyzer.py
│   └── Implements the multi-agent reasoning pipeline:
│       Risk → Verification → Final Judge.
│
└── manifest_debug.py
    └── Utility for inspecting/debugging Android manifest
        information during analysis.
```

---

## How the Components Connect

The individual scripts are designed as stages of the broader analysis workflow rather than unrelated standalone programs.

### APK Analysis

`apk_analyzer.py` uses **Androguard** to inspect an Android APK and extract component metadata such as:

* Activities
* Services
* Broadcast Receivers
* Content Providers
* Exported status
* Permissions

This provides the initial Android-specific context.

### ICC Detection

`icc_detector.py` performs a lightweight rule-based security check.

One important example is an Android component that is:

```text
exported = true
permission = none
```

Such configurations may warrant further investigation because an externally accessible component without an associated permission can potentially increase the attack surface.

Importantly, the detector treats these as **potential risks**, not automatically confirmed vulnerabilities.

### Security Report Generation

`security_report.py` converts relevant manifest information into structured JSON.

The report captures information such as:

```text
Component
Exported status
Permissions
Intent actions
Intent categories
Component type
```

This structured representation becomes the input to the LLM-based reasoning stages.

### LLM-Based Analysis

`llm_analyzer.py` provides a single-agent analysis baseline.

The model is instructed to reason using Android-specific context and classify findings as:

```text
Real Vulnerability
False Positive
Needs Manual Review
```

The prompt explicitly considers factors such as exported status, permissions, intent actions, intent categories, and intended Android component behavior.

### Multi-Agent Analysis

`multi_agent_analyzer.py` extends this concept into a multi-agent workflow.

For each finding:

```text
Finding
   │
   ▼
Risk Agent
   │
   ▼
Verification Agent
   │
   ▼
Final Judge
   │
   ▼
Final Security Assessment
```

The final judge is explicitly instructed to be skeptical of both previous analyses and to distinguish evidence from assumptions.

---

## Evidence-Aware Security Reasoning

A central design principle of the framework is that **a suspicious configuration is not automatically a vulnerability**.

For example, an exported component may be intentionally exposed because of legitimate Android functionality.

The final reasoning stage therefore distinguishes between:

### High Evidence

Directly observable from the supplied data.

Example:

```text
The component is exported.
```

### Medium Evidence

A reasonable inference based on Android behavior.

Example:

```text
The component may be reachable by another application.
```

### Low Evidence

A claim that requires additional source-code or runtime analysis.

Example:

```text
The component is definitely exploitable.
```

This approach is intended to reduce overconfident vulnerability claims and make the output more useful to a human security analyst.

---

## Research Evaluation

The accompanying research evaluated the framework using ICC findings extracted from **21 mature open-source Android applications**, resulting in **75 findings** for evaluation.

The reported evaluation found that the multi-agent framework identified **33.3% of findings as benign false positives**, while the remaining **66.7% were prioritized for further manual review**.

The research also investigates the cost and practicality of using LLM-based multi-agent reasoning as an intermediate security-triage layer.

For the complete methodology, experimental setup, results, and discussion, please refer to the research paper linked at the top of this README.

---

## Why the Full Dataset Is Not Included

The original research involved a substantially larger experimental dataset and generated analysis artifacts.

The full dataset is **intentionally not included in this GitHub repository**.

There are several practical reasons for this:

* The complete dataset is several gigabytes in size.
* Large experimental datasets are unnecessary for understanding the implementation.
* Including generated APKs and analysis artifacts would make the repository unnecessarily large.
* A recruiter or researcher evaluating the implementation primarily needs the source code and documentation.
* Keeping generated outputs outside the source repository keeps the project lightweight and easier to clone.
* The research paper provides the appropriate context for the experimental dataset and evaluation.

Therefore, this repository is intended primarily as a **code and research-prototype repository**, rather than a complete archive of every experimental artifact used during the study.

The omission of the dataset does **not** mean the experiments were performed without data; the experimental dataset and evaluation are described in the accompanying research paper.

---

## Why APKs and Generated Outputs Are Not Included

The repository also intentionally excludes large or generated artifacts such as:

```text
*.apk
large datasets
virtual environments
generated JSON reports
temporary manifest files
Python cache files
```

These files are either:

1. Large binary inputs,
2. Generated during execution,
3. Environment-specific, or
4. Reproducible from the analysis pipeline.

Keeping them out of version control makes the repository substantially smaller while preserving the important implementation logic.

---

## Reproducibility

The repository contains the core Python implementation used for the analysis workflow.

The general workflow is:

```text
APK
 ↓
Manifest / Component Extraction
 ↓
ICC Detection
 ↓
Structured Security Report
 ↓
LLM Analysis
 ↓
Multi-Agent Reasoning
 ↓
Security Classification
```

A local APK can be supplied to the analysis scripts, and the resulting component metadata can be passed through the subsequent analysis stages.

The repository intentionally does not include API credentials, large APK collections, or the full research dataset.

---

## Technologies

* **Python**
* **Androguard**
* **Google Gemini API**
* **Large Language Models (LLMs)**
* **Android Manifest Analysis**
* **Inter-Component Communication (ICC) Security**
* **Static Security Analysis**
* **Multi-Agent Reasoning**
* **Security Triage**

---

## Security and Responsible Use

This project is intended for:

* Security research
* Android application analysis
* Academic research
* Security triage
* False-positive reduction
* Defensive analysis of Android applications

Only analyze applications and APKs that you are authorized to inspect.

The framework is a **triage and reasoning system**, not a complete vulnerability verification system. A finding classified as a potential vulnerability should be independently validated through appropriate source-code, dynamic, or manual security analysis before being treated as a confirmed vulnerability.

---

## Research Paper

**An LLM-Assisted Multi-Agent Framework for Context-Aware Triage of Android Inter-Component Communication Security Findings**

Research paper:

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7233718

The paper contains the detailed research methodology, evaluation, experimental results, and discussion underlying this repository.

---

## Author

**Pradyumna Sharma Kattel**

B.Tech. Computer Science & Engineering
National Institute of Technology Hamirpur

Research interests include:

* Android Security
* Software Security
* AI/ML for Security
* LLM-Assisted Security Analysis
* Secure Software Engineering

---

## Disclaimer

This repository represents a research prototype and supporting implementation for the accompanying academic work. It should not be interpreted as a replacement for professional security auditing or comprehensive Android vulnerability analysis.

Security conclusions should be independently validated using appropriate evidence and testing.
