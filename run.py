from app import create_app


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {}


if __name__ == "__main__":
    app.run(port=5000, debug=app.config["DEBUG"] == True)
