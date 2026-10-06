---
name: research-question-designer
description: Use when turning a broad research idea or candidate gap into precise, falsifiable questions, hypotheses, and evidence requirements.
---

# Research Question Designer

## Purpose

Convert a scoped idea into questions and claims that can be tested or reasoned about. The skill clarifies what evidence would support or falsify each hypothesis; it does not predict results as facts.

## When to Use

- An idea is broad, vague, or framed as “method X is better.”
- A candidate gap needs an operational research question.
- Experiments need explicit claims, comparators, and falsification criteria.

## Inputs

Required: idea, problem context, and intended outcome. Optional: literature matrix, target population/domain, constraints, candidate methods, metrics, and available evidence. Ask for critical missing context or label working assumptions.

## Workflow

1. Restate the problem and scope; distinguish motivation, observed problem, and proposed solution.
2. Draft one or more answerable research questions. Define population/task, conditions, and phenomenon when applicable.
3. For each question, state a testable hypothesis with method/intervention, comparator, conditions, primary metric, and guardrail where appropriate.
4. Define the claim the paper may make if supported and an explicit falsification or weakening condition.
5. Specify required evidence, baselines, measurement protocol, and analysis needed to answer the question.
6. List plausible confounders, assumptions, alternative explanations, and limits on generalization.
7. Check feasibility and alignment with the motivating gap. Narrow or split questions that require incompatible evidence.

## Output

Provide the scoped question; hypotheses; intended claim; conditions, comparator, metric, and guardrail; falsification criteria; evidence and baseline requirements; confounders/assumptions; and scope limits. Mark unresolved design choices rather than silently choosing consequential ones.

## Validation

For each hypothesis ask: could a possible observation contradict it? Is the comparator defined? Does the metric measure the stated outcome? Does the falsification criterion differ from the success criterion? Confirm the experiment can deliver the required evidence.

## Failure Modes

- Vague claims such as “better,” “robust,” or “generalizable” without conditions or measures.
- Hypotheses that restate an expected result and cannot be falsified.
- Confusing a motivation or research gap with a testable question.
- Selecting metrics or baselines after seeing test results.

## Research Integrity Rules

Do not invent expected findings, prior-work gaps, or evidence. Do not imply causality unless the design can support it. Keep hypotheses distinct from observations and conclusions; follow [evidence policy](../../shared/evidence-policy.md).

## Interaction With Other Skills

Upstream: research-gap-finder or a scoped idea. Downstream: experiment-designer turns each claim into a protocol; result-analyzer and claim-evidence-checker later evaluate what the evidence actually supports.
