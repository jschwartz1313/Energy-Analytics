PYTHON ?= python3

.PHONY: all ingest transform queue markets finance charts dashboard qa clean test

all: ingest transform queue markets finance charts dashboard qa

ingest:
	$(PYTHON) -m energy_analytics ingest

transform:
	$(PYTHON) -m energy_analytics transform

queue:
	$(PYTHON) -m energy_analytics queue

markets:
	$(PYTHON) -m energy_analytics markets

finance:
	$(PYTHON) -m energy_analytics finance

charts:
	$(PYTHON) -m energy_analytics charts

dashboard:
	$(PYTHON) -m energy_analytics dashboard

qa:
	$(PYTHON) -m energy_analytics qa

test:
	$(PYTHON) -m unittest discover -s tests -q

clean:
	rm -f data/raw/*.csv data/staged/*.csv data/curated/*.csv data/curated/*.parquet
	rm -f data/marts/*.csv
	rm -f reports/charts/*.svg reports/qa_report.md reports/ingestion_metadata.log
	rm -f reports/market_findings.md
	rm -f reports/dashboard/*.html
