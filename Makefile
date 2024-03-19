SHELL := /bin/bash


# BUILD

define build
	$(eval $@_SNAP = $(1))
	@echo "Building ${$@_SNAP} snap..."
	cd ${$@_SNAP}
	snapcraft --debug
endef

.PHONY: follower
.ONESHELL:
follower:
	@$(call build, "follower")

.PHONY: registration-agent
.ONESHELL:
registration-agent:
	@$(call build, "registration-agent")

.PHONY: server
.ONESHELL:
server:
	@$(call build, "server")

.PHONY: all
all: follower registration-agent server

.DEFAULT_GOAL := all


# INSTALL
# To use the make targets below, make sure you have yq installed.
# You can install it using Homebrew or as a snap:
# 	$ brew install yq
# 	$ snap install yq

define install
    $(eval $@_SNAP = $(1))
	@echo "Installing ${$@_SNAP} snap..."
	$(eval VERSION=$(shell yq ".version" ${$@_SNAP}/snap/snapcraft.yaml))
	sudo snap install --devmode ${$@_SNAP}/aspects-${$@_SNAP}_$(VERSION)_amd64.snap
	snap connections aspects-${$@_SNAP} | awk '{print $$2}' | tail -n +2 | xargs -I {} sudo snap connect {}
endef

.PHONY: install-follower
install-follower:
	@$(call install, "follower")

.PHONY: install-registration-agent
install-registration-agent:
	@$(call install, "registration-agent")

.PHONY: install-server
install-server:
	@$(call install, "server")

.PHONY: install-all
install-all: install-follower install-registration-agent install-server
