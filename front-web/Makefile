REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t notasquare/workboard/front-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t notasquare/workboard/front-web/test .
	sudo docker tag notasquare/workboard/front-web/test $(REGISTRY)/notasquare/workboard/front-web/test
	sudo docker push $(REGISTRY)/notasquare/workboard/front-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t notasquare/workboard/front-web/prod .
	sudo docker tag notasquare/workboard/front-web/prod $(REGISTRY)/notasquare/workboard/front-web/prod
	sudo docker push $(REGISTRY)/notasquare/workboard/front-web/prod
