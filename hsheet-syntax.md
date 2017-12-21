inside a hierarchical sheet:

# on creation:
```
$Comp
L R R45
U 1 1 5A4BC9D6
P 3950 3100
F 0 "R45" H 4020 3146 50  0000 L CNN
F 1 "R" H 4020 3055 50  0000 L CNN
F 2 "" V 3880 3100 30  0000 C CNN
F 3 "" H 3950 3100 30  0000 C CNN
	1    3950 3100
	1    0    0    -1  
$EndComp
```
# on copy
```
$Comp
L R R45
U 1 1 5A4BC9D6
P 3950 3100
AR Path="/5A4BC762/5A4BC9D6" Ref="R45"  Part="1" <-- this was original reference, added as AR...
AR Path="/5A4BDC69/5A4BC9D6" Ref="R46"  Part="1" <-- this is newly created copy
F 0 "R46" H 4020 3146 50  0000 L CNN  <-- points last created copy, has no meaning (AFAIK)
F 1 "R" H 4020 3055 50  0000 L CNN
F 2 "" V 3880 3100 30  0000 C CNN
F 3 "" H 3950 3100 30  0000 C CNN
	1    3950 3100
	1    0    0    -1  
$EndComp
```
