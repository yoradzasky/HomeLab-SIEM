import json
import requests
import time
import os

# --- KONFIGURASI ---
TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
# Path ini harus mengarah ke file alerts.json di folder volume Docker kamu
LOG_PATH = "/var/lib/docker/volumes/single-node_wazuh_logs/_data/alerts/alerts.json"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Error Telegram: {response.text}")
    except Exception as e:
        print(f"Gagal kirim pesan: {e}")

def monitor_alerts():
    print("🚀 SOC Automation: Monitoring Wazuh Alerts started...")
    print(f"Watching: {LOG_PATH}")

    # Memastikan file ada sebelum mulai
    if not os.path.exists(LOG_PATH):
        print(f"❌ Error: File {LOG_PATH} tidak ditemukan!")
        return

    with open(LOG_PATH, 'r') as f:
        # Pindah ke baris paling akhir agar tidak memproses log lama
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            try:
                alert = json.loads(line)
                level = alert.get('rule', {}).get('level', 0)

                # --- FILTER LEVEL ---
                # Ganti ke 3 untuk ngetes (agar login sukses pun masuk notif)
                # Ganti ke 12 untuk versi produksi (Hanya Critical)
                if level >= 3:
                    description = alert.get('rule', {}).get('description')
                    agent_name = alert.get('agent', {}).get('name')
                    rule_id = alert.get('rule', {}).get('id')

                    msg = (
                        f"🚨 *WAZUH ALERT DETECTED*\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🔹 *Level:* {level}\n"
                        f"🔹 *Agent:* {agent_name}\n"
                        f"🔹 *Rule ID:* {rule_id}\n"
                        f"🔹 *Event:* {description}\n"
                        f"━━━━━━━━━━━━━━━━━━━━"
                    )

                    print(f"Match found (Level {level})! Sending to Telegram...")
                    send_telegram(msg)

            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    monitor_alerts()
