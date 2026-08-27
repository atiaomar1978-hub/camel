#!/usr/bin/env python3
"""Generate electricity utility Camel integration draw.io diagram (v5 — paired rows)."""

# Each flow: input touch point → ingress route → egress route → output touch point
# Protocol labels appear on every connecting line.
INTEGRATION_FLOWS = [
    {
        "flow": "Meter-to-MDM",
        "in_num": "⑯", "in_name": "AMI Head-End", "in_proto": "paho-mqtt5", "in_desc": "Smart meter reads",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "paho-mqtt5", "ingress_route": "route-ami-ingest",
        "egress_proto": "kafka", "egress_route": "route-mdm-out",
        "out_num": "㉔", "out_name": "MDM", "out_proto": "kafka", "out_desc": "Validated reads",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "Oracle CDC-to-Billing",
        "in_num": "㉝", "in_name": "Oracle CIS Change Data", "in_proto": "debezium-oracle", "in_desc": "Real-time CDC",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "debezium-oracle", "ingress_route": "route-oracle-cdc",
        "egress_proto": "jdbc", "egress_route": "route-oracle-cis-out",
        "out_num": "㉖", "out_name": "Oracle CIS Database", "out_proto": "jdbc", "out_desc": "Billing updates",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "Billing-Cycle-SP",
        "in_num": "㉒", "in_name": "Protection Relays", "in_proto": "timer", "in_desc": "Scheduled poll",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "timer", "ingress_route": "route-relay-poll",
        "egress_proto": "sql", "egress_route": "route-oracle-sp",
        "out_num": "㉖", "out_name": "Oracle CIS Database", "out_proto": "sql", "out_desc": "Stored procedures",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "Portal-to-CRM",
        "in_num": "⑨", "in_name": "Customer Portal", "in_proto": "platform-http", "in_desc": "Self-service API",
        "in_fill": "#81C784", "in_stroke": "#1B5E20",
        "ingress_proto": "platform-http", "ingress_route": "route-portal-in",
        "egress_proto": "salesforce", "egress_route": "route-crm-out",
        "out_num": "㉘", "out_name": "Salesforce CRM", "out_proto": "salesforce", "out_desc": "Customer 360",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "Mobile-to-Payment",
        "in_num": "⑩", "in_name": "Mobile App", "in_proto": "rest", "in_desc": "Outage map / pay",
        "in_fill": "#81C784", "in_stroke": "#1B5E20",
        "ingress_proto": "rest", "ingress_route": "route-mobile-in",
        "egress_proto": "http", "egress_route": "route-payment-out",
        "out_num": "④", "out_name": "Payment Gateway", "out_proto": "http", "out_desc": "Card / ACH",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "SCADA-to-OMS",
        "in_num": "⑱", "in_name": "SCADA / RTU", "in_proto": "cxf-soap", "in_desc": "Grid events",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "cxf-soap", "ingress_route": "route-scada-in",
        "egress_proto": "amqp", "egress_route": "route-oms-out",
        "out_num": "⑳", "out_name": "OMS", "out_proto": "amqp", "out_desc": "Outage tickets",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "HMI-to-DMS",
        "in_num": "㉓", "in_name": "Substation HMI", "in_proto": "platform-http", "in_desc": "Local API",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "platform-http", "ingress_route": "route-hmi-in",
        "egress_proto": "jms", "egress_route": "route-dms-out",
        "out_num": "⑲", "out_name": "DMS / EMS", "out_proto": "jms", "out_desc": "Switch orders",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "Weather-to-ISO",
        "in_num": "③", "in_name": "Weather API", "in_proto": "http", "in_desc": "Load forecast",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "http", "ingress_route": "route-weather-in",
        "egress_proto": "ftp", "egress_route": "route-iso-bid",
        "out_num": "①", "out_name": "ISO/RTO Market", "out_proto": "ftp", "out_desc": "Day-ahead bids",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "DER-to-Oracle",
        "in_num": "⑥", "in_name": "DER / Solar farms", "in_proto": "rest", "in_desc": "Net metering",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "rest", "ingress_route": "route-der-in",
        "egress_proto": "jdbc", "egress_route": "route-oracle-cis-out",
        "out_num": "㉖", "out_name": "Oracle CIS Database", "out_proto": "jdbc", "out_desc": "Rate credits",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "EV-to-MDM",
        "in_num": "⑦", "in_name": "EV Charging Network", "in_proto": "rest", "in_desc": "V2G telemetry",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "rest", "ingress_route": "route-ev-in",
        "egress_proto": "kafka", "egress_route": "route-mdm-out",
        "out_num": "㉔", "out_name": "MDM", "out_proto": "kafka", "out_desc": "Validated reads",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "Webhook-to-Credit",
        "in_num": "⑬", "in_name": "Webhook partners", "in_proto": "webhook", "in_desc": "Stripe / Gov",
        "in_fill": "#81C784", "in_stroke": "#1B5E20",
        "ingress_proto": "webhook", "ingress_route": "route-webhook-in",
        "egress_proto": "http", "egress_route": "route-credit-out",
        "out_num": "⑤", "out_name": "Credit Bureau", "out_proto": "http", "out_desc": "Credit check",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "Prices-to-ISO",
        "in_num": "⑭", "in_name": "Wholesale trader", "in_proto": "kafka", "in_desc": "Price signals",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "kafka", "ingress_route": "route-price-in",
        "egress_proto": "sftp", "egress_route": "route-iso-settle",
        "out_num": "①", "out_name": "ISO/RTO Market", "out_proto": "sftp", "out_desc": "Settlement files",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "SaaS-to-ITSM",
        "in_num": "⑮", "in_name": "Cloud SaaS", "in_proto": "aws2-sqs", "in_desc": "Event ingest",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "aws2-sqs", "ingress_route": "route-saas-in",
        "egress_proto": "servicenow", "egress_route": "route-itsm-out",
        "out_num": "㉙", "out_name": "ServiceNow", "out_proto": "servicenow", "out_desc": "Work orders",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "IoT-to-GIS",
        "in_num": "⑰", "in_name": "Grid IoT Sensors", "in_proto": "coap", "in_desc": "Voltage / temp",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "coap", "ingress_route": "route-iot-ingest",
        "egress_proto": "http", "egress_route": "route-gis-out",
        "out_num": "㉑", "out_name": "ADMS / GIS", "out_proto": "http", "out_desc": "Crew routing",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "Relays-to-Control",
        "in_num": "㉒", "in_name": "Protection Relays", "in_proto": "file", "in_desc": "Fault logs",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "file", "ingress_route": "route-relay-in",
        "egress_proto": "slack", "egress_route": "route-control-out",
        "out_num": "㉕", "out_name": "Control Room", "out_proto": "slack", "out_desc": "Critical alerts",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "MutualAid-to-DMS",
        "in_num": "⑧", "in_name": "Adjacent Utility", "in_proto": "amqp", "in_desc": "Mutual aid",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "amqp", "ingress_route": "route-mutualaid-in",
        "egress_proto": "jms", "egress_route": "route-dms-out",
        "out_num": "⑲", "out_name": "DMS / EMS", "out_proto": "jms", "out_desc": "Switch orders",
        "out_fill": "#FFE082", "out_stroke": "#F57C00",
    },
    {
        "flow": "CDC-to-SMS",
        "in_num": "㉝", "in_name": "Oracle CIS Change Data", "in_proto": "debezium-oracle", "in_desc": "Outage trigger",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "debezium-oracle", "ingress_route": "route-oracle-cdc",
        "egress_proto": "smpp", "egress_route": "route-sms-out",
        "out_num": "⑪", "out_name": "SMS Gateway", "out_proto": "smpp", "out_desc": "Outage alerts",
        "out_fill": "#90CAF9", "out_stroke": "#0D47A1",
    },
    {
        "flow": "Billing-to-Email",
        "in_num": "㉒", "in_name": "Protection Relays", "in_proto": "timer", "in_desc": "Monthly trigger",
        "in_fill": "#FFECB3", "in_stroke": "#FF8F00",
        "ingress_proto": "timer", "ingress_route": "route-relay-poll",
        "egress_proto": "mail", "egress_route": "route-bill-email",
        "out_num": "⑫", "out_name": "Email / Billing", "out_proto": "mail", "out_desc": "E-bills",
        "out_fill": "#90CAF9", "out_stroke": "#0D47A1",
    },
    {
        "flow": "Aggregate-to-FERC",
        "in_num": "⑧", "in_name": "Adjacent Utility", "in_proto": "file", "in_desc": "Compliance data",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "file", "ingress_route": "route-mutualaid-in",
        "egress_proto": "sftp", "egress_route": "route-ferc-file",
        "out_num": "②", "out_name": "FERC / State PUC", "out_proto": "sftp", "out_desc": "Compliance filing",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
    {
        "flow": "Billing-to-SAP",
        "in_num": "㉝", "in_name": "Oracle CIS Change Data", "in_proto": "debezium-oracle", "in_desc": "GL events",
        "in_fill": "#A5D6A7", "in_stroke": "#2E7D32",
        "ingress_proto": "debezium-oracle", "ingress_route": "route-oracle-cdc",
        "egress_proto": "cxf-soap", "egress_route": "route-sap-out",
        "out_num": "㉗", "out_name": "SAP ERP", "out_proto": "cxf-soap", "out_desc": "Finance / GL",
        "out_fill": "#BBDEFB", "out_stroke": "#1565C0",
    },
]

# Layout constants — flow goes RIGHT (input) → LEFT (output)
COL_OUT_X = 40
COL_EGR_X = 260
COL_CAM_X = 450
COL_ING_X = 570
COL_IN_X = 750

W_OUT = 200
W_ROUTE = 160
W_CAM = 100
W_IN = 200

ROW_H = 58
ROW_GAP = 14
START_Y = 130
PAGE_W = 980
PAGE_H = START_Y + len(INTEGRATION_FLOWS) * (ROW_H + ROW_GAP) + 120

cells = []
edge_cells = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def rect(cid, label, x, y, w, h, fill, stroke, sw=1, fs=9, bold=True):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid}" value="{esc(label)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={sw};fontSize={fs};fontStyle={fw};align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def text(cid, label, x, y, w, h, size=12, color="#37474F", bold=False, align="center"):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid}" value="{esc(label)}" style="text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;fontSize={size};fontStyle={fw};fontColor={color};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def edge_labeled(eid, src, tgt, proto, color, width=2):
    """Edge with protocol label on the connecting line."""
    return f'''        <mxCell id="{eid}" value="" style="edgeStyle=none;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth={width};endArrow=classic;endFill=1;" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="{eid}-lbl" value="{esc(proto)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=9;fontStyle=1;fontColor={color};labelBackgroundColor=#FFFFFF;" vertex="1" connectable="0" parent="{eid}">
          <mxGeometry x="-0.1" relative="1" as="geometry"><mxPoint y="-10" as="offset"/></mxGeometry>
        </mxCell>'''


# Title & column headers
cells.append(text("title", "Electricity Utility — Apache Camel Paired Integration Flows", 20, 12, PAGE_W - 40, 32, 18, "#1B3A4B", True))
cells.append(text("subtitle", "Each row: INPUT → Ingress Route ↔ Egress Route → OUTPUT  |  Protocol on every connecting line", 20, 42, PAGE_W - 40, 20, 11, "#546E7A"))
cells.append(text("h-out", "◀ OUTPUT", COL_OUT_X, 95, W_OUT, 18, 11, "#1565C0", True))
cells.append(text("h-egr", "EGRESS ROUTE", COL_EGR_X, 95, W_ROUTE, 18, 10, "#1565C0", True))
cells.append(text("h-cam", "CAMEL", COL_CAM_X, 95, W_CAM, 18, 11, "#E65100", True))
cells.append(text("h-ing", "INGRESS ROUTE", COL_ING_X, 95, W_ROUTE, 18, 10, "#2E7D32", True))
cells.append(text("h-in", "INPUT ▶", COL_IN_X, 95, W_IN, 18, 11, "#2E7D32", True))

# Central Camel hub background (spine)
hub_h = len(INTEGRATION_FLOWS) * (ROW_H + ROW_GAP) - ROW_GAP
cells.append(rect("camel-spine", "Apache Camel&#xa;Integration&#xa;Middleware", COL_CAM_X, START_Y, W_CAM, hub_h, "#FFE0B2", "#E65100", 3, 10))

for i, f in enumerate(INTEGRATION_FLOWS):
    y = START_Y + i * (ROW_H + ROW_GAP)
    prefix = f"r{i}"

    out_label = f"{f['out_num']} {f['out_name']}&#xa;Protocol: {f['out_proto']}&#xa;{f['out_desc']}"
    egr_label = f"EGRESS&#xa;Protocol: {f['egress_proto']}&#xa;{f['egress_route']}"
    cam_label = f["flow"]
    ing_label = f"INGRESS&#xa;Protocol: {f['ingress_proto']}&#xa;{f['ingress_route']}"
    in_label = f"{f['in_num']} {f['in_name']}&#xa;Protocol: {f['in_proto']}&#xa;{f['in_desc']}"

    out_id = f"{prefix}-out"
    egr_id = f"{prefix}-egr"
    cam_id = f"{prefix}-cam"
    ing_id = f"{prefix}-ing"
    in_id = f"{prefix}-in"

    cells.append(rect(out_id, out_label, COL_OUT_X, y, W_OUT, ROW_H, f["out_fill"], f["out_stroke"]))
    cells.append(rect(egr_id, egr_label, COL_EGR_X, y, W_ROUTE, ROW_H, "#E3F2FD", "#1565C0"))
    cells.append(rect(cam_id, cam_label, COL_CAM_X + 8, y + 8, W_CAM - 16, ROW_H - 16, "#FFCC80", "#E65100", 2, 8))
    cells.append(rect(ing_id, ing_label, COL_ING_X, y, W_ROUTE, ROW_H, "#E8F5E9", "#2E7D32"))
    cells.append(rect(in_id, in_label, COL_IN_X, y, W_IN, ROW_H, f["in_fill"], f["in_stroke"]))

    # Connections RIGHT → LEFT with protocol labels on each line
    # Input → Ingress (ingress protocol)
    edge_cells.append(edge_labeled(f"{prefix}-e1", in_id, ing_id, f["ingress_proto"], "#2E7D32", 2))
    # Ingress → Camel (ingress protocol)
    edge_cells.append(edge_labeled(f"{prefix}-e2", ing_id, cam_id, f["ingress_proto"], "#43A047", 2))
    # Camel → Egress (egress protocol)
    edge_cells.append(edge_labeled(f"{prefix}-e3", cam_id, egr_id, f["egress_proto"], "#1E88E5", 2))
    # Egress → Output (egress protocol)
    edge_cells.append(edge_labeled(f"{prefix}-e4", egr_id, out_id, f["egress_proto"], "#1565C0", 2))

# Footer
fy = START_Y + hub_h + 20
cells.append(rect("footer", "", 30, fy, PAGE_W - 60, 55, "#FAFAFA", "#CFD8DC"))
cells.append(text("footer-t", f"{len(INTEGRATION_FLOWS)} paired integration flows  |  Ingress ↔ Egress routes face each other per touch point  |  Oracle: jdbc, sql, debezium-oracle", 40, fy + 6, PAGE_W - 80, 18, 10, "#37474F", True, "left"))
cells.append(text("footer-d", "Open: https://app.diagrams.net  |  GitHub: utility/electricity-company-camel-integration-architecture.drawio", 40, fy + 28, PAGE_W - 80, 18, 9, "#78909C", False, "left"))

xml = f'''<mxfile host="app.diagrams.net" modified="2026-08-27T23:35:00.000Z" agent="Cursor" version="24.7.0" type="device">
  <diagram id="utility-camel-v5" name="Electricity Utility Camel Paired Flows">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{chr(10).join(cells)}
{chr(10).join(edge_cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

out_path = "/workspace/utility/electricity-company-camel-integration-architecture.drawio"
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(xml)
print(f"Written: {out_path} ({len(INTEGRATION_FLOWS)} paired flows, {len(xml)} bytes)")
