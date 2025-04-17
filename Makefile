NAME = datascience

$(NAME): all

all:
	docker compose up -d

clean:
	docker compose down

fclean: clean
	docker system prune -a -f

re: fclean all

.PHONY: all clean fclean re