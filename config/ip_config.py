import tools.ip_tool as tool
local_ip = tool.get_local_ip()

SOVITS_IP = local_ip
MQTT_ip = local_ip
LLM_host = "localhost"

sovits_server = 'http://' + local_ip + ':9880'
LLM_server = 'http://' + LLM_host + ':11434'+'/api/chat'
UI_server = 'http://' + local_ip + ':8080'
