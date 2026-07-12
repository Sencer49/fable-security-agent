import os
from typing import List, Dict

class CodeScanner:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.supported_extensions = ('.py', '.js', '.ts', '.go', '.java')

    def scan(self) -> List[Dict[str, str]]:
        scanned_files = []
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(self.supported_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            scanned_files.append({
                                "file_path": file_path,
                                "content": f.read()
                            })
                    except Exception as e:
                        print(f"[!] {file_path} okunurken hata oluştu: {e}")
        return scanned_files
