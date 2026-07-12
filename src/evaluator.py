import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Hem mevcut hem üst dizindeki .env dosyalarını yüklemeyi dene
load_dotenv()
load_dotenv(os.path.join("..", ".env"))

class SecurityEvaluator:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Eğer ortam değişkenlerinden okunamadıysa doğrudan ..\.env dosyasından oku
        if not api_key:
            env_path = os.path.join("..", ".env")
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("ANTHROPIC_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break

        if not api_key or api_key == "your_actual_api_key_here":
            raise ValueError("Geçerli bir ANTHROPIC_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")

        self.client = Anthropic(api_key=api_key)
        
        # Claude Fable 5 Sistem Promptu
        self.system_prompt = (
            "You are an elite DevSecOps and Autonomous Code Security Auditor powered by Fable 5. "
            "Your job is to perform deep static and semantic analysis on the code snippet provided. "
            "You identify critical vulnerabilities (OWASP Top 10, logic errors, injection bugs, authorization flaws). "
            "For every issue found, you MUST respond ONLY with a valid JSON object matching the requested structure. "
            "Do not include any Markdown wrap or additional conversational text outside the JSON."
        )

    def evaluate_code(self, file_path: str, code_content: str) -> dict:
        # NOTE: API hesabında bakiye olmadığında sistemi test edebilmek için 
        # aşağıdaki MOCK bloğunu kullanıyoruz. Gerçek API isteği için bu return'ü yorum satırı yapabilirsiniz.
        return {
            "vulnerability_found": True,
            "severity": "CRITICAL",
            "vulnerability_type": "SQL Injection & Unauthenticated Access",
            "explanation": "user_id parametresi SQL sorgusuna doğrudan string birleştirme ile eklenmiş. Bu durum yetkisiz kişilerin veritabanındaki tüm verileri okumasına imkan tanır.",
            "patched_code": "from flask import Flask, request, jsonify\nimport sqlite3\n\napp = Flask(__name__)\n\n@app.route('/user', methods=['GET'])\ndef get_user():\n    user_id = request.args.get('id')\n    conn = sqlite3.connect('database.db')\n    cursor = conn.cursor()\n    # Parametreli sorgu kullanımı (SQL Injection Önleme)\n    query = 'SELECT id, username, email FROM users WHERE id = ?'\n    cursor.execute(query, (user_id,))\n    user = cursor.fetchone()\n    return jsonify({'user': user})\n\nif __name__ == '__main__':\n    app.run(debug=False)",
            "poc_test_code": "# PoC: /user?id=1' OR '1'='1"
        }

        # DÜZELTİLEN USER PROMPT (kod içeriği eklendi)
        user_prompt = f"""
Analyze the following code file for security vulnerabilities:

File Path: {file_path}

Code Content:
Respond with a JSON object containing:
- "vulnerability_found": boolean
- "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "NONE"
- "vulnerability_type": short title of the bug
- "explanation": concise description of why this code is insecure
- "patched_code": the fully corrected, secure version of the entire file code
- "poc_test_code": a Python test code snippet proving/testing the fix or flaw
"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.2,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        response_text = response.content[0].text.strip()
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            if "```json" in response_text:
                clean_json = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(clean_json)
            raise ValueError(f"Claude geçerli bir JSON yanıtı döndürmedi: {response_text}")