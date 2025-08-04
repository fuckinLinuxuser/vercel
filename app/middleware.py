class DBMiddleware:
    def __init__(self, pool):
        self.pool = pool

    async def __call__(self, handler, event, data):
        async with self.pool.acquire() as conn:
            data['db'] = conn
            return await handler(event, data)
