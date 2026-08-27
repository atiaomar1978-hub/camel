#!/usr/bin/env python3
"""Generate electricity utility Camel integration draw.io diagram."""

OUTPUTS = [
    ("①", "ISO/RTO Market", "ftp + sftp", "Day-ahead bids", "#BBDEFB", "#1565C0"),
    ("②", "FERC / State PUC", "sftp", "Compliance filings", "#BBDEFB", "#1565C0"),
    ("④", "Payment Gateway", "http", "Card / ACH charges", "#BBDEFB", "#1565C0"),
    ("⑤", "Credit Bureau", "http", "Credit check requests", "#BBDEFB", "#1565C0"),
    ("⑪", "SMS Gateway", "smpp", "Outage alerts", "#90CAF9", "#0D47A1"),
    ("⑫", "Email / Billing", "mail", "Statements & e-bills", "#90CAF9", "#0D47A1"),
    ("⑲", "DMS / EMS", "jms", "Switch orders", "#FFE082", "#F57C00"),
    ("⑳", "OMS", "amqp", "Outage tickets", "#FFE082", "#F57C00"),
    ("㉑", "ADMS / GIS", "http", "Crew routing", "#FFE082", "#F57C00"),
    ("㉔", "MDM", "kafka", "Validated reads", "#FFE082", "#F57C00"),
    ("㉕", "Control Room", "slack", "Critical alerts", "#FFE082", "#F57C00"),
    ("㉖", "CIS / Billing", "jdbc", "Billing updates", "#BBDEFB", "#1565C0"),
    ("㉗", "SAP ERP", "cxf-soap", "Finance / GL", "#BBDEFB", "#1565C0"),
    ("㉘", "Salesforce CRM", "salesforce", "Customer 360", "#BBDEFB", "#1565C0"),
    ("㉙", "ServiceNow", "servicenow", "Field crew orders", "#BBDEFB", "#1565C0"),
]

INPUTS = [
    ("③", "Weather API", "http", "Load forecast", "#A5D6A7", "#2E7D32"),
    ("⑥", "DER / Solar", "rest + kafka", "Net metering", "#A5D6A7", "#2E7D32"),
    ("⑦", "EV Charging", "rest", "V2G telemetry", "#A5D6A7", "#2E7D32"),
    ("⑧", "Adjacent Utility", "file + amqp", "Mutual aid", "#A5D6A7", "#2E7D32"),
    ("⑨", "Customer Portal", "platform-http", "Self-service API", "#81C784", "#1B5E20"),
    ("⑩", "Mobile App", "rest", "Outage map / pay", "#81C784", "#1B5E20"),
    ("⑬", "Webhook partners", "webhook", "Stripe / Gov", "#81C784", "#1B5E20"),
    ("⑭", "Wholesale trader", "kafka", "Price signals", "#A5D6A7", "#2E7D32"),
    ("⑮", "Cloud SaaS", "aws2-sqs", "Event ingest", "#A5D6A7", "#2E7D32"),
    ("⑯", "AMI Head-End", "paho-mqtt5", "Smart meter reads", "#FFECB3", "#FF8F00"),
    ("⑰", "Grid IoT", "coap", "Voltage / temp", "#FFECB3", "#FF8F00"),
    ("⑱", "SCADA / RTU", "cxf-soap", "Grid events", "#FFECB3", "#FF8F00"),
    ("㉒", "Protection Relays", "timer + file", "Fault logs", "#FFECB3", "#FF8F00"),
    ("㉓", "Substation HMI", "platform-http", "Local API", "#FFECB3", "#FF8F00"),
    ("㉝", "CIS Change Data", "debezium", "Real-time CDC", "#A5D6A7", "#2E7D32"),
]

BOX_W = 240
BOX_H = 68
GAP = 14
START_Y = 140

LEFT_X = 40
LEFT_ZONE_W = 320
CENTER_X = 400
CENTER_W = 440
RIGHT_X = 880
RIGHT_ZONE_W = 320
PAGE_W = 1240
PAGE_H = START_Y + 15 * (BOX_H + GAP) + 200

cells = []
edges = []
cid = 2


def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def rect(cid_val, label, x, y, w, h, fill, stroke, stroke_w=1, style_extra=""):
    return f'''        <mxCell id="{cid_val}" value="{esc(label)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={stroke_w};fontSize=10;fontStyle=1;align=center;verticalAlign=middle;{style_extra}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def text(cid_val, label, x, y, w, h, size=12, color="#37474F", bold=False):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid_val}" value="{esc(label)}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize={size};fontStyle={fw};fontColor={color};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def edge(eid, src, tgt, color, width=1, dashed=False):
    dash = "dashed=1;dashPattern=4 4;" if dashed else ""
    return f'''        <mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth={width};endArrow=classic;endFill=1;{dash}" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>'''

# Title
cells.append(text("title", "Electricity Utility — Apache Camel Integration Architecture", 20, 20, PAGE_W - 40, 36, 20, "#1B3A4B", True))
cells.append(text("subtitle", "30 touch points  |  INPUT (right)  →  APACHE CAMEL (center)  →  OUTPUT (left)", 20, 56, PAGE_W - 40, 24, 12, "#546E7A"))

# Zone backgrounds
cells.append(rect("zone-out-bg", "", LEFT_X, 100, LEFT_ZONE_W, PAGE_H - 320, "#E3F2FD", "#1565C0", 2))
cells.append(rect("zone-camel-bg", "", CENTER_X, 100, CENTER_W, PAGE_H - 320, "#FFF3E0", "#E65100", 4))
cells.append(rect("zone-in-bg", "", RIGHT_X, 100, RIGHT_ZONE_W, PAGE_H - 320, "#E8F5E9", "#2E7D32", 2))

cells.append(text("lbl-out", "◀ OUTPUT", LEFT_X + 10, 108, LEFT_ZONE_W - 20, 22, 13, "#0D47A1", True))
cells.append(text("lbl-camel", "APACHE CAMEL", CENTER_X + 10, 108, CENTER_W - 20, 22, 14, "#BF360C", True))
cells.append(text("lbl-in", "INPUT ▶", RIGHT_X + 10, 108, RIGHT_ZONE_W - 20, 22, 13, "#1B5E20", True))

# Egress / ingress buses
OUT_BUS_X = LEFT_X + LEFT_ZONE_W - 30
IN_BUS_X = RIGHT_X + 10
bus_top = START_Y
bus_h = 15 * (BOX_H + GAP) - GAP

cells.append(rect("out-bus", "EGRESS", OUT_BUS_X, bus_top, 16, bus_h, "#1565C0", "#0D47A1", 2))
cells.append(rect("in-bus", "INGRESS", IN_BUS_X, bus_top, 16, bus_h, "#2E7D32", "#1B5E20", 2))

# Output boxes (left)
out_ids = []
for i, (num, name, comp, desc, fill, stroke) in enumerate(OUTPUTS):
    y = START_Y + i * (BOX_H + GAP)
    bid = f"out{i+1}"
    out_ids.append(bid)
    label = f"{num} {name}&#xa;{comp}&#xa;{desc}"
    cells.append(rect(bid, label, LEFT_X + 15, y, BOX_W - 30, BOX_H, fill, stroke))

# Input boxes (right)
in_ids = []
for i, (num, name, comp, desc, fill, stroke) in enumerate(INPUTS):
    y = START_Y + i * (BOX_H + GAP)
    bid = f"in{i+1}"
    in_ids.append(bid)
    label = f"{num} {name}&#xa;{comp}&#xa;{desc}"
    cells.append(rect(bid, label, RIGHT_X + 40, y, BOX_W - 30, BOX_H, fill, stroke))

# Camel center components
cy = START_Y + 20
cells.append(rect("camel-core", "CamelContext&#xa;Integration Runtime&#xa;Spring Boot / K8s", CENTER_X + 120, cy, 200, 90, "#FFCC80", "#E65100", 3))
cells.append(rect("camel-in-port", "INGRESS&#xa;Routes", CENTER_X + CENTER_W - 70, cy + 15, 55, 60, "#C8E6C9", "#2E7D32", 2))
cells.append(rect("camel-out-port", "EGRESS&#xa;Routes", CENTER_X + 15, cy + 15, 55, 60, "#BBDEFB", "#1565C0", 2))

cy2 = cy + 120
domains = [
    ("Meter-to-Cash", "mqtt → VEE → bill"),
    ("Grid Ops", "SCADA → OMS"),
    ("Market Ops", "forecast → ISO"),
    ("Customer", "portal → CRM"),
    ("Regulatory", "aggregate → sftp"),
    ("DER / EV", "enroll → credits"),
]
for j, (dname, dflow) in enumerate(domains):
    row, col = divmod(j, 3)
    dx = CENTER_X + 20 + col * 140
    dy = cy2 + row * 58
    cells.append(rect(f"dom{j}", f"{dname}&#xa;{dflow}", dx, dy, 130, 50, "#FFFFFF", "#EF6C00"))

cy3 = cy2 + 130
cells.append(rect("patterns", "Patterns: seda | idempotentConsumer | circuitBreaker | deadLetterChannel | throttle", CENTER_X + 15, cy3, CENTER_W - 30, 40, "#FFF8E1", "#F57C00"))
cells.append(rect("kafka", "kafka — Event Bus", CENTER_X + 15, cy3 + 50, 130, 40, "#CE93D8", "#6A1B9A", 2))
cells.append(rect("vault", "hashicorp-vault", CENTER_X + 155, cy3 + 50, 120, 40, "#FFCDD2", "#C62828"))
cells.append(rect("otel", "opentelemetry2", CENTER_X + 285, cy3 + 50, 120, 40, "#E8F5E9", "#2E7D32"))
cells.append(rect("stores", "mongodb | redis | elasticsearch", CENTER_X + 15, cy3 + 100, 200, 40, "#E1BEE7", "#6A1B9A"))
cells.append(rect("s3", "aws2-s3 data lake", CENTER_X + 225, cy3 + 100, 180, 40, "#E1BEE7", "#6A1B9A"))

# Main flow arrows
edges.append(edge("flow-in-bus", "in-bus", "camel-in-port", "#2E7D32", 4))
edges.append(edge("flow-in-core", "camel-in-port", "camel-core", "#2E7D32", 2))
edges.append(edge("flow-core-out", "camel-core", "camel-out-port", "#1565C0", 2))
edges.append(edge("flow-out-bus", "camel-out-port", "out-bus", "#1565C0", 4))

# Individual input → ingress bus
for i, iid in enumerate(in_ids):
    edges.append(edge(f"ei{i}", iid, "in-bus", "#66BB6A", 1))

# Egress bus → individual outputs
for i, oid in enumerate(out_ids):
    edges.append(edge(f"eo{i}", "out-bus", oid, "#42A5F5", 1))

# Footer
fy = PAGE_H - 90
cells.append(rect("footer-box", "", 40, fy, PAGE_W - 80, 70, "#FAFAFA", "#CFD8DC"))
cells.append(text("footer-t", "30 Touch Points — Inputs: ③⑥⑦⑧⑨⑩⑬⑭⑮⑯⑰⑱㉒㉓㉝  |  Outputs: ①②④⑤⑪⑫⑲⑳㉑㉔㉕㉖㉗㉘㉙", 50, fy + 8, PAGE_W - 100, 20, 11, "#37474F", True))
cells.append(text("footer-d", "Generated for electricity utility reference architecture — open with https://app.diagrams.net", 50, fy + 32, PAGE_W - 100, 20, 10, "#78909C"))

xml = f'''<mxfile host="app.diagrams.net" modified="2026-08-27T23:15:00.000Z" agent="Cursor" version="24.7.0" type="device">
  <diagram id="utility-camel-v3" name="Electricity Utility Camel Integration">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{chr(10).join(cells)}
{chr(10).join(edges)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

out_path = "/workspace/utility/electricity-company-camel-integration-architecture.drawio"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Written: {out_path} ({len(xml)} bytes)")
