import os
from app import create_app
from app import models
from configurations.config import DevelopmentConfig, ProductionConfig


if os.getenv("LIVE"):
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

app = create_app(config)


@app.shell_context_processor
def make_shell_context():
    return {}


if __name__ == "__main__":
    app.run(port=5000, debug=app.config["DEBUG"] == True)
