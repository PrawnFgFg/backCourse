git config --local user.name "Fg Fg"
git config --local user.email "frizzergg@gmail.com"


docker network create MyNetwork


docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcdestick7856mvz \
    -e POSTGRES_DB=booking \
    --network=MyNetwork \
    --volume pg-booking-data:/var/lib/pgsql/data \
    -d postgres:16


docker run --name booking_cache \
    -p 7379:6379 \
    --network=MyNetwork \
    -d redis:8.2



docker run --name booking_back \
    -p 7777:8000 \
    --network=MyNetwork \
    booking_image



docker run --name booking_celery_worker \
    --network=MyNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=MyNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .



docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=MyNetwork \
    --rm -p 80:80 -p 443:443 -d nginx