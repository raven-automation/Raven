from litestar import Router, get
from ..common.models import Session, AuthState
from .auth import AuthController, AuthScopesController

CONTROLLERS = [AuthController, AuthScopesController]

@get("/")
async def get_root(session: Session) -> AuthState:
    return await session.get_authstate()


API_ROUTER = Router(path="/api", route_handlers=[*CONTROLLERS, get_root])
