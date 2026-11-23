---
title: Some AfriSpeech references contain text the speaker never said (page headers, glued words)
tags: [data, scoring]
source: "issue #6; common/test_set.csv"
author: Joseph Etse
ai-use: Claude spotted these while reading the worst clips; Joseph checked them
---

# Some AfriSpeech references contain text the speaker never said (page headers, glued words)

**What we found:** a few references are noisy, and every model is charged for it equally:

- **Text left over from a scanned book** that the speaker skipped: `qxd 08052010 3:08 PM Page 34 Aptara1 Vital Signs 35 At times, it is necessary…`
- **Words glued together:** `thediagnostictestofchoiceis`, `massoccurring`, `infectioncellulitis`. 17 references have a word of 20 letters or more. Some of these are real medical words (`crescendo-decrescendo`), others are glued.

**What we did:** nothing. The test set and references stay as they are (decision 0009), because changing them by hand would be a choice nobody could check. The same noise hits every model, so comparisons stay fair. The error analysis (M5) should say that part of the WER floor comes from the references.

Related: [[afrispeech-200]], [[whisper-writes-spoken-punctuation-as-words]]
