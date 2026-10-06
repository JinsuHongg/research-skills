---
name: method-diagram
description: Use when explaining a research method with a model architecture, conceptual figure, comparison diagram, or data/training/inference pipeline.
---

# Method Diagram

## Purpose

Plan or create a diagram that makes the supplied research method easier to understand. Scientific fidelity and clear relationships take precedence over decoration.

## When to Use

- A paper needs a model or system architecture figure.
- Training, calibration, inference, or data-processing stages need explanation.
- Methods, uncertainty workflows, or alternatives need a visual comparison.

## Inputs

Required: method description or source section and intended reader. Optional: equations, pseudocode, components, data flow, dimensions, target venue template, and existing figures. Ask about missing components that affect the diagram's meaning.

## Workflow

1. Extract named components, inputs/outputs, stages, dependencies, and training/inference distinctions from the provided method.
2. Decide the diagram's single main explanatory question and scope. Choose pipeline, architecture, conceptual, or comparison form.
3. Draft a node/edge inventory with labels and direction. Preserve conditional paths, repeated operations, and data boundaries.
4. Verify every component and relationship against the method source. Mark ambiguous or missing information for clarification; never infer an unreported mechanism.
5. Lay out the diagram with consistent grouping, arrows, symbols, and restrained emphasis. Define abbreviations and avoid ornamental elements that obscure flow.
6. Check readability in the intended paper column and consistency with method terminology, equations, and captions.

## Output

Provide the diagram or a renderable specification, its intended message, component/edge mapping to the source method, unresolved details, and caption suggestion. Include editable/vector output where the chosen tool permits.

## Validation

Walk each path from input to output and compare it with the method text; verify training, calibration, and inference stages are not conflated; check labels, arrows, abbreviations, and caption agree with manuscript terminology.

## Failure Modes

- Adding an intuitive but unreported module or data flow.
- Conflating training and inference, or calibration and evaluation.
- Using decorative detail that changes apparent emphasis or hides dependencies.
- Presenting a conceptual sketch as an implementation-faithful architecture.

## Research Integrity Rules

Do not create components, equations, results, or causal relationships absent from supplied evidence. Label abstraction and uncertainty. If method details conflict across sources, report the conflict and request resolution instead of silently choosing one.

## Interaction With Other Skills

Upstream: latex-paper-writer or experiment-designer provides the method/protocol; literature-review may supply sourced comparisons. Downstream: publication-figure and paper-consistency-checker check clarity and naming; submission-readiness reviews sizing and current venue requirements.
