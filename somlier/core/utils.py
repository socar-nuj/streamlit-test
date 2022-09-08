from functools import lru_cache


@lru_cache
def can_access_internal_service(internal_service_url: str, timeout: int = 5) -> bool:
    """
    Internal Service들에 접근할 수 있는 지 체크합니다
    Args:
        internal_service_url: 내부 서비스 URL
        timeout: 커넥션 타임아웃
    Returns:
        bool: Internal Service들에 접근할 수 있는 지 여부
    """
    import requests

    session = requests.Session()
    try:
        response = session.get(internal_service_url, timeout=timeout)
    except requests.exceptions.ConnectTimeout:
        return False

    return response.ok is True
