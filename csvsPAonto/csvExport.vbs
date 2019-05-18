'vbs to run excel to csv export macro
Set objExcel = CreateObject("Excel.Application")
objExcel.Application.Run "'C:\Users\Ocker\LRZ Sync+Share\ubuntueXchange\py\csvs\_AgentInitializationV7.3.xlsm'!Modul1.ExportSheetsToCSV"
objExcel.DisplayAlerts = False
objExcel.Application.Quit
Set objExcel = Nothing