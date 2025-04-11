from fastmcp import create_app, McpServerTool, McpServerToolType
from typing import Optional
import requests
from http import HTTPStatus

WAYBACK_MACHINE_CDX_API = "https://web.archive.org/cdx/search/cdx"
BASE_URL = "https://web.archive.org/web/"

@McpServerToolType
class WaybackMachineTools:
    """Provides access to the Wayback Machine archive."""

    @McpServerTool(description="Retrieves archived content from the Wayback Machine.")
    @staticmethod
    def archive_url(url: str, timestamp: Optional[str] = None) -> dict:
        """
        Retrieves the archived content of a URL at a specific timestamp.

        Args:
            url: The URL to archive.
            timestamp: The timestamp in YYYYMMDDHHMMSS format. If not provided,
                       returns the latest archived version.

        Returns:
            A dictionary containing the archived HTML content and metadata.
        """
        if not url:
            return {"error": "URL is required"}, HTTPStatus.BAD_REQUEST

        cdx_params = {
            "url": url,
            "output": "json",
        }
        if timestamp:
            cdx_params["from"] = timestamp
            cdx_params["to"] = timestamp

        try:
            cdx_response = requests.get(WAYBACK_MACHINE_CDX_API, params=cdx_params)
            cdx_response.raise_for_status()
            cdx_data = cdx_response.json()

            if not cdx_data or len(cdx_data) < 2:
                return {"error": "URL not found in archive"}, HTTPStatus.NOT_FOUND

            closest_snapshot = cdx_data[1]
            archived_timestamp = closest_snapshot[1]
            archived_url = f"{BASE_URL}{archived_timestamp}/{url}"

            content_response = requests.get(archived_url)
            content_response.raise_for_status()
            archived_content = content_response.text

            return {
                "data": archived_content,
                "metadata": {"archived_url": archived_url},
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Error accessing Wayback Machine: {e}"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from Wayback Machine"}, HTTPStatus.INTERNAL_SERVER_ERROR

app = create_app(WaybackMachineTools)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

