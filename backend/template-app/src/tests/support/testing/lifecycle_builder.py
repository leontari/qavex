from __future__ import annotations

from tests.support.fakes.lifecycle import FakeLifecycleHook


class LifecycleBuilder:
    """
    Runtime lifecycle builder.
    """

    @staticmethod
    def hook() -> FakeLifecycleHook:
        """
        Build fake lifecycle hook.
        """
        return FakeLifecycleHook()
