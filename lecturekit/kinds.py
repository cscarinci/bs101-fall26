"""Every block type: (class, full label, short label). The class fixes the look and the numbering."""

KINDS = {
    "definition": ("foundation", "Definition", "Def"),
    "axiom": ("foundation", "Axiom", "Axiom"),
    "postulate": ("foundation", "Postulate", "Post"),
    "theorem": ("result", "Theorem", "Thm"),
    "proposition": ("result", "Proposition", "Prop"),
    "lemma": ("result", "Lemma", "Lem"),
    "corollary": ("result", "Corollary", "Cor"),
    "claim": ("result", "Claim", "Claim"),
    "fact": ("result", "Fact", "Fact"),
    "conjecture": ("result", "Conjecture", "Conj"),
    "example": ("illustration", "Example", "Ex"),
    "counterexample": ("illustration", "Counterexample", "Cex"),
    "exercise": ("practice", "Exercise", "Exer"),
    "problem": ("practice", "Problem", "Prob"),
    "motivation": ("motivation", "Motivation", "Motiv"),
    "intuition": ("motivation", "Intuition", "Idea"),
    "remark": ("remark", "Remark", "Rmk"),
    "note": ("remark", "Note", "Note"),
    "notation": ("remark", "Notation", "Notation"),
    "recall": ("remark", "Recall", "Recall"),
    "warning": ("remark", "Warning", "Warn"),
    "proof": ("argument", "Proof", "Pf"),
    "sketch": ("argument", "Proof sketch", "Sketch"),
    "solution": ("solution", "Solution", "Sol"),
}

# Classes that share the per-lecture counter (Definition 3.1, Theorem 3.2, Example 3.3, ...)
SHARED_COUNTER = {"foundation", "result", "illustration", "practice"}

# Everything the numbering pass looks for in the notebook source, and the counter each one uses
COUNTERS = {kind: ("block" if cls in SHARED_COUNTER else None) for kind, (cls, *_) in KINDS.items()}
COUNTERS.update({"section": "section", "figure": "figure", "interactive": "figure"})
