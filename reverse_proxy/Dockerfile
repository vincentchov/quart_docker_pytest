FROM caddy:2-builder as builder

# Originally written when Caddy 2.6.1 came out. Update this comment if
# switching to caddy:3 or higher

ENV LETSENCRYPT_DNS_PLUGIN="cloudflare"

RUN if [[ -n "${LETSENCRYPT_DNS_PLUGIN}" ]]; then \
        xcaddy build \
        --with github.com/caddy-dns/${LETSENCRYPT_DNS_PLUGIN} ; \
    else \
        echo "This file is only here since Docker doesn't support conditionally copying files." > /usr/bin/workaround_file ; \
    fi

FROM caddy:2

# Replace the default Caddy with the built-version only if it exists.
# Otherwise copy the workaround file since Docker requires at least
# one of these files to exist.
COPY --from=builder /usr/bin/caddy* /usr/bin/workaround_file* /usr/bin/
COPY ./Caddyfiles /etc/caddy/
