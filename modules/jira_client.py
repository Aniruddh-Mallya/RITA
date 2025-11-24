import requests
from requests.auth import HTTPBasicAuth
import json

class JiraClient:
    @staticmethod
    def create_issue(domain: str, email: str, api_token: str, project_key: str, summary: str, description: str = ""):
        """
        Creates a single user story in Jira using Atlassian Document Format.
        """
        # Ensure domain has no trailing slash and has protocol
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        base_url = domain.rstrip('/')
        url = f"{base_url}/rest/api/3/issue"
        
        auth = HTTPBasicAuth(email, api_token)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Jira requires "Atlassian Document Format" for the description field
        payload = {
            "fields": {
                "project": {
                    "key": project_key
                },
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description if description else summary
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": "Story" 
                }
            }
        }

        try:
            response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
            
            # Check for HTTP errors
            if response.status_code not in [200, 201]:
                return {"success": False, "error": f"{response.status_code}: {response.text}"}
                
            return {"success": True, "key": response.json().get("key")}
            
        except Exception as e:
            print(f"[JIRA-ERROR] Request Failed: {e}")
            return {"success": False, "error": str(e)}