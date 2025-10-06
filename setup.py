from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="1.0.0",
    description="Cryptographic system with custom key generator",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.20.0",
        "psutil>=5.8.0",
    ],
    entry_points={
        'console_scripts': [
            'cryptocore=cryptocore:main',  # ⚡ Точка входа для CLI
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)