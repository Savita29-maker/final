$PGPATH = "C:\Program Files\PostgreSQL\18\bin"
$env:PGPASSWORD = "2004"

Write-Host "Using PostgreSQL from: $PGPATH" -ForegroundColor Cyan
Write-Host "Dropping existing database..." -ForegroundColor Yellow
& "$PGPATH\dropdb.exe" -U postgres -h localhost smart_patient_queue 2>$null

Write-Host "Creating database..." -ForegroundColor Green
& "$PGPATH\createdb.exe" -U postgres -h localhost smart_patient_queue

Write-Host "Loading schema..." -ForegroundColor Green
& "$PGPATH\psql.exe" -U postgres -h localhost -d smart_patient_queue -f database/schema.sql

Write-Host "Verifying..." -ForegroundColor Green
& "$PGPATH\psql.exe" -U postgres -h localhost -d smart_patient_queue -c "SELECT COUNT(*) FROM patients;"

Write-Host "✅ Done!" -ForegroundColor Green
