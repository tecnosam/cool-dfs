from flask import Response


def response(route):
    def inner(*args, **kwargs):
        res = route(*args, **kwargs)
        if isinstance(res, (Response, dict)):
            return res
        if res.status_code < 400:
            return res.json()

        return Response(res.text, res.status_code)

    return inner
