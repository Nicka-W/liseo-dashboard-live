# Run once:  powershell -ExecutionPolicy Bypass -File scripts\register_local_autopublish.ps1
$script = Join-Path $PSScriptRoot "run_local_autopublish.pyw"
$pyw = (Get-Command pythonw.exe -ErrorAction Stop).Source
$action = New-ScheduledTaskAction -Execute $pyw -Argument "`"$script`"" -WorkingDirectory (Split-Path $PSScriptRoot)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Liseo Dashboard Auto Publish" -Action $action -Trigger $trigger -Settings $settings -Force
