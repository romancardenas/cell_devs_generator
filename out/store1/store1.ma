
[top]
components : store1

[store1]
type : cell
dim : (72,100)
delay : transport
defaultDelayTime : 1000
border : nonwrapped

neighbors :           store1(0,-1)
neighbors : store1(-1,0)  store1(0,0)  store1(1,0) 
neighbors :           store1(0,1)

initialValue : 0
initialCellsValue : store1.val
localtransition : rules

[rules]

% ...
rule: {(0,0)}   0   { t }
