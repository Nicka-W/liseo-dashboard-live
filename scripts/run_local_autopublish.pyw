import os, sys, traceback
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_autopublish.log")
try:
    import publish_dashboard_data as p
    p.main()
except BaseException:
    with open(log, "a") as f:
        f.write(datetime.now().isoformat() + "\n" + traceback.format_exc() + "\n")
