from template_app.bootstrap.runtime import (
    bootstrap_application,
)


def bootstrap_testing_application():
    context = bootstrap_application()

    context.container.redis = None
    context.container.kafka = None

    return context
