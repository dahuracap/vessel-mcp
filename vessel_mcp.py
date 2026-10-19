from fastmcp import FastMCP
import pandas as pd
 
# Create MCP Server
mcp = FastMCP("DEFRA Vessel Lookup")
 
# Load vessel data
df = pd.read_excel(
    "October_2026_Under_10m_vessel_list.xlsx",
    header=4,
    engine="openpyxl"
)
 
# Remove duplicate licence entries for the same RSS
df = df.drop_duplicates(
    subset=["Registry of Shipping and Seamen number"]
)
 
@mcp.tool()
def find_vessel_by_rss(rss: str) -> dict:
    """
    Find vessel details from an RSS number.
    """
 
    matches = df[
        df["Registry of Shipping and Seamen number"]
        .astype(str)
        .str.upper()
        == rss.strip().upper()
    ]
 
    if matches.empty:
        return {
            "found": False,
            "message": "No vessel found."
        }
 
    vessel = matches.iloc[0]
 
    return {
        "found": True,
        "vessel_name": vessel["Vessel name"],
        "rss": vessel["Registry of Shipping and Seamen number"],
        "home_port": vessel["Home port"],
        "administrative_port": vessel["Administrative port"],
        "overall_length": vessel["Overall length"],
        "licence_category": vessel["Licence Category"]
    }
 
 
@mcp.tool()
def find_vessel_by_name(vessel_name: str) -> dict:
    """
    Find vessel details from a vessel name.
    """
 
    matches = df[
        df["Vessel name"]
        .astype(str)
        .str.upper()
        == vessel_name.strip().upper()
    ]
 
    if matches.empty:
        return {
            "found": False,
            "message": "No vessel found."
        }
 
    vessel = matches.iloc[0]
 
    return {
        "found": True,
        "vessel_name": vessel["Vessel name"],
        "rss": vessel["Registry of Shipping and Seamen number"],
        "home_port": vessel["Home port"],
        "administrative_port": vessel["Administrative port"],
        "overall_length": vessel["Overall length"],
        "licence_category": vessel["Licence Category"]
    }
 
 
@mcp.tool()
def search_vessels_by_name(search_term: str) -> dict:
    """
    Search for vessels using a partial vessel name.
    """
 
    results = df[
        df["Vessel name"]
        .astype(str)
        .str.upper()
        .str.contains(search_term.strip().upper(), na=False)
    ]
 
    if results.empty:
        return {
            "found": False,
            "count": 0,
            "matches": []
        }
 
    matches = []
 
    for _, vessel in results.head(20).iterrows():
        matches.append({
            "vessel_name": vessel["Vessel name"],
            "rss": vessel["Registry of Shipping and Seamen number"],
            "home_port": vessel["Home port"]
        })
 
    return {
        "found": True,
        "count": len(matches),
        "matches": matches
    }
 
 
@mcp.tool()
def validate_rss(rss: str) -> dict:
    """
    Validate that an RSS exists and return the vessel name.
    Useful when callers provide an RSS before the vessel name.
    """
 
    result = find_vessel_by_rss(rss)
 
    if result["found"\]:
        return {
            "valid": True,
            "vessel_name": result["vessel_name"],
            "message": (
                f"RSS found. Please confirm the vessel name "
                f"'{result['vessel_name']}' with the caller."
            )
        }
 
    return {
        "valid": False,
        "message": (
            "RSS not found. Ask the caller for the vessel name "
            "and continue the conversation."
        )
    }
 
 
if __name__ == "__main__":
    mcp.run()