from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Default metadata for header (customize here or pass overrides to export_chat)
DEFAULT_PROJECT_DESCRIPTION = "GDPR Compliance Assistant - Chat export"
DEFAULT_PROJECT_AUTHOR = "Unknown"
DEFAULT_PROJECT_URL = "N/A"


def export_chat(
    chat_name: str,
    messages: List[Dict],
    project_description: Optional[str] = None,
    author: Optional[str] = None,
    url: Optional[str] = None,
) -> Tuple[bytes, str]:
    """
    Prepare an export of a chat as human-readable TXT bytes and a suggested filename.

    Each message is expected to be a dict with at least keys:
      - role: "user" | "assistant"
      - content: str
      - sources: Optional[List[Dict]] (with optional document/page/content)
      - timestamp: Optional[str] (ISO-8601). If missing, it will be filled with export time.
    """
    exported_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    # Resolve header values
    header_description = project_description or DEFAULT_PROJECT_DESCRIPTION
    header_author = author or DEFAULT_PROJECT_AUTHOR
    header_url = url or DEFAULT_PROJECT_URL

    lines: List[str] = []
    # Standard header
    lines.append(header_description)
    lines.append(f"Author: {header_author}")
    lines.append(f"URL: {header_url}")
    lines.append(f"Exported at: {exported_at}")
    lines.append(f"Chat: {chat_name}")
    lines.append("" )

    for idx, msg in enumerate(messages, start=1):
        role = msg.get("role") or "unknown"
        content = (msg.get("content") or "").rstrip()
        timestamp = (msg.get("timestamp") or exported_at)
        lines.append(f"--- Message {idx} ---")
        lines.append(f"Time: {timestamp}")
        lines.append(f"Role: {role}")
        lines.append("")
        lines.append(content)

        sources = msg.get("sources") or []
        if sources:
            lines.append("")
            lines.append("Sources:")
            for s_idx, src in enumerate(sources, start=1):
                doc_name = src.get("document") or (src.get("metadata", {}) or {}).get("document_name")
                page_num = src.get("page") or (src.get("metadata", {}) or {}).get("page_number") or (src.get("metadata", {}) or {}).get("page")
                header = f"[{s_idx}] {doc_name or 'Unknown document'}" + (f" — page {page_num}" if page_num is not None else "")
                src_content = (src.get("content", "") or "").rstrip()
                lines.append(header)
                if src_content:
                    lines.append(src_content)
                lines.append("")

        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    data = text.encode("utf-8")
    safe_name = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in chat_name).strip("_") or "chat"
    filename = f"{safe_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    return data, filename


