WORKBOARD_API_MYSQL_HOST_PORT=3350
WORKBOARD_API_WEB_HOST_PORT=8050
WORKBOARD_ADMIN_MYSQL_HOST_PORT=3351
WORKBOARD_ADMIN_WEB_HOST_PORT=8051
WORKBOARD_FRONT_MYSQL_HOST_PORT=3352
WORKBOARD_FRONT_WEB_HOST_PORT=8052


create-storage:
	sudo docker run -d --name=notasquare-dev.workboard-api.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true
	sudo docker run -d --name=notasquare-dev.workboard-admin.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true
	sudo docker run -d --name=notasquare-dev.workboard-front.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true

clear-storage:
	-sudo docker stop notasquare-dev.workboard-api.mysql.storage
	-sudo docker rm notasquare-dev.workboard-api.mysql.storage
	-sudo docker stop notasquare-dev.workboard-admin.mysql.storage
	-sudo docker rm notasquare-dev.workboard-admin.mysql.storage
	-sudo docker stop notasquare-dev.workboard-front.mysql.storage
	-sudo docker rm notasquare-dev.workboard-front.mysql.storage

deploy:
	sudo docker run -d --name=notasquare-dev.workboard-api.mysql \
		--volumes-from=notasquare-dev.workboard-api.mysql.storage \
		-p $(WORKBOARD_API_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=notasquare-dev.workboard-api.web \
		--link notasquare-dev.workboard-api.mysql:mysql \
		-v $(NOTASQUARE_WORKBOARD_HOME)/not-a-square-workboard/api-web/src/www:/opt/www \
		-p $(WORKBOARD_API_WEB_HOST_PORT):80 \
		notasquare/workboard/api-web/dev

	sudo docker run -d --name=notasquare-dev.workboard-admin.mysql \
		-p $(WORKBOARD_ADMIN_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=notasquare-dev.workboard-admin.web \
		--link notasquare-dev.workboard-admin.mysql:mysql \
		--link notasquare-dev.workboard-api.web:workboard-api \
		-v $(NOTASQUARE_WORKBOARD_HOME)/not-a-square-workboard/admin-web/src/www:/opt/www \
		-p $(WORKBOARD_ADMIN_WEB_HOST_PORT):80 \
		notasquare/workboard/admin-web/dev

	sudo docker run -d --name=notasquare-dev.workboard-front.mysql \
		-p $(WORKBOARD_FRONT_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=notasquare-dev.workboard-front.web \
		--link notasquare-dev.workboard-front.mysql:mysql \
		--link notasquare-dev.workboard-api.web:workboard-api \
		-v $(NOTASQUARE_WORKBOARD_HOME)/not-a-square-workboard/front-web/src/www:/opt/www \
		-p $(WORKBOARD_FRONT_WEB_HOST_PORT):80 \
		notasquare/workboard/front-web/dev

	sudo cp nginx/notasquare-workboard-api-web /etc/nginx/sites-enabled
	sudo cp nginx/notasquare-workboard-admin-web /etc/nginx/sites-enabled
	sudo cp nginx/notasquare-workboard-front-web /etc/nginx/sites-enabled
	sudo service nginx reload

	sleep 60

	-sudo docker exec -it notasquare-dev.workboard-api.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS api_db;"
	-sudo docker exec -it notasquare-dev.workboard-api.web python /opt/www/manage.py migrate

	-sudo docker exec -it notasquare-dev.workboard-admin.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS admin_db;"
	-sudo docker exec -it notasquare-dev.workboard-admin.web python /opt/www/manage.py migrate
	-sudo docker exec -it notasquare-dev.workboard-admin.web python /opt/www/manage.py linkstatic

	-sudo docker exec -it notasquare-dev.workboard-front.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS front_db;"
	-sudo docker exec -it notasquare-dev.workboard-front.web python /opt/www/manage.py migrate
	-sudo docker exec -it notasquare-dev.workboard-front.web python /opt/www/manage.py linkstatic

clean:
	-sudo docker stop notasquare-dev.workboard-admin.mysql
	-sudo docker stop notasquare-dev.workboard-admin.web
	-sudo docker stop notasquare-dev.workboard-front.mysql
	-sudo docker stop notasquare-dev.workboard-front.web
	-sudo docker stop notasquare-dev.workboard-api.mysql
	-sudo docker stop notasquare-dev.workboard-api.web

	-sudo docker rm notasquare-dev.workboard-admin.mysql
	-sudo docker rm notasquare-dev.workboard-admin.web
	-sudo docker rm notasquare-dev.workboard-front.mysql
	-sudo docker rm notasquare-dev.workboard-front.web
	-sudo docker rm notasquare-dev.workboard-api.mysql
	-sudo docker rm notasquare-dev.workboard-api.web

	-sudo rm /etc/nginx/sites-enabled/notasquare-workboard-api-web
	-sudo rm /etc/nginx/sites-enabled/notasquare-workboard-admin-web
	-sudo rm /etc/nginx/sites-enabled/notasquare-workboard-front-web

start:
	sudo docker start notasquare-dev.workboard-api.mysql
	sudo docker start notasquare-dev.workboard-api.web
	sudo docker start notasquare-dev.workboard-admin.mysql
	sudo docker start notasquare-dev.workboard-admin.web
	sudo docker start notasquare-dev.workboard-front.mysql
	sudo docker start notasquare-dev.workboard-front.web

stop:
	sudo docker stop notasquare-dev.workboard-api.mysql
	sudo docker stop notasquare-dev.workboard-api.web
	sudo docker stop notasquare-dev.workboard-admin.mysql
	sudo docker stop notasquare-dev.workboard-admin.web
	sudo docker stop notasquare-dev.workboard-front.mysql
	sudo docker stop notasquare-dev.workboard-front.web

migrate:
	-sudo docker exec -it notasquare-dev.workboard-api.web python /opt/www/manage.py migrate
	-sudo docker exec -it notasquare-dev.workboard-admin.web python /opt/www/manage.py migrate
	-sudo docker exec -it notasquare-dev.workboard-front.web python /opt/www/manage.py migrate

ssh-api-mysql:
	sudo docker exec -it notasquare-dev.workboard-api.mysql bash

ssh-api-web:
	sudo docker exec -it notasquare-dev.workboard-api.web bash

ssh-admin-mysql:
	sudo docker exec -it notasquare-dev.workboard-admin.mysql bash

ssh-admin-web:
	sudo docker exec -it notasquare-dev.workboard-admin.web bash

ssh-front-mysql:
	sudo docker exec -it notasquare-dev.workboard-front.mysql bash

ssh-front-web:
	sudo docker exec -it notasquare-dev.workboard-front.web bash
