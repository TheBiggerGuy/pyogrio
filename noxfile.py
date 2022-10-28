import nox


@nox.session
def build(session):
    session.install("pip>=10.0", "packaging")
    session.run("python3", "setup.py", "develop")


@nox.session
def test(session):
    session.install("pip>=10.0", "wheel")
    session.install("-e", ".[dev,test,geopandas]")

    pytest_args = ["-v"]
    if "--coverage" in session.posargs:
        pytest_args += ["--cov=pyogrio", "--cov-report", "term-missing"]

    if "--memory" in session.posargs:
        session.install("pytest-memray")
        pytest_args += ["--memray"]

    if "--watch" in session.posargs:
        session.install("pytest-watch")
        session.run(
            *(
                [
                    "pytest-watch",
                    "--beforerun",
                    "python setup.py develop",
                    "pyogrio/tests",
                    "--",
                ]
                + pytest_args
            )
        )
    else:
        session.run("python", "setup.py", "develop")
        session.run(*(["pytest", "pyogrio/tests"] + pytest_args))


@nox.session
def benchmark(session):
    session.install("pip>=10.0", "wheel")
    session.install("-e", ".[dev,benchmark,geopandas]")

    session.run("python3", "setup.py", "develop")

    session.run(
        *(["pytest", "-v", "benchmarks", "--benchmark-autosave"] + session.posargs)
    )


@nox.session
def benchmark_vs_main(session):
    test_branch = session.run(
        "git", "branch", "--show-current", silent=True, external=True
    ).strip()
    branches = ["main", test_branch]
    session.log("Testing with %s branches", branches)

    session.install("pip>=10.0", "wheel")
    session.install("-e", ".[dev,benchmark,geopandas]", "pytest-benchmark[histogram]")

    for branch in branches:
        session.run("git", "checkout", branch)

        session.run("python3", "setup.py", "develop")

        session.run(
            *(
                [
                    "pytest",
                    "-v",
                    "benchmarks",
                    "--benchmark-min-time=2.0",
                    "--benchmark-min-time=3.0",
                    f"--benchmark-save={branch}",
                ]
                + session.posargs
            ),
            success_codes=(0, 1),  # continue on error
        )

    histogram_path = f"histogram-{'-vs-'.join(branches)}.svg"
    session.run(
        *(
            ["pytest-benchmark", "compare", f"--histogram={histogram_path}"]
            + [f"*{branch}" for branch in branches]
        )
    )
    session.log("histogram: %s", histogram_path)
