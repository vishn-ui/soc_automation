from flask import Flask, jsonify, request
import requests
import urllib3
import os
import json

urllib3.disable_warnings()

app = Flask(__name__)

WAZUH_HOST = "https://localhost:55000"
WAZUH_USER = "wazuh"
WAZUH_PASS = os.environ.get("WAZUH_PASS", "YOUR_pass")
def get_alerts(limit=20):
    try:
        r = requests.post(
            "https://localhost:9200/wazuh-alerts-4.x-2026.06.04/_search",
            auth=("admin", "YOUR_LOGIN_PASS"),
            verify=False,
            headers={"Content-Type": "application/json"},
            json={
                "size": limit,
                "sort": [{"timestamp": {"order": "desc"}}],
                "query": {"match_all": {}}
            }
        )
        hits = r.json().get("hits", {}).get("hits", [])
        return [h.get("_source", {}) for h in hits]
    except Exception as e:
        return []

@app.route("/")
def index():
    return jsonify({
        "status": "Wazuh MCP Server running",
        "version": "1.0",
        "endpoints": ["/health", "/alerts", "/summary", "/agents", "/mcp"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/alerts")
def alerts():
    try:
        limit = request.args.get("limit", 20)
        data = get_alerts(limit)
        return jsonify({"alerts": data, "total": len(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/summary")
def summary():
    try:
        alerts = get_alerts(100)
        result = {"high": [], "medium": [], "low": []}
        for a in alerts:
            level = a.get("rule", {}).get("level", 0)
            desc = a.get("rule", {}).get("description", "unknown")
            agent = a.get("agent", {}).get("name", "unknown")
            if level >= 10:
                result["high"].append({"desc": desc, "agent": agent, "level": level})
            elif level >= 7:
                result["medium"].append({"desc": desc, "agent": agent, "level": level})
            else:
                result["low"].append({"desc": desc, "agent": agent, "level": level})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/agents")
def agents():
    try:
        token = get_token()
        r = requests.get(
            f"{WAZUH_HOST}/agents",
            headers={"Authorization": f"Bearer {token}"},
            verify=False
        )
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mcp", methods=["POST"])
def mcp():
    body = request.json
    method = body.get("method", "")
    req_id = body.get("id", 1)

    if method == "initialize":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "wazuh-mcp", "version": "1.0"}
            }
        })

    if method == "tools/list":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "get_alerts",
                        "description": "Get recent Wazuh security alerts",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "limit": {"type": "integer", "description": "Number of alerts", "default": 20}
                            }
                        }
                    },
                    {
                        "name": "get_summary",
                        "description": "Get summary of alerts grouped by severity",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "get_agents",
                        "description": "Get list of Wazuh agents and their status",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        })

    if method == "tools/call":
        tool = body.get("params", {}).get("name", "")
        args = body.get("params", {}).get("arguments", {})

        if tool == "get_alerts":
            data = get_alerts(args.get("limit", 20))
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(data, indent=2)}]
                }
            })

        if tool == "get_summary":
            alerts = get_alerts(100)
            result = {"high": [], "medium": [], "low": []}
            for a in alerts:
                level = a.get("rule", {}).get("level", 0)
                desc = a.get("rule", {}).get("description", "unknown")
                agent = a.get("agent", {}).get("name", "unknown")
                if level >= 10:
                    result["high"].append({"desc": desc, "agent": agent, "level": level})
                elif level >= 7:
                    result["medium"].append({"desc": desc, "agent": agent, "level": level})
                else:
                    result["low"].append({"desc": desc, "agent": agent, "level": level})
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        if tool == "get_agents":
            try:
                token = get_token()
                r = requests.get(
                    f"{WAZUH_HOST}/agents",
                    headers={"Authorization": f"Bearer {token}"},
                    verify=False
                )
                data = r.json()
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(data, indent=2)}]
                    }
                })
            except Exception as e:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                })

    return jsonify({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
