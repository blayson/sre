from flask.cli import FlaskGroup

from app import create_app, DB

app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    DB.create_all()


@cli.command("recreate_db")
def recreate_db():
    DB.drop_all()
    DB.create_all()
    DB.session.commit()


if __name__ == "__main__":
    cli()
