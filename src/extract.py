
import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase, RoutingControl

load_dotenv()

URI = os.environ["NEO4J_URI"]
USER = os.environ["NEO4J_USER"]
PASSWORD = os.environ["NEO4J_PASSWORD"]
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# Extract 1,000 CVE nodes and their vulnerability details
QUERY = """
MATCH (c:UcoCVE)
WHERE c.label IS NOT NULL
WITH c
LIMIT $limit

OPTIONAL MATCH
    (c)-[:UCOHASCVE_ID]-(v:UcoVulnerability)

WITH c, head(collect(v)) AS v

RETURN
    c.label AS cve_id,
    c.ucobaseSeverity AS severity,
    c.ucovectorString AS cvss_vector,
    c.ucovulnStatus AS status,
    c.uri AS uri,
    v.ucosummary AS description,
    toString(v.ucopublishedDateTime) AS published_date,
    toString(v.ucolastModifiedDateTime) AS modified_date
"""

with GraphDatabase.driver(
    URI, auth=(USER, PASSWORD)
) as driver:
    driver.verify_connectivity()
    print("Connected to Neo4j!")

    records, _, _ = driver.execute_query(
        QUERY,
        limit=1000,
        database_=DATABASE,
        routing_=RoutingControl.READ
    )

df = pd.DataFrame([r.data() for r in records])

# Save raw extraction
os.makedirs("data/raw", exist_ok=True)
df.to_parquet(
    "data/raw/cve_sample.parquet",
    index=False
)

print(f"Extracted {len(df)} vulnerabilities")
print(df.head())
print("\nSeverity distribution:")
print(df["severity"].fillna("").value_counts(dropna=False))
print("\nMissing descriptions:", df["description"].isna().sum())
