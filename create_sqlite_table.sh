#!/bin/sh

sqlite3 ml_streamlit_application_data.db <<'END_SQL'

.timeout 2000

.read queries/create_predictions_table.sql

END_SQL