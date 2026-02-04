"""
Setup configuration for AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iban-extraction-system",
    version="1.0.0",
    author="Eduardo Nascimento",
    author_email="eduardo.nascimento@charteredaccountants.ie",
    description="AI-Powered Automated IBAN Extraction System for Dynamics GP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ENinstitute/Vendor-Payee-Verification",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "anthropic>=0.40.0",
        "pandas>=2.2.0",
        "numpy>=1.26.4",
        "schwifty>=2024.6.1",
        "PyPDF2>=3.0.1",
        "Pillow>=10.4.0",
        "psycopg2-binary>=2.9.9",
        "SQLAlchemy>=2.0.36",
        "python-dotenv>=1.0.1",
        "cryptography>=43.0.3",
        "requests>=2.32.3",
        "azure-storage-blob>=12.23.1",
        "tqdm>=4.66.5",
        "colorlog>=6.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "pytest-cov>=6.0.0",
            "pytest-mock>=3.14.0",
            "black>=24.10.0",
            "flake8>=7.1.1",
            "mypy>=1.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "iban-train=main:train_model",
            "iban-process=main:process_invoices",
            "iban-load=main:load_to_dynamics",
        ],
    },
)
