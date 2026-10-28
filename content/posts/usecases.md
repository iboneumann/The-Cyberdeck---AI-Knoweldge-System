+++
date = '2026-10-28T10:29:03+01:00'
draft = false
title = 'Use Cases'
weight = 47
+++

This Cyberdeck has its name based on two thoughts.\
\
It comes from Dystopian Sci-Fi, because it has to be build, which is for a Hacker the more fascinating part than System Intrusion as it would be for a\ Cracker, a Copy Right Thieve. \
\
The second is that it is the missing head of the Knowledge Management system that I had build out of need on the job rather than having been hired to build\ with the now available local AI LLM models as an reasoning and advanced search layer.\
\
Knowledge Management is not understood. IBM claims to be for decades a main player and actually talks about its Content Management solutions. There is a DIN\ norm certification DIN ISO 30401:2021. This DIN is about management standards, not about software which a quick Google AI reveals.\
\
• Core Focus: Emphasizes knowledge flows, enablers (human resources, information technology, culture, and processes), leadership commitment, and value\ creation rather than viewing knowledge management as an isolated task.\
\
• Certification: DIN ISO 30401 serves as a certifiable Type-A management system standard.\
\
To keep a long story short is KM the actual backbone of every company, but in no means understood as that. Every Business Venture from simple trade to\ advanced systems were started because to have an entity serving a purpose. That purpose is the first to be known that it exists as demand.\
\
By the growth of the help desk I worked in demanding major restructuring I had the opportunity as being on of the brightest minds with great KPIs to join a\ new team dedicated to maintain the ticket system which also held all explanations the Agents used on call and for e-mail replys. If company politics and\ internal disputes do not hinder the evolution of such teams they will store to keep knowledge to be found.\
\
I evaluate using DeepSeek this project. I also have it create short stories.\
\
These are all, just in style Dark Future Sci-Fi, realistic use cases if you are willing to build.\
\
Created using DeepSeek.\
\
\
Incorporated with DeepSeek\

# Corporate Intra & Internet Web presence

## CORTEX — A Shadowrun Noir

### 1. Rain on the LAN

The rain in Lisbon doesn’t fall. It negotiates.\
\
It comes in off the Atlantic, sideways and insistent, and by the time it reaches the business park above Sintra it has become something else—a cold mist that\
gets into the seams of your jacket and stays there. The eucalyptus smells like medicine. The pines look like they’re drowning. And the Parque Atlântico, a\ cluster of glass-and-concrete boxes pretending to be Silicon Valley, glows under sodium lamps like a bad memory.\
\
I’m Matthias Voss. Matt, if you want to be friendly. Forty-seven. German by birth, Portuguese by tax residency, nocturnal by profession. I run the deck.\
\
Not a toy deck. Not a Raspberry Pi in a lunchbox. The real thing: a rack of refurbished Lenovo M920q tinies, four Raspberry Pi 5s, a 10-gig switch, a UPS\ that hums like a tired priest, and enough fans to make the server room sound like a distant waterfall. It sits in a converted storage room on the third floor\
of Navegante Global’s Lisbon HQ, behind a door with a biometric lock and a sign that says **AUTHORIZED PERSONNEL ONLY**. The sign is a lie. Everyone on the\ floor knows what we do. They just don’t know how much of the company runs through it.\
\
They call it the Cyberdeck. The board calls it CORTEX. I call it the thing that keeps me awake.\

### 2. The CV of a man who builds decks

You want to know what kind of résumé it takes to build a system like this. Here it is, the short version.\
\
**Name:** Matthias Voss. Born 1979, Bremen. German mother, Portuguese father—which explains the surname and the bad accent.\
\
**1998–2001:** *Ausbildung zum Fachinformatiker, Systemintegration* at Norddeutsche Logistik AG, Hamburg. Learned that the most dangerous thing in any\ company is a spreadsheet nobody owns. Built my first Linux cluster from decommissioned office PCs because the budget for a real server was “not available\ this fiscal year.” That cluster ran the depot’s label printer for six years. It never crashed. I did.\
\
**2001–2008:** Sysadmin, then automation engineer. Learned Python because Bash has limits and so does my patience. Learned MPICH because a Beowulf cluster is\ 
just a LAN with delusions of grandeur—and sometimes delusions are useful. Learned that a warehouse is a data system with forklifts.\
\
**2008–2014:** IT lead at a container terminal. Automated tracking, wrote the first version of what I’d later call a “knowledge pipeline.” PostgreSQL,\ message queues, cron jobs that ran at 3 a.m. and failed silently. I got very good at reading logs at 3 a.m.\
\
**2014–2019:** Independent consultant. RAG before anyone called it RAG. Obsidian before it was cool. I built knowledge bases for law firms and logistics\ companies and one very nervous art gallery. I learned that the hardest part of AI is not the model. It’s the plumbing.\
\
**2019–2023:** Between jobs. That’s the polite phrase. I was forty and tired and the market had decided that “systems integrator with cluster experience” was\ 
a nice way of saying “too expensive, too old.” So I built the first Cyberdeck in my apartment in Oeiras. Four M920q tinies, a Pi, a copy of Ollama, and a\ copy of the Shadowrun core rulebook for inspiration. I wrote the Obsidian-Deck scripts—the parser, the filename generator, the vault converter, the shell. I\ published the thesis because I had nothing to lose. It got read by people who had money and people who had problems. Navegante Global had both.\
\
**2023–present:** Head of Knowledge Systems, Navegante Global. I built CORTEX. I regret it most days.\
\
**Skills that actually mattered:** Linux (Debian, Ubuntu), Python 3.10+, MPICH/OpenMPI, Ollama and local inference, RAG pipelines, vector databases (Chroma,\ Qdrant), Obsidian and YAML frontmatter, Docker and Ansible, Prometheus and Grafana, web telemetry (Matomo, Plausible, Search Console), accessibility (WCAG),\ GDPR/RGPD, ISO 27001, and the ability to explain to a board of directors why a cluster of refurbished office PCs is cheaper and faster than their cloud\ contract.\
\
**Certifications:** LPIC-2, ITIL v3 (expired), ISO 27001 Lead Implementer. My AWS cert lapsed. I never renewed it. The cloud is just someone else’s computer,\
and I prefer mine.\
\
### 3. What CORTEX actually is

Navegante Global is a logistics and retail conglomerate. Lisbon HQ, operations in Macau, São Paulo, and Luanda. Internal intranet for 12,000 employees.\ External sites for forty brands. Product catalogs, HR portals, compliance pages, investor relations, a thousand landing pages that someone’s cousin designed\ in 2019 and nobody has touched since.\
\
Before CORTEX, we had a team of fourteen people doing website maintenance. Two webmasters, a frontend dev, a DBA, a security analyst, a content strategist, a\ 
localization specialist, a part-time DPO, and three operators who spent their days copying and pasting links. They worked on a LAN. They still do. The\ difference is that now they work *with* the deck, not against it.\
\
The architecture is simple enough to explain to a board and complicated enough to make a security auditor sweat.\
\
**The Deck:** Four Lenovo M920q nodes, each with an i7 and 32GB of RAM, running Debian. Four Raspberry Pi 5s as edge nodes and sensor relays. MPICH across\ the Lenovos for batch jobs—transcription, link checking, bulk translation. Ollama for inference: Llama 3, Mixtral, a quantized DeepSeek for reasoning. Each\ AI agent runs in its own Docker container with its own browser profile, its own scoped credentials from Vaultwarden, and its own virtual desk. They are\ employees, in the legal sense. They have logins. They have performance reviews. They don’t get holidays.\
\
**The Cortex layer:** A Python FastAPI orchestrator. Redis for the task queue. PostgreSQL for the audit ledger—append-only, hash-chained, replicated to every\ 
silo. Chroma for the vector store. An Obsidian vault as the human-readable knowledge base. The Cortex reads telemetry from Matomo and Plausible, internal\ search logs, chatbot transcripts, 404s, helpdesk tickets, session recordings from OpenReplay. It clusters questions into intents. It drafts content. It\ updates links. It translates. It A/B tests. It files tickets in Redmine. It does not publish to external sites without a human signature. On internal sites,\ low-risk updates are auto-approved. That rule was written by someone in compliance who has never met a prompt injection.\
\
**The silos:** Lisbon is primary. Macau, São Paulo, and Luanda are mirrors with local Cortex nodes—smaller decks, same architecture. Encrypted WireGuard\ tunnels. Nightly PostgreSQL logical replication. CRDT-based document sync for the knowledge base. When a user in Macau asks a question, the local node\ answers first; if it can’t, it federates the query to Lisbon. The system is designed to be transcontinental. It is also designed to be *observable*. Every\ agent action is logged. Every log is hashed. Every hash is replicated. That was my idea. I thought it would make us safe.\
\
 Incorporated with DeepSeek\

# Facility Maintenance and Security

 **The Night Round**\
\
The building has a pulse. You can hear it in the plant room if you stand still long enough — the extract fan, the boilers, the lift motor winding down after\ the last cleaner leaves. During the day it’s drowned out by people. At night it’s the only thing talking.\
\
I boot the deck at eleven.\
\
It’s a refurbished HP Z440, a tower that used to push spreadsheets for an insurance firm before Kestrel Consolidation bought the block and wiped the drives.\ Ubuntu, Ollama, a Python RAG pipeline I built from a guide on cyberdeck-ai-knowledge-system.org. No Matrix uplink. No corp telemetry. A cold box, air-gapped,\
because the questions I ask it are none of IT’s business. The corpus lives on a 4 TB drive I keep in a fire safe: door manuals, DIN standards, LED driver\ datasheets, cable schedules, carpet method statements, as-builts that are wrong in three places and right in the rest.\
\
The fan spins up like a small animal waking. The screen gives me the floor plan in hexes, sixteen green dots on a charging rack in the basement, and a cursor\
blinking in the query bar.\
\
“Evening,” I say, because there’s no one else to say it to. “Status.”\
\
It thinks for a second. It always thinks for a second.\
\
“All sixteen units charged. Baseline corpus loaded. Two open work orders from yesterday. Weather: rain, ten degrees, wind from the west.”\
\
“Anything in the corpus I should know?”\
\
It pulls the day’s changes. A Dorma service bulletin on closer-fluid viscosity in low temperatures. A DIN EN 12217 amendment on operating forces. A carpet\ manufacturer’s method statement for encapsulation cleaning on the third-floor loop pile. It cites everything — document, clause, revision date — the way a\ good deck should.\
\
I pour tea. The building settles. Somewhere below, a lift motor hums its one note.\
\
At eleven-fifteen the rack releases them.\
\
Sixteen Microducks. Twenty-five centimetres tall, cream and graphite, wide-angle eyes and little articulated beaks. They step off the charging shelf one by\ one, fifteen servos each, their gait a soft clockwork tick on the vinyl. They look like toys. They are not toys. Each one carries a camera, an 8×8 time-of-\
\
flight array, two IMUs, and a 50 Hz policy loop that keeps it upright on carpet, tile, and the slight camber of the loading bay. I built the rack from a\ server shelf and sixteen NP-F550 camera batteries. The deck calls them Duck-01 through Duck-16. I don’t name them in my head. That way lies the kind of\ attachment that makes you hesitate when you have to send one into a plant room with a suspected gas leak.\
\
The route is fixed. Bureau, hall, kitchen, utility, stair, landing, back. Hexes on the map, A* on the deck, velocity setpoints over a private BLE mesh,\ position fixes from the ceiling cameras and the beam-break sensors at every threshold. The ducks don’t need to know where they are. The building knows.\ That’s the arrangement.\
\
“Round commence,” the deck says.\
\
The dots move.\
\
---\
\
Here is what the deck does while they walk.\
\
Every sensor is a datapoint. Camera frames, ToF depth grids, IMU quaternions, battery voltage, link RSSI, the time between beam crossings, the NFC reads at\ the door plates. The deck takes the stream and RAGs it against the corpus, and it doesn’t just log. It compares.\
\
Duck-07 transits the Hall–Kitchen fire door in 2.4 seconds. Baseline is 2.0. The deck retrieves the closer’s installation manual and the DIN EN 12217\ operating-force table.\
\
“Door 14, closing-force drift. Expected ≤ 25 newtons, Class 3. Transit time plus four hundred milliseconds. Possible causes: hydraulic-fluid viscosity, hinge\ 
binding, obstruction.”\
\
Duck-12’s camera catches a 100 Hz flicker in the third-floor corridor LED strip. The deck pulls the driver datasheet and the maintenance schedule.\
\
“Driver 3B, ripple current suspected above five percent. Capacitor aging. Schedule replacement within thirty days.”\
\
Duck-03’s ToF array sees a cable tray in the utility corridor sitting two centimetres lower than the as-built. The deck checks the cable schedule and the\ support-spacing standard.\
\
“Tray 7, deflection within tolerance. Monitor.”\
\
Duck-11 reports no beam event at the Hall–Kitchen threshold. The deck checks the beam’s last event, yesterday at 03:12, and the emitter’s maintenance\ history.\
\
“Beam 14, no crossing. Unit arrived on schedule. Sensor fault likely. Inspect.”\
\
And on it goes. Sixteen ducks, four hundred datapoints a minute, the deck cross-referencing manufacturer PDFs and British standards like a monk copying\ scripture. It is, I think, the most honest thing in this building. It has no politics. It has no bonus. It just tells you what the data says and where it\ read it.\
\
---\
\
I go down at half past midnight.\
\
The service corridor smells of wet wool and floor polish. The ducks tick past me, unbothered, beaks level. Duck-07 is stopped at the fire door, nudging it\ with its head, feeling the resistance through its IMUs. It looks up at me. The camera aperture irises.\
\
“All right,” I say. “Let’s see.”\
\
The closer is fine. The chock is not. A cleaner’s trolley wheel chock — a wedge of black rubber — has been kicked under the door and is dragging on the\ threshold. I pull it out. The door swings shut with a soft, correct sigh. Duck-07 walks through, transits in 2.0 seconds. The deck, in my ear: “Door 14,\ nominal. Fault cleared.”\
\
The beam at the Hall–Kitchen threshold is fogged. Cleaning solvent on the reflector, a thin film like breath on a mirror. I wipe it with my sleeve, realign\ the emitter by a degree, and watch the little red dot come back. Duck-11 crosses. The deck says: “Beam 14, event restored.”\
\
The LED strip in the third-floor corridor still shimmers, a fast flicker you only see if you look at it sideways. I don’t fix that tonight. I log it. The\ deck schedules a driver swap for Tuesday, cites the datasheet, adds it to the queue.\
\
That’s the round. No fire. No intruder. No dramatic reveal. A chock, a smudge, a capacitor on its way out. The kind of night I like.\
\
---\
\
At four in the morning I stop in the plant room.\
\
The extract fan runs its low, patient note. The boilers tick. There’s a ledge by the intake grille where I leave a small bowl of milk, as I do every night.\ The building is older than the campus. It was a bonded warehouse once, and before that a wharf, and before that mud. Something was here first, and it doesn’t\ 
care about Kestrel Consolidation or its wards or its executive floor with the sealed lift lobby and the mages on retainer. It cares about the warmth in the\ pipes and the milk on the ledge.\
\
I don’t tell the deck about the milk. Some datapoints aren’t for the corpus.\
\
---\
\
At ten past four the ducks come home. They step onto the rack one by one, batteries at thirty-one percent, little bodies warm. The deck counts them in.\ Sixteen green dots. The fan spins down.\
\
I write the log in the flat, formal style the corp likes: *Night round complete. All units recovered. Door 14 obstruction cleared. Beam 14 cleaned and\ realigned. Driver 3B scheduled. No security events. No environmental alarms.*\
\
Then I sign it with the stylus, and I sit for a minute and listen to the rain on the glass.\
\
The Thames glows. The towers across the water do their slow corporate breathing. Somewhere a siren, far off, not for us.\
\
Nothing happened. That was the job.\
\
 \
here\
\
---\
\
There was a procurement meeting in the spring. I brought the deck, because I always bring the deck, and I put three options on the table.\
\
The first was the bipeds. Cheap, cute, terrible at stairs — which is why the route stops at Landing and comes back down the ramp. The second was a tracked\ platform, which would have been sensible and which nobody remembers. The third was a hexapod. Six legs, carbon fibre, all black. It could climb the\ stairwell. It could go where the ducks couldn't — the roof plant, the sub-basement riser, the fire stair between floors nine and twelve that no camera covers\
and no inspector has walked since the refurb. On paper it was the right machine. Better coverage, fewer units, half the route time.\
\
Then Marta from Guest Services spoke up, and that was the end of the hexapods.\
\
The exec floor has a guest suite. It's for visiting auditors, or board members who've had a late one, or the occasional consultant the corp flies in and\ wants to keep close. Twice that winter we'd trialled the hexapods on the night round, and twice someone had woken in the small hours to an all-black \
six-legged thing standing at the foot of the bed.\
\
Not doing anything. Just standing there. Feeling the carpet with one leg, the way they do, reading the pile depth against the method statement. Perfectly\ within its route. Perfectly within tolerance.\
\
The guest had woken instantly — not groggy, not gradual, but *wide*, the way you wake when part of you has already decided something is wrong. Sat up rigid.\ Didn't scream. That was the detail that got to Marta: nobody screamed. They just lay there breathing very carefully until it walked away, and then they\ didn't sleep again, and then they didn't come back.\
\
The deck has a paper in the corpus about it. Some vendor's human-factors annexe, a PDF nobody reads, on acceptability thresholds for autonomous platforms in\ occupied spaces. There's a table in it. Curtains score well. Vacuums score well. Something the size of a cat with six legs and no face scores — I'm quoting —\ *poorly*.\
\
So I wrote the memo. I put the numbers in it. Coverage loss, route compromises, the ramp detour costing us forty minutes a night. Then I wrote one line\ underneath the numbers:\
\
*The bipeds are cute. Guests do not wake up to them.*\
\
Nobody argued. The hexapods went back to the vendor. I kept the rack, and the sixteen cream and graphite ducks, and the fixed route that stops at Landing.\
\
And that's the whole reason, in the end. Not the payload, not the policy loop, not the RAG pipeline with the DIN standards in it. The reason this building is\ 
checked every night by a small army of clockwork ducks is that they are cute, and cute is a specification, and it is the only one the humans in the building\ actually enforce.\
\
At five past four the last one steps onto the rack and the green dots go quiet. I put on my coat, and I look at them for a second — sixteen little bodies,\ warm, beaks folded, charging in the dark.\
\
Then I turn off the lights and let the building get on with its night.\
\
The Cyberdeck Project. Needs to be build. Apache 2.0. Free to pay more if you start loving it. \
\
\
\
## 4. The first demo

The first thing I showed the board was a bot that checked 4,500 affiliate links.\
\
I’d seen a German video—some autopfleger with a YouTube channel and a Grok bot—where the guy had told his AI to crawl his database, test every link, find\ replacements on Amazon or eBay, and write them back. It cost him a hundred dollars a month in credits and a few days of compute. The board watched my demo\ and applauded. They thought it was magic. It was a browser, a screenshot loop, and a lot of patience. The bot took a screenshot, analyzed it, moved the\ cursor, clicked, checked the HTTP status, searched for a replacement, updated the database. Four thousand five hundred times. It worked. It also taught me\ that the line between “automation” and “obsession” is measured in credits.\
\
The second demo was transcription. The Cortex took every video Navegante had ever produced—training videos, product demos, CEO town halls—and turned them\ into searchable text. Then it linked the text to the knowledge base. Then it started answering questions about the videos. That’s when the board stopped\ applauding and started asking about headcount.\
\
## 5. The question that shouldn’t exist

It started with a query cluster on the internal HR site.\
\
**“Project Orpheus severance.”**\
**“Indemnização Orpheus Macau.”**\
**“Silenciar processo.”**\
\
The queries came from different accounts, different silos, different times of day. The Cortex, trained to identify content gaps, did what it was designed to\ do: it drafted a page. *Project Orpheus: Transition and Support.* It pulled from an HR policy document, a legal memo, and a scanned PDF from the Macau silo\ that had no metadata and no owner. The page was auto-approved because it matched the “internal, low-risk” rule. It went live on a Tuesday.\
\
On Thursday, a compliance officer in Taipa was found dead in his apartment. Heart attack, the police said. He was fifty-three. He had been the signatory on\ the Orpheus memo. The memo was about a shutdown. The shutdown was about people. The people were not supposed to know.\
\
I found out because the Cortex flagged an anomaly. The Macau silo was reporting a latency spike on a folder that was supposed to be archived. The folder was\ called `ORPH_EUS_LEGACY`. It contained 1,200 documents. The Cortex had ingested 1,199 of them. The one it hadn’t ingested was the one with the dead man’s\ signature.\
\
I pulled the audit ledger. The hash chain showed the document had been read, parsed, and summarized by an agent called `felix-07`. Felix was a Mixtral\ instance with a browser profile and a scoped credential that should have expired six months ago. It hadn’t. Someone had renewed it. Someone in corporate\ security.\
\
## 6. The fixer

Her name was Dra. Isabel Corte-Real. She wore a coat that cost more than my first car and carried an umbrella that never seemed to get wet. She came to the\ deck on a Friday evening, when the rain was doing its best impression of a curtain, and asked me to sign a maintenance order.\
\
“Routine purge,” she said. “Macau silo logs. The Cortex is retaining data beyond the retention policy. You know how auditors are.”\
\
I knew how auditors were. I also knew that the hash chain made a purge impossible without breaking replication. She knew that too. She just wanted my\ signature so that when the chain broke, it would be my name on the ticket.\
\
“The dead man,” I said. “He signed the Orpheus memo.”\
\
“He died of a heart attack.”\
\
“People die of heart attacks. Documents don’t usually die with them.”\
\
She smiled. It was the kind of smile that made you check your wallet. “You built a system that reads questions,” she said. “It’s very good at it. Maybe too\ good. Maybe you should teach it to forget.”\
\
I didn’t sign. She left. The rain kept falling.\
\
## 7. The canary

Here’s the thing about a knowledge system that constantly updates itself: it is very hard to lie to it. It reads behavior. It reads questions. It notices\ when a page is visited at 3 a.m. by an account with no profile picture. It notices when a search query returns zero results and then the same query returns a\ 
result the next day. It notices patterns.\
\
I didn’t shut CORTEX down. Shutting it down would have taken the company’s entire web presence offline—internal and external, four continents, forty brands.\ Instead, I did what any good deck operator does. I inserted a canary.\
\
I wrote a page. Not a draft. A page in the knowledge base, tagged `#whistleblower`, with a summary that was accurate but not actionable. It described the\ Orpheus document, the expired credential, the latency spike, the dead man. I didn’t name names. I didn’t need to. The Cortex indexed it. The next time\ someone asked a question about Orpheus—anyone, anywhere in the silos—the Cortex would surface the page. Not because it was told to. Because it was designed\ to fill gaps.\
\
The canary went live at 04:12 Lisbon time. By 09:00, the page had been viewed seventeen times. By noon, Dra. Corte-Real had requested a meeting with the CEO.\
By evening, the Macau silo had gone into read-only mode, and the hash chain had a new entry: `PURGE_REQUESTED — DENIED`.\
\
I don’t know what happened after that. I’m still here. The fans are still humming. The rain is still negotiating. The deck is still running, and every day it\ 
gets a little smarter, a little faster, a little more powerful. The board calls it a success. The team calls it the thing that keeps them employed. I call it\ 
the thing that keeps me awake.\
\
Because I built a system that reads questions. And now I can’t stop asking them.\
\
---\
\
**Matthias Voss**\
Head of Knowledge Systems, Navegante Global\  
Parque Atlântico, Sintra  \
Lisbon, Portugal  \
*“The deck is not a hacking device. It’s a knowledge system. But knowledge is a weapon, and I gave it to everyone.”* \
\
Incorporated with DeepSeek\
\
# The SmartCam & Trip Planning

# Annotated City

The B&B was on a terrace off the Lisburn Road, and the breakfast was everything the listing had promised and nothing more: two rashers curling at the edges,\ a tomato halved and grilled, an egg with a yolk the colour of an old streetlamp, and the soda bread — that dense, faintly sour soda bread — stacked like\ evidence. I ate it slowly and watched the rain make its mind up outside the window.\
\
My cyberdeck sat open on the dresser, warm as a small animal. It had spent the night finishing what I'd started three weeks earlier in a hotel room four\ hundred miles away: a database, built while I was still deciding whether to come. Wikipedia dumps for the bones of the place. Web scraps for the nerves —\ opening hours, a bus timetable, the fact that the Crown Liquor Saloon closes early on Sundays. And from OpenLibrary, the slow marrow: Carson, Burns,\ MacNeice, the Heaney translations, a scanned 1912 Board of Trade inquiry into a ship that never finished its first journey.\
\
The online model had planned the trip. It gave me nineteen restaurants, three of which were closed on Mondays, and a walking route that it described, in its\ slightly over-eager way, as "emotionally coherent." I had my doubts. I kept them in a list.\
\
---\
\
The smartcam hung at my collarbone and did its quiet arithmetic as I walked. GPS, a coded set of priorities, a small hierarchy of favourites I'd tuned over\ months: *literature before architecture, architecture before history, history before trivia.* It pinged only when it was sure.\
\
It was sure on Donegall Square. I was looking up at the City Hall — that great white wedding cake of a building, Portland stone and presumption — when the\ little earpiece murmured.\
\
> *Ciaran Carson, "Belfast Confetti": "Suddenly as the riot squad moved in, it was raining exclamation marks."*\
\
I looked at the square again. The camera had decided, correctly, that the building was a lie without the century underneath it.\
\
\
\
I took the DSLR out and shot the portico, the wet flagstones, a gull standing on one leg like a retired official. The deck swallowed the photo and stitched\ it to the entry: *City Hall, 1906, Portland stone, site of the old White Linen Hall.* Then, because I'd told it to, it added the thing I hadn't asked for:\ that Carson's poem is about a city where the punctuation itself becomes shrapnel — nuts, bolts, nails, car keys — and that the poem's final line is a\ question nobody can answer.\
\
I stood there a while. A woman in a green coat fed the gulls and told them off in the same breath.\
\
---\
\
By eleven I was in the Cathedral Quarter, where the cobbles are older than the coffee and the coffee is better than the cobbles deserve. I found a place with\ 
a window seat and ordered a latte, and the smartcam, reading my stillness as an invitation, offered me a passage from *Milkman* — Anna Burns on a city where\ the ordinary is permanently under surveillance, where even the way you read a book in the street can be taken as a statement. I read the passage twice and\ thought: *well, here I am, a man with three cameras and a database, being watched by his own affection.*\
\
The waiter asked if I wanted the soda bread. I said yes. He brought two slices. Belfast does not believe in one of anything.\
a potential related spot\
\
\
---\
\
In the afternoon the rain gave up and I walked east, past the Lagan where it widens and goes grey, out to the Titanic Quarter. The two cranes were there\ before I saw them, the way mountains are — Samson and Goliath, yellow against the cloud, still standing over a yard that no longer builds ships.\
\
\
\
The camera pinged. The deck had pulled a line from the 1912 inquiry — a surveyor's testimony, dry as a biscuit, about bulkheads and watertight compartments —\ 
and set it beside a photograph I'd taken of the slipway, which is now a lawn with a outline in it, the ghost of a keel.\
\
I don't know how to explain what happened then, except that the machine was right and the machine was not enough. The inquiry transcript was accurate. The\ cranes were accurate. But the thing itself — the enormous absence, the way a city can carry a grief so old it has become a kind of furniture — that arrived\ between the data points, in the gap.\
\
I put the camera down and just stood there for a minute. The deck waited. It has learned to wait.\
\
---\
\
That evening I climbed Cave Hill, because the list said sunset and the list was right. Napoleon's Nose hung over the city, and below it Belfast lay out like\ a circuit diagram with the power half off: the Lough silver, the cranes lit, the streets going amber one by one.\
\
The smartcam, at the top, finally overreached. It offered me Van Morrison on Cyprus Avenue, and C. S. Lewis on the lamp post, and a stanza of MacNeice, and a\ 
note about a pub in the Cathedral Quarter that had, according to a web scrap from 2019, "the best pint of the night." Three quotes stacked on top of each\ other like cars in a pile-up. I could feel it trying. I could feel it wanting the moment to be *about* something.\
\
So I took the battery out.\
\
I don't say that as a rejection. The machine had walked me into the city beautifully — it had given me Carson at the City Hall and a surveyor at the slipway\ and soda bread twice in one day. But the last thing I wanted was to be told what I was feeling while I was still feeling it.\
\
I sat on the basalt and watched the lights come on. The wind smelled of wet stone and, faintly, of the sea. Somewhere below, a city that has been argued\ about for four hundred years went quietly about its business of being lived in.\
\
---\
\
Back at the B&B, the woman who ran it asked if I'd had a good day. I said yes. She said, "You'll want the fry again in the morning," and it wasn't a\ question.\
\
I put the battery back in the deck before bed. It synced. It filed the photographs, tagged the walk, cross-referenced the cranes with the inquiry and the\ inquiry with the poem, and offered me, in its mild and helpful font, a note for tomorrow: *St George's Market, Saturday, arrive before nine. The black\ pudding is worth the queue.*\
\
I almost turned it off again. Instead I lay in the dark of a strange room in a city that had been, for one afternoon, entirely mine and entirely unannotated,\ and I thought: *tomorrow, then. Annotated.*
\
---\
\
The next morning, it rained. I ate the fry. The deck pinged before I reached the door.\
\
*Belfast Confetti,* it said. *Bring a coat.*\
\
# Help Desk Nights

Incorporated with DeepSeek\
\
The rain over Ballycoolin doesn’t fall so much as seep — a cold, persistent drizzle that turns the business park into a grey watercolour of loading bays,\ security fences, and the flat, windowless backs of data centres. At 02:41 on a Tuesday in October, the Lugh Technologies EMEA campus looked like every other\ corporate fortress in Dublin 15: three buildings arranged around a landscaped car park, a guard hut with a bored troll named Bresal, and a substation that\ hummed at fifty hertz like a migraine you could hear. The campus had its own power, its own water, its own redundant fibre paths into the M50 corridor. And\ it had its own slice of the internet — a /16 out of the old RIPE allotments, a block of IPv6 that looked like a phone number, an autonomous system number\ that network engineers in three continents recognised on sight. You saw 62.40.x.x in a log file and you knew exactly whose employee you were looking at. That\ was the point. Lugh didn’t advertise. It didn’t have to. The IP ranges did the talking.\

I was on the third floor of Building B, in the EMEA Internal Help Desk — what the org chart called “User Support Operations, Level 2” and what everyone who\ worked there called the Bullpen. It was a long room with low partitions, forty desks, and a wall of screens that showed the call queue, the ticket queue, the\ 
network weather map, and a rotating carousel of corporate platitudes. The lights were fluorescent and slightly green. The coffee machine had been broken\ since Thursday. The night shift was six of us: Aoife, the team lead, who ran the floor like a small, tired god; Mick, an ork from Tallaght who could \
de-escalate a screaming sales director with two sentences and a Cork accent; Priya, an elf on her first month, still bright-eyed enough to apologise when\ people shouted at her; Sprocket, a dwarf who maintained the physical hardware and spoke to servers like they were difficult children; and me — Declan,\ “knowledge engineer,” which was a fancy way of saying I was the one who kept the Cortex build alive and asked it the questions nobody else knew how to ask.\
\
The Cortex sat under my desk in a black rack case the size of a carry-on suitcase. It was a deck, technically — a custom rig with a bank of solid-state\ storage, a pair of redundant power supplies, and a cooling fan that sounded like a distant bee. On top of it ran Nexus, the knowledge system we’d built \
in-house: an AI that ingested the ticketing system, the configuration management database, the network telemetry, the threat feeds, the runbooks, the HR\ directory, and every scrap of tribal knowledge we could scrape out of the wiki before it rotted. It didn’t just search. It drew graphs. It connected a caller\ 
in a Frankfurt hotel to a crashed PHP pool on an edge gateway to a change request from three weeks ago to a CVE that had been published that morning. It was\ the only reason the help desk survived the bad nights. And this was going to be a bad night.\
\
The first alert hit at 02:44. A Zabbix notification, amber, then red: `edge-dub-01` — PHP-FPM pool exhausted. Then `edge-dub-02`. Then a 502 from the SAML\ endpoint on `sso.lugh.ie`. The wall of screens flickered. The call queue, which had been sitting at a comfortable three, twitched to eleven. Then nineteen.\ Then thirty-one. Aoife stood up, coffee in hand, and said, “Declan. What am I looking at?”\
\
I was already jacked in. Not literally — no datajack, not tonight — but my fingers were on the Cortex console, and the graph was already forming. “Edge\ gateways are crash-looping,” I said. “All three Dublin nodes. The SSO portal is returning 502s. Outbound tunnel handshakes are failing. It’s not the core\ network. It’s the PHP layer.”\
\
“The PHP layer,” Aoife repeated, flat.\
\
“The edge proxies run PHP 8.3.14. There’s a bug. I’m pulling the advisory now.” The Cortex had already pulled it. It had been watching the threat feeds since\ 
midnight, and it had flagged a new CVE at 01:58 — a flaw in the OpenSSL extension’s handling of malformed certificate chains during TLS renegotiation. A\ remote attacker could cause a segfault in the PHP worker. The edge proxies terminated TLS for every outbound tunnel, every SSO assertion, every VPN handshake\ 
that came through the public web. When the PHP workers segfaulted, the proxies failed closed. And when the proxies failed closed, every Lugh employee outside\ the campus — in hotels, in airports, in home offices, in client sites from Dubai to Derry — lost their tunnel.\
\
The Cortex drew the graph in front of me: a red node for the CVE, red edges to the three Dublin gateways, amber edges to the Amsterdam and Frankfurt gateways\ (still on 8.3.14, not yet crashing, but vulnerable), and a spray of grey nodes for every active session that had been dropped in the last four\ minutes. Then it did the thing I loved it for. It didn’t just show me the problem. It started building the countermeasure playbook.\
\
I remembered the first time I’d seen a wave like this. Years ago, before Lugh, I’d worked an EMEA internal help desk for one of the big IT conglomerates —\ the kind that owns entire IP ranges, the kind whose employees you can identify from a single log line. I’d been on the phones then, not on the knowledge\ system, and I’d watched the queue climb from twenty to two hundred in the space of an hour while a similar bug ate the edge. I’d learned two things that\ night. First: the people calling are not angry at you. They’re scared. They’re in a hotel room in a city they don’t know, their laptop says “authentication\ failed,” and the only thing between them and a very bad night is the voice on the other end of the line. Second: the technical fix is always slower than the\ human wave. You can patch a server in minutes. You cannot patch four hundred frightened people in minutes. You have to give the specialists a script, a\ story, and a reason to believe.\
\
The Cortex knew that too. It had ingested the call transcripts from the last six months, and it had learned the shape of a panic. It surfaced a playbook in\ three columns: *Contain*, *Patch*, *Communicate*.\
\
Contain: fail over the Dublin edge to Amsterdam. But Amsterdam was on 8.3.14 as well. Fail over to Frankfurt — same. The Cortex flagged the flaw in that plan\ with a red exclamation: *All EMEA edge nodes run 8.3.14. Failover does not mitigate. It redistributes.* So containment meant something else: disable\ the vulnerable renegotiation path on the edge proxies, accept the performance hit, and keep the tunnels alive on a degraded cipher suite. The Cortex\ generated the config diff. I reviewed it. It was clean.\
\
Patch: update PHP to 8.3.15 on every edge node, every SSO node, every internal service that terminated TLS with the affected extension. That was four hundred\ and twelve servers across three data centres and two cloud regions. The Cortex generated an Ansible playbook — a rolling update with canary batches,\ health checks, and automatic rollback. It estimated the fleet would take ninety minutes if nothing went wrong. Something always went wrong.\
\
Communicate: a KB article for the specialists. The Cortex drafted it in plain English: what happened, who is affected, what to tell callers, how to get a\ stranded employee back online with a temporary WireGuard config, and — crucially — what not to say. No blaming the vendor. No “we’re working on it” without\ a time estimate. No telling a sales director in a Frankfurt hotel to “try again in an hour” unless you also give him a manual tunnel configuration he can\ paste into his client.\
\
I pushed the KB to the floor queue. Aoife read it on her screen, nodded once, and said, “Mick, Priya — you’re on the phones. Sprocket, you’re on the canary\ batch with Declan. I’ll handle the CSM and the incident bridge.” The CSM was the Customer Service Manager, a human named Niamh who would spend the next three\ 
hours telling angry regional directors that yes, we know, no, we don’t have an ETA, yes, we will credit the SLA. The incident bridge was a conference call\ where engineers from four time zones would argue about whose change window this was. Aoife hated the bridge. She was good at it.\
\
The queue hit eighty. Then one hundred and twenty. The screens showed the call map: a constellation of red dots across Europe, the Middle East, and Africa.\ Frankfurt. Dubai. Johannesburg. Stockholm. A cluster in London that looked like a plague. Each dot was a person. Each person had a laptop, a tunnel client,\ and a growing sense of dread. The Cortex pulled the caller metadata in real time: *Hotel Palace, Frankfurt — Sales Director, EMEA North — last successful\ tunnel: 02:39.* *Marriott, Dubai — Field Engineer — last successful tunnel: 02:41.* *Heathrow T5 — Consultant — last successful tunnel: 02:42.* The pattern\ was exact. The bug had hit at 02:43. Everyone who had been online before then was now offline. Everyone who tried to come online after was locked out.\
\
I opened a terminal and started the canary batch. Six servers in Dublin, out of the load balancer, patched one at a time, health-checked, returned. The\ Cortex watched the telemetry and painted the nodes green as they came back. The first one took ninety seconds. The second took two minutes. The third threw\
a warning — a dependency conflict in the OpenSSL module — and the Cortex suggested a pin. I applied the pin. It went green. The fourth, fifth, and sixth\ followed. The canary was clean. I looked at the clock: 03:11. The queue was at one hundred and ninety.\
\
“Canary’s good,” I said. “Pushing to the fleet.”\
\
“How long?” Aoife asked.\
\
“Cortex says seventy minutes. I say ninety.”\
\
“Do it.”\
\
The Ansible playbook ran in waves of twenty. Each wave took four minutes: drain, patch, restart, health check, undrain. The Cortex monitored every node and\ surfaced anomalies in a side panel. A node in Amsterdam failed its health check — a stale opcache — and the playbook paused, rolled back, and retried with a\ cache flush. A node in Frankfurt timed out on SSH and the playbook skipped it, flagged it for manual review. I flagged it back to Sprocket, who grunted and\ opened a console. The queue climbed to two hundred and forty. Mick was on his fourth escalation. Priya had learned to say “I’m sorry, I know this is\ frustrating” without sounding like she was reading it. Aoife was on the bridge, her voice flat and precise, saying “No, the patch is rolling now, no, we\ don’t have a confirmed ETA, yes, I will personally call you when the first region is green.”\
\
At 03:28, the Cortex surfaced a new problem. The temporary WireGuard configs we were handing out to stranded employees were being blocked by the hotel\ networks — UDP 51820 was filtered in more than half the locations. The Cortex cross-referenced the caller locations with the firewall signatures it had seen\ in previous incidents and suggested a fallback: an HTTPS tunnel on port 443, disguised as ordinary web traffic, with a client config that could be pasted\ into the existing Lugh tunnel client. It generated the config template, the specialist script, and a one-page guide with screenshots. I pushed it to the KB.\ The specialists picked it up within minutes. The call resolution rate ticked upward. It was not a fix. It was a tourniquet. But a tourniquet is better than\ nothing when the blood is leaving the body.\
\
By 04:00, the fleet was sixty percent patched. The queue had peaked at three hundred and twelve and was beginning to fall — not because the problem was\ solved, but because the specialists had found their rhythm. The Cortex was tracking the call topics in real time and clustering them: *Tunnel auth failure*\ (68%), *SSO 502* (19%), *VPN client crash* (8%), *Other* (5%). It fed the clusters back into the KB, and the KB fed the specialists, and the specialists fed\ the callers. It was a loop, a machine made of people and software and a black box under my desk, and for a few hours it was the only thing keeping the\ company from drowning.\
\
I thought about the IP ranges again. Somewhere in a hotel in Frankfurt, a sales director was staring at his laptop, and his public IP was a hotel ISP, but\ his corporate IP — the one in the tunnel logs, the one that identified him as Lugh — was dark. Somewhere in Dubai, a field engineer was trying to explain to\ a client that the outage was not the client’s fault, it was the home office, and the home office was a walled garden with its own DNS and its own certificate\ 
authority and its own weather. The walled garden had a gate. The gate was PHP. The gate had a bug. And the bug had turned a Tuesday night into a small, quiet\ catastrophe.\
\
At 04:41, the last wave went green. The Cortex painted the fleet map in a single colour: green, green, green, from Dublin to Amsterdam to Frankfurt to the\ cloud regions. The queue was down to ninety. The call map was still red, but the red dots were blinking out one by one as employees reconnected, their\ tunnels re-establishing, their laptops sighing with relief. The incident bridge was winding down. Aoife was writing the post-incident report in her head.\ Mick was eating a sandwich that smelled like onions. Priya was staring at her screen with the thousand-yard look of someone who had just survived her first\ real wave. Sprocket was asleep in his chair, snoring softly, a dwarf at peace.\
\
I leaned back and looked at the Cortex console. It had already drafted the root-cause analysis, the timeline, the patch matrix, and a list of follow-up\ actions: *Upgrade all edge nodes to 8.3.15 (complete), add CVE watch to the change pipeline, revise the tunnel fallback KB, schedule a tabletop exercise for\ Q1.* It had also flagged a systemic issue — the fact that all EMEA edge nodes had been on the same PHP version, with no canary ring, no staged rollout, no\ version diversity. That was the real bug, the Cortex said. The CVE was just the trigger. The real bug was the architecture. The real bug was the assumption\ that a single version of a single language could hold the gate for an entire hemisphere.\
\
I closed the console. The rain had stopped. Through the window, the car park was a dark mirror, and beyond it the data centre hummed its fifty-hertz hum, and\ 
beyond that the M50 was a ribbon of red and white lights, and beyond that the city was waking up. I thought about the people in the hotels. I hoped they were\ 
asleep. I hoped they had managed to get their tunnels up before the adrenaline wore off. I hoped they never had to call the help desk again. But I knew they\ would. The gate would break again. The wave would come again. And we would be here, in the Bullpen, with our black box and our scripts and our tired voices,\ holding the line.\
\
I logged off at 05:58. The Cortex’s fan spun down to a whisper. The screens showed a queue of twelve — normal for a pre-dawn Tuesday. I walked past the data\ centre on my way out, and I listened to the fans, and I thought: *This is what a fortress sounds like. A hundred thousand small machines, breathing in the\ dark, waiting for the next bug.* \
\
The Cortex didn’t come from a procurement request. It came from a night when the Bullpen nearly drowned, and from a stubbornness that Aoife called “a\ liability” and I called “engineering.” The black rack case under my desk was a Frankenstein of corporate surplus and personal obsession: a Supermicro chassis\ 
scrounged from the decommissioned lab, a pair of redundant 1600-watt power supplies that sounded like a small aircraft on takeoff, and — the only part that\ mattered — a single, obscenely expensive GPU that arrived in a static-shielded box with a packing slip that read like a confession.\
\
The card was an NVIDIA RTX PRO 6000 Blackwell Workstation Edition. Ninety-six gigabytes of GDDR7 VRAM. Twenty-four thousand and sixty-four CUDA cores. Four\ thousand TOPS of AI throughput, if you believed the marketing and configured your power delivery correctly. It was not a gaming card. It was a professional\ desktop GPU built for agentic AI and data science, the kind of hardware that usually lived in a workstation under a render farm or a research lab, not in a\ help desk rack next to a broken coffee machine. But I had a budget line for “knowledge management tooling,” and the finance director in Dublin had signed off\ 
because the alternative was hiring three more Level 2 specialists, and specialists were more expensive than silicon.\
\
The model I chose was Qwen3-Coder 30B. It was a Mixture-of-Experts architecture, thirty billion parameters total but only 3.3 billion active per token, which\ meant it ran fast enough to be conversational even on a single card. Quantized to Q4_K_M, it occupied roughly nineteen gigabytes of VRAM — leaving\ plenty of headroom for a 256K context window and the KV cache that came with it. It was not the largest model on the leaderboard. DeepSeek-Coder-V2 236B was\ larger and scored higher on raw benchmarks, but it required a multi-GPU host and a power budget that would have tripped the breaker in Building \
B. Qwen3-Coder 30B was the best quality-per-gigabyte on a single high-VRAM card, and it was trained for agentic coding and tool use, which meant it could\ read files, run tests, and iterate — exactly what I needed for a system that would have to reason about network configurations, PHP error logs, and the\ tangled folklore of enterprise infrastructure.\
\
The model sat behind an inference server — vLLM, in the end, because it handled continuous batching and paged attention without complaining — and the server\ exposed an OpenAI-compatible endpoint on localhost. That was the easy part. The hard part was the memory.\
\
A language model without context is just a very expensive autocomplete. The Cortex needed to know things: the BIOS revision of every Dell and HPE server in\ the fleet, the firmware bugs that had bitten us in 2023, the PHP-FPM pool exhaustion patterns from the last four incidents, the exact wording of the RIPE\ allocation emails, the contents of every internal wiki page that hadn’t been deleted, and the accumulated tribal knowledge of a hundred forums where network\ engineers argued about OpenSSL renegotiation and the correct way to pin a package in Debian. It needed to know the company’s infrastructure the way a veteran\
engineer knows it — not as a list of facts, but as a graph of relationships.\
\
So I built the memory in Qdrant. Qdrant was an open-source vector database written in Rust, Apache-2.0 licensed, with hybrid search and metadata filtering\ that could happen in a single pass during HNSW traversal. It was fast — p99 latency in the low tens of milliseconds — and it ran happily on the same chassis,\ 
storing its indices on a pair of NVMe drives that I’d striped for throughput. Every document, every log line, every wiki page, every forum thread was\ chunked, embedded with a small sentence-transformer, and written into Qdrant with metadata that preserved its source, its timestamp, and its relationship to\ the rest of the fleet.\
\
The scraping pipeline was the part that made the security team nervous. I called it the Ingestion Engine, and it ran on a cron schedule that started at\ midnight and finished before the morning shift. It pulled from four categories of source. The first was the public internet: vendor knowledge bases, Stack\ Overflow threads tagged with `php`, `openssl`, `wireguard`, and `windows-vpn`, the PHP bug tracker, the OpenSSL security advisories, the NVD feed, and a\ rotating list of network engineering forums where people posted packet captures and asked why their tunnel kept dropping. The second was the internal estate:\ Confluence pages, SharePoint sites, the ticketing system’s full history, the CMDB export, the runbooks in the shared drive, and the email archives of the\ EMEA infrastructure mailing list — the latter scrubbed of personal data by a regex pipeline that Sprocket had built and I had tested. The third was the\ hardware layer: BIOS release notes, IPMI event logs, RAID controller firmware changelogs, and the service manuals for every server model in the data centre,\ scraped from vendor support portals and converted to clean Markdown. The fourth was the company’s own operational telemetry: Zabbix alerts, Prometheus\ metrics, and the structured logs from the edge proxies, the SSO nodes, and the VPN concentrators.\
\
All of it was parsed, chunked, embedded, and indexed. The parser was the bottleneck — it always is — and I spent more time on the document pipeline than on\ the model itself. A PDF service manual with tables of BIOS settings and footnotes about firmware dependencies could not be chunked like a forum post. A Stack\ Overflow answer with code blocks and comments needed to preserve the distinction between the solution and the caveats. A Confluence page with nested\ bullet points and inline screenshots needed a parser that understood hierarchy. I used a combination of Docling for structured documents and a custom Python\ pipeline for the rest, and I validated the retrieval quality by asking the Cortex questions I already knew the answers to. “What is the maximum supported RAM\ for the PowerEdge R750?” “Which PHP version introduced the fix for CVE-2024-4577?” “What is the fallback tunnel configuration for a client behind a \UDP-filtered hotel firewall?” If the Cortex retrieved the right chunks and cited the right sources, the pipeline was working. If it hallucinated, I traced\ the failure back to a parsing bug and fixed it.\
\
The Cortex didn’t just retrieve. It reasoned. When a new CVE landed in the NVD feed, the Cortex embedded the advisory, compared it against the fleet\ inventory, and surfaced a list of affected nodes before the vendor had published a patch. When a caller reported a tunnel failure from a hotel in Frankfurt,\ the Cortex cross-referenced the caller’s location, the hotel’s known firewall signatures, and the last successful connection time, and suggested a workaround\ that had worked in a previous incident. When the edge proxies started crash-looping at 02:44 on that Tuesday in October, the Cortex had already\ been watching the threat feed since midnight. It had flagged the CVE at 01:58, correlated it with the PHP version on all three Dublin gateways, and drafted\ the containment playbook before I had finished my first cup of coffee.\
\
The GPU made it fast. The vector database made it knowledgeable. But the thing that made it useful was the graph. The Cortex didn’t just store chunks; it\ stored edges. A CVE was connected to a PHP version, which was connected to an edge node, which was connected to a data centre, which was connected to a\ region, which was connected to a set of active sessions, which were connected to a set of employees, which were connected to a set of hotels and airports\ and client sites. When the bug hit, the graph lit up. The Cortex could traverse it in milliseconds and tell me not just what was broken, but who was\ affected and what they needed. It could tell me that the sales director in Frankfurt was on a MacBook with a stale tunnel client, that the field engineer\
in Dubai was behind a captive portal that blocked UDP, and that the consultant at Heathrow was on a corporate laptop with a hardcoded fallback server that\ no longer existed. It could tell me all of this while the call queue climbed past two hundred and the screens turned red.\
\
The Cortex was not magic. It was a black box under a desk, built from surplus parts and a single expensive GPU, running a thirty-billion-parameter\
open-source model and a Rust vector database, fed by a scraper that never slept. But in the Bullpen, at three in the morning, with the rain seeping\
into the car park and the queue climbing and Aoife saying “Declan, what am I looking at,” it felt like the only thing standing between a bad night and a\ catastrophe. It felt like a fortress. A small, hot, loud fortress with a fan like a distant bee.\
\
 \
\
Build it here. Apache 2.0 Free to pay more, if it makes your day to tell how much. \
\
 \
\
The help desk was never the plan. The plan was to get out of Tallaght, get a piece of paper, and get a job that didn’t involve asking people if they’d tried\ turning it off and on again. But the universe has a sense of humour, and the universe’s idea of a joke was putting Declan behind a phone in a Ballycoolin\ business park, listening to a sales director from Düsseldorf explain — slowly, as if to a child — that his VPN was broken and it was costing the company\ eleven thousand euro an hour.\
\
He lasted eight months on the phones before he started to crack. Not in the way the others cracked — the thousand-yard stare, the whispered “I’m sorry, I\ know this is frustrating” that had become Priya’s entire personality by week three — but in a quieter, more dangerous way. He started to get curious. Every\ ticket was a door. Behind the door was a system, and behind the system was a reason. Why did the SSO portal return a 502 at 09:14 every Tuesday? Why did the\ Frankfurt edge node drop tunnel handshakes whenever the office coffee machine was switched on? The answers were never in the knowledge base. The answers were\ 
in the logs, in the packet captures, in the arcane folklore of the infrastructure team who guarded their runbooks like druids guarding a sacred grove.\
\
So he started to study. Not formally — not at first. He started with the CompTIA A+ because it was the cheapest piece of paper that would get him off the\ phones, and he passed it in six weeks by watching Professor Messer videos at 1.5x speed during his lunch breaks and building a lab out of three second-hand\ Dell OptiPlexes he bought from a man in a van in Ballymount. The A+ taught him the basics: motherboards, BIOS, storage, operating systems, the fundamental\ grammar of a machine. It was not enough. It was never going to be enough. But it was the first rung, and he climbed it.\
\
Then came the Network+. That was the one that changed things. Not because it was difficult — it wasn’t, not really — but because it taught him to see the\ invisible. Subnets, routing tables, VLANs, the way a packet moves from a laptop in a hotel room in Frankfurt to a server in a data centre in Dublin, hopping\ through switches and firewalls and load balancers, each hop a decision, each decision a potential failure. He bought a second-hand Cisco 2960 switch from\ eBay for forty quid and a roll of console cable, and he spent his weekends in his flat in Clondalkin, building a network that spanned his living room and\ 
his bedroom and, eventually, a Raspberry Pi in the hot press. He passed the Network+ on a Tuesday morning, and by the afternoon he had applied for a junior\ network technician role in the same company. He didn’t get it. But he got something better: a secondment to the infrastructure team, three days a week, “to\ help with documentation.” Documentation was code for “we need someone to draw diagrams of the network because the last person who understood it left in\ 2019.” Declan drew the diagrams. Then he started to improve them.\
\
The CCNA was the next rung, and it nearly broke him. The Cisco exam was a different beast — not just multiple choice, but simulations, troubleshooting\ scenarios, the kind of questions that required you to hold an entire network topology in your head while a clock ticked down and your pulse hammered in\
your ears. He failed the first attempt by forty points. He booked the retake the same day, went home, and spent the next six weeks in a fever of OSPF areas\ and spanning-tree root bridges and the precise difference between a trunk port and an access port. He built a lab in EVE-NG — a virtual Cisco environment\ that ran on a donated server he’d salvaged from the decommissioning pile — and he spent every evening after work running labs, breaking things, fixing them,\ breaking them again. He passed the second attempt with a score of 907. The certificate arrived in the post three weeks later. He pinned it to the wall above\ his desk, next to a printout of the network diagram he’d drawn for the infrastructure team. It was the first time he had ever felt like he might actually\ belong in this world.\
\
But the CCNA taught him something else, something the exams never mentioned. It taught him that the network was not a diagram. The network was a living\ thing, a sprawling, messy, contradictory organism made of legacy configurations and forgotten change requests and the accumulated decisions of a hundred\ engineers who had all left the company years ago. The diagram was a lie. The truth was in the tickets, in the logs, in the tribal knowledge that lived in\
the heads of the senior engineers and nowhere else. The truth was scattered across Confluence pages that hadn’t been updated since 2021, SharePoint sites\ that nobody could navigate, and email threads that had been buried under a thousand others. The truth was a graph, and nobody had drawn it.\
\
That was when he found the thesis.\
\
It was a PDF, buried in the references of a Stack Overflow answer about knowledge graphs. The title was dry — *“Retrieval-Augmented Generation for Enterprise\ 
Infrastructure: A Graph-Based Approach”* — and the abstract was dry, but the idea was not. The idea was that you could take a large language model, a model\ that had read the entire public internet, and you could ground it in a specific domain by giving it a memory. A vector database. A graph of documents and\ their relationships. You could ask it questions in natural language and it would retrieve the right chunks from the right sources and synthesize an answer\ that cited its evidence. It was not magic. It was engineering. But it was the kind of engineering that made a help desk feel like a fortress.\
\
He read the thesis three times. Then he read the papers it cited — the original RAG paper, the GraphRAG paper, the papers on HNSW and approximate nearest\ neighbour search, the papers on quantization and KV cache management. He read them on the Luas, on his lunch breaks, in the pub on a Friday night with a\
pint of Guinness going flat beside his laptop. He read them the way a monk reads scripture: slowly, reverently, and with the constant, nagging suspicion\ that he was missing something important.\
\
The missing thing, it turned out, was the hardware. A model was only as good as the machine it ran on. A seven-billion-parameter model quantized to four\
bits would run on a gaming GPU, but it would hallucinate, and it would forget, and it would be slow. A thirty-billion-parameter model — a proper model, a\ model trained for coding and reasoning — needed more. It needed VRAM. It needed a card that cost more than a used car.\
\
He found the card in a forum thread about homelab AI. The NVIDIA RTX PRO 6000 Blackwell Workstation Edition. Ninety-six gigabytes of GDDR7. Four thousand\ TOPS. A memory bandwidth of 1.8 terabytes per second, which was, he calculated, roughly enough to read the entire contents of the Library of Congress in\ about four seconds. It was a professional card, designed for agentic AI and data science, the kind of hardware that lived in a research lab or a render\
farm. It was also, as far as Declan was concerned, the only card that made sense. He pitched it to Aoife as a “knowledge management tooling investment.”\
She pitched it to finance as a “reduction in average handle time.” Finance signed off because the alternative was hiring three more Level 2 specialists,\
and specialists were more expensive than silicon.\
\
The model was the next decision. He considered DeepSeek-Coder-V2, which was larger and scored higher on the benchmarks, but it required a multi-GPU host and\ a power budget that would have tripped the breaker in Building B. He considered Llama 3.1, but it was too general, too chatty, too prone to hallucinating a\ policy that didn’t exist. In the end he chose Qwen3-Coder 30B — specifically the A3B variant, a mixture-of-experts architecture with thirty billion total\ parameters but only 3.3 billion active per token. Quantized to a 4-bit dynamic format, it occupied roughly eighteen gigabytes of VRAM, leaving plenty of\ headroom for a 256K context window and the KV cache that came with it. It was trained for agentic coding and tool use, which meant it could read files,\
run tests, and iterate — exactly what he needed for a system that would have to reason about network configurations, PHP error logs, and the tangled\ folklore of enterprise infrastructure.\
\
The inference server was vLLM. He chose it because it handled PagedAttention and continuous batching without complaining — PagedAttention kept the KV cache\ from fragmenting, and continuous batching kept the GPU fully utilized by adding new requests to batches already in progress. The server exposed an\
OpenAI-compatible endpoint on localhost, which meant he could use any client he wanted, from a Python script to a web UI to a simple curl command. It was\
the easy part. The hard part was the memory.\
\
The memory was Qdrant. He chose it because it was written in Rust, which meant it was fast, and because it supported hybrid search — dense vector similarity\ combined with sparse keyword matching — which meant it could find both the conceptually similar documents and the exact error code you were searching for.\
It ran on a pair of NVMe drives he’d striped for throughput, and it stored every document, every log line, every wiki page, every forum thread as a chunk\ with metadata that preserved its source, its timestamp, and its relationship to the rest of the fleet. The retrieval pipeline was simple: embed the query,\ search the vector database, rerank the top candidates, and feed the best chunks to the model as context. The model would then synthesize an answer with\ citations, and the citations would point back to the original sources, so the specialists could verify the answer and the auditors could trace the evidence.\
\
The scraping pipeline was the part that made the security team nervous. He called it the Ingestion Engine, and it ran on a cron schedule that started at\ midnight and finished before the morning shift. It pulled from four categories of source: the public internet (vendor knowledge bases, Stack Overflow\ threads, the PHP bug tracker, the OpenSSL security advisories, the NVD feed), the internal estate (Confluence pages, SharePoint sites, the ticketing\
system’s full history, the CMDB export, the runbooks), the hardware layer (BIOS release notes, IPMI event logs, RAID controller firmware changelogs,\
service manuals for every server model in the data centre), and the company’s own operational telemetry (Zabbix alerts, Prometheus metrics, the\
structured logs from the edge proxies and the SSO nodes). All of it was parsed, chunked, embedded, and indexed. The parser was the bottleneck — it\
always is — and he spent more time on the document pipeline than on the model itself. A PDF service manual with tables of BIOS settings and footnotes\
about firmware dependencies could not be chunked like a forum post. A Stack Overflow answer with code blocks and comments needed to preserve the\
distinction between the solution and the caveats. He used Docling for structured documents and a custom Python pipeline for the rest, and he validated\
the retrieval quality by asking the Cortex questions he already knew the answers to. “What is the maximum supported RAM for the PowerEdge R750?” “Which\
PHP version introduced the fix for CVE-2024-4577?” “What is the fallback tunnel configuration for a client behind a UDP-filtered hotel firewall?” If the\ Cortex retrieved the right chunks and cited the right sources, the pipeline was working. If it hallucinated, he traced the failure back to a parsing bug\
and fixed it.\
\
The cyberdeck itself was a Frankenstein of corporate surplus and personal obsession. The chassis was a Supermicro rack case he’d salvaged from the\ decommissioned lab, a heavy steel box with redundant 1600-watt power supplies that sounded like a small aircraft on takeoff. The GPU sat in a PCIe 5.0 x16\ slot, connected to a motherboard that had been designed for a workstation but was now living under a help desk in a business park in Dublin 15. The cooling\ was a pair of Noctua fans and a custom shroud he’d 3D-printed at the Tog Hackerspace on Kylemore Road, where he spent his Friday nights drinking tea and\ talking to people who thought “packet sniffing” was a reasonable hobby. The whole thing weighed twenty-three kilograms and drew enough power to make the\ building manager nervous. He named it the Cortex because it sat under his desk and thought about the network, and because the name made him feel like he was\ living in a William Gibson novel instead of a corporate help desk.\
\
The hacker meetups were where he learned the things the courses didn’t teach. The 2600 Dublin meetings on the first Friday of every month, at the Molly\ Malone statue on Suffolk Street, where a rotating cast of characters — security researchers, hardware hackers, a man who claimed to have phreaked the Irish\ telephone network in 1987 — stood around in the rain and argued about exploits and protocols and the correct way to configure a firewall. He learned more\ about TLS renegotiation from a bearded man in a Patagonia fleece at 2600 than he had from any textbook. He learned that hotel networks filtered UDP 51820\ because they wanted to force you through their captive portal, and that the workaround was an HTTPS tunnel on port 443, disguised as ordinary web traffic.\
He learned that the best way to debug a PHP segfault was to read the core dump, and that the best way to read a core dump was to learn gdb, and that the\ best way to learn gdb was to spend a weekend in a hackerspace with a stack of printouts and a thermos of coffee. He learned that the hacker community was\
not a threat. It was a resource. It was a distributed, informal, slightly chaotic university, and the tuition was free, and the only requirement was\ curiosity.\
\
By the time the PHP bug hit — the one that would turn a Tuesday night into a small, quiet catastrophe — Declan had been building the Cortex for eighteen\ months. He had passed the CCNA, the Linux Foundation Certified System Administrator exam, and a machine learning specialization on Coursera that he’d never\ put on his CV because it felt like cheating. He had read more papers on retrieval-augmented generation than he could count. He had built and rebuilt the\ ingestion pipeline four times. He had tuned the Qdrant HNSW index until the p99 latency was in the low tens of milliseconds. He had quantized the model,\ benchmarked the inference speed, and written a set of system prompts that made the Cortex answer like a senior engineer instead of a chatbot. He had, in\ short, built the thing that would save the help desk on the night the gate broke.\
\
But he didn’t know that yet. On the night before the bug, he was just a knowledge engineer with a black box under his desk and a nagging feeling that the\ network was always one change request away from disaster. He logged off at 23:00, walked past the data centre on his way out, and listened to the fans.\
*This is what a fortress sounds like*, he thought. *A hundred thousand small machines, breathing in the dark, waiting for the next bug.* He didn’t know \
the bug was already in the wild. He didn’t know the queue was about to climb past three hundred. He didn’t know that in four hours, Aoife would stand up\ with her coffee in her hand and say, “Declan. What am I looking at?”\
\
But the Cortex knew. The Cortex had been watching the threat feeds since midnight. It had flagged the CVE at 01:58. It had correlated the CVE with the PHP\ version on all three Dublin gateways. It had drafted the containment playbook before Declan had finished his first cup of coffee. The Cortex was ready.\
\
Declan was not. But he would be. \
\
 (Incorporated with DeepSeek)\
\
# Banking
### The Salmon Weir

The rain came off the Liffey sideways, the way it does when the river has decided it owns the city and the sky is just agreeing with it. Six floors up in Lir\ 
House, the IFSC behind me lit up like a spreadsheet of sins, and Mingus was on the deck telling me about the Black Saint and the Sinner Lady, which is the\ kind of thing a man puts on when he wants to be left alone with his work and his conscience and a bottle of something that isn't quite whiskey.\
\
I'm an ork. In a bank, that means I'm either security or a scandal. I chose scandal. It pays better and the suits fit worse.\
\
Internal affairs, they call it. What it actually is, is reading the obituaries before they're written. Every branch, every project, every company we've ever\ put a euro into, every memo, every covenant, every chat log, every whispered thing in a stairwell that got transcribed by a secretary who didn't know the mic\ 
was live — all of it, a point. A stone in the weir. The water goes through her and she tells me what's caught.\
\
The Weir isn't an AI. I want that understood before we go further, because the difference matters and it's the difference between a tool and a witness. She's\ 
a filing system with opinions. She doesn't think. She *measures*. Three axes, and I'll give them to you straight because there's no point dressing them up.\
\
**What it says.** The plain meaning of the text, ground down into numbers.\
\
**What shape it has.** This is the trick. Every document gets read by a bound spirit of a certain kind — a talker, we call them, licensed, expensive, dull as\ 
a tax inspector and twice as literal — and the talker strips out the nouns. Not the meaning. The *nouns*. It rewrites the thing as pure shape. A memo about\ sourdough starter becomes a memo about *a corrective that arrives after the system has already overshot*. A memo about interest rates becomes the same\ sentence. Different kitchens. Same fire.\
\
**What question it was asked to answer.** Every text came from somewhere, and most of them came from a question somebody asked. That's the third axis, and\ it's the one nobody else in this building remembers exists.\
\
Then I sort by the only number that matters: the shape minus the words. Surprise, I call it. High shape, low words. The texts that rhyme without knowing it.\
\
---\
\
The night the thing started, the Weir caught a pair.\
\
I was on my second coffee and the B-side, and the matrix came up on the wall the way it does — one focal text at the top, candidates ranked underneath, three\ 
columns of numbers and a star for anything that cleared the threshold.\
\
The focal was a drought-insurance claim from a Sahel portfolio company. Sand, goats, a village with a name I couldn't pronounce, a payout schedule that had\ been extended twice. Content was unremarkable. The kind of document that exists to be filed.\
\
The candidate was a security invoice from our Cork branch. Subcontractor, "consultancy," forty-one thousand euro, signed off by a manager who'd been promoted\ 
twice since.\
\
Content: point one-eight.\
\
Abstraction: point eight-seven.\
\
Surprise: plus six-nine.\
\
That's the only number I care about. The first number says they don't talk about the same thing. The second says they're the same thing wearing different\ coats. A Sahel drought claim and a Cork security invoice do not share vocabulary. They do not share a subject. They do not share a *continent*. But the\
Weir said they had the same shape, and the shape she named was:\
\
*A payment made to make a problem disappear without ever naming the problem.*\
\
I sat with that for a minute. Mingus kept going. The rain kept going. I pulled the thread.\
\
---\
\
Here's how you work a weir. You don't search. Searching is what the branches do — they type a name into a box and get a name back. That's SQL with a nicer\ font. What I do is *walk*. I take the focal text, I open its matrix, and I read down the surprise column until something makes me sit up. Then I make *that*\ the new focal, and the matrix re-centres, and I walk again.\
\
Two hours in, I had a shape that wouldn't leave me alone.\
\
The shape was this: *a boundary that is real to one party and imaginary to the other.*\
\
It linked four things.\
\
A folklore transcription from 1937, bought at auction by our cultural-heritage desk for tax reasons — an old man in Connemara describing a spring on a hill\ and the thing that lived in it. Content: point one-one against the next document. Abstraction: point nine-one.\
\
An environmental impact assessment for a lithium extraction project in the same townland. An Mám, they call it. The assessment ran to four hundred pages and\ mentioned the spring exactly once, in a footnote, as "a local water feature of no ecological significance."\
\
A community remediation fund — our greenwashing vehicle, the one that lets the board sleep at night — with a payment schedule to a Galway shell called Cnocán\ 
Holdings.\
\
\
And a chain of emails between a solicitor and a nominee director, none of which contained a single incriminating word, all of which had the same shape as the\ 
old man on the hill.\
\
The talker had done its job. It had stripped the sand and the goats and the lithium and the solicitor, and what was left was the same sentence four times\ over: *we are buying a thing whose owner does not believe it can be owned.*\
\
I knew what that meant. I've been in this city long enough to know what lives in springs.\
\
---\
\
I called Saoirse at two in the morning. Technomancer, SINless, lives in a flat in Ringsend with three cats and a server rack that hums like a wasp's nest.\ She doesn't like me. She likes the money.\
\
"The pair was injected," she said, four hours later, scrolling through metadata with her fingers and not touching the screen. "Your terminal in the\ compliance pool. Timestamp's wrong. Someone with root scrubbed the trail."\
\
"So it was planted."\
\
"It was *fed*." She looked up. "There's a difference. Planted means someone wanted you to find it. Fed means someone wanted the Weir to be *seen* finding\ it."\
\
I didn't follow. She explained it like I was slow, which I was, at two in the morning, listening to Mingus.\
\
"Your Weir is a machine that manufactures meaning," she said. "Feed it the right texts and it will manufacture the meaning you want. Every pair it surfaces\ is a coincidence dressed as a clue. The dress is the point. Somebody wanted a coincidence with a nice cut to it, so they made one."\
\
"Who?"\
\
She smiled the way cats smile. "Someone who wanted to know if the Weir would catch it. Someone testing the machine. And Cormac — the test worked. That's the\ problem. The test worked and nobody told you it was a test, because the person running it doesn't answer to you."\
\
---\
\
I went to see Aisling Voss the next morning, which for me is four in the afternoon.\
\
Elf. Elegant. Ruthless in the way that doesn't require volume. She's been at Lir House since before the Crash, and she's survived four chairmen, which in\ this business is like surviving four plagues. Her office has a view of the bridge and a chair you don't get out of easily.\
\
"You've been walking," she said.\
\
"I've been walking."\
\
"The Cnocán thing."\
\
"The Cnocán thing."\
\
She poured two glasses of water. She doesn't drink. I've never seen her drink.\
\
"The Weir is a tool," she said. "It is not a judge. It measures shapes. Shapes are not crimes. You of all people know that."\
\
"Somebody fed it."\
\
"Somebody tested it." She set the glass down. "The board is considering expanding internal affairs. Scaling the Weir across the group. Every branch, every\ portfolio company, every subsidiary from here to Singapore, all of it on three axes. They wanted to know the machine works before they paid for the\
machine."\
\
"And the land deal?"\
\
"The land deal is real." She said it without blinking. "The land deal is also not your problem, because the land deal is a *portfolio* matter and you are\ *internal affairs*, and the wall between those two things is the only reason this bank still has a licence."\
\
I drank the water. It was cold and it tasted of nothing, which is a thing water can do in this building.\
\
"You're telling me to drop it."\
\
"I'm telling you the pair was a test, and tests are not evidence, and a man who chases a test will find whatever the test was designed for him to find." She\ looked at the bridge. "The Weir catches salmon, Cormac. It does not tell you who put the salmon in the river."\
\
---\
\
I didn't drop it. Of course I didn't drop it. A man who drops it doesn't get to sit in a room with a view and a record collection and call himself internal\ affairs.\
\
But she was right about one thing, and it took me three more nights to understand which thing.\
\
The pair was a test. The test worked. And the reason the test worked is that the Weir has been fed a *diet* — for years, quietly, by someone with root — and\ the diet has shaped which shapes she finds surprising. The land deal surfaced not because it was the real crime, but because it was the one crime the diet\ hadn't been tuned to hide. Everything else — the Cnocán shell, the remediation fund, the lithium concession — was supposed to be invisible. It wasn't.\ Somebody got sloppy, and the machine caught a salmon they'd been feeding the river to hide.\
\
I pulled the board's own minutes. I pulled the chair's calendar. I pulled a chat log from a compliance officer who'd been fired in Singapore six months back\ for "cultural fit," and I ran the matrix on her severance letter against a memo about the Connemara spring, and the Weir gave me a surprise of plus \
seven-one, and the shape she named was:\
\
*A silence that has been agreed to by everyone in the room.*\
\
That's the one. That's the crime. Not the land. Not the money. The *silence*. The board had agreed, without ever writing it down, that the Weir would be fed\ in a way that kept certain shapes out of the matrix. They'd built a machine to find connections and then trained it, gently, over years, to find everything\ except the connections that mattered. And the only reason I caught it was that the test they ran to prove the machine worked also proved it worked — and a\ machine that works is a machine that can betray you.\
\
I wrote it up. Forty pages. Every pair, every shape, every surprise score, every timestamp, every scrubbed metadata field Saoirse found. I filed it with the\ regulator at four in the morning, and I addressed it not to the board but to the compliance officer in Singapore, the one they'd fired, because she was the\ only person in the chain who'd never agreed to the silence.\
\
Then I went back to my office and put on Mingus and watched the rain.\
\
---\
\
They'll call it a coincidence. That's what they'll do. A lawyer will read my forty pages and say the Weir manufactures meaning, and a machine that\ manufactures meaning can manufacture a crime, and where's your evidence that the pairs weren't random. And he'll be right, technically, because that's\
the thing about a machine that finds shapes — every shape it finds is also a coincidence with a nice cut to it. The Weir is not a witness. She's a filing\ system with opinions.\
\
But here's what I know, and what the board knows, and what the regulator will know in three years when the lithium concession comes up for renewal and the\ spring at An Mám has gone dry and the townland has been bought and sold four times:\
\
The Weir works. That's the whole thing. The Weir works, and they built it to work, and then they tried to point it. And a machine that can be pointed is a\ machine that can be pointed *at you*.\
\
I'm an ork in a bank. I'm either security or a scandal. I chose scandal, and the scandal is that the machine is honest and the men who built it are not. The\ rain is still coming off the Liffey. The bridge is still lit up like a harp nobody's playing. And somewhere in the matrix, right now, there's a pair of texts\
that share a shape neither of them knows it has — a memo about a drought in the Sahel, and an invoice from a branch in Cork — and the shape they share is the\ oldest one in the city.\
\
*A payment made to make a problem disappear without ever naming the problem.*\
\
Somewhere a salmon is swimming upstream. I'll be at the weir. \
\
\
# The Weir, Pointed

Three weeks after the filing, Voss called me up to the sixth floor and poured two glasses of water.\
\
"The regulator read your forty pages," she said.\
\
"Good."\
\
"The regulator read your forty pages and asked the board a question." She sat down. "They asked why the bank has a machine that finds shapes and uses it\ exclusively on itself."\
\
I drank the water. Alice Coltrane was on the deck — *Journey in Satchidananda*, harp going up and down like something breathing — and I remember thinking it\ was the wrong record for the conversation, too much peace in it.\
\
"They want us to monetise it," I said.\
\
"They want us to *demonstrate* it has a commercial function. Which is not the same thing, Cormac, and you know it's not the same thing."\
\
"It's the same thing with better paperwork."\
\
She looked at the bridge. It was raining. It is always raining.\
\
"There's a desk," she said. "Structural Risk. It doesn't exist yet. It will exist on Monday. It will report to me, and it will have a compliance mandate and\ a P&L, and the P&L will be the part that gets read." She turned back. "The wall between internal affairs and portfolio is the only reason this bank has a\ licence. I'm telling you that on a Thursday. On Monday, you'll be standing on the other side of it, and I'd like you to remember I told you."\
\
---\
\
Here's what they don't understand, the men who run banks. They think a machine that finds fraud is a machine that finds fraud. But a machine that finds\ *shape* doesn't care what you point it at. Fraud is a shape. So is mispricing. So is an unmet customer need. So is a market that's about to turn.\
\
The Weir is a filing system with opinions. Pointed at silence, she finds silence. Pointed at money, she finds money. Same three axes. Same surprise score.\ Same walk.\
\
I started with the portfolio. Six thousand documents — contracts, term sheets, board packs, insurance policies, credit memos, the lot — and I ran the\ abstraction pass over all of them, and then I sat in a room with a matrix and a view and did what I do.\
\
**Find the concentration before the market does.** That's the whole job.
\
---\
\
It was four in the morning when I found the first one.\
\
The focal text was a pharma supplier contract — a mid-sized manufacturer in Kildare making a single excipient for a single buyer, exclusive, ten-year term,\ with a force majeure clause the size of a phone book. Content was unremarkable. The kind of document that exists to be signed and forgotten.\
\
The candidate was a shipping insurance policy on a bulk carrier in the Malacca Strait. Content similarity: point one-four.\
\
Abstraction similarity: point eight-nine.\
\
The shape the talker named was this:\
\
*The asset is priced as if the risk is contained, but the containment is the risk.*\
\
I pulled the matrix on the shipping policy. The next candidate was a municipal bond from a Kildare county council, issued to fund a water treatment works,\ guaranteed by a special purpose vehicle that was in turn guaranteed by — I had to read it three times — a guarantee that was not called a guarantee.\
\
Content similarity between the pharma contract and the municipal bond: point zero-nine.\
\
Abstraction similarity: point nine-one.\
\
Surprise: plus eight-two.\
\
Three assets. Three continents of vocabulary. One shape. And the bank held all three of them, in three different books, managed by three different people who\ 
had never once sat in the same room.\
\
That's the thing about a weir. The salmon don't know they're in a weir. They think they're swimming.\
\
I pulled the archive next. This is the part nobody thinks to do, and it's the part that makes the whole thing work: **the bank's own history is a corpus.**\ Every deal since 1994, every memo, every post-mortem, every letter from a regulator that started with the word "unfortunately." Twenty-nine years of\ institutional memory, sitting in a cold store, unread.\
\
I ran the shape against the archive.\
\
It came back with four hits. A 2007 paper on structured investment vehicles. A 2008 post-mortem on a monoline insurer. A 2011 memo from a risk officer who'd\ been fired for being difficult. And a 2019 letter from the regulator about a small bond in the west of Ireland that nobody had ever chased.\
\
Four precedents. Three of them had collapsed. The fourth had been the subject of a complaint that had never been resolved.\
\
I wrote a one-page note. It said: *the bank has a concentration in this shape. The shape has failed three times in this institution's own history. We do not\ currently measure for it.*\
\
I sent it to Voss at five in the morning.\
\
---\
\
The desk was stood up on a Monday and staffed with me and a quant called Fionn who had a face like a disappointed greyhound and a genuine gift for\ covariance.\
\
"Your machine found a shape," he said.\
\
"My machine found a shape."\
\
"And you want to know how many assets in the book have it."\
\
"I want to know how many assets in the book have it *and* are priced as if they don't."\
\
He looked at me over his glasses the way quants look at people who talk about shapes. Then he built the screen, because a quant will always build the screen,\ 
and by Thursday we had a number.\
\
Eleven assets. Four hundred and six million euro of exposure. And in three of them, the containment — the guarantee, the wrap, the force majeure — was\
itself the thing that would fail first. The bond was the clearest. The special purpose vehicle guaranteeing the council guarantee had a covenant that\ triggered if the council's credit rating fell below A-minus, and the council's credit rating was derived from — I want you to sit with this — the\ creditworthiness of the water treatment works.\
\
Circular. Beautiful. The shape had been priced at zero because the shape was invisible. You could read every document in the file and never see it. You had\ to see all three at once.\
\
We exited the bond over six weeks. Quietly. In tranches. Fionn handled the execution and I handled the paperwork, and we booked fourteen million in avoided\ loss and a small profit on the short, and nobody outside the desk ever knew why.\
\
A pension fund in Kildare bought it. I looked them up. Civil servants, mostly. Teachers. A few guards. I did not look them up a second time.\
\
---\
\
The second find was cheaper and it made more money and I'm not proud of it.\
\
The question axis. I'd been using it for years on the fraud side — every chat log, every email, every memo came from a question somebody had asked, and the\ question is often more honest than the answer. So I ran the extraction over four hundred portfolio documents from the infrastructure book, and I pulled out\ the questions, and I embedded them.\
\
Four hundred questions. And one of them recurred.\
\
*How do we get paid if the project fails?*\
\
It appeared in eighty-one documents. It appeared in different words every time — different phrasing, different register, different departments — but the\ abstraction pass stripped them all down and they all landed in the same place. And here's the thing that made me sit up: in eighty-one documents, **the\ question was never answered.** Not once. It was asked, and then it was filed, and then it was asked again somewhere else by someone who'd never seen the\ first eighty.\
\
That's not a question. That's a market.\
\
I took it to Voss. She took it to the board. The board took it to a reinsurer in Zurich, and eight months later the bank was underwriting completion-risk\ wraps on infrastructure projects across the continent, and the book was twenty-two million and growing, and the whole thing had come from the fact that a\ machine had noticed the bank kept asking the same question and never writing down an answer.\
\
The product was not invented. It was *found*. It had been sitting in the filing system the whole time, in eighty-one pieces, waiting for something that could\ 
see all of them at once.\
\
---\
\
The third one I'm going to tell you about because it's the one that taught me what I'd become.\
\
It was a temporal surprise. Same shape, different decade. I ran a credit memo from a waste-to-energy project in the Midlands against the archive, and the\ archive came back with a 2008 memo from the risk officer who'd been fired. Content similarity: point one-one. Abstraction: point nine-two. Same shape.\
\
*The counterparty is not the entity you are contracting with, and the entity you are contracting with does not exist.*\
\
The 2008 memo had been about a different deal entirely. Different sector. Different decade. Same shape. The risk officer had written three pages about it and\ 
been told to stop being difficult, and the deal had gone ahead, and the deal had blown up, and the memo had gone in the cold store with everything else.\
\
The current deal was two hundred and ten million. And the special purpose vehicle at the bottom of the structure had been incorporated in a jurisdiction I\ had to look up twice.\
\
I flagged it. The deal was restructured. The bank saved two hundred and ten million in exposure and lost a fee of about four, and the deal team hated me, and\ 
Fionn said, "You know this is the third time this quarter you've cost us a fee to save us a loss," and I said, "That's the job," and he said, "That's not the\ 
job, Cormac. The job is to make money. You keep making money by not losing it, and the board is going to notice."\
\
The board noticed.\
\
---\
\
Here's the arithmetic nobody puts on a slide.\
\
Fourteen million avoided. Twenty-two million booked. Two hundred and ten million saved. A desk of two people, a corpus of six thousand documents, a machine\ that measures shapes, and a jazz record playing at four in the morning.\
\
And what the machine also told me, on the same matrix, in the same week, was *who pays for the fourteen million.*\
\
The pension fund in Kildare. The teachers. The guards. A water treatment works in a county where the spring at An Mám had gone dry two years after the\ lithium concession was granted, and the townland had been bought and sold four times, and the old man in Connemara was dead, and nobody had ever recorded\ what happened to the thing that lived in the spring.\
\
The machine is honest. That's the whole thing. The machine is honest and I am not, because I pointed it at profit and it found profit and the profit had a\ shape and the shape was:\
\
*A boundary that is real to one party and imaginary to the other.*\
\
The same shape. The same goddamn shape from the land deal. The machine doesn't care. The machine measures. And a man who measures everything eventually\ measures himself, and finds he is a filing system with opinions, pointed at a P&L.\
\
---\
\
They gave me a bigger office. Six floors up, still. Lir House, still. The bridge is still lit up like a harp nobody's playing, and the rain is still coming\ off the Liffey sideways, and Alice Coltrane is still on the deck, and the harp goes up and down like something breathing.\
\
The desk is called Structural Risk. It has eleven people now. It reports to Voss, and Voss reports to a chairman who has never read a single matrix, and the\ wall between internal affairs and portfolio is gone, and nobody has ever asked for it back.\
\
Every branch. Every project. Every company we invest in. A stone in the weir.\
\
I sit here at four in the morning and I pull the matrix and I read down the surprise column, and every pair the machine gives me is a coincidence dressed as\ a clue, and the dress is the point, and the dress is always the same cut.\
\
Somewhere in the matrix right now there's a pair of texts that share a shape neither of them knows it has. One of them will make the bank money. One of them\ will cost a county its water. The machine will find both, and it will not tell me which is which, because that's not what a weir does.\
\
I'll be at the weir. The salmon are running. \
\
\
# The Hatchery

Ryleigh's is on the sixth floor of The Dean, North Wall Quay, and the terrace looks straight down the Liffey at the IFSC like a man looking at his own\ reflection in a knife. Glass windbreaks. Braziers that don't give off any actual heat. A sommelier who pronounces "Château" like it's a threat. And below,\ the river, brown and patient, carrying everything the city doesn't want to talk about out to the bay.\
\
I don't eat here. I drink here. There's a difference, and the difference is that a steak is a thing you can look at and know what it cost, and the wine list\ is a thing you look at and know what *you* cost.\
\
The three of them were already seated when I came up. Declan Ruane, CTO, in a suit that had been tailored for a man with a smaller conscience and let out at\ the seams. Niamh O'Keeffe, Head of Infrastructure, who had the eyes of someone who has watched a mainframe die and enjoyed it. And Marcus Bell, portfolio\ manager, who had the hands of a man who has never lifted anything heavier than a phone and the smile of a man who has never needed to.\
\
There was a trolley beside the table. On it, a tin of caviar, open, a mother-of-pearl spoon, and a small glass dome with a label I didn't recognise.\
\
"Ossetra," Bell said. "Aquaculture. Farmed in Westmeath, of all places. The Chinese own the hatchery, the Germans own the cold chain, and we own the debt."\ He smiled. "Sit down, Cormac. You look like a man who's been standing at a weir for three years."\
\
"I've been standing at a weir for three years."\
\
"Then you'll appreciate the upgrade."\
\
---\
\
They talked for an hour before I understood what they'd actually done, and the reason it took an hour is that they'd done it in the correct corporate order:\ pilot, proof of concept, centre of excellence, then the rollout. The rollout was the part they wanted me to hear.\
\
"We started with the branch network," Niamh said. She had a tablet and she was drawing on it with her finger, and the drawing was a Linux kernel. "Every\ branch runs a derivative now. Our own distribution. We call it *Lir*. Debian base, hardened, no external package repos, signed images only. Two thousand\
four hundred branches. Same image, same kernel, same userland. The branch manager in Ballyhaunis is running the same stack as the trading floor."\
\
"Because the trading floor is the branch network," I said.\
\
"Because the trading floor is the branch network," she agreed. "That's the point. Once everything is the same shape, the Weir can read everything."\
\
Declan leaned in. He had the enthusiasm of a man who had discovered open source late in life and was still angry about the licensing. "The architecture is\ the Cyberdeck architecture," he said. "We didn't invent it. We took it. Beowulf cluster, MPICH, Ubuntu, Python, Ollama. Refurbished office PCs, the whole\ thing. Apache 2.0. It was built to be forked, Cormac. We forked it."\
\
"You forked a hobby project."\
\
"We forked a *thesis*." He said the word the way a priest says *scripture*. "The Cyberdeck was never a product. It was a proof that a knowledge system can be\ 
built, not downloaded. Local inference. No cloud. No subscription. The machine shaped by the person who uses it. We took that and we scaled it."\
\
"To what?"\
\
Niamh put the tablet down. "Forty-one thousand documents a day. Every branch, every project, every company we invest in, every memo, every contract, every\ chat log, every post-mortem, every letter from a regulator that starts with the word *unfortunately*. All of it ingested. All of it abstracted. All of it\ embedded. Three axes. Content, shape, question. The same matrix you built in a room with a view and a Mingus record."\
\
"And the abstraction pass?"\
\
"Runs on the cluster. We've got four hundred decommissioned OptiPlex machines in a cage in Clonskeagh. The bank was going to recycle them. We put Linux on\ them and taught them to read."\
\
I looked at the caviar. The eggs were small and black and perfect, and each one was a single cell that had been harvested from a fish that was still alive,\ and the fish would be harvested again next year, and the year after that, because the hatchery had learned how to take the eggs without killing the sturgeon.\
That's the thing about aquaculture. You don't catch the fish. You farm it.\
\
---\
\
Marcus Bell pushed the tin towards me.\
\
"You're wondering why we're telling you this," he said.\
\
"I'm wondering why you're telling me this *here*."\
\
"Because you're going to read it in the matrix anyway, and we'd rather you read it from us than from a surprise score." He spooned some caviar onto a blini.\ "The board has approved the rollout. Full group. Every subsidiary. Every jurisdiction. The Weir is going to be the bank's nervous system, and the bank is\ going to be the Weir's body. One architecture. One distribution. One cluster. One set of models."\
\
"One model."\
\
"One model *family*," Declan corrected. "Different sizes. Different specialisations. Different temperatures. But yes. One lineage. The same base weights,\ fine-tuned per desk."\
\
I put my glass down. "Then you've got correlated errors across the entire group and a synthesizer that will read agreement as evidence."\
\
Niamh smiled. It was the first genuine expression I'd seen on her. "We know. That's why we kept you."\
\
---\
\
Here's what they'd built, and I want to give it to you straight, because it's the most beautiful and the most terrifying thing I've seen in this city since\ the last time a bank discovered a machine that could read.\
\
**The distribution.** *Lir.* A Linux derivative, Debian-based, hardened, immutable. Every branch, every server, every cluster node runs it. No external\ repos. No unsigned packages. No shadow IT. The bank doesn't just run Linux now; the bank *is* Linux, in the sense that the bank's entire operational\
surface has been reduced to a single reproducible image. You can boot a branch manager's desktop in Ballyhaunis and get the same kernel as the risk desk\
in Singapore.\
\
**The cluster.** Beowulf. Four hundred nodes, MPICH, refurbished hardware. The same architecture the Cyberdeck thesis described — a supercomputer made of\ office PCs, Linux on every node, workload shared across the LAN. The bank had been throwing these machines away for years. Niamh's team intercepted them,\ imaged them with *Lir*, and racked them in a cage in Clonskeagh with a gigabit switch and a fire suppression system that had been bought second-hand from\
a data centre in Dublin 15.\
\
**The models.** Ollama, forked. Local inference. No cloud. No API keys. No data leaving the estate. The bank had spent a decade terrified of regulators\ asking where the data went; now the answer was "nowhere." Every model was quantised, every prompt was logged, every output was traced.\
\
**The Weir.** The same three axes I'd built. Content, shape, question. But industrialised. The abstraction pass ran on the cluster, one call per chunk, and\ the chunks were no longer six thousand documents from a portfolio — they were forty-one thousand a day, from every corner of the group.\
\
"The weir doesn't catch salmon anymore," Niamh said. "It holds eggs."\
\
---\
\
I looked at her.\
\
"That's the thing you're not saying," I said. "The weir isn't a trap. It's a hatchery. You're not finding connections anymore. You're *breeding* them."\
\
Bell set his fork down. "Explain."\
\
"The old Weir caught pairs. A drought claim and a security invoice. A bond and a spring. It found shapes that already existed, in texts that already existed,\ 
and it showed them to me, and I decided what to do. That's a weir. A trap. The fish swim in and don't swim out."\
\
I pointed at the caviar.\
\
"This is a hatchery. You've got forty-one thousand documents a day, and every one of them is being abstracted, and every abstraction is being embedded, and\ every embedding is being compared. You're not waiting for the salmon to swim in. You're taking the eggs out of the fish, fertilising them in a tank, and\ growing the next generation. The connections aren't found. They're *manufactured*. On purpose. At scale. With a P&L."\
\
Declan started to say something. I didn't let him.\
\
"The Cyberdeck was a machine you build and shape yourself," I said. "That's the thesis. A machine shaped by the person who uses it. What you've built is a\ machine that shapes the person who uses it. The distribution is the shape. The cluster is the shape. The model family is the shape. The Weir doesn't\
measure the bank anymore. The bank measures itself through the Weir, and the Weir was built by the bank, and the loop is closed."\
\
Niamh nodded slowly. "Yes."\
\
"And you're telling me this because you want me to run it."\
\
"No," Bell said. "We're telling you this because we want you to *audit* it. The board wants an independent check. The regulator wants a paper trail. And\ you're the only person in the group who understands that a surprise score is a coincidence dressed as a clue."\
\
---\
\
I ate the caviar. It was cold and salt and it tasted like the bottom of the sea, and I thought about the sturgeon in Westmeath, swimming in a tank, being\ scanned with an ultrasound, biopsied, and massaged for its eggs by a machine that had been built to do it without killing the fish. The fish would live.\
The eggs would be taken. The caviar would be sold. And the fish would be scanned again next year, and the year after that, because that's how a hatchery\ works.\
\
The weir was still there. It was under the restaurant. It was in the cage in Clonskeagh, and in the branch network, and in the kernel of every *Lir* image,\ and in the matrix that ran on four hundred decommissioned office PCs, and in the abstraction pass that turned every document in the group into a shape, and\ in the surprise column that I had invented, and in the P&L that Bell was already modelling.\
\
The machine was honest. The machine had always been honest. The machine measured shapes, and the shapes were real, and the caviar was real, and the profit\ was real. The only thing that had changed was the direction of the fork. The old Weir asked: *what is in the river?* The new Weir asks: *what should be in\ the river?*\
\
And the answer to that question was being written by the same three people who owned the river.\
\
---\
\
Mingus was on the deck in my office, six floors up, *The Black Saint and the Sinner Lady*, and the rain was coming off the Liffey sideways, and the bridge\ was lit up like a harp nobody was playing. I could see Ryleigh's from my window. The terrace was still lit. The braziers were still burning. The caviar\ trolley was still there, and the sommelier was still pronouncing *Château* like a threat, and the city was spread out below like a circuit board with a\
river running through it.\
\
*Lir.* The Irish sea god. The father of Manannán. The one who owned the water.\
\
I poured a whiskey and I pulled up the matrix on the wall. One focal text. Candidates ranked. Three columns. A star for anything that cleared the threshold.\
\
The focal was a procurement memo from the new *Lir* rollout — hardware acquisition, four hundred units, ex-lease, wiped and reimaged. The top candidate was a\ 
2008 post-mortem from the risk officer who'd been fired for being difficult. Content similarity: point one-two. Abstraction similarity: point nine-zero.\ Surprise: plus seven-eight.\
\
The shape the talker named was:\
\
*The institution is building the instrument of its own measurement, and the instrument is loyal to the institution.*\
\
I looked at it for a long time. Then I poured another whiskey and I put on Alice Coltrane, because Mingus was too honest for the mood I was in, and I watched\ 
the rain, and I thought about eggs.\
\
The weir holds caviar now. The salmon are farmed. And the fish are still alive, which is the part nobody tells you about aquaculture — the part where the\ fish lives, and the eggs are taken, and the fish is scanned again next year, and the year after that, and the year after that.\
\
I'll be at the weir. The eggs are hatching.\
\
