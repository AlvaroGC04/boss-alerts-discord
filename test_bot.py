import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1403222300341440573/AbFEz9OSrf9r4aD4D1L3sXQ7_L0nh4vkVurjQoR0lSn0fmafCEeqhKB_ItujGLjVxVAF"

requests.post(WEBHOOK_URL, json={"content": "✅ El webhook funciona correctamente.."})
