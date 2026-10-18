#!/usr/bin/env python3
"""Generate Lireate cover via kie.ai nano-banana-2 (action selfie)."""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
RECORD_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
DEFAULT_FACE_URL = (
    "http://lyratetrademark.ru/wp-content/uploads/2025/12/photo_2025-12-24_12-17-06.jpg"
)
COVER_SIZE = (860, 400)
SMALL_SIZE = (350, 163)
PREVIEW_SIZE = (396, 300)


def _api_key():
    return (os.environ.get("KIE_API_KEY") or "").strip()


def _http_json(method, url, data=None, headers=None, timeout=120):
    hdrs = dict(headers or {})
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError("HTTP {0}: {1}".format(e.code, err_body[:500]))


def upload_face_ref(local_path, api_key):
    """Upload local PNG/JPG; return downloadUrl."""
    import mimetypes

    path = Path(local_path)
    if not path.is_file():
        raise FileNotFoundError(str(path))
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    with path.open("rb") as f:
        file_data = f.read()
    # multipart via stdlib
    import uuid

    boundary = uuid.uuid4().hex
    parts = []
    for name, filename, val in (
        ("uploadPath", None, "lireate/face-ref"),
        ("fileName", None, path.name),
    ):
        parts.append(
            "--{0}\r\nContent-Disposition: form-data; name=\"{1}\"\r\n\r\n{2}\r\n".format(
                boundary, name, val
            ).encode("utf-8")
        )
    parts.append(
        (
            "--{0}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{1}\"\r\n"
            "Content-Type: {2}\r\n\r\n"
        )
        .format(boundary, path.name, mime)
        .encode("utf-8")
    )
    parts.append(file_data)
    parts.append("\r\n--{0}--\r\n".format(boundary).encode("utf-8"))
    body = b"".join(parts)
    req = urllib.request.Request(
        UPLOAD_URL,
        data=body,
        headers={
            "Authorization": "Bearer {0}".format(api_key),
            "Content-Type": "multipart/form-data; boundary={0}".format(boundary),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    url = payload.get("downloadUrl") or payload.get("data", {}).get("downloadUrl")
    if not url:
        raise RuntimeError("upload missing downloadUrl: {0}".format(payload))
    return url


def load_prompt_template(root):
    text = (root / "memory/blog/cover-action-selfie.md").read_text(encoding="utf-8")
    m = re.search(
        r"## Промпт \(подставить.*?\n```\n([\s\S]*?)```",
        text,
    )
    if not m:
        raise RuntimeError("prompt block not found in cover-action-selfie.md")
    return m.group(1).strip()


def build_prompt(template, theme, era, headline):
    p = template.replace("{{THEME}}", theme)
    p = p.replace("{{ERA}}", era)
    p = p.replace("{{HEADLINE}}", headline)
    return p


def create_task(api_key, prompt, face_url):
    payload = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt,
            "image_input": [face_url],
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "output_format": "png",
        },
    }
    return _http_json(
        "POST",
        CREATE_URL,
        data=payload,
        headers={"Authorization": "Bearer {0}".format(api_key)},
    )


def poll_task(api_key, task_id, max_wait=600, interval=8):
    url = RECORD_URL + "?taskId=" + urllib.parse.quote(str(task_id))
    deadline = time.time() + max_wait
    while time.time() < deadline:
        info = _http_json(
            "GET",
            url,
            headers={"Authorization": "Bearer {0}".format(api_key)},
        )
        status = (info.get("status") or info.get("data", {}).get("status") or "").lower()
        if status in ("success", "succeeded", "completed", "done"):
            return info
        if status in ("fail", "failed", "error"):
            raise RuntimeError("kie task failed: {0}".format(info))
        time.sleep(interval)
    raise RuntimeError("kie poll timeout for task {0}".format(task_id))


def extract_image_url(record):
    for key in ("resultUrl", "outputUrl", "imageUrl", "url"):
        if record.get(key):
            return record[key]
    data = record.get("data") or record.get("result") or {}
    if isinstance(data, dict):
        for key in ("resultUrl", "outputUrl", "imageUrl", "url", "output"):
            val = data.get(key)
            if isinstance(val, str) and val.startswith("http"):
                return val
            if isinstance(val, list) and val:
                return val[0]
    raise RuntimeError("no image url in record: {0}".format(record))


def download_file(url, dest):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def resize_cover(src_path, cover_path, small_path):
    from PIL import Image

    im = Image.open(src_path).convert("RGB")
    w, h = im.size
    target_aspect = COVER_SIZE[0] / float(COVER_SIZE[1])
    src_aspect = w / float(h)
    if src_aspect > target_aspect:
        new_w = int(h * target_aspect)
        left = int((w - new_w) / 2)
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(w / target_aspect)
        top = 0
        box = (0, top, w, top + new_h)
    cropped = im.crop(box)
    cover = cropped.resize(COVER_SIZE, Image.Resampling.LANCZOS)
    cover_path.parent.mkdir(parents=True, exist_ok=True)
    cover.save(cover_path, format="PNG", optimize=True)
    small = cropped.resize(SMALL_SIZE, Image.Resampling.LANCZOS)
    small.save(small_path, format="PNG", optimize=True)
    preview = cover.resize(PREVIEW_SIZE, Image.Resampling.LANCZOS)
    return cover, small, preview


def write_qa_checklist(path, headline, era, checks):
    lines = [
        "# Cover KIE QA checklist",
        "",
        "- **cover_era:** {0}".format(era),
        "- **cover_headline:** {0}".format(headline),
        "",
        "## Automated",
    ]
    for c in checks:
        lines.append("- {0}".format(c))
    lines.extend(
        [
            "",
            "## Human (required before merge)",
            "- [ ] Лицо узнаваемо (identity lock)",
            "- [ ] Кириллица в заголовке без ошибок",
            "- [ ] Заголовок не на лице",
            "- [ ] Читаемо при 396×300",
            "- [ ] Руки без артефактов",
            "- [ ] Только @LIREATE латиницей внизу",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_qa_automated(preview_path, headline):
    checks = []
    ok = True
    if not preview_path.is_file():
        checks.append("FAIL: preview 396x300 missing")
        ok = False
    else:
        from PIL import Image

        im = Image.open(preview_path)
        if im.size != PREVIEW_SIZE:
            checks.append("FAIL: preview size {0}".format(im.size))
            ok = False
        else:
            checks.append("PASS: preview 396x300 exists")
    if not headline or len(headline.split()) > 5:
        checks.append("WARN: headline should be 2-5 words")
    else:
        checks.append("PASS: headline word count")
    if re.search(r"[A-Za-z]", headline):
        checks.append("FAIL: headline must not contain Latin letters")
        ok = False
    return checks, ok


def main():
    import urllib.parse

    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, required=True)
    ap.add_argument("--theme", required=True)
    ap.add_argument("--headline", required=True, help="2-5 Russian words")
    ap.add_argument("--era", help="cover_era; default from article.meta.json")
    ap.add_argument("--face-ref-url", default="")
    ap.add_argument("--face-ref-file", type=Path, default=None)
    ap.add_argument("--max-attempts", type=int, default=2)
    ap.add_argument("--dry-run", action="store_true", help="Build prompt only, no API")
    args = ap.parse_args()

    api_key = _api_key()
    if not args.dry_run and not api_key:
        print("COVER_BLOCKER: KIE_API_KEY not set")
        return 2

    root = REPO_ROOT
    article_dir = args.article_dir
    meta_path = article_dir / "article.meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    era = args.era or meta.get("cover_era") or ""
    if not era:
        print("COVER_BLOCKER: cover_era missing; run lireate_cover_era_pick.py")
        return 2

    sys.path.insert(0, str(root / "scripts"))
    from lireate_cover_era_check import check_article_dir

    era_errors = check_article_dir(root, article_dir)
    if era_errors:
        print("COVER_BLOCKER: era rotation", era_errors)
        return 2

    template = load_prompt_template(root)
    prompt = build_prompt(template, args.theme, era, args.headline)
    cover_dir = article_dir / "cover"
    cover_dir.mkdir(parents=True, exist_ok=True)
    (cover_dir / "kie-prompt.txt").write_text(prompt, encoding="utf-8")

    if args.dry_run:
        print("OK dry-run prompt written to cover/kie-prompt.txt")
        return 0

    face_url = args.face_ref_url or DEFAULT_FACE_URL
    if args.face_ref_file:
        face_url = upload_face_ref(args.face_ref_file, api_key)

    last_err = None
    for attempt in range(1, args.max_attempts + 1):
        try:
            created = create_task(api_key, prompt, face_url)
            task_id = created.get("taskId") or created.get("data", {}).get("taskId")
            if not task_id:
                raise RuntimeError("no taskId: {0}".format(created))
            record = poll_task(api_key, task_id)
            img_url = extract_image_url(record if isinstance(record, dict) else {})
            raw_path = cover_dir / "kie-raw.png"
            download_file(img_url, raw_path)
            cover_path = cover_dir / "cover.png"
            small_path = cover_dir / "cover-small.png"
            _cover, _small, preview = resize_cover(raw_path, cover_path, small_path)
            preview_path = cover_dir / "cover-preview-396x300.png"
            preview.save(preview_path, format="PNG", optimize=True)
            checks, auto_ok = run_qa_automated(preview_path, args.headline)
            write_qa_checklist(cover_dir / "cover-kie-qa.md", args.headline, era, checks)
            meta["cover_headline"] = args.headline
            meta["cover_era"] = era
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if not auto_ok:
                print("COVER_BLOCKER: automated QA failed")
                return 2
            print("OK cover written", cover_path)
            return 0
        except Exception as e:
            last_err = e
            print("kie attempt {0} failed: {1}".format(attempt, e))
    print("COVER_BLOCKER: kie failed after {0} attempts: {1}".format(args.max_attempts, last_err))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
