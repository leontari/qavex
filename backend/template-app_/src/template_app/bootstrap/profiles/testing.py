from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def bootstrap_testing_application():
    context = bootstrap_kernel()

    context.container.redis = None
    context.container.kafka = None

    return context
