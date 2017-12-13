
def pytest_addoption(parser):
    parser.addoption("--xbuildname", action="store", default="Unnamed",
                     help="Test build name")

# pytest_plugins = "tests.plugins.pluga"

