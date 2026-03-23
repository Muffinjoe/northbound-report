#!/usr/bin/env python3
"""Add next 4 URLs from the queue to sitemap.xml, then remove them from the queue."""

import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://northboundreport.com"
QUEUE_FILE = os.path.join(BASE, "sitemap-queue.txt")
SITEMAP_FILE = os.path.join(BASE, "sitemap.xml")
BATCH_SIZE = 4

# Priority mapping
def get_priority(slug):
    if "-v" in slug:
        return "0.8"
    if slug in ["sleep-quality-guide/", "emergency-preparedness-checklist/", "brain-health-over-40/", "water-quality-report/", "off-grid-living-beginners/"]:
        return "0.7"
    return "0.9"


def main():
    # Read queue
    if not os.path.exists(QUEUE_FILE):
        print("No queue file found. Nothing to do.")
        return

    with open(QUEUE_FILE, "r") as f:
        queue = [line.strip() for line in f if line.strip()]

    if not queue:
        print("Queue is empty. All pages have been added to sitemap.")
        return

    # Take next batch
    batch = queue[:BATCH_SIZE]
    remaining = queue[BATCH_SIZE:]

    # Read current sitemap
    with open(SITEMAP_FILE, "r") as f:
        sitemap = f.read()

    # Build new entries
    new_entries = ""
    for slug in batch:
        priority = get_priority(slug)
        new_entries += f'  <url><loc>{DOMAIN}/{slug}</loc><changefreq>weekly</changefreq><priority>{priority}</priority></url>\n'

    # Insert before closing </urlset>
    sitemap = sitemap.replace("</urlset>", new_entries + "</urlset>")

    # Write updated sitemap
    with open(SITEMAP_FILE, "w") as f:
        f.write(sitemap)

    # Write remaining queue
    with open(QUEUE_FILE, "w") as f:
        for slug in remaining:
            f.write(slug + "\n")

    print(f"Added {len(batch)} URLs to sitemap:")
    for slug in batch:
        print(f"  + {DOMAIN}/{slug}")
    print(f"Remaining in queue: {len(remaining)}")


if __name__ == "__main__":
    main()
