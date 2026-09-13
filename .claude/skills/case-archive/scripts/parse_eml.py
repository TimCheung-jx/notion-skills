#!/usr/bin/env python3
"""case-archive: parse an .eml file into ingestion-friendly text.

Usage:
    python3 parse_eml.py <file.eml> [--outdir DIR]

Output (stdout): structured summary — thread-relevant headers (Date, From,
To, Cc, Subject, Message-ID, In-Reply-To, References), body text, and the
attachment list. Attachments under 5MB are extracted into
<outdir>/<stem>_attachments/ so embedded documents can be ingested further.

Stdlib only. Purely local — nothing is sent anywhere.
"""
import argparse
import re
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path

MAX_ATTACHMENT_BYTES = 5 * 1024 * 1024


class _TextExtractor(HTMLParser):
    """Pull visible text out of an HTML email body."""

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def html_to_text(html):
    extractor = _TextExtractor()
    try:
        extractor.feed(html)
        return "\n".join(extractor.parts)
    except Exception:
        return re.sub(r"<[^>]+>", " ", html)


def decode(value):
    if value is None:
        return ""
    try:
        return str(make_header(decode_header(str(value))))
    except Exception:
        return str(value)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("eml")
    ap.add_argument("--outdir", default=None, help="attachment output dir (default: alongside the .eml)")
    args = ap.parse_args()

    src = Path(args.eml)
    msg = BytesParser(policy=policy.default).parsebytes(src.read_bytes())

    outdir = Path(args.outdir) if args.outdir else src.parent
    att_dir = outdir / (src.stem[:60] + "_attachments")

    lines = [f"文件: {src.name}"]
    for header in ("Date", "From", "To", "Cc", "Subject"):
        value = msg.get(header)
        if value:
            lines.append(f"{header}: {decode(value)}")
    for header in ("Message-ID", "In-Reply-To", "References"):
        value = msg.get(header)
        if value:
            lines.append(f"{header}: {value}")

    body_text = None
    attachments = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        disposition = str(part.get("Content-Disposition") or "")
        filename = part.get_filename()
        if filename or "attachment" in disposition:
            attachments.append((decode(filename) if filename else "unnamed",
                                part.get_payload(decode=True) or b""))
            continue
        ctype = part.get_content_type()
        if ctype in ("text/plain", "text/html") and body_text is None:
            raw = part.get_payload(decode=True) or b""
            charset = part.get_content_charset() or "utf-8"
            try:
                text = raw.decode(charset, errors="replace")
            except LookupError:
                text = raw.decode("utf-8", errors="replace")
            if ctype == "text/html":
                text = html_to_text(text)
            body_text = text

    lines += ["", "== 正文 ==",
              body_text.strip() if body_text else "(无正文)",
              "", f"== 附件 {len(attachments)} 个 =="]

    if attachments:
        att_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in attachments:
        size = len(payload)
        line = f"- {name} ({size} bytes)"
        if size <= MAX_ATTACHMENT_BYTES:
            safe = re.sub(r"[\\/:*?\"<>|]", "_", name) or "unnamed"
            target = att_dir / safe
            counter = 1
            while target.exists():
                target = att_dir / f"{target.stem}_{counter}{target.suffix}"
                counter += 1
            target.write_bytes(payload)
            line += f" → 已保存: {target}"
        else:
            line += " → 超过 5MB，未保存（请手动处理）"
        lines.append(line)

    print("\n".join(lines))


if __name__ == "__main__":
    main()
