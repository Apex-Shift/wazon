# core/config.py

WAZON_VERSION = "1.0.0-beta"
CODENAME = "Mission Impossible"

DEFAULT_TIMEOUT = 5  # Secondes pour les sockets/requêtes HTTP

# User-Agents pour passer incognito sur les interfaces web des BMS
STEALTH_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "JCI-Metasys-Client-Agent/3.2"
]