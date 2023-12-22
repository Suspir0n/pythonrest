function Write-Log($message) {
    Write-Host "$message"
}

function Run-Command($command) {
    Write-Log "Running command: $command"
    try {
        Invoke-Expression $command
    } catch {
        Write-Host "Error: $_"
        exit 1
    }
}

# Get the absolute path of the current script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

try {
    Set-Location "$scriptPath"
} catch {
    Write-Host "Error: $_"
    exit 1
}

# Building the CLI exe pyinstaller command
Run-Command "pyinstaller --onefile --add-data 'pythonrest.py;.' --add-data 'databaseconnector;databaseconnector' --add-data 'domaingenerator;domaingenerator' --add-data 'apigenerator;apigenerator' --collect-submodules typing --collect-submodules re --collect-submodules typer --collect-submodules yaml --collect-submodules parse --collect-submodules mergedeep --collect-submodules pymysql --collect-submodules psycopg2 --collect-submodules psycopg2-binary --collect-submodules pymssql pythonrest.py"

try {
    Move-Item "$scriptPath\dist\pythonrest.exe" "$scriptPath\windowsinstaller" -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

try {
    Set-Location "$scriptPath\windowsinstaller"
} catch {
    Write-Host "Error: $_"
    exit 1
}

# Building the Installer exe pyinstaller command
Run-Command "pyinstaller --onefile --add-data 'pythonrest.exe;.' --add-data 'install_pythonrest.py;.' --add-data 'addpythonresttouserpath.ps1;.' --name PythonRESTInstaller install_pythonrest.py"

# Building the Uninstaller exe pyinstaller command
Run-Command "pyinstaller --onefile --add-data 'uninstall_pythonrest.py;.' --add-data 'removepythonrestfromuserpath.ps1;.' --name PythonRESTUninstaller uninstall_pythonrest.py"

$executablesDir = "$scriptPath\PythonRestExecutables"
if (-not (Test-Path -Path $executablesDir -PathType Container)) {
    Write-Log "Creating PythonRestExecutables directory..."
    try {
        New-Item -ItemType Directory -Force -Path $executablesDir
    } catch {
        Write-Host "Error: $_"
        exit 1
    }
} else {
    Write-Log "Cleaning PythonRestExecutables directory..."
    try {
        Remove-Item -Path "$executablesDir\*" -Force
    } catch {
        Write-Host "Error: $_"
        exit 1
    }
}

# Set location back to the original root directory
Set-Location $scriptPath

try {
    Move-Item "$scriptPath\windowsinstaller\dist\PythonRESTInstaller.exe" "$executablesDir" -Force
    Move-Item "$scriptPath\windowsinstaller\dist\PythonRESTUninstaller.exe" "$executablesDir" -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

# Delete the 'build' and 'dist' folders
try {
    Remove-Item -Path "$scriptPath\build" -Recurse -Force
    Remove-Item -Path "$scriptPath\dist" -Recurse -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

try {
    Remove-Item -Path "$scriptPath\windowsinstaller\build" -Recurse -Force
    Remove-Item -Path "$scriptPath\windowsinstaller\dist" -Recurse -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

# Remove all spec files in the root folder
try {
    Remove-Item -Path "$scriptPath\*.spec" -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

# Remove all spec files in the windowsinstaller folder
try {
    Remove-Item -Path "$scriptPath\windowsinstaller\*.spec" -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

# Remove any remaining exe files in the windowsinstaller folder
try {
    Remove-Item -Path "$scriptPath\windowsinstaller\*.exe" -Force
} catch {
    Write-Host "Error: $_"
    exit 1
}

Write-Log "PythonRestExecutables successfully generated on path $executablesDir"