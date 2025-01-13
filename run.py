import os
from app import create_app
from app import models, db
from configurations.config import DevelopmentConfig, ProductionConfig
from livereload import Server
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
if os.getenv("LIVE") == "development":
    config = DevelopmentConfig()
else:
    config = ProductionConfig()

app = create_app(config)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": models.User,
        "Patient": models.Patient,
        "PatientRecord": models.PatientRecord,
        "Image": models.Image,
    }


@app.shell_context_processor
def make_shell_context():
    return {}


if __name__ == "__main__":
    app.run(port=5000, debug=app.config["DEBUG"] == True)
