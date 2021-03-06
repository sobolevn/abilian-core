class Config:
    # specific (for this development instance)
    # SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    ANTIVIRUS_CHECK_REQUIRED = False
    SECRET_KEY = "toto"

    # develop settings
    DEBUG = True
    ASSETS_DEBUG = True
    DEBUG_TB_ENABLED = True
    # TEMPLATE_DEBUG = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = False

    # Generic for this project
    SITE_NAME = "Abilian Core Demo"
    MAIL_SENDER = "sender@example.com"
    SESSION_COOKIE_NAME = "abilian-core-session"
    PRIVATE_SITE = True
    MAIL_ASCII_ATTACHMENTS = True
    BABEL_ACCEPT_LANGUAGES = ("fr", "en", "es", "tr", "zh")

    # celery settings
    REDIS_URI = "redis://localhost/0"
    BROKER_URL = REDIS_URI
    CELERY_RESULT_BACKEND = REDIS_URI
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ALWAYS_EAGER = False  # True: run tasks locally, no async
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

    # uncomment if you don't want to use system timezone
    # CELERY_TIMEZONE = 'Europe/Paris'
