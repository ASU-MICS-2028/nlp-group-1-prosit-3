---
title: The Prosit 3 report follows the ACL paper format
tags: [report, prosit-3]
source: Lecture 12 (Prosit 3 launch), Lecture 2 part 2, Lecture 4; ACL formatting guidelines (checked 2026-11-18)
author: Joseph Etse
ai-use: Claude found the lecture quotes and summarised the ACL guidelines; Joseph checked them
---

# The Prosit 3 report follows the ACL paper format

## What the instructor said

- **Lecture 12 (Prosit 3 launch):** the report should be "similar to what is used in ACL or other NLP publications and should be under 10 pages." The report has to argue for our recommendation like a research paper, not just describe what we built.
- **Lecture 2 part 2 (Prosit 1):** "use a good format for your technical report… a research paper type format."
- **Lecture 4 (citations):** cite results and claims taken from others, and put anyone's exact words in quotation marks. General knowledge in your own words (for example, what an RNN is) needs no citation. Not every sentence needs one.
- He named no specific template or section list beyond "ACL".
- **Still open:** is the report individual or joint? In Lecture 12 the instructor said "the report is individual… Section A that's individual and then section B", but promised to confirm with the brief's author. Whatever the answer, the whole team must recommend the same approach, because we build it together.

## What the ACL format means

Source: [ACL formatting guidelines](https://acl-org.github.io/ACLPUB/formatting.html) and [ACL style files](https://github.com/acl-org/acl-style-files).

- **Template:** use the official one, unmodified. [Overleaf template](https://www.overleaf.com/latex/templates/association-for-computational-linguistics-acl-conference/jvxskxpnznfj). LaTeX (`acl_latex.tex`) and Word versions are in the GitHub repo.
- **Layout:** A4, two columns, 2.5 cm margins, Times 11 pt body. The output is a PDF with all fonts embedded. Use the final ("camera-ready") mode: no line numbers, no page numbers.
- **Sections, in order:**
  1. Title and authors
  2. Abstract (200 words at most)
  3. Numbered sections, typically Introduction, Related Work, Method, Experiments, Results and Analysis, Conclusion
  4. **Limitations** (required; no new results in it)
  5. Ethical Considerations (optional)
  6. Acknowledgments
  7. References
  8. Appendices (lettered A, B…)
- **What counts toward the length:** ACL's own limit is 8–9 pages of content. Our brief says under 10 pages. References, Limitations, Ethics and appendices do not count under ACL rules. Ask the instructor whether the same applies to our 10 pages.
- **Citations:** author-year, "(Radford et al., 2023)" or "Radford et al. (2023) showed…". References are alphabetical, with DOIs or ACL Anthology links where available.
- **Captions:** "Figure 1: …" and "Table 1: …", placed below the figure or table.

## What the brief adds

- The GitHub link goes on **page 1** of the report (and on slide 1).
- The report must make a scholarly case: RNNs or an alternative, with reasons and evidence, then show how we built and evaluated our recommendation.

Related: [[prosit-3-brief]], [[cite-claims-not-general-knowledge]], [[team-agrees-on-one-recommendation]]
