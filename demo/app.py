"""
"""
from flask import Blueprint, redirect

from abilian.app import Application as BaseApplication
from abilian.core.celery import FlaskCelery as BaseCelery
from abilian.core.celery import FlaskLoader as CeleryBaseLoader
from abilian.services.vocabularies import Vocabulary
from abilian.web.util import url_for

from .config import Config

__all__ = ["create_app"]

APP_NAME = "abilian_core_demo"


def create_app(config=None, **kw):
    app = Application(__name__, **kw)
    # Default config for this app
    app.config.from_object(Config)

    app.setup(config)

    app.register_blueprint(main)
    return app


# loader to be used by celery workers
class CeleryLoader(CeleryBaseLoader):
    flask_app_factory = "demo.app.create_app"


class CeleryApp(BaseCelery):
    loader_cls = CeleryLoader


celery = CeleryApp(loader=CeleryLoader)

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def home():
    """
    Home page. Actually there is no home page, so for this demo
    we redirect to the most appropriate place.
    """
    return redirect(url_for("admin.settings"))


class Application(BaseApplication):
    celery_app_cls = CeleryApp

    # def __init__(self, name=APP_NAME, config=None, **kwargs):
    #     super(Application, self).__init__(
    #         name, config=config, instance_relative_config=True, **kwargs
    #     )
    #
    # def init_extensions(self):
    #     super(Application, self).init_extensions()
    #
    #     # Additional service
    #     from abilian.services.security import security
    #
    #     security.init_app(self)
    #
    # def register_plugins(self):
    #     super(Application, self).register_plugins()
    #     self.register_blueprint(main)


Vocabulary_demo = Vocabulary(group="Test", name="Test", label="This is a test")
