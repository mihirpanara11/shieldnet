from typing import Optional
import time
import logging
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger("shieldnet.agent.auth")

security_scheme = HTTPBearer(auto_error=False)


class JWTHandler:
    def __init__(self, secret: str = "shieldnet-secret",
                 algorithm: str = "HS256",
                 expiry_hours: int = 1):
        self.secret = secret
        self.algorithm = algorithm
        self.expiry_hours = expiry_hours

    def create_token(self, subject: str, role: str = "viewer") -> str:
        try:
            import jwt
            payload = {
                "sub": subject,
                "role": role,
                "iat": int(time.time()),
                "exp": int(time.time()) + self.expiry_hours * 3600,
            }
            return jwt.encode(payload, self.secret, algorithm=self.algorithm)
        except ImportError:
            return f"mock_token_{subject}_{role}_{int(time.time())}"

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            import jwt
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except Exception:
            return None

    def get_role(self, token: str) -> str:
        payload = self.verify_token(token)
        if payload:
            return payload.get("role", "viewer")
        return ""

    def require_auth(self, credentials: HTTPAuthorizationCredentials = Security(security_scheme)) -> dict:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Missing authorization header")
        payload = self.verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return payload

    def require_role(self, required_role: str = "viewer"):
        def role_checker(credentials: HTTPAuthorizationCredentials = Security(security_scheme)) -> dict:
            if credentials is None:
                raise HTTPException(status_code=401, detail="Missing authorization header")
            payload = self.verify_token(credentials.credentials)
            if payload is None:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            role = payload.get("role", "viewer")
            allowed = {"viewer": ["viewer", "operator", "admin"],
                       "operator": ["operator", "admin"],
                       "admin": ["admin"]}
            if required_role not in allowed.get(role, []):
                raise HTTPException(status_code=403, detail=f"Requires {required_role} role")
            return payload
        return role_checker
