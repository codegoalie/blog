PREFIX  ?= /opt/blog-publish
SYSTEMD ?= /etc/systemd/system

.PHONY: install enable disable uninstall deps

deps:
	@python3 -c 'import sys, zoneinfo; assert sys.version_info >= (3, 9)' \
		&& echo "OK: stdlib-only (Python >= 3.9 with tzdata)." \
		|| echo "Need Python >= 3.9 and timezone data (apt install tzdata)."

install:
	install -d $(PREFIX)
	install -m 755 publish.py $(PREFIX)/publish.py
	install -m 644 blog-publish.service $(SYSTEMD)/blog-publish.service
	install -m 644 blog-publish.path    $(SYSTEMD)/blog-publish.path
	systemctl daemon-reload
	@echo "Installed. Run 'make enable' to start watching."

enable: install
	systemctl enable --now blog-publish.path
	@echo "Watching /home/chris/vault/Blog/Publish"

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
