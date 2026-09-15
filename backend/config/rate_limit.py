from django.core.cache import caches


RATE_LIMIT_SCRIPT = """
local current = redis.call('INCR', KEYS[1])

if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

if current > tonumber(ARGV[2]) then
    return 1
end

return 0
"""


def is_rate_limited(key, limit, window):
    redis = caches["default"].client.get_client(write=True)

    script = redis.register_script(RATE_LIMIT_SCRIPT)

    result = script(
        keys=[key],
        args=[window, limit],
    )

    return result == 1