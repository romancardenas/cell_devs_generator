
[top]
components : carleton_campus

[carleton_campus]
type : cell
dim : (59,100)
delay : transport
defaultDelayTime : 1000
border : nonwrapped

neighbors :           carleton_campus(0,-1)
neighbors : carleton_campus(-1,0)  carleton_campus(0,0)  carleton_campus(1,0) 
neighbors :           carleton_campus(0,1)

initialValue : 0
initialCellsValue : carleton_campus.val
localtransition : rules

[rules]

% ...

rule: {(0,0)}   0   { t }
