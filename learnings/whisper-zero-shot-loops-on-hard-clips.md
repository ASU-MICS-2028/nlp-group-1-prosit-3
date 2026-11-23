---
title: Zero-shot Whisper gets stuck repeating itself on about 5% of clips, and that alone adds about 15 WER points
tags: [M3, whisper, decoding]
source: "issue #6; eval/results/m3-whisper-small-zeroshot/"
author: Joseph Etse
ai-use: Claude ran the analysis and wrote the note; Joseph checked the examples
---

# Zero-shot Whisper gets stuck repeating itself on about 5% of clips, and that alone adds about 15 WER points

**Question:** why is zero-shot `whisper-small` at WER 0.480 on our test set?

**What we found:** on 49 of the 1,000 clips, Whisper falls into a loop ("we are right we are right…", "i do i do i do…", "u u u u…"). One clip with a 12-word reference produced about 290 words. Those 49 clips have a WER of 6.06 between them.

| What was scored | WER |
|---|---|
| All 1,000 clips (the number we report) | 0.480 |
| Leaving out the 49 looping clips (diagnostic only, never reported as our result) | 0.326 |
| The 49 clips, greedy decoding | 6.063 |
| The 49 clips, with temperature fallback | 1.205 |
| **All 1,000 clips, with temperature fallback** | **0.350** (clinical 0.389, general 0.322) |

**Temperature fallback** is Whisper's own defence against loops. If an output compresses too well (gzip ratio above 1.35, a sign of repetition) or is too unlikely, the clip is decoded again with a little randomness. Fallback removes most of the runaway loops. 44 of the 49 clips stay above WER 1.0, because the speech itself is hard (fast, accented, full of drug names).

**Winner:** temperature fallback. On the full test set it gives WER 0.350, down from 0.480, in about the same time (1,869 s against 1,824 s). Every Whisper run from now on uses it.

**Limits:** this is `whisper-small` only. Larger models loop less often. The check is a WER > 1 threshold, which also catches some clips that are wrong but don't loop.

Related: [[word-error-rate]], [[encoder-decoder]], [[whisper-writes-spoken-punctuation-as-words]]
