from pathlib import Path

main = Path('Before_the_Name_1880-1969.md').read_text(encoding='utf-8').rstrip()
map_text = Path('Before_the_Name_master_integration_map.md').read_text(encoding='utf-8').strip()
addendum = Path('Before_the_Name_combined_addendum.md').read_text(encoding='utf-8').strip()
out = '\n\n'.join([
    '<!-- EDITORIAL MASTER: canonical manuscript below is verbatim. Do not edit it. -->',
    main,
    '---\n\n# Editorial Integration Map\n\nThis map controls chapter-specific supplemental insertion during webpage generation.\n\n' + map_text,
    '---\n\n# Consolidated Supplemental Addendum\n\nThis source-preserving appendix contains the deduplicated addendum material. Use only entries mapped to the relevant chapter; retain source comments and evidence grades.\n\n' + addendum,
]) + '\n'
Path('Before_the_Name_complete_master.md').write_text(out, encoding='utf-8')
