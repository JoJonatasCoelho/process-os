import json
from pathlib import Path

SEED = 67

BASE_DIR = Path(__file__).parent
INPUT_JSON = "json1.json"

with open(BASE_DIR / "inputs" / INPUT_JSON) as f:
    config = json.load(f)

meta = config['metadata']
processes = config['workload']['processes']
ctx_cost = meta['contextswitchcost']
T = meta['throughputwindowT']
quantums = meta['rrquantums']

COLORS = {
    'P01': '#4E9AF1',
    'P02': '#F4A460',
    'P03': '#6ECB63',
    'P04': '#E066A0',
    'P05': '#A78BFA',
    'CTX': '#888888',
    'IDLE': '#DDDDDD',
}
