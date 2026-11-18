---
title: One shared GPU account, with a cost estimate before every run and a log after
status: Proposed
date: 2026-11-18
decided-by: Joseph (ceiling and approval rule pending)
ai-use: none
---

# 0005. One shared GPU account, with a cost estimate before every run and a log after

## Context

Fine-tuning needs rented GPUs (RunPod, Modal, AWS or similar). Each run costs real money.

## Options considered

- Each person pays for their own account: no shared key, but uneven costs and no overview.
- One shared account set up by Joseph.

## Decision

One shared account, set up by Joseph. The key lives only in each person's git-ignored `.env`. Each run's expected cost goes in the issue plan before it starts, and a row goes in `docs/gpu-log.md` after it ends. **Still to decide:** the provider, the total spending ceiling, and who approves runs above a threshold. Set this decision to Accepted once those are added.

## Consequences

- One place to see what has been spent.
- A shared key: anyone who leaks it exposes everyone. The secret guards block `.env` and keys from commits.
