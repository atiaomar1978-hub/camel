#!/usr/bin/env python3
"""Generate electricity utility Camel integration draw.io diagram (v4)."""

# (id, system name, [protocols], description, fill, stroke)
OUTPUTS = [
    ("①", "ISO/RTO Market", ["ftp", "sftp"], "Day-ahead bids", "#BBDEFB", "#1565C0"),
    ("②", "FERC / State PUC", ["sftp"], "Compliance filings", "#BBDEFB", "#1565C0"),
    ("④", "Payment Gateway", ["http"], "Card / ACH charges", "#BBDEFB", "#1565C0"),
    ("⑤", "Credit Bureau", ["http"], "Credit check requests", "#BBDEFB", "#1565C0"),
    ("⑪", "SMS Gateway", ["smpp"], "Outage alerts", "#90CAF9", "#0D47A1"),
    ("⑫", "Email / Billing", ["mail"], "Statements & e-bills", "#90CAF9", "#0D47A1"),
    ("⑲", "DMS / EMS", ["jms"], "Switch orders", "#FFE082", "#F57C00"),
    ("⑳", "OMS", ["amqp"], "Outage tickets", "#FFE082", "#F57C00"),
    ("㉑", "ADMS / GIS", ["http"], "Crew routing", "#FFE082", "#F57C00"),
    ("㉔", "MDM", ["kafka"], "Validated reads publish", "#FFE082", "#F57C00"),
    ("㉕", "Control Room", ["slack"], "Critical alerts", "#FFE082", "#F57C00"),
    ("㉖", "CIS / Billing", ["jdbc"], "Billing updates", "#BBDEFB", "#1565C0"),
    ("㉗", "SAP ERP", ["cxf-soap"], "Finance / GL posting", "#BBDEFB", "#1565C0"),
    ("㉘", "Salesforce CRM", ["salesforce"], "Customer 360 sync", "#BBDEFB", "#1565C0"),
    ("㉙", "ServiceNow", ["servicenow"], "Field crew work orders", "#BBDEFB", "#1565C0"),
]

INPUTS = [
    ("③", "Weather API", ["http"], "Load forecast data", "#A5D6A7", "#2E7D32"),
    ("⑥", "DER / Solar farms", ["rest", "kafka"], "Net metering telemetry", "#A5D6A7", "#2E7D32"),
    ("⑦", "EV Charging Network", ["rest"], "V2G telemetry", "#A5D6A7", "#2E7D32"),
    ("⑧", "Adjacent Utility", ["file", "amqp"], "Mutual aid requests", "#A5D6A7", "#2E7D32"),
    ("⑨", "Customer Portal", ["platform-http"], "Self-service API", "#81C784", "#1B5E20"),
    ("⑩", "Mobile App", ["rest"], "Outage map / payments", "#81C784", "#1B5E20"),
    ("⑬", "Webhook partners", ["webhook"], "Stripe / Gov events", "#81C784", "#1B5E20"),
    ("⑭", "Wholesale trader", ["kafka"], "Price signals", "#A5D6A7", "#2E7D32"),
    ("⑮", "Cloud SaaS", ["aws2-sqs"], "Event ingest", "#A5D6A7", "#2E7D32"),
    ("⑯", "AMI Head-End", ["paho-mqtt5"], "Smart meter reads", "#FFECB3", "#FF8F00"),
    ("⑰", "Grid IoT Sensors", ["coap"], "Voltage / temperature", "#FFECB3", "#FF8F00"),
    ("⑱", "SCADA / RTU", ["cxf-soap"], "Legacy grid events", "#FFECB3", "#FF8F00"),
    ("㉒", "Protection Relays", ["timer", "file"], "Fault event logs", "#FFECB3", "#FF8F00"),
    ("㉓", "Substation HMI", ["platform-http"], "Local substation API", "#FFECB3", "#FF8F00"),
    ("㉝", "CIS Change Data", ["debezium-postgres"], "Real-time CDC events", "#A5D6A7", "#2E7D32"),
]

# Camel hub routes — one touch point per protocol (direction, protocol, route purpose)
CAMEL_INGRESS_ROUTES = [
    ("paho-mqtt5", "route-ami-ingest", "AMI meter reads → VEE"),
    ("coap", "route-iot-ingest", "Grid sensor telemetry"),
    ("cxf-soap", "route-scada-in", "SCADA/RTU events (OT)"),
    ("platform-http", "route-portal-in", "Customer portal API"),
    ("platform-http", "route-hmi-in", "Substation HMI API"),
    ("rest", "route-mobile-in", "Mobile app requests"),
    ("rest", "route-der-in", "DER / solar enrollments"),
    ("rest", "route-ev-in", "EV charging telemetry"),
    ("http", "route-weather-in", "Weather forecast pull"),
    ("webhook", "route-webhook-in", "Partner webhook events"),
    ("kafka", "route-price-in", "Wholesale price signals"),
    ("aws2-sqs", "route-saas-in", "Cloud SaaS events"),
    ("file", "route-relay-in", "Protection relay logs"),
    ("file", "route-mutualaid-in", "Adjacent utility files"),
    ("amqp", "route-mutualaid-in", "Mutual aid messages"),
    ("timer", "route-relay-poll", "Scheduled relay poll"),
    ("debezium-postgres", "route-cis-cdc", "CIS change-data-capture"),
]

CAMEL_EGRESS_ROUTES = [
    ("ftp", "route-iso-bid", "ISO day-ahead bid submit"),
    ("sftp", "route-iso-settle", "ISO settlement files"),
    ("sftp", "route-ferc-file", "Regulatory compliance filing"),
    ("http", "route-payment-out", "Payment gateway charge"),
    ("http", "route-credit-out", "Credit bureau inquiry"),
    ("http", "route-gis-out", "ADMS/GIS crew routing"),
    ("smpp", "route-sms-out", "Customer outage SMS"),
    ("mail", "route-bill-email", "E-bill / statement email"),
    ("jms", "route-dms-out", "DMS switch orders"),
    ("amqp", "route-oms-out", "OMS outage tickets"),
    ("kafka", "route-mdm-out", "MDM validated reads"),
    ("jdbc", "route-cis-out", "CIS billing update"),
    ("jdbc", "route-dwh-out", "Data warehouse load"),
    ("cxf-soap", "route-sap-out", "SAP ERP GL posting"),
    ("salesforce", "route-crm-out", "Salesforce Customer 360"),
    ("servicenow", "route-itsm-out", "ServiceNow work orders"),
    ("slack", "route-control-out", "Control room alerts"),
]

CAMEL_INTERNAL_ROUTES = [
    ("kafka", "route-event-bus", "Enterprise event backbone"),
    ("seda", "route-buffer", "Peak-load buffering"),
    ("mongodb", "route-outage-store", "Outage state store"),
    ("redis", "route-cache", "Session / lookup cache"),
    ("elasticsearch", "route-search", "Outage search index"),
    ("aws2-s3", "route-datalake", "Interval read archive"),
    ("hashicorp-vault", "route-secrets", "OT/IT credential lookup"),
    ("opentelemetry2", "route-traces", "Distributed tracing"),
    ("micrometer", "route-metrics", "Route metrics export"),
]

BOX_W = 250
GAP = 12
START_Y = 150
LEFT_X = 30
LEFT_ZONE_W = 340
CENTER_X = 390
CENTER_W = 900
RIGHT_X = 1310
RIGHT_ZONE_W = 340
PAGE_W = 1680

cells = []
edges = []


def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def box_height(protocol_count):
    """Base + one line per protocol + description."""
    return 34 + protocol_count * 16 + 18


def format_touchpoint(num, name, protocols, desc):
    lines = [f"{num} {name}"]
    for p in protocols:
        lines.append(f"Protocol: {p}")
    lines.append(desc)
    return "&#xa;".join(lines)


def rect(cid_val, label, x, y, w, h, fill, stroke, stroke_w=1, fontsize=10, bold=True):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid_val}" value="{esc(label)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={stroke_w};fontSize={fontsize};fontStyle={fw};align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def text(cid_val, label, x, y, w, h, size=12, color="#37474F", bold=False, align="center"):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid_val}" value="{esc(label)}" style="text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;fontSize={size};fontStyle={fw};fontColor={color};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def edge(eid, src, tgt, color, width=1, dashed=False):
    dash = "dashed=1;dashPattern=4 4;" if dashed else ""
    return f'''        <mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth={width};endArrow=classic;endFill=1;{dash}" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>'''

# Compute side column heights
out_heights = [box_height(len(p)) for _, _, p, _, _, _ in OUTPUTS]
in_heights = [box_height(len(p)) for _, _, p, _, _, _ in INPUTS]
side_content_h = sum(out_heights) + GAP * (len(OUTPUTS) - 1)
side_content_h = max(side_content_h, sum(in_heights) + GAP * (len(INPUTS) - 1))

# Camel routes section height
ROUTE_BOX_H = 44
ROUTE_GAP = 6
ROUTE_COLS = 2
ingress_rows = (len(CAMEL_INGRESS_ROUTES) + ROUTE_COLS - 1) // ROUTE_COLS
egress_rows = (len(CAMEL_EGRESS_ROUTES) + ROUTE_COLS - 1) // ROUTE_COLS
internal_rows = (len(CAMEL_INTERNAL_ROUTES) + 2) // 3
routes_section_h = 50 + ingress_rows * (ROUTE_BOX_H + ROUTE_GAP) + 40 + egress_rows * (ROUTE_BOX_H + ROUTE_GAP) + 40 + internal_rows * (ROUTE_BOX_H + ROUTE_GAP) + 30

zone_h = max(side_content_h + 60, routes_section_h + 280) + 80
PAGE_H = zone_h + 280

# Title
cells.append(text("title", "Electricity Utility — Apache Camel Integration Architecture", 20, 15, PAGE_W - 40, 34, 20, "#1B3A4B", True))
cells.append(text("subtitle", "Every protocol on its own line  |  INPUT (right) → APACHE CAMEL ROUTES (center) → OUTPUT (left)", 20, 48, PAGE_W - 40, 22, 12, "#546E7A"))

# Zone backgrounds
cells.append(rect("zone-out-bg", "", LEFT_X, 95, LEFT_ZONE_W, zone_h, "#E3F2FD", "#1565C0", 2))
cells.append(rect("zone-camel-bg", "", CENTER_X, 95, CENTER_W, zone_h, "#FFF3E0", "#E65100", 4))
cells.append(rect("zone-in-bg", "", RIGHT_X, 95, RIGHT_ZONE_W, zone_h, "#E8F5E9", "#2E7D32", 2))

cells.append(text("lbl-out", "◀ OUTPUT / EGRESS", LEFT_X + 10, 102, LEFT_ZONE_W - 20, 20, 13, "#0D47A1", True))
cells.append(text("lbl-camel", "APACHE CAMEL — INTEGRATION ROUTES", CENTER_X + 10, 102, CENTER_W - 20, 20, 14, "#BF360C", True))
cells.append(text("lbl-in", "INPUT / INGRESS ▶", RIGHT_X + 10, 102, RIGHT_ZONE_W - 20, 20, 13, "#1B5E20", True))

# Buses
OUT_BUS_X = LEFT_X + LEFT_ZONE_W - 28
IN_BUS_X = RIGHT_X + 12
cells.append(rect("out-bus", "EGRESS", OUT_BUS_X, START_Y, 14, side_content_h, "#1565C0", "#0D47A1", 2))
cells.append(rect("in-bus", "INGRESS", IN_BUS_X, START_Y, 14, side_content_h, "#2E7D32", "#1B5E20", 2))

# Output boxes
out_ids = []
y = START_Y
for i, (num, name, protocols, desc, fill, stroke) in enumerate(OUTPUTS):
    h = out_heights[i]
    bid = f"out{i+1}"
    out_ids.append(bid)
    label = format_touchpoint(num, name, protocols, desc)
    cells.append(rect(bid, label, LEFT_X + 14, y, BOX_W, h, fill, stroke, fontsize=9))
    y += h + GAP

# Input boxes
in_ids = []
y = START_Y
for i, (num, name, protocols, desc, fill, stroke) in enumerate(INPUTS):
    h = in_heights[i]
    bid = f"in{i+1}"
    in_ids.append(bid)
    label = format_touchpoint(num, name, protocols, desc)
    cells.append(rect(bid, label, RIGHT_X + 38, y, BOX_W, h, fill, stroke, fontsize=9))
    y += h + GAP

# Camel core + ports
cy = START_Y
cells.append(rect("camel-core", "CamelContext&#xa;Integration Runtime&#xa;Spring Boot / Kubernetes", CENTER_X + 310, cy, 280, 85, "#FFCC80", "#E65100", 3, 12))
cells.append(rect("camel-in-port", "INGRESS&#xa;Gateway", CENTER_X + CENTER_W - 72, cy + 12, 62, 62, "#C8E6C9", "#2E7D32", 2, 11))
cells.append(rect("camel-out-port", "EGRESS&#xa;Gateway", CENTER_X + 12, cy + 12, 62, 62, "#BBDEFB", "#1565C0", 2, 11))

# Enlarged routes section
ry = cy + 105
cells.append(rect("routes-panel", "", CENTER_X + 10, ry, CENTER_W - 20, routes_section_h, "#FFFFFF", "#EF6C00", 2))
cells.append(text("routes-title", "Apache Camel Routes — One Touch Point Per Protocol", CENTER_X + 20, ry + 8, CENTER_W - 40, 22, 13, "#BF360C", True))

# Ingress routes
iy = ry + 38
cells.append(text("ingress-lbl", "INGRESS ROUTES (from → Camel)", CENTER_X + 20, iy, 400, 18, 11, "#2E7D32", True, "left"))
iy += 22
route_w = (CENTER_W - 50) // 2
ingress_route_ids = []
for idx, (protocol, route_id, purpose) in enumerate(CAMEL_INGRESS_ROUTES):
    col = idx % ROUTE_COLS
    row = idx // ROUTE_COLS
    rx = CENTER_X + 20 + col * (route_w + 10)
    ry2 = iy + row * (ROUTE_BOX_H + ROUTE_GAP)
    rid = f"route-in-{idx}"
    ingress_route_ids.append(rid)
    label = f"Protocol: {protocol}&#xa;Route: {route_id}&#xa;{purpose}"
    cells.append(rect(rid, label, rx, ry2, route_w, ROUTE_BOX_H, "#E8F5E9", "#2E7D32", 1, 9))

iy += ingress_rows * (ROUTE_BOX_H + ROUTE_GAP) + 12

# Egress routes
cells.append(text("egress-lbl", "EGRESS ROUTES (Camel → to)", CENTER_X + 20, iy, 400, 18, 11, "#1565C0", True, "left"))
iy += 22
egress_route_ids = []
for idx, (protocol, route_id, purpose) in enumerate(CAMEL_EGRESS_ROUTES):
    col = idx % ROUTE_COLS
    row = idx // ROUTE_COLS
    rx = CENTER_X + 20 + col * (route_w + 10)
    ry2 = iy + row * (ROUTE_BOX_H + ROUTE_GAP)
    rid = f"route-out-{idx}"
    egress_route_ids.append(rid)
    label = f"Protocol: {protocol}&#xa;Route: {route_id}&#xa;{purpose}"
    cells.append(rect(rid, label, rx, ry2, route_w, ROUTE_BOX_H, "#E3F2FD", "#1565C0", 1, 9))

iy += egress_rows * (ROUTE_BOX_H + ROUTE_GAP) + 12

# Internal / platform routes
cells.append(text("internal-lbl", "PLATFORM & INTERNAL ROUTES", CENTER_X + 20, iy, 400, 18, 11, "#6A1B9A", True, "left"))
iy += 22
internal_w = (CENTER_W - 60) // 3
for idx, (protocol, route_id, purpose) in enumerate(CAMEL_INTERNAL_ROUTES):
    col = idx % 3
    row = idx // 3
    rx = CENTER_X + 20 + col * (internal_w + 10)
    ry2 = iy + row * (ROUTE_BOX_H + ROUTE_GAP)
    label = f"Protocol: {protocol}&#xa;Route: {route_id}&#xa;{purpose}"
    cells.append(rect(f"route-int-{idx}", label, rx, ry2, internal_w, ROUTE_BOX_H, "#F3E5F5", "#6A1B9A", 1, 9))

# Patterns bar below routes
py = ry + routes_section_h + 10
cells.append(rect("patterns", "EIP Patterns: idempotentConsumer | circuitBreaker | deadLetterChannel | throttle | content-based-router | wireTap", CENTER_X + 10, py, CENTER_W - 20, 36, "#FFF8E1", "#F57C00", 1, 9, False))

# Main flow
edges.append(edge("flow-in-bus", "in-bus", "camel-in-port", "#2E7D32", 4))
edges.append(edge("flow-in-core", "camel-in-port", "camel-core", "#2E7D32", 2))
edges.append(edge("flow-core-out", "camel-core", "camel-out-port", "#1565C0", 2))
edges.append(edge("flow-out-bus", "camel-out-port", "out-bus", "#1565C0", 4))

# Connect ingress routes to gateway (sample dashed links to avoid clutter - connect panel to gateway)
edges.append(edge("routes-to-in", "routes-panel", "camel-in-port", "#66BB6A", 1, dashed=True))
edges.append(edge("routes-to-out", "camel-out-port", "routes-panel", "#42A5F5", 1, dashed=True))

for i, iid in enumerate(in_ids):
    edges.append(edge(f"ei{i}", iid, "in-bus", "#66BB6A", 1))
for i, oid in enumerate(out_ids):
    edges.append(edge(f"eo{i}", "out-bus", oid, "#42A5F5", 1))

# Protocol count footer
all_protocols = set()
for _, _, ps, _, _, _ in OUTPUTS + INPUTS:
    all_protocols.update(ps)
for ps, _, _ in CAMEL_INGRESS_ROUTES + CAMEL_EGRESS_ROUTES + CAMEL_INTERNAL_ROUTES:
    all_protocols.add(ps)

fy = 95 + zone_h + 20
cells.append(rect("footer-box", "", 30, fy, PAGE_W - 60, 90, "#FAFAFA", "#CFD8DC"))
proto_list = ", ".join(sorted(all_protocols))
cells.append(text("footer-t", f"Unique Camel protocols: {len(all_protocols)} — {proto_list}", 45, fy + 8, PAGE_W - 90, 36, 10, "#37474F", True, "left"))
cells.append(text("footer-d", "Ingress routes: 17  |  Egress routes: 17  |  Platform routes: 9  |  Open: https://app.diagrams.net", 45, fy + 48, PAGE_W - 90, 20, 10, "#78909C", False, "left"))

xml = f'''<mxfile host="app.diagrams.net" modified="2026-08-27T23:25:00.000Z" agent="Cursor" version="24.7.0" type="device">
  <diagram id="utility-camel-v4" name="Electricity Utility Camel Integration">
    <mxGraphModel dx="1800" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H + 120}" math="0" shadow="0">
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
print(f"Written: {out_path} ({len(xml)} bytes, {len(all_protocols)} unique protocols)")
