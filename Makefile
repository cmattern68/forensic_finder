.PHONY: dev
dev:
	python3 -m venv venv && \
	. ./venv/bin/activate && \
	pip3 install -r requirements/requirements.txt

run:
	. ./venv/bin/activate && \
	python3 forensic_finder/main.py /home/corentin/Perso/Rosette/save_photorec --ext "ext.txt" --dest /home/corentin/Perso/result_filter_photorec --verbose --clamav
	#python3 forensic_finder/main.py /home/corentin/Perso/save_photorec --ext "ext.txt" --dest /home/corentin/Perso/result_filter_photorec --verbose --clamav
