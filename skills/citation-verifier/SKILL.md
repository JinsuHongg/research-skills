---
name: citation-verifier
description: Use when checking whether cited works exist, bibliographic metadata is correct, or a source supports a manuscript statement.
---

# Citation Verifier

## Purpose

Check bibliographic identity and source-to-claim support as separate tasks. This skill reports verification status; it never supplies plausible substitute papers when a reference cannot be confirmed.

## When to Use

- Auditing citations, reference lists, BibTeX, DOIs, or identifiers.
- Verifying a citation before writing a literature claim.
- Checking whether a primary source supports the sentence attached to it.

## Inputs

Required: citation/reference and, for semantic checking, the associated manuscript statement. Optional: BibTeX, DOI/identifier, source file or URL, venue/year constraints, and access to authoritative indexes.

## Workflow

1. Normalize each supplied record without filling missing metadata.
2. Verify paper existence and compare title, authors, venue, year, identifier, and BibTeX fields against an authoritative publisher/proceedings/journal record or trusted bibliographic index. Record source and access limitations.
3. Identify version checked: published version, preprint, or other canonical source; note material version differences.
4. Separately inspect the cited source for semantic support. Record the exact section/page/table/equation or passage that bears on the attached statement.
5. Classify metadata as **verified**, **partially verified**, **mismatched**, or **unresolved**; classify semantic support as **supported**, **partially supported**, **not supported**, or **not checked**.
6. Correct fields only when evidence is authoritative; preserve original values and explain changes. If verification is impossible, specify the exact unresolved item.

## Output

Return a per-citation audit with original record, checked metadata, verification source, version, metadata status, semantic-support status/location, discrepancy, and action required. Provide corrected BibTeX only for verified fields.

## Validation

Recheck corrected metadata against the source; ensure semantic support was read in the paper and not inferred from another citation; verify unresolved fields remain visibly unresolved. Use [citation policy](../../shared/citation-policy.md).

## Failure Modes

- Treating a matching title or search snippet as proof that all metadata are correct.
- Treating correct metadata as proof of semantic support.
- Citing a paper only because another paper cites it.
- Creating placeholder references or silently swapping in a nearby-looking paper.

## Research Integrity Rules

Never fabricate authors, titles, venues, years, identifiers, BibTeX, quotations, or support. Prefer primary sources. Distinguish metadata verification from semantic verification and mark impossible checks explicitly **unresolved** or **not checked**.

## Interaction With Other Skills

Upstream: literature-review or manuscript citation list. Downstream: claim-evidence-checker uses semantic support; latex-paper-writer uses verified metadata; paper-reviewer flags unresolved high-impact citations.
