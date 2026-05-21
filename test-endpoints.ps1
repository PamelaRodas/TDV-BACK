# Test all API endpoints
Write-Host "=========================" -ForegroundColor Cyan
Write-Host "Testing All Endpoints" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Test 1: Health check
Write-Host "`n✅ TEST 1: HEALTH CHECK" -ForegroundColor Green
try {
  $health = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing
  $health.Content | ConvertFrom-Json | ConvertTo-Json
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 2: Register new user
Write-Host "`n✅ TEST 2: REGISTER USER" -ForegroundColor Green
try {
  $registerBody = @{
    name = "Test User"
    email = "testuser@example.com"
    password = "testpass123"
  } | ConvertTo-Json
  
  $register = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body $registerBody `
    -UseBasicParsing
  
  $registerResp = $register.Content | ConvertFrom-Json
  $token = $registerResp.token
  Write-Host "User registered successfully!" -ForegroundColor Green
  Write-Host "Token: $($token.Substring(0, 40))..." -ForegroundColor Yellow
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 3: Login
Write-Host "`n✅ TEST 3: LOGIN" -ForegroundColor Green
try {
  $loginBody = @{
    email = "demo@example.com"
    password = "demo123"
  } | ConvertTo-Json
  
  $login = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginBody `
    -UseBasicParsing
  
  $loginResp = $login.Content | ConvertFrom-Json
  $token = $loginResp.token
  Write-Host "Login successful!" -ForegroundColor Green
  Write-Host "Token: $($token.Substring(0, 40))..." -ForegroundColor Yellow
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 4: Get home
Write-Host "`n✅ TEST 4: GET HOME" -ForegroundColor Green
try {
  $home = Invoke-WebRequest -Uri "http://localhost:5000/api/home" -UseBasicParsing
  Write-Host "Response:" -ForegroundColor Green
  $home.Content | ConvertFrom-Json | ConvertTo-Json
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 5: Get growth with token
Write-Host "`n✅ TEST 5: GET GROWTH CONTENT" -ForegroundColor Green
try {
  $growth = Invoke-WebRequest -Uri "http://localhost:5000/api/growth" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -UseBasicParsing
  Write-Host "Response:" -ForegroundColor Green
  $growth.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 6: Get sacred spaces
Write-Host "`n✅ TEST 6: GET SACRED SPACES" -ForegroundColor Green
try {
  $sacred = Invoke-WebRequest -Uri "http://localhost:5000/api/sacred-space" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -UseBasicParsing
  Write-Host "Response:" -ForegroundColor Green
  $sacred.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 7: Get diary entries
Write-Host "`n✅ TEST 7: GET DIARY ENTRIES" -ForegroundColor Green
try {
  $diary = Invoke-WebRequest -Uri "http://localhost:5000/api/diary" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -UseBasicParsing
  Write-Host "Response:" -ForegroundColor Green
  $diary.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

# Test 8: Get photos
Write-Host "`n✅ TEST 8: GET PHOTOS" -ForegroundColor Green
try {
  $photos = Invoke-WebRequest -Uri "http://localhost:5000/api/photos" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -UseBasicParsing
  Write-Host "Response:" -ForegroundColor Green
  $photos.Content | ConvertFrom-Json | ConvertTo-Json -Depth 2
} catch {
  Write-Host "ERROR: $_" -ForegroundColor Red
}

Write-Host "`n=========================" -ForegroundColor Cyan
Write-Host "✅ ALL TESTS COMPLETE!" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
