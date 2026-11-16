$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonProjeto = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonProjeto)) {
    throw 'Ambiente .venv não encontrado. Consulte GUIA_RAPIDO.md.'
}
$pastaRuntime = Join-Path $PSScriptRoot '.jupyter-local'
New-Item -ItemType Directory -Force -Path $pastaRuntime | Out-Null
$runtimeAnterior = $env:JUPYTER_RUNTIME_DIR
$env:JUPYTER_RUNTIME_DIR = $pastaRuntime
try {
    $servidor = $null
    foreach ($arquivo in Get-ChildItem -LiteralPath $pastaRuntime -Filter 'jpserver-*.json') {
        try {
            $candidato = Get-Content -LiteralPath $arquivo.FullName -Raw | ConvertFrom-Json
            $urlTeste = $candidato.url + 'api/status?token=' + $candidato.token
            $null = Invoke-RestMethod -Uri $urlTeste -TimeoutSec 3
            $servidor = $candidato
            break
        } catch { }
    }
    if ($null -eq $servidor) {
        $argumentosJupyter = @(
            '-m', 'jupyterlab', '--no-browser',
            '--ServerApp.ip=127.0.0.1', '--ServerApp.port=8888',
            '--ServerApp.port_retries=10',
            '--ServerApp.default_url=/lab/tree/GUIA_RAPIDO.md'
        )
        $processoJupyter = Start-Process -FilePath $pythonProjeto -ArgumentList $argumentosJupyter `
            -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $pastaRuntime 'servidor.stdout.log') `
            -RedirectStandardError (Join-Path $pastaRuntime 'servidor.stderr.log')
        for ($tentativa = 0; $tentativa -lt 45; $tentativa++) {
            Start-Sleep -Seconds 1
            foreach ($arquivo in Get-ChildItem -LiteralPath $pastaRuntime -Filter 'jpserver-*.json') {
                try {
                    $candidato = Get-Content -LiteralPath $arquivo.FullName -Raw | ConvertFrom-Json
                    $null = Invoke-RestMethod -Uri ($candidato.url + 'api/status?token=' + $candidato.token) -TimeoutSec 2
                    $servidor = $candidato
                    break
                } catch { }
            }
            if ($null -ne $servidor) { break }
            if ($processoJupyter.HasExited) { break }
        }
    }
    if ($null -eq $servidor) {
        throw 'Jupyter não respondeu. Verifique .jupyter-local\servidor.stderr.log.'
    }
    $urlProjeto = $servidor.url + 'lab/tree/GUIA_RAPIDO.md?token=' + $servidor.token
    Set-Content -LiteralPath (Join-Path $pastaRuntime 'url.txt') -Value $urlProjeto -Encoding utf8
    Write-Output ('Jupyter ativo: ' + $servidor.url + 'lab')
    Write-Output 'Abrindo o guia no navegador. Kernel: Python 3.12 (.venv Caruaru).'
    Start-Process $urlProjeto
} finally {
    $env:JUPYTER_RUNTIME_DIR = $runtimeAnterior
}
