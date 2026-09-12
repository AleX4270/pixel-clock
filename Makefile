DRIVE := /Volumes/CIRCUITPY

deploy:
	rsync -rltv --delete --exclude='.*' --exclude='lib/' src/ $(DRIVE)/
	sync