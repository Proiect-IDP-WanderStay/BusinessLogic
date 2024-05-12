from flask.cli import FlaskGroup
from project import app 
from project.business import bp_business

cli = FlaskGroup(app)

# blueprints
app.register_blueprint(bp_business)

@cli.command("start")
def start():
    # destroy all tables and creat new ones
    # this is good for testing, you can delete it if you want full persistency
    print("start 3")



if __name__ == "__main__":
    cli()