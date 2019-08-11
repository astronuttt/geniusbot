if [ "$1" = "Update" ]; then
  git pull
  echo -e "\033[01;31m Bot Successful Update \033[0m"
else
  echo -e "
        \033[01;31m  Telegram Bot \033[0m"

  while true; do
	nohup python bot.py
	sleep 0.5
  done
fi

