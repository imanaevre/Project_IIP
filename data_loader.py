import xml.etree.ElementTree as ET
import pandas as pd

XML_FILE = "data.xml"

STEP_TYPE = "HKQuantityTypeIdentifierStepCount"

rows = []

for event, elem in ET.iterparse(XML_FILE, events=("end",)):
    if elem.tag == "Record":
        if elem.attrib.get("type") == STEP_TYPE:
            rows.append({
                "startDate": elem.attrib.get("startDate"),
                "endDate": elem.attrib.get("endDate"),
                "steps": int(float(elem.attrib.get("value"))),
                "sourceName": elem.attrib.get("sourceName"),
            })
        elem.clear()

df = pd.DataFrame(rows)

df["startDate"] = pd.to_datetime(df["startDate"], errors="coerce")
df["date"] = df["startDate"].dt.date

daily_steps = df.groupby("date", as_index=False)["steps"].sum()

daily_steps.to_csv("daily_steps.csv", index=False)

print(daily_steps)
