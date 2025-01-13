from setuptools import setup, find_packages

setup(
    name="golf_card_game",
    version="0.4.1",
    author="SakuOrdrTab",
    description="RL agent training and Golf cardgame.",
    long_description=open("README.md").read(),
    url="https://github.com/SakuOrdrTab/golf_card_game",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
