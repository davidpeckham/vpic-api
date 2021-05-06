from requests import Session


class VpicAPISession(Session):
    def __init__(self, *args, **kwargs):
        """
        Creates a new CoreAPISession instance.
        """
        super(VpicAPISession, self).__init__(*args, **kwargs)

        self.headers.update(
            {
                "Accept-Charset": "utf-8",
                # "Content-Type": "text/plain",
            }
        )


__all__ = ["VpicAPISession"]
