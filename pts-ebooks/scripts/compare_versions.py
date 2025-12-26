import os
import re
import json
from pathlib import Path
from collections import defaultdict

class FastComparator:
    def __init__(self):
        self.base_path = Path(os.getcwd())
        self.nikayas = {
            'an': ('v1.1', 'v2.0_processed'),
            'dn': ('v1.2', 'v2.0_processed'),
            'mn': ('v1.2', 'v2.0_processed'),
            'sn': ('v1.0', 'epub_v2_styled_sn'),
        }
        self.summaries = {}

    def analyze_file(self, old_path, new_path):
        with open(old_path, 'r', encoding='utf-8', errors='replace') as f:
            old_text = f.read()
        with open(new_path, 'r', encoding='utf-8', errors='replace') as f:
            new_text = f.read()

        changes = defaultdict(list)
        
        # Check Character Normalization
        if 'ɱ' in old_text and 'ṁ' in new_text:
            changes['Normalization'].append("Converted 'ɱ' to 'ṁ'")
        if 'ŋ' in old_text and 'ṅ' in new_text:
            changes['Normalization'].append("Converted 'ŋ' to 'ṅ'")

        # Check Header Re-org
        old_headers = re.findall(r'<(h[1-4])[^>]*>(.*?)</\1>', old_text, re.S)
        new_headers = re.findall(r'<(h[1-4])[^>]*>(.*?)</\1>', new_text, re.S)
        
        if len(old_headers) != len(new_headers):
            changes['Structure'].append(f"Header count changed from {len(old_headers)} to {len(new_headers)}")
        
        # Check ID Preservation
        old_ids = set(re.findall(r'id="(sigil_toc_id_\d+)"', old_text))
        new_ids = set(re.findall(r'id="(sigil_toc_id_\d+)"', new_text))
        preserved = old_ids.intersection(new_ids)
        if old_ids:
            changes['ID Preservation'].append(f"Preserved {len(preserved)} of {len(old_ids)} Sigil TOC IDs")

        # Check Boilerplate Removal
        for term in ["Translated by", "Copyright", "Public Domain", "Commercial Rights"]:
            if term in old_text and term not in new_text:
                changes['Cleanup'].append(f"Removed '{term}' boilerplate")

        # Check Link Cleanup
        old_links = len(re.findall(r'<a\s', old_text))
        new_links = len(re.findall(r'<a\s', new_text))
        if old_links > new_links:
            changes['Cleanup'].append(f"Reduced links from {old_links} to {new_links} (stripped web-specific anchors)")

        return changes

    def run(self):
        report = "# PTS Ebooks v2.0 Changes Summary\n\n"
        
        for nikaya, (old_v, new_v) in self.nikayas.items():
            old_dir = self.base_path / nikaya / "src" / old_v
            new_dir = self.base_path / nikaya / "src" / new_v
            
            if not old_dir.exists() or not new_dir.exists():
                continue
                
            common = sorted(list(set(f.name for f in old_dir.glob("*.htm*")) & set(f.name for f in new_dir.glob("*.htm*"))))
            if not common: continue
            
            # Sample up to 10 files
            sample = common[:10]
            nikaya_changes = defaultdict(set)
            
            for filename in sample:
                file_changes = self.analyze_file(old_dir / filename, new_dir / filename)
                for cat, msgs in file_changes.items():
                    for m in msgs:
                        nikaya_changes[cat].add(m)
            
            report += f"## {nikaya.upper()} ({old_v} → 2.0)\n\n"
            
            # Re-org notes based on project knowledge
            if nikaya == 'sn':
                report += "- **Significant Re-org**: Flattened complex nested directory structure from website into a single directory. Combined multi-line English headers into hierarchical H1/H2/H3 structure to match legacy TOC.\n"
            elif nikaya == 'an':
                report += "- **Significant Re-org**: Promoted Book and Chapter titles to H1/H2 to improve navigation consistency.\n"
            elif nikaya == 'mn':
                report += "- **Significant Re-org**: Standardized H1 (Number. Title) and H2 (Pali Title) format across all suttas.\n"

            for cat, msgs in nikaya_changes.items():
                report += f"### {cat}\n"
                for m in sorted(list(msgs)):
                    report += f"- {m}\n"
                report += "\n"
            report += "---\n\n"

        with open("v2_CHANGES_SUMMARIES.md", "w") as f:
            f.write(report)
        print("Generated v2_CHANGES_SUMMARIES.md")

if __name__ == "__main__":
    FastComparator().run()