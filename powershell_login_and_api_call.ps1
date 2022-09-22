[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$url = 'https://www.nordnet.dk/logind'
$r1 = iwr $url -SessionVariable cookies

$body = @{'username'=''; 'password'=''}
$headers = @{'Accept' = '*/*'; 'client-id' = 'NEXT'; 'sub-client-id' = 'NEXT'}
  
$url = 'https://www.nordnet.dk/api/2/authentication/basic/login'
$r2 = iwr $url -method 'POST' -Body $body -Headers $headers -WebSession $cookies

$url = 'https://www.nordnet.dk/mediaapi/transaction/csv/filtered?locale=da-DK&account_id=1&from=2019-08-01&to=2019-10-01'
$r3 = iwr $url -WebSession $cookies
 
$content = $r3.Content
$encoding = [System.Text.Encoding]::unicode
$bytes = $encoding.GetBytes($content)
 
$decoded_content = [System.Text.Encoding]::utf32.GetString($bytes)
$decoded_content = $decoded_content.Substring(1,$decoded_content.length-1)
Write-Host $decoded_content