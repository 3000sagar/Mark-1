import os 
from tools.base_tool import BaseTool

WORKSPACE = "workspace"

def safe_path(path: str) -> str:
    '''Ensure all path stay inside the workspace'''
    full_path = os.path.abspath(os.path.join(WORKSPACE, path))
    workspace_path = os.path.abspath(WORKSPACE)

    if not full_path.startswith(workspace_path):
        raise PermissionError("Access outside workspace is not allowed")
    return full_path

class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read contents of a file"

    def execute(self, **kwargs):
        try:
            path = kwargs.get("path")
            full_path = safe_path(path)

            with open(full_path,"r") as f:
                content = f.read()
            
            return {"success": True, "result": content, "error": None}
        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}

class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write content to a file"

    def execute(self, **kwargs):
        try:
            path = kwargs.get("path")
            content = kwargs.get("content","")

            full_path = safe_path(path)

            os.makedirs(os.path.dirname(full_path), exist_ok = True)
            
            with open(full_path, "w") as f:
                f.write(content)

            return {"success": True, "result": f"File written to {path}", "error": None}
        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}
        

class ListDirectoryTool(BaseTool):
    name = "list_directory"
    description = "List files in a directory"

    def execute(self, **kwargs):
        try:
            path = kwargs.get("path", "")
            full_path = safe_path(path)

            files = os.listdir(full_path)

            return {"success": True, "result": files, "error": None}

        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}
        

