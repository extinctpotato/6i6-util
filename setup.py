import setuptools

setuptools.setup(
        name="sixsixutil",
        version="0.1.1",
        author="Adam Olech",
        author_email="nddr89@gmail.com",
        description="A tiny script to manage the Focusrite Scarlett 6i6 card",
        packages=["sixsixutil"],
        python_requires='>=3.5',
        entry_points={
            "console_scripts": ["6i6 = sixsixutil.cli:main"]
            },
        install_requires=["pyalsaaudio"],
        )
