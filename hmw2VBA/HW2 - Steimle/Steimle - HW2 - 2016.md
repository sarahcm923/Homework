Sub Button1_3_Click()

'Turn off screen updating so it runs faster
Application.ScreenUpdating = False

Workbooks("Multiple_year_stock_data.XLSm").Activate
Worksheets("2016").Activate
ActiveSheet.Range("A1").Select

'sort columns just in case data source isn't already sorted
Columns("A:G").Sort key1:=Range("A1"), order1:=xlAscending, Header:=xlYes, key2:=Range("B1"), order2:=xlAscending, Header:=xlYes

'create output headers
Range("j1").Value = "Ticker"
Range("K1").Value = "Yearly Change"
Range("L1").Value = "% Change"
Range("M1").Value = "Total Stock Volume"
Range("O2").Value = "Greatest % Increase"
Range("O3").Value = "Greatest % Decrease"
Range("O4").Value = "Greatest Total Volume"
Range("P1").Value = "Ticker"
Range("Q1").Value = "Value"

'define variables
Dim Ticker_Name As String
'Dim Ticker_Date As Date
Dim Ticker_Open As Double
Dim Ticker_High As Double
Dim Ticker_Low As Double
Dim Ticker_Close As Double
Dim Ticker_Year_Change As Double
Dim Ticker_pct_Change As Double
Dim Ticker_Volume As LongLong
Dim i As Integer
i = 2

ActiveSheet.Range("A2").Select
Ticker_Name = ActiveCell.Value
'Ticker_Date = ActiveCell.Offset(0, 1).Value
Ticker_Open = ActiveCell.Offset(0, 2).Value
Ticker_Volume = ActiveCell.Offset(0, 6).Value

'loop through sheet until first column is blank (end of data)
Do While ActiveCell.Value <> ""
Ticker_Name = ActiveCell.Value
'Ticker_Date = ActiveCell.Offset(0, 1).Value
Ticker_Open = ActiveCell.Offset(0, 2).Value
Ticker_Volume = ActiveCell.Offset(0, 6).Value
ActiveCell.Offset(1, 0).Select
 
'loop through cells for the same ticker name
Do While ActiveCell.Value = Ticker_Name
Ticker_Volume = (Ticker_Volume) + (ActiveCell.Offset(0, 6).Value)
ActiveCell.Offset(1, 0).Select
Loop
Ticker_Close = ActiveCell.Offset(-1, 5).Value

Ticker_Year_Change = Ticker_Close - Ticker_Open
Ticker_pct_Change = (Ticker_Year_Change / Ticker_Open) * 100
Ticker_pct_Change = Round(Ticker_pct_Change, 1)

ActiveSheet.Range("J" & i).Value = Ticker_Name
ActiveSheet.Range("K" & i).Value = Ticker_Year_Change

'conditional formatting
If Range("K" & i).Value >= 0 Then
Range("K" & i).Interior.ColorIndex = 10
Else
Range("K" & i).Interior.ColorIndex = 9
End If

ActiveSheet.Range("L" & i).Value = Ticker_pct_Change
ActiveSheet.Range("L" & i).NumberFormat = "0.0"
ActiveSheet.Range("M" & i).Value = Ticker_Volume
i = i + 1

'ActiveCell.Offset(1, 0).Select

Loop

'**BONUS** - Find min/max values for bonus
Dim min_pct_change As Double
Dim max_pct_change As Double
Dim max_stock_vol As Double
Dim min_pct_change_ticker As String
Dim max_pct_change_ticker As String
Dim max_stock_vol_ticker As String

Dim lastrow As Long
lastrow = Cells(Rows.Count, 10).End(xlUp).Row

min_pct_change = Cells(2, 12).Value
max_pct_change = Cells(2, 12).Value
max_stock_vol = Cells(2, 13).Value

For j = 2 To lastrow

    If Cells(j, 12) < min_pct_change Then
    min_pct_change = Cells(j, 12).Value
    min_pct_change_ticker = Cells(j, 10).Value
    End If

    If Cells(j, 12) > max_pct_change Then
    max_pct_change = Cells(j, 12).Value
    max_pct_change_ticker = Cells(j, 10).Value
    End If

    If Cells(j, 13) > max_stock_vol Then
    max_stock_vol = Cells(j, 13).Value
    max_stock_vol_ticker = Cells(j, 10).Value
    End If

Next j

Range("P2").Value = max_pct_change_ticker
Range("P3").Value = min_pct_change_ticker
Range("P4").Value = max_stock_vol_ticker
Range("Q2").Value = max_pct_change
Range("Q3").Value = min_pct_change
Range("Q4").Value = max_stock_vol

End Sub