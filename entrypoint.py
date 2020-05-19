import json
from app import app, args, config

app.run()
with open(args.config, 'w+') as f:
    f.write(json.dumps(config))