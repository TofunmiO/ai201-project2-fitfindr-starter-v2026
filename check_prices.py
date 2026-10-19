"""Reproduce the criterion 5 check: every result stays within the price ceiling.

    python check_prices.py

Runs the same query as the criterion 5 scenario in scenarios.py, parses it the
way the agent does, searches through the MCP server like run_agent does, and
prints every returned listing with its price. Exits with an error if any
listing costs more than the ceiling.
"""

import sys

from agent import parse_query
from mcp_client import call_tool

QUERY = "vintage graphic tee under $30"

parsed = parse_query(QUERY)
ceiling = parsed["max_price"]

results = call_tool(
    "search_listings",
    {
        "description": parsed["description"],
        "size": parsed["size"],
        "max_price": ceiling,
    },
)

print(f"query:   {QUERY}")
print(f"parsed:  {parsed}")
print(f"results: {len(results)} listings\n")
for listing in results:
    print(f"{listing['id']}  ${listing['price']:>5g}  {listing['title']}")

over = [listing for listing in results if listing["price"] > ceiling]
print(f"\nhighest price: ${max(listing['price'] for listing in results):g}  (ceiling ${ceiling:g})")
if over:
    print(f"FAIL  {len(over)} listing(s) over the ceiling")
    sys.exit(1)
print("PASS  every listing is within the ceiling")
