# Script to record the current song played by Spotify based on Windows process name
# Source: https://github.com/Trezub/playing-now-spotify

$song = $null
$old_song = $null
while ($true) {
    $processes = Get-Process spotify
    $title = (Out-String -InputObject $processes.mainWindowTitle) -replace "`n","" -replace "`r",""
    if (-Not $title.Contains('Spotify')) {
        $song = $title
    }
    if ($song -ne $old_song -and $song -ne "Drag") {
        $old_song = $song
        $time = Get-Date
        $newrow = [PSCustomObject] @{"timestamp" = $time; "song" = $song}
        $Addr = $newrow
        $Addr | Export-Csv -Path songs.csv -Force -NoTypeInformation -Append
        Write-Output "$time, $song"
    }
    Start-Sleep -Seconds 5
}
