import json


def load_rules():
    with open("data/rules.json") as f:
        return json.load(f)


def detect_conflicts(medications):
    rules = load_rules()
    conflicts = []

    names = [m["name"] for m in medications]

    # Rule 1: Same drug different dose
    seen = {}
    for med in medications:
        name = med["name"]
        dose = med["dose"]

        if name in seen and seen[name] != dose:
            conflicts.append({
                "drug": name,
                "type": "dose_mismatch",
                "description": f"{name} has conflicting doses {seen[name]} vs {dose}"
            })
        else:
            seen[name] = dose

    # Rule 2: Blacklisted combinations
    for combo in rules["blacklisted_combinations"]:
        if combo[0] in names and combo[1] in names:
            conflicts.append({
                "drug": f"{combo[0]} + {combo[1]}",
                "type": "drug_interaction",
                "description": f"{combo[0]} should not be combined with {combo[1]}"
            })

    return conflicts