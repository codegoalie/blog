# --- configuration (single source of truth; override on the command line) ----
#   make install USER=bob VAULT=/srv/vault REPO=/srv/blog
#
# USER resolves to the human user even under sudo (via SUDO_USER); VAULT and REPO
# default to that user's home. These are substituted into publish.py and the
# systemd units at install time, so the source files stay generic.
USER  := $(if $(SUDO_USER),$(SUDO_USER),$(USER))
VAULT ?= /home/$(USER)/Notes
REPO  ?= /home/$(USER)/blog

PREFIX  ?= /opt/blog-publish
SYSTEMD ?= /etc/systemd/system

.PHONY: config deps install enable disable uninstall status logs

config:
	@echo "USER  = $(USER)"
	@echo "VAULT = $(VAULT)"
	@echo "REPO  = $(REPO)"
	@echo "PREFIX  = $(PREFIX)"
	@echo "SYSTEMD = $(SYSTEMD)"

deps:
	@python3 -c 'import sys, zoneinfo; assert sys.version_info >= (3, 9)' \
		&& echo "OK: stdlib-only (Python >= 3.9 with tzdata)." \
		|| echo "Need Python >= 3.9 and timezone data (apt install tzdata)."

install:
	install -d $(PREFIX)
	sed -e 's|^VAULT_ROOT.*|VAULT_ROOT    = pathlib.Path("$(VAULT)")|' \
	    -e 's|^BLOG_REPO.*|BLOG_REPO     = pathlib.Path("$(REPO)")|' \
	    publish.py | install -m 755 /dev/stdin $(PREFIX)/publish.py
	sed -e 's|^User=.*|User=$(USER)|' \
	    -e 's|^ExecStart=.*|ExecStart=/usr/bin/python3 $(PREFIX)/publish.py|' \
	    blog-publish.service | install -m 644 /dev/stdin $(SYSTEMD)/blog-publish.service
	sed 's|^PathChanged=.*|PathChanged=$(VAULT)/blog/Publish|' \
	    blog-publish.path | install -m 644 /dev/stdin $(SYSTEMD)/blog-publish.path
	systemctl daemon-reload
	@echo "Installed for user '$(USER)' (vault=$(VAULT), repo=$(REPO))."
	@echo "Run 'make enable' to start watching."

enable: install
	systemctl enable --now blog-publish.path
	@echo "Watching $(VAULT)/blog/Publish"

disable:
	systemctl disable --now blog-publish.path || true

uninstall: disable
	rm -f $(SYSTEMD)/blog-publish.service $(SYSTEMD)/blog-publish.path
	rm -rf $(PREFIX)
	systemctl daemon-reload
	@echo "Uninstalled."

status:
	systemctl status blog-publish.path blog-publish.service

logs:
	journalctl -u blog-publish.service -f
