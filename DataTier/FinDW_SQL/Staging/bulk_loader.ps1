Set-Location -Path "C:\Users\user\Dropbox\FinDW\Data\Loading\holding"


$xml_format_file = "$PSScriptRoot/Statement.BulkFormat.xml"
$bulk_import_log = "$PSScriptRoot/Statement.BulkImport.log"
Remove-Item -Path $bulk_import_log
$flat_files = Get-ChildItem -Filter "*.csv"
foreach($flat_file in $flat_files)
{
    Write-Host $flat_file
    bcp FinDW.Staging.FinancialStatement in "$flat_file" -f $xml_format_file -T -F 2 -e $bulk_import_log
}