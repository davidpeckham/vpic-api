from requests import Session


class VpicAPISession(Session):
    def __init__(self, *args, **kwargs):
        super(VpicAPISession, self).__init__(*args, **kwargs)

        self.headers.update(
            {
                "Accept-Charset": "utf-8",
            }
        )


__all__ = ["VpicAPISession"]
