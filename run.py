import os
from app import create_app
from app import models, db
from configurations.config import DevelopmentConfig, ProductionConfig
from livereload import Server


if os.getenv("LIVE"):
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

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
    server = Server(app.wsgi_app)
    server.serve(port=5000)
    # app.run(port=5000, debug=app.config["DEBUG"] == True)
