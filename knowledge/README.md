# Knowledge

What everyone on the team should know, **one idea per file** (Zettelkasten style). Each note links to related notes with `[[slug]]` and names its source. Lecture, paper and prosit summaries live in [`sources/`](sources/README.md). Start with [the Prosit 3 brief](sources/prosit-3-brief.md), [team](team.md) and [environment](environment.md).

New note: copy [`TEMPLATE.md`](TEMPLATE.md), then run `python3 scripts/build_indexes.py`. The table below is generated; don't edit it by hand.

<!-- index -->

| Title | tags | author |
|---|---|---|
| [An ablation study removes parts one at a time to see what each contributed](ablation-study.md) | [experiments, lecture-04] | NLP Group 1 |
| [Ad hoc retrieval has changing queries over fixed documents; filtering has a fixed query over changing documents](ad-hoc-retrieval-vs-filtering.md) | [retrieval, lecture-04] | NLP Group 1 |
| [AfriSpeech-200 is 200 hours of African-accented English, clinical and general](afrispeech-200.md) | [dataset, asr] | Joseph Etse |
| [An agent runs a while loop of plan, act, check until the goal is met](agent-loop.md) | [agents, lecture-08] | NLP Group 1 |
| [Agents became possible once models could work for 15 to 30 minutes on one task without going off track](agents-do-long-horizon-work.md) | [agents, lecture-09] | NLP Group 1 |
| [An aligned model is helpful, honest and harmless, and the three can conflict](alignment-3h.md) | [alignment, lecture-06] | NLP Group 1 |
| [Domain, vocabulary, noise, sample rate and speaker traits all make ASR harder](asr-challenges.md) | [asr, prosit-3] | Joseph Etse |
| [Automatic speech recognition turns a waveform into text, and the use decides the design](asr-task.md) | [asr] | Joseph Etse |
| [Attention lets a model weight the words that matter most for the current prediction](attention.md) | [architectures, lecture-05] | NLP Group 1 |
| [Always put a backend between the user's page and the agent, so input can be cleaned and prompt injection blocked](backend-between-page-and-agent.md) | [security, lecture-08] | NLP Group 1 |
| [Backpropagation computes the gradients; gradient descent uses them to update every weight](backprop-and-gradient-descent.md) | [training, lecture-03-part-2] | NLP Group 1 |
| [Byte pair encoding builds a subword vocabulary by repeatedly merging the most frequent adjacent pair](byte-pair-encoding.md) | [tokenisation, lecture-09] | NLP Group 1 |
| [Fine-tuning every weight can make a model forget what it could do before](catastrophic-forgetting.md) | [fine-tuning, M3, M4] | Joseph Etse |
| [Chatbots do not learn from conversations: their weights are frozen, so memory is only the context](chatbots-dont-learn-after-training.md) | [learning, lecture-03-part-1] | NLP Group 1 |
| [When an API limits input size, split the input into chunks, process each, and join the results](chunk-long-input.md) | [deployment, lecture-11] | NLP Group 1 |
| [Cite results and others' claims; general knowledge in your own words needs no citation](cite-claims-not-general-knowledge.md) | [rules, report] | Joseph Etse |
| [A CNN slides a small kernel over the input; it is really cross-correlation](cnn-is-cross-correlation.md) | [asr, architectures] | Joseph Etse |
| [Code is liability: submit the smallest code that does the job](code-is-liability.md) | [rules, viva] | Joseph Etse |
| [Cross-entropy loss measures the gap between the predicted distribution and the one-hot truth](cross-entropy-loss.md) | [training, lecture-03-part-2] | NLP Group 1 |
| [CTC lets a speech model learn without anyone marking which sound goes with which letter](ctc.md) | [asr, M1, M2] | Joseph Etse |
| [Simpler models can win on small data; bigger models win once there is enough](data-size-decides-which-model-wins.md) | [modelling, prosit-1] | Joseph Etse |
| [Greedy, top-k, top-p and temperature are ways to pick a token from the distribution at inference](decoding-strategies.md) | [language-models, lecture-03-part-2] | NLP Group 1 |
| [An encoder-decoder compresses the input into a representation, then generates the output from it](encoder-decoder.md) | [asr, architectures, M3, M4] | Joseph Etse |
| [Encoder-only models classify, decoder-only models generate, encoder-decoders map sequence to sequence](encoder-only-vs-decoder-only.md) | [architectures, lecture-03-part-2] | NLP Group 1 |
| [Enterprises use AI models under licences, in their own cloud, or as open weights to protect their data](enterprise-model-use.md) | [deployment, lecture-11] | NLP Group 1 |
| [How to set up your machine for Prosit 3](environment.md) | [setup] | Joseph Etse |
| [An eval is a fixed set of prompts with a definition of good output, used to compare models](evals-choose-models.md) | [evaluation, lecture-10] | NLP Group 1 |
| [Gradient descent, reinforcement learning and evolutionary strategies are three ways to optimise a model](evolutionary-strategies-vs-rl.md) | [training, lecture-03-part-1] | NLP Group 1 |
| [In complex systems, experience finds bugs that prompting alone misses](experience-beats-prompting-in-complex-systems.md) | [ai-use, lecture-11] | NLP Group 1 |
| [Hallucination is confident, fluent output that is wrong, because the model fills gaps with likely content](hallucination.md) | [llm-behaviour, lecture-04] | NLP Group 1 |
| [How to score a model on the shared test set](how-to-score-a-model.md) | [evaluation, howto, s0] | Joseph Etse |
| [Train on Kaggle's free GPUs, with every run's logs saved as proof](how-to-train-on-kaggle.md) | [gpu, kaggle, how-to] | Joseph Etse |
| [Human-in-the-loop means people check AI output they can actually judge before it is used](human-in-the-loop.md) | [ai-use, lecture-07] | NLP Group 1 |
| [Instruction tuning (SFT) fine-tunes a pre-trained model on instruction-answer pairs so it follows requests](instruction-tuning.md) | [post-training, lecture-04] | NLP Group 1 |
| [A languageless LLM would keep knowledge and reasoning in a shared core, with each language as a thin layer](languageless-llm.md) | [multilingual, lecture-03-part-1] | NLP Group 1 |
| [A language model outputs a probability distribution over the vocabulary, not a single token](lm-outputs-a-distribution.md) | [language-models, lecture-03-part-2] | NLP Group 1 |
| [LoRA fine-tunes a big model by training two small matrices instead of the full weights](lora.md) | [fine-tuning, M4] | Joseph Etse |
| [A speech encoder's lower layers learn sounds shared by all languages, so fine-tuning can leave them frozen](lower-layers-learn-shared-sounds.md) | [fine-tuning, whisper, M3] | Joseph Etse |
| [Measure before adding complexity: a simpler design often wins](measure-before-adding-complexity.md) | [modelling, prosit-2] | Joseph Etse |
| [A mel spectrogram turns raw audio into a time-by-frequency picture that models read](mel-spectrogram.md) | [asr, features] | Joseph Etse |
| [Model merging combines two fine-tuned models of the same architecture into one that does both tasks](model-merging.md) | [training, lecture-03-part-1] | NLP Group 1 |
| [An agent is a model plus a harness: the model predicts tokens, the harness gives it tools and a loop](model-plus-harness.md) | [agents, lecture-10] | NLP Group 1 |
| [An n-gram model predicts the next word from only the previous N-1 words](n-gram-language-model.md) | [language-models, lecture-02] | NLP Group 1 |
| [A neuron outputs a weighted sum of its inputs, and a model is just its learned weights](neuron-weighted-sum.md) | [neural-networks, lecture-01] | NLP Group 1 |
| [Output tokens cost more than input tokens because generation is one token at a time](output-tokens-cost-more.md) | [llm-economics, lecture-05] | NLP Group 1 |
| [Parameters are learned from data; hyperparameters are chosen by you and tuned by trial](parameters-vs-hyperparameters.md) | [training, lecture-02] | NLP Group 1 |
| [Parameter-efficient fine-tuning trains only a small subset of parameters instead of the whole model](peft.md) | [post-training, lecture-05] | NLP Group 1 |
| [Perplexity measures how surprised a language model is by real text; lower is better](perplexity.md) | [evaluation, lecture-02] | NLP Group 1 |
| [Transformers process all tokens at once, so they need positional embeddings to know word order](positional-embeddings.md) | [architectures, lecture-05] | NLP Group 1 |
| [Preference data asks people to pick the better of two outputs, which is easier than writing good ones](preference-data.md) | [alignment, lecture-06] | NLP Group 1 |
| [RAG retrieves relevant documents at answer time and has the model answer from them](rag.md) | [retrieval, lecture-04] | NLP Group 1 |
| [Reinforcement learning trains an agent to choose actions that maximise reward in an environment](reinforcement-learning.md) | [learning, lecture-06] | NLP Group 1 |
| [The Prosit 3 report follows the ACL paper format](report-format.md) | [report, prosit-3] | Joseph Etse |
| [An RNN reads a sequence one step at a time, carrying a hidden state forward](rnn.md) | [asr, architectures, M1] | Joseph Etse |
| [Rule-based NLP breaks because every new rule meets a case it gets wrong](rule-based-systems-break.md) | [history, lecture-01] | NLP Group 1 |
| [Every number in the report must come from a saved result file](save-every-result-to-a-file.md) | [rules, evaluation] | Joseph Etse |
| [Pre-training hides part of unlabelled text and learns to predict it, so no human labels are needed](self-supervised-pretraining.md) | [training, lecture-01] | NLP Group 1 |
| [Sparse retrieval matches word counts; dense retrieval matches meaning with embeddings](sparse-vs-dense-retrieval.md) | [retrieval, lecture-04] | NLP Group 1 |
| [The whole team must recommend the same approach, because we build it together](team-agrees-on-one-recommendation.md) | [rules, report, prosit-3] | Joseph Etse |
| [Who is on the team, which slot each owns, and where things live](team.md) | [team, prosit-3] | Joseph Etse |
| [TF-IDF scores a word in a document by how often it appears there, damped by a log](tf-idf.md) | [retrieval, lecture-04] | NLP Group 1 |
| [Languages that split into more tokens cost more compute for the same problem](token-cost-across-languages.md) | [multilingual, lecture-03-part-1] | NLP Group 1 |
| [An agent needs tools because an LLM only produces text; MCP lets services list their tools](tools-and-mcp.md) | [agents, lecture-08] | NLP Group 1 |
| [Top-5 accuracy is the share of examples whose true label is among the model's five most likely predictions](top-5-accuracy.md) | [evaluation, lecture-09] | NLP Group 1 |
| [Embeddings turn meaningless token IDs into vectors where similar meanings sit close together](word-embeddings.md) | [representations, lecture-03-part-2] | NLP Group 1 |
| [Word error rate counts the edits needed to turn the model's text into the right text](word-error-rate.md) | [asr, evaluation] | Joseph Etse |
