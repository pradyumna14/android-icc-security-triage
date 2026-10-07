# android-icc-security-triage

Research Paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7233718

Android security analysis tools are highly effective
at identifying potentially dangerous behaviors, particularly those
related to Inter-Component Communication (ICC). However,
traditional static analysis approaches generate a massive volume
of false positives by indiscriminately flagging legitimate Android
components. This excessive noise creates a severe manual verifi-
cation burden for security analysts.
This paper presents a novel LLM-assisted multi-agent frame-
work designed for the context-aware triage of Android ICC
security findings. We introduce a collaborative three-agent rea-
soning pipeline (Context, Security, and Decision agents) that
debates component purpose, exposure characteristics, and threat
models before finalizing classifications. We evaluate the frame-
work against traditional rule-based scanners and single-agent
LLM baselines using 75 ICC findings extracted from 21 mature
open-source applications. The multi-agent system successfully
identified 33.3% of findings as benign false positives and priori-
tized the remaining 66.7% with structured contexts for manual
review, all while avoiding the hallucinated vulnerability claims
common in single-agent setups. Our empirical evaluation and cost
analysis demonstrate that multi-agent LLM systems are a viable,
cost-effective intermediate triage layer, dramatically improving
precision over single-agent baselines while radically enhancing
the efficiency of security analysts and modern Android security
workflows.

