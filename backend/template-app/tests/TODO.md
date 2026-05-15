test package version:

when installed:
if not _version exist -> version is 0.0.0

when installed -> python template_app:version
when installed -> python template_app.__version__
when installed -> template_app --version or template_app -v

when is not installed:
test that it is installed or not

test version is the same that in _version.py
test _version.py exist in installation in site_packages
