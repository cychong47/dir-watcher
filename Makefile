APP_NAME=dir-watcher
DOCKER_REPO=ghcr.io/cychong47
DOCKER=podman

build:
	$(DOCKER) image build -f Dockerfile -t $(APP_NAME) .

run:
	$(DOCKER) run -d \
		--env-file=app.env \
		-v /home/cychong/work/cbs-ost:/home/cychong/work/cbs-ost \
		-v /home/cychong/public/ost:/home/cychong/public/ost \
		--name $(APP_NAME) \
		$(APP_NAME) 

tag:
	$(DOCKER) tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(shell cat VERSION)

push:
	$(DOCKER) push $(DOCKER_REPO)/$(APP_NAME):$(shell cat VERSION)

stop:
	$(DOCKER) stop $(APP_NAME)

rm:
	$(DOCKER) rm $(APP_NAME)

rmi:
	$(DOCKER) rmi localhost/$(APP_NAME):latest
