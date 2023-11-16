_svr_name = gptsindex
_build_time = $(shell date +%y%m%d%H%M%S) 
_image_name = ${_svr_name}:v${_build_time}

docker-build:
	docker build -f deploy/Dockerfile -t ${_image_name} .

docker-run:
	docker run -d --name ${_image_name} -p 8068:8068 ${_image_name}

dev:
	uvicorn main:app --port=8068 --reload

tst:
	pm2 start deploy.sh --name gptsindex

tidy:
	pipreqs . --encoding=utf8 --force
