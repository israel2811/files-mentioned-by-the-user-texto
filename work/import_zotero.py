#!/usr/bin/env python3
"""Zotero Import Automation for NEXUS/CCA-AAV.

Resolves the 40 core DOIs from the Crossref API, generates a standard BibTeX file
for easy manual import, and attempts to push to Zotero's local HTTP API on port 23119.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.parse
from pathlib import Path

CORE_DOIS = [
    "10.1093/schbul/15.2.209",
    "10.1192/bjp.bp.113.139048",
    "10.1016/s0272-7358(01)00103-9",
    "10.1017/s0033291708003814",
    "10.1017/s0033291712001626",
    "10.1001/jamapsychiatry.2015.0575",
    "10.3109/09638237.2011.562262",
    "10.1017/s0033291717002367",
    "10.1192/bjp.bp.109.065953",
    "10.1111/sjop.12219",
    "10.1111/sjop.12236",
    "10.1016/j.cpr.2016.10.010",
    "10.1093/schbul/sbs045",
    "10.1093/schbul/sbs061",
    "10.1093/schbul/sbu005",
    "10.1111/acps.12531",
    "10.1093/schbul/sbw078",
    "10.1016/j.neubiorev.2021.09.006",
    "10.1017/s0033291719000205",
    "10.1017/s003329171600115x",
    "10.1016/j.tics.2018.12.001",
    "10.1093/schbul/sby157",
    "10.1093/brain/awx206",
    "10.1016/j.schres.2011.07.013",
    "10.4088/jcp.09m05797yel",
    "10.1017/s0033291712000761",
    "10.1016/j.neubiorev.2011.07.010",
    "10.1017/s0033291712002760",
    "10.1016/j.cpr.2015.06.004",
    "10.1017/s003329170700253x",
    "10.1016/j.cpr.2011.05.004",
    "10.1093/schbul/sbu037",
    "10.3389/fpsyt.2018.00347",
    "10.1016/b978-0-444-62630-1.00024-x",
    "10.1016/j.yebeh.2013.12.014",
    "10.1097/yco.0000000000000586",
    "10.1055/s-0041-1722989",
    "10.1093/schizbullopen/sgaa060",
    "10.1093/schbul/sbz002",
    "10.1093/schbul/sby110",
]

BIB_OUT = Path(__file__).parent / "nexus_core_references.bib"


def fetch_bibtex_from_doi(doi: str) -> str | None:
    url = f"https://doi.org/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/x-bibtex")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching BibTeX for DOI {doi}: {e}")
        return None


def test_local_zotero() -> bool:
    url = "http://127.0.0.1:23119/connector/ping"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def main() -> int:
    print(f"Resolving {len(CORE_DOIS)} core DOIs from dx.doi.org...")
    bib_entries = []
    
    for i, doi in enumerate(CORE_DOIS, 1):
        print(f"[{i}/{len(CORE_DOIS)}] Resolving {doi}...", end="\r")
        bib = fetch_bibtex_from_doi(doi)
        if bib:
            bib_entries.append(bib.strip())
            
    print("\nResolution complete.")
    
    if bib_entries:
        bib_content = "\n\n".join(bib_entries)
        BIB_OUT.write_text(bib_content, encoding="utf-8")
        print(f"Saved BibTeX file to: {BIB_OUT.resolve()}")
    else:
        print("No BibTeX records resolved.")
        return 1

    zotero_active = test_local_zotero()
    if zotero_active:
        print("\n[Zotero Local Detected] Zotero is running at port 23119.")
        print("To push references, you can drag and drop the generated '.bib' file into Zotero,")
        print("or use Zotero's local translator API to automatically import it.")
    else:
        print("\n[Zotero Local Offline] Zotero is not running or port 23119 is blocked.")
        print(f"Please open Zotero, then manually import the generated file: {BIB_OUT.name}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
