from typing import Any
import inspect


async def lyric_decrypt_adapter(context) -> Any:
    """专为歌词接口定制的解密适配器."""
    # 1. 动态反射拿到上游原生的 module 和 method
    module = getattr(context.client, context.route.module)
    bound_method = getattr(module, context.route.method)

    # 2. 执行原始请求拿到结果
    result = bound_method(**context.params)
    if inspect.isawaitable(result):
        result = await result

    # 3. 核心：如果结果有解密方法，在这里解密
    if hasattr(result, "decrypt") and callable(getattr(result, "decrypt")):
        result = result.decrypt()

    return result