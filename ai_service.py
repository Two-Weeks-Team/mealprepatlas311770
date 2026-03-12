def _coerce_unstructured_payload(raw_text: str) -> dict[str, object]:
    compact = raw_text.strip()
    normalized = compact.replace("\n", ",")
    tags = [part.strip(" -•\t") for part in normalized.split(",") if part.strip(" -•\t")]
    if not tags:
        tags = ["guided plan", "saved output", "shareable insight"]
    headline = tags[0].title()
    items = []
    for index, tag in enumerate(tags[:3], start=1):
        items.append({
            "title": f"Stage {index}: {tag.title()}",
            "detail": f"Use {tag} to move the request toward a demo-ready outcome.",
            "score": min(96, 80 + index * 4),
        })
    highlights = [tag.title() for tag in tags[:3]]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact or f"{headline} fallback is ready for review.",
        "tags": tags[:6],
        "items": items,
        "score": 88,
        "insights": [f"Lead with {headline} on the first screen.", "Keep one clear action visible throughout the flow."],
        "next_actions": ["Review the generated plan.", "Save the strongest output for the demo finale."],
        "highlights": highlights,
    }

def _normalize_inference_payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return _coerce_unstructured_payload(str(payload))
    normalized = dict(payload)
    summary = str(normalized.get("summary") or normalized.get("note") or "AI-generated plan ready")
    raw_items = normalized.get("items")
    items: list[dict[str, object]] = []
    if isinstance(raw_items, list):
        for index, entry in enumerate(raw_items[:3], start=1):
            if isinstance(entry, dict):
                title = str(entry.get("title") or f"Stage {index}")
                detail = str(entry.get("detail") or entry.get("description") or title)
                score = float(entry.get("score") or min(96, 80 + index * 4))
            else:
                label = str(entry).strip() or f"Stage {index}"
                title = f"Stage {index}: {label.title()}"
                detail = f"Use {label} to move the request toward a demo-ready outcome."
                score = float(min(96, 80 + index * 4))
            items.append({"title": title, "detail": detail, "score": score})
    if not items:
        items = _coerce_unstructured_payload(summary).get("items", [])
    raw_insights = normalized.get("insights")
    if isinstance(raw_insights, list):
        insights = [str(entry) for entry in raw_insights if str(entry).strip()]
    elif isinstance(raw_insights, str) and raw_insights.strip():
        insights = [raw_insights.strip()]
    else:
        insights = []
    next_actions = normalized.get("next_actions")
    if isinstance(next_actions, list):
        next_actions = [str(entry) for entry in next_actions if str(entry).strip()]
    else:
        next_actions = []
    highlights = normalized.get("highlights")
    if isinstance(highlights, list):
        highlights = [str(entry) for entry in highlights if str(entry).strip()]
    else:
        highlights = []
    if not insights and not next_actions and not highlights:
        fallback = _coerce_unstructured_payload(summary)
        insights = fallback.get("insights", [])
        next_actions = fallback.get("next_actions", [])
        highlights = fallback.get("highlights", [])
    return {
        **normalized,
        "summary": summary,
        "items": items,
        "score": float(normalized.get("score") or 88),
        "insights": insights,
        "next_actions": next_actions,
        "highlights": highlights,
    }


APP_NAME = "Meal Prep Atlas"
APP_TAGLINE = "Build a consumer meal-prep planner that turns a weekly grocery and cooking inspiration video into a prep schedule, groce"
KEY_FEATURES = ["prep block", "grocery lane", "meal board", "container checklist"]
PROOF_POINTS = ["weekly prep plan", "organized grocery groups", "saved meal board", "the first fold shows prep objects, not KPIs"]
REFERENCE_OBJECTS = ["prep block", "grocery lane", "meal board", "container checklist", "recipe slot"]
SAMPLE_SEED_DATA = ["weekly prep plan", "organized grocery groups", "saved meal board", "Sunday prep block"]
SURFACE_LABELS = {"hero": "kitchen prep atlas", "workspace": "prep block", "result": "grocery lane", "support": "saved meal boards", "collection": "prep block planner"}
COLLECTION_TITLE = "Kitchen Prep Atlas stays visible after each run."


def _artifact_label(items, index, fallback):
    if index < len(items) and str(items[index]).strip():
        return str(items[index]).strip()
    return fallback


def _sentence_case(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return text[0].upper() + text[1:]


def build_plan(query: str, preferences: str) -> dict:
    subject = (query or APP_TAGLINE).strip() or APP_NAME
    guidance = (preferences or "Keep the result practical, saveable, and ready to use immediately.").strip()
    result_labels = SAMPLE_SEED_DATA or PROOF_POINTS or KEY_FEATURES
    object_labels = REFERENCE_OBJECTS or KEY_FEATURES
    items = []
    for index in range(3):
        object_label = _artifact_label(object_labels, index, f"Step {index + 1}")
        result_label = _artifact_label(result_labels, index, _artifact_label(PROOF_POINTS, index, "usable output"))
        partner_label = _artifact_label(object_labels, min(index + 1, len(object_labels) - 1), SURFACE_LABELS.get("collection", "saved result"))
        items.append(
            {
                "title": _sentence_case(object_label),
                "detail": f"Shape {result_label.lower()} through {object_label.lower()}, keep {partner_label.lower()} visible, and follow: {guidance}.",
                "score": min(96, 78 + index * 5),
            }
        )
    summary_result = _artifact_label(result_labels, 0, "usable output")
    summary_objects = ", ".join(label.lower() for label in object_labels[:2])
    return {
        "summary": f"{APP_NAME} turned '{subject}' into {summary_result.lower()} with {summary_objects} and a reusable {SURFACE_LABELS.get('collection', 'saved result').lower()}.",
        "score": 88,
        "items": items,
    }


def build_insights(selection: str, context: str) -> dict:
    focus = (selection or _artifact_label(REFERENCE_OBJECTS, 0, APP_NAME)).strip()
    base_context = (context or APP_TAGLINE).strip()
    collection_label = SURFACE_LABELS.get("collection", "saved result")
    support_label = SURFACE_LABELS.get("support", "support rail")
    return {
        "insights": [
            f"Lead with {focus} so the first screen proves {_artifact_label(PROOF_POINTS, 0, 'usable value').lower()} immediately.",
            f"Keep {support_label.lower()} and {collection_label.lower()} visible so the workflow reads like a dedicated product, not a generic tool.",
        ],
        "next_actions": [
            f"Save the strongest {collection_label.lower()} after each run.",
            f"Use {base_context} to refine the next {_artifact_label(REFERENCE_OBJECTS, 1, 'artifact').lower()}.",
        ],
        "highlights": PROOF_POINTS[:3] or SAMPLE_SEED_DATA[:3],
    }
