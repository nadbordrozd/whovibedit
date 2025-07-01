# Master Clue ID List for The Gallery Murder

## Clue IDs by NPC

### Edward's Clues
- `benjamin_threat` - Benjamin threatened Marcus at 7:15 PM
- `gallery_lockdown` - Security system engaged at 8:00 PM
- `alice_bribe` - Alice paid Edward $500 to leave post
- `alice_gambling` - Alice has gambling debts to bookies
- `alice_to_office` - Alice went toward Marcus's office at 7:46 PM
- `benjamin_pacing` - Benjamin was pacing by studio at 7:48 PM
- `edward_guilt` - Edward's first time taking a bribe in 4 years

### David's Clues
- `edward_left_post` - Edward left his security post at 7:45 PM
- `david_viewing_room` - David was in viewing room 7:55-8:40 PM
- `david_forgeries` - David owns three forged paintings worth $1.2M
- `collector_lawsuit` - Another collector contacted David about identical paintings
- `david_confrontation` - David came to confront Marcus privately

### Alice's Clues
- `catherine_meetings` - Catherine had tense private meetings with Marcus
- `marcus_afraid` - Marcus seemed afraid when Catherine visited
- `benjamin_strange` - Benjamin acting strange after the toast
- `body_discovery` - Found body with Catherine at 8:45 PM
- `embezzlement_scheme` - Alice stealing $3-4k monthly for 18 months
- `alice_debts` - Alice owes $47,000 to bookies
- `safe_open` - Found Marcus's safe already open
- `alice_theft` - Took $2,000 from safe (in purse)
- `catherine_blackmail_confirmed` - Confirms Catherine was blackmailing Marcus

### Catherine's Clues
- `benjamin_agitated` - Benjamin particularly agitated after toast
- `alice_desperate` - Alice taking calls about "needing more time"
- `edward_return` - Saw Edward return to post at 7:50 PM
- `everyone_suspicious` - Everyone had suspicious behavior
- `forgery_details` - Marcus selling fake Benjamin Hayes paintings
- `benjamin_unknowing` - Benjamin unknowingly painted forgeries
- `blackmail_amount` - Extracting $10,000/month for six months
- `provenance_discovery` - Found inconsistencies in documents
- `catherine_motive` - Marcus alive worth $120,000/year to her

### Benjamin's Clues
- `working_in_studio` - Claims working in studio after 8:00 PM
- `murder_method` - Poisoned wine with Prussian blue and turpentine
- `poisoned_toast` - Ensured Marcus got poisoned glass at 7:50 PM
- `insurance_copies` - Tricked into painting "insurance copies"
- `contract_trap` - Legally trapped by contracts
- `destroyed_evidence` - Destroyed fake paintings after murder
- `legacy_motive` - Marcus was destroying his artistic legacy

## Implementation Notes

Each clue ID should be:
- Unique across all NPCs
- Descriptive enough to understand at a glance
- Consistent in naming convention (lowercase with underscores)
- Grouped by the NPC who reveals it

NPCs should include relevant clue IDs in their `clues_revealed` array whenever they mention the corresponding information, whether in casual conversation or during confession.