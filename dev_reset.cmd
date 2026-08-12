@REM ./rodar_do_zero.cmd
docker compose down --rmi local -v
docker builder prune -f
docker compose up --build
