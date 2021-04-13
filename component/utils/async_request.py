import asyncio

import aiohttp


async def fetch(session, url, method, data=None):
    post_data = [{"params": data}, {"json": data}][method == "post"]
    async with getattr(session, method)(url, **post_data, timeout=60) as resp:
        if resp.status != 200:
            resp.raise_for_status()
        data = await resp.json()
        return data


async def fetch_multi(session, request_data_map, method):
    tasks = []
    for url, data in request_data_map.items():
        tasks.append(fetch(session, url, method, data))

    # gather: 搜集所有future对象，并等待返回
    results = await asyncio.gather(*tasks)
    return results


async def async_request(method, request_data_map=None, limit=20):
    """
    method : get,post
    """
    request_data_map = request_data_map or {}
    conn = aiohttp.TCPConnector(limit=limit, verify_ssl=False)

    async with aiohttp.ClientSession(connector=conn) as session:
        result_list = await fetch_multi(session, request_data_map, method=method)
        return result_list
