from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Biconditional(AKnight, Not(AKnave)),
    Implication(And(AKnight, AKnave), AKnight),
    Implication(And(AKnight, AKnave), Not(AKnave)),
    Implication(Or(Not(AKnight), Not(AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Implication(And(AKnave, BKnave), AKnight),
    Implication(Or(Not(AKnave), Not(BKnave)), AKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Implication(And(AKnight, BKnight), AKnight),
    Implication(And(AKnave, BKnave), AKnight),
    Implication(And(AKnight, BKnave), AKnave),
    Implication(And(AKnave, BKnight), AKnave),
    Implication(And(AKnave, BKnight), BKnight),
    Implication(And(AKnight, BKnave), BKnight),
    Implication(And(AKnight, BKnight), BKnave),
    Implication(And(AKnave, BKnave), BKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    Implication(AKnave, Not(AKnave)),
    Biconditional(And(AKnave, CKnave), BKnight),
    Biconditional(Not(And(AKnave, CKnave)), BKnave),

    Biconditional(AKnight, CKnight),
    Biconditional(Not(AKnight), CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
