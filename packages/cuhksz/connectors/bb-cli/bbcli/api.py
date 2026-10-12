"""Learn REST API wrappers (/learn/api/public/v1, all GET, authenticated by the student-session cookie).

Pagination: follows paging.nextPage, guarding against self-reference and
runaway loops (cap of 10000 pages).
Course lookup: resolve_course accepts a course id (_18038_1), a course code,
or a name substring.
"""

from __future__ import annotations

from urllib.parse import quote, urljoin

from . import config
from .transport import ApiError, Transport, TransportError

API = "/learn/api/public/v1"


class BBClient:
    def __init__(self, transport: Transport):
        self.t = transport
        self._me = None

    # ---- Basics ----
    def get(self, path: str, params: dict | None = None) -> dict:
        return self.t.get_json(path, params=params)

    def _paginate(self, path: str, params: dict | None = None) -> list[dict]:
        params = dict(params or {})
        params.setdefault("limit", 100)
        results: list[dict] = []
        url = path
        seen: set[str] = set()
        for _ in range(10000):
            if url in seen:
                break
            seen.add(url)
            data = self.get(url, params=params if url == path else None)
            results.extend(data.get("results") or [])
            nxt = (data.get("paging") or {}).get("nextPage")
            if not nxt:
                break
            url = urljoin(config.BB_HOST + "/", nxt.lstrip("/"))
        return results

    # ---- Identity and courses ----
    def me(self) -> dict:
        if self._me is None:
            self._me = self.get(f"{API}/users/me")
        return self._me

    def terms(self) -> list[dict]:
        return self._paginate(f"{API}/terms")

    def my_courses(self) -> list[dict]:
        uid = self.me()["id"]
        rows = self._paginate(f"{API}/users/{uid}/courses", {"expand": "course"})
        out = []
        for r in rows:
            c = r.get("course") or {}
            c["membershipId"] = r.get("id")
            c["courseRoleId"] = r.get("courseRoleId")
            out.append(c)
        return out

    def resolve_course(self, arg: str) -> dict:
        courses = self.my_courses()
        if arg.startswith("_"):
            for c in courses:
                if c.get("id") == arg:
                    return c
        low = arg.lower()
        hits = [
            c for c in courses
            if low in (c.get("name") or "").lower()
            or low in (c.get("courseId") or "").lower()
            or low in (c.get("externalId") or "").lower()
        ]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise SystemExit(f"No course matched: {arg} (run `bb-cli courses` to see the list)")
        raise SystemExit("Ambiguous course match; use a longer substring or the course id:\n" + "\n".join(
            f"  {c['id']}  {c.get('name')}" for c in hits
        ))

    # ---- Content tree and attachments ----
    def contents(self, cid: str) -> list[dict]:
        return self._paginate(f"{API}/courses/{cid}/contents")

    def children(self, cid: str, content_id: str) -> list[dict]:
        return self._paginate(f"{API}/courses/{cid}/contents/{content_id}/children")

    def walk(self, cid: str, max_depth: int = 12):
        """Yield (path-segment list, node); cycle guard + depth limit."""
        seen: set[str] = set()

        def rec(parent_ids: list[str], nodes: list[dict], depth: int):
            for n in sorted(nodes, key=lambda x: (x.get("position") or 0, x.get("title") or "")):
                nid = n.get("id") or ""
                if nid in seen:
                    continue
                seen.add(nid)
                path = parent_ids + [n.get("title") or nid]
                yield path, n
                if n.get("hasChildren") and depth < max_depth:
                    yield from rec(path, self.children(cid, nid), depth + 1)

        yield from rec([], self.contents(cid), 1)

    def attachments(self, cid: str, content_id: str) -> list[dict]:
        try:
            return self._paginate(f"{API}/courses/{cid}/contents/{content_id}/attachments")
        except Exception:
            return []  # attachment-less resource nodes return 4xx; treat as empty

    @staticmethod
    def download_url(cid: str, content_id: str, attachment_id: str) -> str:
        return f"{API}/courses/{cid}/contents/{content_id}/attachments/{attachment_id}/download"

    # ---- Announcements ----
    def announcements(self, cid: str | None = None) -> list[dict]:
        if cid:
            return self._paginate(f"{API}/courses/{cid}/announcements")
        return self._paginate(f"{API}/announcements")  # institution-level

    def course_announcements_all(self) -> tuple[list[dict], list[dict]]:
        """Pull announcements course by course; a single course failing (e.g. announcements tool disabled, 400) is skipped into skipped — without failing the whole run."""
        out, skipped = [], []
        for c in self.my_courses():
            try:
                rows = self._paginate(f"{API}/courses/{c['id']}/announcements")
            except (ApiError, TransportError) as e:
                skipped.append({"course": c.get("name"), "id": c.get("id"), "error": str(e)[:120]})
                continue
            for a in rows:
                a["courseName"] = c.get("name")
                out.append(a)
        return out, skipped

    # ---- Gradebook ----
    def grade_columns(self, cid: str) -> list[dict]:
        return self._paginate(f"{API}/courses/{cid}/gradebook/columns")

    def column_status(self, cid: str, col_id: str) -> dict | None:
        uid = self.me()["id"]
        r = self.t.request("GET", f"{API}/courses/{cid}/gradebook/columns/{col_id}/users/{uid}")
        if r.status_code == 404:
            return {"status": "None", "score": None}  # not submitted (bbwatch semantics)
        if r.status_code != 200:
            return None
        try:
            return r.json()
        except ValueError:
            return None

    def column_attempts(self, cid: str, col_id: str) -> list[dict]:
        """Pull attempts per column (a student session only returns one's own)."""
        return self._paginate(f"{API}/courses/{cid}/gradebook/columns/{col_id}/attempts")

    def attempt_files(self, cid: str, attempt_id: str) -> list[dict]:
        return self._paginate(f"{API}/courses/{cid}/gradebook/attempts/{attempt_id}/files")

    @staticmethod
    def attempt_download_url(cid: str, attempt_id: str, file_id: str, file_name: str) -> str:
        # REST /download is 404 (student session); the Classic route works (verified 2026-09-30)
        return (f"/webapps/assignment/download?course_id={cid}&attempt_id={attempt_id}"
                f"&file_id={file_id}&fileName={quote(file_name)}")

    # ---- Calendar / roster ----
    def calendar_items(self) -> list[dict]:
        return self._paginate(f"{API}/calendars/items")

    def roster(self, cid: str) -> list[dict]:
        return self._paginate(f"{API}/courses/{cid}/users")
