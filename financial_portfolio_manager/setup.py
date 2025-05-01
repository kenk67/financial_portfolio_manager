from setuptools import setup, find_packages

setup(
    name="financial_portfolio_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "matplotlib>=3.3.0",
        "numpy>=1.19.0",
        "pandas>=1.1.0",
    ],
    author="Akarsh",
    author_email="akarshr233@gmail.com",
    description="A Financial Portfolio Manager for tracking investments",
    keywords="finance, portfolio, investments",
    url="https://github.com/akarsh323/financialportfoliomangaer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.6",
)