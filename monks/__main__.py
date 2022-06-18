import os
import pathlib

from monks import client


def main() -> None:
    monks_client: client.Client = client.Client(
        os.environ["PUBLIC_KEY"],
        int(os.environ["APPLICATION_ID"]),
        os.environ["DISCORD_TOKEN"],
    )

    for path in pathlib.Path("./monks/modules").glob("*.py"):
        monks_client.load_module(str(path).replace("\\", ".").replace(".py", ""))

    monks_client.run("0.0.0.0", 5000)


if __name__ == "__main__":
    main()
