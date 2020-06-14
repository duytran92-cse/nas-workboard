REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t notasquare/workboard/api-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t notasquare/workboard/api-web/test .
	sudo docker tag notasquare/workboard/api-web/test $(REGISTRY)/notasquare/workboard/api-web/test
	sudo docker push $(REGISTRY)/notasquare/workboard/api-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t notasquare/workboard/api-web/test .
	sudo docker tag notasquare/workboard/api-web/prod $(REGISTRY)/notasquare/workboard/api-web/prod
	sudo docker push $(REGISTRY)/notasquare/workboard/api-web/prod
