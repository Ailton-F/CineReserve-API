import pytest
from django.core.cache import cache
from cinereserve_api.celery import debug_task

@pytest.mark.django_db
def test_redis_cache_integration():
    key = "integration_test_key"
    value = "redis_is_working"

    cache.set(key, value, timeout=10)

    result = cache.get(key)
    assert result == value

    cache.delete(key)
    assert cache.get(key) is None

# def test_celery_redis_broker_dispatch():
#     try:
#         result = debug_task.delay()

#         assert result.id is not None
#         assert isinstance(result.id, str)
#     except Exception as e:
#         pytest.fail(f"Failed to dispatch Celery task to Redis: {e}")

@pytest.mark.django_db
def test_redis_raw_connection():
    from django_redis import get_redis_connection

    con = get_redis_connection("default")

    assert con.ping() is True

    con.set("raw_key", "raw_value", ex=10)
    assert con.get("raw_key").decode('utf-8') == "raw_value"
    con.delete("raw_key")