"""Web API cookie credential parsing tests."""

from starlette.requests import Request

from web.src.core.auth import credential_from_cookies


def _request_with_cookie(cookie: str) -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": "/login/refresh_credential",
            "raw_path": b"/login/refresh_credential",
            "query_string": b"",
            "headers": [(b"cookie", cookie.encode())],
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
        }
    )


def test_credential_from_cookies_preserves_explicit_qq_login_type_zero() -> None:
    """显式 QQ 类型 0 不应因 truthy 检查而被丢弃."""
    credential = credential_from_cookies(
        _request_with_cookie("musicid=123456; musickey=qq-key; login_type=0; refresh_token=refresh")
    )

    assert credential.musicid == 123456
    assert credential.login_type == 0
    assert credential.refresh_token == "refresh"


def test_credential_from_cookies_preserves_explicit_wechat_login_type() -> None:
    """兼容驼峰 Cookie, 保留微信登录类型."""
    credential = credential_from_cookies(
        _request_with_cookie("musicid=123456; musickey=key; loginType=1")
    )

    assert credential.login_type == 1


def test_credential_from_cookies_still_infers_login_type_when_unspecified() -> None:
    """未提供登录类型时继续沿用凭据模型的推断逻辑."""
    credential = credential_from_cookies(_request_with_cookie("musicid=123456; musickey=W_X-key"))

    assert credential.login_type == 1
