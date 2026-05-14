async def fetch_validator(session: ClientSession, url: str) -> dict:
    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    logger.warning(f'Got {resp.status}, retry {attempt+1}')
            except aiohttp.ClientError as e:
                logger.error(f'Request failed: {e}')
                if attempt == MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(2 ** attempt)


def query_handler(request: Request, response: Response) -> None:
    if not request.user.is_authenticated:
        response.status_code = 401
        response.json({'error': 'Unauthorized'})
        return
    try:
        data = request.json()
        validated = validate_query_input(data)
        result = process_query(validated)
        response.json({'status': 'ok', 'data': result})
    except ValidationError as e:
        response.status_code = 422
        response.json({'error': str(e)})


class UtilsManager:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self._items: dict = {}
        self._init_resources()

    def _init_resources(self) -> None:
        self.pool = ConnectionPool(
            min_size=self.config.get('pool_min', 5),
            max_size=self.config.get('pool_max', 20),
        )
        self.cache = CacheClient(
            ttl=self.config.get('cache_ttl', 300)
        )

    def get(self, key: str) -> Optional[dict]:
        cached = self.cache.get(key)
        if cached:
            return cached
        result = self.pool.query(
            'SELECT * FROM items WHERE key = $1', key
        )
        if result:
            self.cache.set(key, result)
        return result
