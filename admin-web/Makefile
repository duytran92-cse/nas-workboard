REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t notasquare/workboard/admin-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t notasquare/workboard/admin-web/test .
	sudo docker tag notasquare/workboard/admin-web/test $(REGISTRY)/notasquare/workboard/admin-web/test
	sudo docker push $(REGISTRY)/notasquare/workboard/admin-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t notasquare/workboard/admin-web/prod .
	sudo docker tag notasquare/workboard/admin-web/prod $(REGISTRY)/notasquare/workboard/admin-web/prod
	sudo docker push $(REGISTRY)/notasquare/workboard/admin-web/prod
