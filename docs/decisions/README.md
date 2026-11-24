# Decisions

Numbered decision records (ADRs). Never edit a decision away: write a new one and mark the old one `Superseded by NNNN`. New one: skill `new-decision` (template [`TEMPLATE.md`](TEMPLATE.md)). Two PRs that grab the same number fail the index check; renumber the newer one. The table below is generated.

<!-- index -->

| Title | status | date |
|---|---|---|
| [Split the work by model, each person end to end](0001-split-by-model.md) | Accepted | 2026-11-18 |
| [Owners chosen by poll; Joseph takes shared bottlenecks](0002-owners-by-poll.md) | Accepted | 2026-11-18 |
| [GitHub issues, one plan per issue, one change file per PR](0003-issues-plans-and-change-files.md) | Accepted | 2026-11-18 |
| [Knowledge and learnings as atomic notes with generated indexes](0004-atomic-notes-with-generated-indexes.md) | Accepted | 2026-11-18 |
| [One shared GPU account, with a cost estimate before every run and a log after](0005-shared-gpu-account-and-log.md) | Proposed | 2026-11-18 |
| [The report follows the ACL paper format (joint vs individual pending)](0006-report-format.md) | Proposed | 2026-11-18 |
| [One branch per issue, merged by PR](0007-one-branch-per-issue.md) | Accepted | 2026-11-18 |
| [Dependencies for the shared code: jiwer, huggingface_hub, librosa, pytest](0008-dependencies.md) | Accepted | 2026-11-18 |
| [One fixed 1,000-clip test set, one scorer, one predictions format; checkpoints off the repo](0009-test-set-predictions-and-checkpoints.md) | Accepted | 2026-11-20 |
| [Use the public copy evie-8/afrispeech-200 because official access was not granted](0010-public-mirror-of-afrispeech.md) | Accepted | 2026-11-20 |
| [torch and transformers for the transformer models](0011-torch-and-transformers.md) | Accepted | 2026-11-23 |
| [Train on Kaggle's free T4 GPUs, with logs saved as proof](0012-kaggle-free-gpus.md) | Accepted | 2026-11-23 |
