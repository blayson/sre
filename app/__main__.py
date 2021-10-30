import uvicorn

from .settings import settings


uvicorn.run(
    'app.main:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
    log_level='debug',
    debug=settings.debug
)
