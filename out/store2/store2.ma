
[top]
components : store2

[store2]
type : cell
dim : (64,100)
delay : transport
defaultDelayTime : 1000
border : nonwrapped

neighbors :           store2(0,-1)
neighbors : store2(-1,0)  store2(0,0)  store2(1,0) 
neighbors :           store2(0,1)

initialValue : 0
initialCellsValue : store2.val
localtransition : rules

[rules]

% ...

rule: {(0,0)}   0   { t }
