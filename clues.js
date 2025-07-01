// Sample implementation for the Gallery Murder clue system

// Master clue database
const CLUES = {
  // Edward's clues
  benjamin_threat: {
    id: "benjamin_threat",
    npc: "Edward",
    text: "Benjamin threatened Marcus at 7:15 PM: 'You're destroying me! I'll destroy you!'",
    category: "threats"
  },
  gallery_lockdown: {
    id: "gallery_lockdown",
    npc: "Edward",
    text: "Security system engaged at 8:00 PM - no one could enter or leave",
    category: "timeline"
  },
  alice_bribe: {
    id: "alice_bribe",
    npc: "Edward",
    text: "Alice paid Edward $500 to leave his post from 7:45-7:55 PM",
    category: "confession"
  },
  alice_gambling: {
    id: "alice_gambling",
    npc: "Edward",
    text: "Alice has gambling debts to bookies",
    category: "secrets"
  },
  alice_to_office: {
    id: "alice_to_office",
    npc: "Edward",
    text: "Alice went toward Marcus's office at 7:46 PM",
    category: "movements"
  },
  benjamin_pacing: {
    id: "benjamin_pacing",
    npc: "Edward",
    text: "Benjamin was pacing by the studio at 7:48 PM",
    category: "movements"
  },
  edward_guilt: {
    id: "edward_guilt",
    npc: "Edward",
    text: "This was Edward's first time taking a bribe in 4 years",
    category: "confession"
  },

  // David's clues
  edward_left_post: {
    id: "edward_left_post",
    npc: "David",
    text: "Edward left his security post at 7:45 PM",
    category: "timeline"
  },
  david_viewing_room: {
    id: "david_viewing_room",
    npc: "David",
    text: "David was in viewing room alone from 7:55-8:40 PM",
    category: "alibis"
  },
  david_forgeries: {
    id: "david_forgeries",
    npc: "David",
    text: "David owns three forged paintings worth $1.2 million",
    category: "confession"
  },
  collector_lawsuit: {
    id: "collector_lawsuit",
    npc: "David",
    text: "Another collector contacted David about owning identical paintings",
    category: "confession"
  },
  david_confrontation: {
    id: "david_confrontation",
    npc: "David",
    text: "David came tonight to confront Marcus privately",
    category: "confession"
  },

  // Alice's clues
  catherine_meetings: {
    id: "catherine_meetings",
    npc: "Alice",
    text: "Catherine had tense private meetings with Marcus recently",
    category: "observations"
  },
  marcus_afraid: {
    id: "marcus_afraid",
    npc: "Alice",
    text: "Marcus seemed afraid when Catherine visited",
    category: "observations"
  },
  benjamin_strange: {
    id: "benjamin_strange",
    npc: "Alice",
    text: "Benjamin was acting strange after the toast",
    category: "observations"
  },
  body_discovery: {
    id: "body_discovery",
    npc: "Alice",
    text: "Alice found Marcus's body with Catherine at 8:45 PM",
    category: "timeline"
  },
  embezzlement_scheme: {
    id: "embezzlement_scheme",
    npc: "Alice",
    text: "Alice has been stealing $3-4k monthly for 18 months",
    category: "confession"
  },
  alice_debts: {
    id: "alice_debts",
    npc: "Alice",
    text: "Alice owes $47,000 to bookies",
    category: "confession"
  },
  safe_open: {
    id: "safe_open",
    npc: "Alice",
    text: "Alice found Marcus's safe already open at 7:45 PM",
    category: "confession"
  },
  alice_theft: {
    id: "alice_theft",
    npc: "Alice",
    text: "Alice took $2,000 from the safe (still in her purse)",
    category: "confession"
  },
  catherine_blackmail_confirmed: {
    id: "catherine_blackmail_confirmed",
    npc: "Alice",
    text: "Alice confirms Catherine was blackmailing Marcus",
    category: "confession"
  },

  // Catherine's clues
  benjamin_agitated: {
    id: "benjamin_agitated",
    npc: "Catherine",
    text: "Benjamin was particularly agitated after the toast",
    category: "observations"
  },
  alice_desperate: {
    id: "alice_desperate",
    npc: "Catherine",
    text: "Alice taking phone calls about 'needing more time' - gambling debts suspected",
    category: "observations"
  },
  edward_return: {
    id: "edward_return",
    npc: "Catherine",
    text: "Catherine saw Edward return to his post at 7:50 PM",
    category: "timeline"
  },
  everyone_suspicious: {
    id: "everyone_suspicious",
    npc: "Catherine",
    text: "Everyone had suspicious behavior tonight",
    category: "observations"
  },
  forgery_details: {
    id: "forgery_details",
    npc: "Catherine",
    text: "Marcus was selling fake Benjamin Hayes paintings",
    category: "confession"
  },
  benjamin_unknowing: {
    id: "benjamin_unknowing",
    npc: "Catherine",
    text: "Benjamin unknowingly painted the forgeries as 'insurance copies'",
    category: "confession"
  },
  blackmail_amount: {
    id: "blackmail_amount",
    npc: "Catherine",
    text: "Catherine was extracting $10,000/month for six months",
    category: "confession"
  },
  provenance_discovery: {
    id: "provenance_discovery",
    npc: "Catherine",
    text: "Catherine found inconsistencies in provenance documents",
    category: "confession"
  },
  catherine_motive: {
    id: "catherine_motive",
    npc: "Catherine",
    text: "Marcus alive was worth $120,000/year to Catherine",
    category: "confession"
  },

  // Benjamin's clues
  working_in_studio: {
    id: "working_in_studio",
    npc: "Benjamin",
    text: "Benjamin claims he was working in the studio after 8:00 PM",
    category: "alibis"
  },
  murder_method: {
    id: "murder_method",
    npc: "Benjamin",
    text: "Benjamin poisoned the wine with Prussian blue thinned with turpentine",
    category: "murder"
  },
  poisoned_toast: {
    id: "poisoned_toast",
    npc: "Benjamin",
    text: "Benjamin ensured Marcus got the poisoned glass during the 7:50 PM toast",
    category: "murder"
  },
  insurance_copies: {
    id: "insurance_copies",
    npc: "Benjamin",
    text: "Benjamin was tricked into painting 'insurance copies' sold as originals",
    category: "confession"
  },
  contract_trap: {
    id: "contract_trap",
    npc: "Benjamin",
    text: "Benjamin was legally trapped by contracts he signed",
    category: "confession"
  },
  destroyed_evidence: {
    id: "destroyed_evidence",
    npc: "Benjamin",
    text: "Benjamin destroyed fake paintings in the studio after the murder",
    category: "confession"
  },
  legacy_motive: {
    id: "legacy_motive",
    npc: "Benjamin",
    text: "Marcus was destroying Benjamin's artistic legacy",
    category: "murder"
  }
};

// Game state
class GalleryMurderGame {
  constructor() {
    this.discoveredClues = new Set();
    this.npcConfessions = {
      Benjamin: false,
      Alice: false,
      Catherine: false,
      David: false,
      Edward: false
    };
    this.currentNPC = null;
  }

  // Process NPC response and extract clues
  async processNPCResponse(npcName, playerMessage) {
    this.currentNPC = npcName;
    
    // Send message to NPC (this would call your LLM)
    const response = await this.sendToNPC(npcName, playerMessage);
    
    try {
      const data = JSON.parse(response);
      
      // Add any new clues to player's notepad
      if (data.clues_revealed && Array.isArray(data.clues_revealed)) {
        data.clues_revealed.forEach(clueId => {
          if (CLUES[clueId] && !this.discoveredClues.has(clueId)) {
            this.discoveredClues.add(clueId);
            this.displayNewClue(CLUES[clueId]);
          }
        });
      }
      
      // Check for confession
      if (data.confessed) {
        this.npcConfessions[npcName] = true;
        this.checkWinCondition();
      }
      
      return data.response;
    } catch (error) {
      console.error("Failed to parse NPC response:", error);
      return "The character seems confused and doesn't respond clearly.";
    }
  }

  // Display new clue notification
  displayNewClue(clue) {
    console.log(`📝 New clue added to notepad: ${clue.text}`);
    // In a real game, this would update the UI
  }

  // Check if player has solved the mystery
  checkWinCondition() {
    if (this.npcConfessions.Benjamin) {
      console.log("🎉 Congratulations! You've solved the murder!");
      console.log("Benjamin Hayes has confessed to poisoning Marcus Webb.");
      // Trigger game ending sequence
    }
  }

  // Get clues organized by category for display
  getCluesByCategory() {
    const cluesByCategory = {};
    
    this.discoveredClues.forEach(clueId => {
      const clue = CLUES[clueId];
      if (!cluesByCategory[clue.category]) {
        cluesByCategory[clue.category] = [];
      }
      cluesByCategory[clue.category].push(clue);
    });
    
    return cluesByCategory;
  }

  // Mock function - replace with actual LLM call
  async sendToNPC(npcName, message) {
    // This would be replaced with your actual LLM API call
    // For now, returning a mock response
    return JSON.stringify({
      response: `${npcName} responds to your question...`,
      confessed: false,
      clues_revealed: []
    });
  }
}

// Example usage
const game = new GalleryMurderGame();

// Player talks to Edward
game.processNPCResponse("Edward", "Tell me about tonight's event.")
  .then(response => {
    console.log("Edward says:", response);
    // This might reveal the "benjamin_threat" clue
  });

// Player confronts Benjamin with evidence
game.processNPCResponse("Benjamin", "We know about the forgeries and your threat to Marcus.")
  .then(response => {
    console.log("Benjamin says:", response);
    // This would trigger Benjamin's confession and reveal murder clues
  });