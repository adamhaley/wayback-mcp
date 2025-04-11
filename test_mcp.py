# test_mcp.py

from schemas.session import SessionContext
from schemas.tool import ToolContext
from schemas.response import ResponsePayload
import json

def test_context_creation():
    try:
        session = SessionContext(
            session_id="test123",
            user_id="user_abc",
            task_description="Retrieve 2011 jQuery plugin page",
            tools_invoked=[
                ToolContext(
                    tool_name="wayback_machine",
                    goal="Fetch archived HTML snapshot",
                    inputs={"url": "https://plugins.jquery.com/someplugin", "timestamp": "20110401000000"}
                )
            ],
            results=[
                ResponsePayload(
                    tool_name="wayback_machine",
                    success=True,
                    output={"snapshot_url": "https://web.archive.org/web/20110401000000/https://plugins.jquery.com/someplugin"},
                    human_readable="Snapshot found from April 1, 2011",
                    timestamp="2025-04-11T10:00:00Z"
                )
            ]
        )

        print("✅ MCP session context created successfully.\n")
        print(json.dumps(session.dict(), indent=2))

    except Exception as e:
        print("❌ Error creating MCP session context:")
        print(e)

if __name__ == "__main__":
    test_context_creation()

