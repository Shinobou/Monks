import os
import pathlib

import snowfin


def main() -> None:
    client: snowfin.Client = snowfin.Client(
        verify_key=os.environ["PUBLIC_KEY"],
        application_id=int(os.environ["APPLICATION_ID"]),
        sync_commands=True,
        token=os.environ["DISCORD_TOKEN"],
        auto_defer=True,
    )

    for path in pathlib.Path("./monks/modules").glob("*.py"):
        client.load_module(str(path).replace("\\", ".").replace(".py", ""))

    client.run("0.0.0.0", 5000)


if __name__ == "__main__":
    main()
