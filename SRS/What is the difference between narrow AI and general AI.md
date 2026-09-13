<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is the difference between narrow AI and general AI

> [!abstract] Short answer
> Narrow AI (weak AI) is systems that **excel at one task or domain and do not transfer** beyond it — spam filters, face recognition, chess engines, code models. General AI (AGI, strong AI) is a hypothetical system with **human-level ability to transfer knowledge across arbitrary domains** and learn new tasks with human-level sample efficiency. Everything deployed today, including the largest LLMs, is narrow AI by this definition.

The distinction is about generality of competence, not about raw benchmark scores. A model that beats grandmasters at chess and does literally nothing else is narrow. A model that writes code, passes law exams, and plans trips is *broad* — but still narrow in the strict sense: it has no autonomous goals, no persistent learning from experience after deployment, and its competence degrades unpredictably outside its training distribution.

## What actually separates them

* **Transfer** — narrow systems fail outside their training distribution; a general learner would re-derive skills in new domains the way humans do. Current models transfer only within what pretraining covered; the mitigation is retrieval or fine-tuning — [[When do you fine-tune versus use RAG versus prompting]].
* **Sample efficiency** — humans learn a new game from a few examples; deep learning typically needs thousands to millions. Transfer learning narrows the gap within a domain: [[What is transfer learning]].
* **Continual learning and agency** — deployed models are frozen; they do not accumulate experience. Lifelong learning, stable world models, and open-ended goal formation are unsolved research problems.
* **Grounding and reasoning reliability** — LLMs produce fluent text with confident errors: [[What is an AI hallucination]]; a general intelligence would know when it does not know.

```d2
direction: right
narrow: "Narrow AI (all deployed systems)\nhigh skill, one domain\nno transfer" {
  width: 240; height: 100
}
broad: "Broad but still narrow\nmany domains from pretraining\nfrozen weights" {
  width: 240; height: 100
}
agi: "AGI (hypothetical)\nhuman-level transfer\ncontinual learning" {
  width: 220; height: 100
}
narrow -> broad: "scale + data + pretraining" { }
broad -> agi: "unsolved research" { style.stroke: "#b71c1c" }
```

**Fig. 1.** Scaling moved systems along the narrow axis — broad competence from pretraining — but the jump to genuine generality remains an open problem, not a scheduled release.

## Why the distinction matters practically

It sets expectations and governance. Narrow AI can be validated on a fixed task distribution, monitored for drift, and audited: [[What is MLOps]]. Claims of generality without those guarantees are marketing. When an interviewer asks this, they are usually probing whether you can say what current systems actually do — pattern completion over a training distribution — versus what the marketing says they do.

> [!warning] Interview trap
> "ChatGPT is AGI." No — impressive breadth is not general intelligence: no persistent memory, no autonomous learning after training, unreliable calibration, and brittle out-of-distribution behavior. The opposite trap is also wrong: "LLMs are just autocomplete, nothing new" — they demonstrate real in-context generalization; the honest position is broad-but-narrow.

> [!tip] Interview answer
> Narrow AI means competence bound to a task or distribution — which is every deployed system today, including large language models. General AI would require human-like transfer, sample efficiency, and continual learning, and none of that exists yet. I would say scaling made systems broader, but breadth from pretraining is still narrow in the strict sense, and the practical consequence is that validation and monitoring stay task-specific.

