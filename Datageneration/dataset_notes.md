# General notes
https://spacy.io/usage/training

Kolla på denna för att kontrollera hur modeller ska tränas.

Måste kolla på hur datastrukturen (hittar inte explicit detta) i dokumentationen än. 
Hur de vill att labels ska fungera korrekt. 
________________________________


# Manual transcriptions
## Dialogue Example 1
file 2020-09-01 10.25:25 timestamp: 6:45 - 7:30<br>
Moving entities: Svarte, Godafors, Stillmover, White Force Queen<br>
Locations: Oxelösund, Kränkan, Vinterklasen???

<b>Incoming:</b><br>
V T S oxelösund svartö (svarte??)<br>
|-------------------------|<br>
Identifiering (entity)

<b>Outgoing:</b><br>
Svarte V T S TVÅ TUSEN<br>

<b>Incoming:</b><br>
anchorage away (close of vinterklasen???) outbound for sea no pilot required<br>

<b> Outgoing:</b><br>
Svarte anchor away proceeding outbound for sea. <br>
You have outbound vessle <b><i>Godafors</b></i> approaching vinterklasen and inbound vessle <b><i>Stillmover</i></b> at kränkan sändöhook (sandihook) in korphålet (???)

<b>Incoming:</b><br>
It's okey well understood thank you <br>

<b> Outgoing:</b><br>
Then you have inbound vessle <b><i> White Force (Horse) Queen </i></b> inbound kränkan. <br>

<b>Incoming:</b><br>
<b><i> White Force (Horse) Queen </i></b> inbound approaching kränkan. <br>


## Dialogue Example 2
file 2020-09-01 10.25:25 timestamp: 9:44 - 10.20<br>
Moving entities: [Gerberton, White Force Queen, Stillmover]<br>
Location entities: [Norrköping, Oxelösund, Kränkan]

<b>Incoming:</b><br>
V T S oxelösund gerberton (???) kom <br>

<b> Outgoing:</b><br>
Gerberton V T S oxelösund <br>

<b>Incoming:</b><br>
Pilot onboard anchor away and we proceeding out at sea <br>

<b> Outgoing:</b><br>
Gerberton anchor away and proceeding outbound for sea. You have inbound vessle <b><i>Stillmover kränkan</i></b> inbound for oxelösund. <b><i> White Force (Horse) Queen </i></b> aproaching kränkan inbound for Norrköping.

<b>Incoming:</b><br>
Two ships inbound okej tack. <br>

<b> Outgoing:</b><br>
Godafors 


## Dialogue Example 3
file 2020-09-01 10.25:25 timestamp: 10.20 - 11.16<br>
Moving entities = Godafoss (Godafors), Svart, stillmover, gerberton (gibbelton), sandihook,<br>
Locations = Norrköping, oxelösund, vinterklasen, kränkan
<br>

<b> Outgoing:</b><br>
Godafoss V T S oxelösund <br>

<b>Incoming:</b><br>
Godafoss V T S replying

<b> Outgoing:</b><br>
Yes I can see you have passed vinterklasen you have vessel <b><i>Svarte</i></b> outbound has just hear that ???? proceeding to sea. <b><i>Gerberton (Gibbelton??) (balkenboard????) </i></b> has also hit that anchor proceeding out.
You have <b><i> Sandihook </b></i> in karpoled bound for steel factory. <b><i>Stillmover</b></i> kränkan inbound for oxelösund and <b><i>White Horse(force) Queen</b></i> aproaching kränkan from Norrköping. 

<b>Incoming:</b><br>
eeeh okey V T S two outbound and one crossing the fairway and two inbound thank you for information.

<b> Outgoing:</b><br>
Thank you.

## Dialogue Example 4
file 2020-09-01 10.25:25 timestamp: 11.42 - 11.55<br>
Moving entities =   Heleneck

<b>Incoming:</b><br>
VTS oxelösund (Heleneck?)

<b> Outgoing:</b><br>
Heleneck V T S oxelösund 

<b>Incoming:</b><br>
Heleneck alongside S S A B ki

<b> Outgoing:</b><br>
Heleneck alongside S S A B thank you 

## Dialogue Example 5
file 2020-09-01 10.25:25 timestamp: 12.25 - 12.58<br>
Moving entities = Sweeper
Locations = Mont Rose

<b> Outgoing:</b><br>
Sweeper V T S oxelösund 

<b>Incoming:</b><br>
Sweeper replying

<b> Outgoing:</b><br>
Question are you aware of eh the anchored vessle mont rose in you heading

<b>Incoming:</b><br>
Yes V T S sorry we should have told you we are bound for mont rose for hall (halv) cleaning 

<b> Outgoing:</b><br>
Okey Sweeper that is understood thank you.