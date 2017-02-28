$BulkFormatRoot = "C:\Users\user\Source\Repos\FinDW\DataTier\FinDW_SQL\Staging"
$BulkFormatFilePath = "$BulkFormatRoot\Statement.BulkFormat.xml"
Set-Location -Path $BulkFormatRoot
$Xml = [xml](Get-Content -Path $BulkFormatFilePath)
$FileColumns = $Xml.BCPFORMAT.RECORD.FIELD
$SqlColumns = $Xml.BCPFORMAT.ROW.COLUMN

$table = New-Object System.Collections.ArrayList

foreach($SqlColumn in $SqlColumns)
{
    $column = @{}
    $column.Name = $SqlColumn.NAME
    $column.Type = $SqlColumn.type
    $column.Size = ($FileColumns | Where-Object {$_.ID -eq $SqlColumn.SOURCE} | Select MAX_LENGTH).MAX_LENGTH
    $column.DDL = ''
    if($column.Type -like '*CHAR*')
    {
        $column.DDL = "{0} VARCHAR({1})" -f $column.Name, $column.Size
    }
    elseif($column.Type -like '*INT*')
    {
        $column.DDL = "{0} {1}" -f $column.Name, $column.Type.Replace('SQL','')
    }


    [void]$table.Add($column)
}


$name = "Statement"
$sql = ('CREATE TABLE {0}
(
    {1}' -f $name, $table[0].DDL)

foreach($i in 1..($table.Count-1))
{
    $sql += '
    {0}' -f $table[$i].DDL
}
$sql +='
);'

Write-host $sql

