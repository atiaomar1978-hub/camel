#!/usr/bin/env python3
"""Generate electricity utility Camel integration draw.io diagram (v6 — FROM→TO per line)."""

# One row per touch point: FROM (left) → Ingress → Camel → Egress → TO (right)
INTEGRATION_FLOWS = [
    {
        "name": "Meter-to-MDM",
        "from_num": "⑯", "from_name": "AMI Head-End", "from_proto": "paho-mqtt5",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "paho-mqtt5", "ingress_route": "route-ami-ingest",
        "egress_proto": "kafka", "egress_route": "route-mdm-out",
        "to_num": "㉔", "to_name": "MDM", "to_proto": "kafka",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "Oracle-CDC-to-Billing",
        "from_num": "㉝", "from_name": "Oracle CIS Change Data", "from_proto": "debezium-oracle",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "debezium-oracle", "ingress_route": "route-oracle-cdc",
        "egress_proto": "jdbc", "egress_route": "route-oracle-cis-out",
        "to_num": "㉖", "to_name": "Oracle CIS Database", "to_proto": "jdbc",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "Billing-Cycle-SP",
        "from_num": "㉒", "from_name": "Protection Relays", "from_proto": "timer",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "timer", "ingress_route": "route-relay-poll",
        "egress_proto": "sql", "egress_route": "route-oracle-sp",
        "to_num": "㉖", "to_name": "Oracle CIS Database", "to_proto": "sql",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "Portal-to-CRM",
        "from_num": "⑨", "from_name": "Customer Portal", "from_proto": "platform-http",
        "from_fill": "#81C784", "from_stroke": "#1B5E20",
        "ingress_proto": "platform-http", "ingress_route": "route-portal-in",
        "egress_proto": "salesforce", "egress_route": "route-crm-out",
        "to_num": "㉘", "to_name": "Salesforce CRM", "to_proto": "salesforce",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "Mobile-to-Payment",
        "from_num": "⑩", "from_name": "Mobile App", "from_proto": "rest",
        "from_fill": "#81C784", "from_stroke": "#1B5E20",
        "ingress_proto": "rest", "ingress_route": "route-mobile-in",
        "egress_proto": "http", "egress_route": "route-payment-out",
        "to_num": "④", "to_name": "Payment Gateway", "to_proto": "http",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "SCADA-to-OMS",
        "from_num": "⑱", "from_name": "SCADA / RTU", "from_proto": "cxf-soap",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "cxf-soap", "ingress_route": "route-scada-in",
        "egress_proto": "amqp", "egress_route": "route-oms-out",
        "to_num": "⑳", "to_name": "OMS", "to_proto": "amqp",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "HMI-to-DMS",
        "from_num": "㉓", "from_name": "Substation HMI", "from_proto": "platform-http",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "platform-http", "ingress_route": "route-hmi-in",
        "egress_proto": "jms", "egress_route": "route-dms-out",
        "to_num": "⑲", "to_name": "DMS / EMS", "to_proto": "jms",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "Weather-to-ISO",
        "from_num": "③", "from_name": "Weather API", "from_proto": "http",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "http", "ingress_route": "route-weather-in",
        "egress_proto": "ftp", "egress_route": "route-iso-bid",
        "to_num": "①", "to_name": "ISO/RTO Market", "to_proto": "ftp",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "DER-to-Oracle",
        "from_num": "⑥", "from_name": "DER / Solar farms", "from_proto": "rest",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "rest", "ingress_route": "route-der-in",
        "egress_proto": "jdbc", "egress_route": "route-oracle-cis-out",
        "to_num": "㉖", "to_name": "Oracle CIS Database", "to_proto": "jdbc",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "EV-to-MDM",
        "from_num": "⑦", "from_name": "EV Charging Network", "from_proto": "rest",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "rest", "ingress_route": "route-ev-in",
        "egress_proto": "kafka", "egress_route": "route-mdm-out",
        "to_num": "㉔", "to_name": "MDM", "to_proto": "kafka",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "Webhook-to-Credit",
        "from_num": "⑬", "from_name": "Webhook partners", "from_proto": "webhook",
        "from_fill": "#81C784", "from_stroke": "#1B5E20",
        "ingress_proto": "webhook", "ingress_route": "route-webhook-in",
        "egress_proto": "http", "egress_route": "route-credit-out",
        "to_num": "⑤", "to_name": "Credit Bureau", "to_proto": "http",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "Prices-to-ISO",
        "from_num": "⑭", "from_name": "Wholesale trader", "from_proto": "kafka",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "kafka", "ingress_route": "route-price-in",
        "egress_proto": "sftp", "egress_route": "route-iso-settle",
        "to_num": "①", "to_name": "ISO/RTO Market", "to_proto": "sftp",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "SaaS-to-ITSM",
        "from_num": "⑮", "from_name": "Cloud SaaS", "from_proto": "aws2-sqs",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "aws2-sqs", "ingress_route": "route-saas-in",
        "egress_proto": "servicenow", "egress_route": "route-itsm-out",
        "to_num": "㉙", "to_name": "ServiceNow", "to_proto": "servicenow",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "IoT-to-GIS",
        "from_num": "⑰", "from_name": "Grid IoT Sensors", "from_proto": "coap",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "coap", "ingress_route": "route-iot-ingest",
        "egress_proto": "http", "egress_route": "route-gis-out",
        "to_num": "㉑", "to_name": "ADMS / GIS", "to_proto": "http",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "Relays-to-Control",
        "from_num": "㉒", "from_name": "Protection Relays", "from_proto": "file",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "file", "ingress_route": "route-relay-in",
        "egress_proto": "slack", "egress_route": "route-control-out",
        "to_num": "㉕", "to_name": "Control Room", "to_proto": "slack",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "MutualAid-to-DMS",
        "from_num": "⑧", "from_name": "Adjacent Utility", "from_proto": "amqp",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "amqp", "ingress_route": "route-mutualaid-in",
        "egress_proto": "jms", "egress_route": "route-dms-out",
        "to_num": "⑲", "to_name": "DMS / EMS", "to_proto": "jms",
        "to_fill": "#FFE082", "to_stroke": "#F57C00",
    },
    {
        "name": "CDC-to-SMS",
        "from_num": "㉝", "from_name": "Oracle CIS Change Data", "from_proto": "debezium-oracle",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "debezium-oracle", "ingress_route": "route-oracle-cdc",
        "egress_proto": "smpp", "egress_route": "route-sms-out",
        "to_num": "⑪", "to_name": "SMS Gateway", "to_proto": "smpp",
        "to_fill": "#90CAF9", "to_stroke": "#0D47A1",
    },
    {
        "name": "Billing-to-Email",
        "from_num": "㉒", "from_name": "Billing Scheduler", "from_proto": "timer",
        "from_fill": "#FFECB3", "from_stroke": "#FF8F00",
        "ingress_proto": "timer", "ingress_route": "route-relay-poll",
        "egress_proto": "mail", "egress_route": "route-bill-email",
        "to_num": "⑫", "to_name": "Email / Billing", "to_proto": "mail",
        "to_fill": "#90CAF9", "to_stroke": "#0D47A1",
    },
    {
        "name": "Compliance-to-FERC",
        "from_num": "⑧", "from_name": "Adjacent Utility", "from_proto": "file",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "file", "ingress_route": "route-mutualaid-in",
        "egress_proto": "sftp", "egress_route": "route-ferc-file",
        "to_num": "②", "to_name": "FERC / State PUC", "to_proto": "sftp",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
    {
        "name": "Billing-to-SAP",
        "from_num": "㉝", "from_name": "Oracle CIS Change Data", "from_proto": "debezium-oracle",
        "from_fill": "#A5D6A7", "from_stroke": "#2E7D32",
        "ingress_proto": "debezium-oracle", "ingress_route": "route-oracle-cdc",
        "egress_proto": "cxf-soap", "egress_route": "route-sap-out",
        "to_num": "㉗", "to_name": "SAP ERP", "to_proto": "cxf-soap",
        "to_fill": "#BBDEFB", "to_stroke": "#1565C0",
    },
]

# LEFT → RIGHT: FROM | ONE big Apache Camel box (all ingress + egress inside) | TO
COL_FROM_X = 30
COL_CAMEL_X = 250
COL_TO_X = 770

W_FROM = 200
W_CAMEL = 500
W_TO = 200
W_ING = 188
W_EGR = 188

ROW_H = 68
ROW_GAP = 16
CAMEL_HEADER = 48
CAMEL_SUBTITLE_H = 22
ROW_START = CAMEL_HEADER + CAMEL_SUBTITLE_H + 8
ING_X = 10
EGR_X = 262
ROUTE_FS = 8
ROUTE_H_PAD = 12
START_Y = 125

hub_content_h = CAMEL_SUBTITLE_H + 8 + len(INTEGRATION_FLOWS) * (ROW_H + ROW_GAP) - ROW_GAP
HUB_H = CAMEL_HEADER + hub_content_h + 20

PAGE_W = 1010
PAGE_H = START_Y + HUB_H + 80

cells = []
edge_cells = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def rect(cid, label, x, y, w, h, fill, stroke, sw=1, fs=9, bold=True, parent="1", align="center"):
    fw = "1" if bold else "0"
    spacing = "spacingLeft=6;spacingTop=4;" if align == "left" else ""
    return f'''        <mxCell id="{cid}" value="{esc(label)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={sw};fontSize={fs};fontStyle={fw};align={align};verticalAlign=middle;{spacing}" vertex="1" parent="{parent}">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def route_box(cid, label, x, y, w, h, fill, stroke, parent):
    """Compact ingress/egress box — small size, left-aligned text."""
    return rect(cid, label, x, y, w, h, fill, stroke, sw=1, fs=ROUTE_FS, bold=False, parent=parent, align="left")


def camel_hub(cid, label, x, y, w, h):
    """Single large Apache Camel container for all routes."""
    return f'''        <mxCell id="{cid}" value="{esc(label)}" style="swimlane;startSize={CAMEL_HEADER};horizontal=0;fillColor=#FFF3E0;strokeColor=#E65100;strokeWidth=4;fontStyle=1;fontSize=13;fontColor=#BF360C;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def text(cid, label, x, y, w, h, size=12, color="#37474F", bold=False, align="center"):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid}" value="{esc(label)}" style="text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;fontSize={size};fontStyle={fw};fontColor={color};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def text_in_parent(cid, label, x, y, w, h, parent, size=10, color="#BF360C", bold=False, align="center"):
    fw = "1" if bold else "0"
    return f'''        <mxCell id="{cid}" value="{esc(label)}" style="text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;fontSize={size};fontStyle={fw};fontColor={color};" vertex="1" parent="{parent}">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def edge_labeled(eid, src, tgt, proto, color, width=2):
    return f'''        <mxCell id="{eid}" value="" style="edgeStyle=none;rounded=0;html=1;strokeColor={color};strokeWidth={width};endArrow=classic;endFill=1;" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="{eid}-lbl" value="{esc(proto)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=9;fontStyle=1;fontColor={color};labelBackgroundColor=#FFFFFF;" vertex="1" connectable="0" parent="{eid}">
          <mxGeometry x="-0.1" relative="1" as="geometry"><mxPoint y="-9" as="offset"/></mxGeometry>
        </mxCell>'''


# Title
cells.append(text("title", "Electricity Utility — Apache Camel Integration Architecture", 15, 10, PAGE_W - 30, 28, 17, "#1B3A4B", True))
cells.append(text("subtitle", "FROM → Apache Camel hub → TO  |  protocol on each arrow", 15, 38, PAGE_W - 30, 18, 10, "#546E7A"))

cells.append(text("h-from", "FROM", COL_FROM_X, 88, W_FROM, 16, 11, "#2E7D32", True))
cells.append(text("h-to", "TO", COL_TO_X, 88, W_TO, 16, 11, "#1565C0", True))

# ONE big Apache Camel box — create before children
CAMEL_ID = "camel-hub"
cells.append(camel_hub(CAMEL_ID, "Apache Camel", COL_CAMEL_X, START_Y, W_CAMEL, HUB_H))
cells.append(text_in_parent("camel-subtitle", "Centralized Integration Middleware", 8, CAMEL_HEADER + 2, W_CAMEL - 16, CAMEL_SUBTITLE_H, CAMEL_ID, 10, "#E65100", True))

for i, f in enumerate(INTEGRATION_FLOWS):
    y = START_Y + ROW_START + i * (ROW_H + ROW_GAP)
    ry = ROW_START + i * (ROW_H + ROW_GAP)
    p = f"r{i}"

    from_id = f"{p}-from"
    ing_id = f"{p}-ing"
    egr_id = f"{p}-egr"
    to_id = f"{p}-to"

    from_lbl = f"FROM: {f['from_num']} {f['from_name']}&#xa;Protocol: {f['from_proto']}"
    ing_lbl = f"{f['ingress_route']}&#xa;Protocol: {f['ingress_proto']}"
    egr_lbl = f"{f['egress_route']}&#xa;Protocol: {f['egress_proto']}"
    to_lbl = f"TO: {f['to_num']} {f['to_name']}&#xa;Protocol: {f['to_proto']}"

    route_h = ROW_H - ROUTE_H_PAD

    # FROM / TO outside the big Camel box (aligned per row)
    cells.append(rect(from_id, from_lbl, COL_FROM_X, y, W_FROM, ROW_H, f["from_fill"], f["from_stroke"], fs=8))
    cells.append(rect(to_id, to_lbl, COL_TO_X, y, W_TO, ROW_H, f["to_fill"], f["to_stroke"], fs=8))

    # Route boxes inside the one big Apache Camel box (no ingress/egress labels)
    cells.append(route_box(ing_id, ing_lbl, ING_X, ry, W_ING, route_h, "#E8F5E9", "#2E7D32", CAMEL_ID))
    cells.append(route_box(egr_id, egr_lbl, EGR_X, ry, W_EGR, route_h, "#E3F2FD", "#1565C0", CAMEL_ID))

    edge_cells.append(edge_labeled(f"{p}-e1", from_id, ing_id, f["ingress_proto"], "#2E7D32"))
    edge_cells.append(edge_labeled(f"{p}-e2", ing_id, egr_id, f["ingress_proto"] + "→" + f["egress_proto"], "#E65100"))
    edge_cells.append(edge_labeled(f"{p}-e3", egr_id, to_id, f["egress_proto"], "#1565C0"))

# Footer
fy = START_Y + HUB_H + 15
cells.append(text("footer", f"{len(INTEGRATION_FLOWS)} flows  |  All routes inside one Apache Camel box  |  diagrams.net", 20, fy, PAGE_W - 40, 20, 9, "#78909C", False, "left"))

xml = f'''<mxfile host="app.diagrams.net" modified="2026-08-27T23:50:00.000Z" agent="Cursor" version="24.7.0" type="device">
  <diagram id="utility-camel-v8" name="Single Camel hub">
    <mxGraphModel dx="1100" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">
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
print(f"Written: {out_path} ({len(INTEGRATION_FLOWS)} rows, {len(xml)} bytes)")
