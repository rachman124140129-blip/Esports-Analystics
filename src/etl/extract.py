import json
import os
from datetime import datetime
import random

RAW_DATA_DIR = os.path.join("data", "raw")

class MockDataGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_tournaments(self):
        return [{
            "tournament_id": 1,
            "name": "M7 World Championship Simulation",
            "start_date": "2026-01-01",
            "end_date": "2026-02-05",
            "tier": "S-Tier"
        }]

    def generate_teams(self):
        return [
            {"team_id": 101, "name": "ONIC Esports", "region": "ID"},
            {"team_id": 102, "name": "AP.Bren", "region": "PH"},
            {"team_id": 103, "name": "Blacklist International", "region": "PH"},
            {"team_id": 104, "name": "RRQ Hoshi", "region": "ID"}
        ]

    def generate_players(self):
        players = []
        roles = ["Jungler", "Roamer", "Midlaner", "Gold Laner", "EXP Laner"]
        team_ids = [101, 102, 103, 104]
        
        player_id = 1001
        for team in team_ids:
            for role in roles:
                players.append({
                    "player_id": player_id,
                    "team_id": team,
                    "in_game_name": f"Player_{player_id}",
                    "role": role,
                    "nationality": "ID" if team in [101, 104] else "PH"
                })
                player_id += 1
        return players

    def generate_matches_and_performance(self, players):
        matches = []
        performances = []
        match_id = 5001
        perf_id = 1
        
        matches.append({
            "match_id": match_id,
            "tournament_id": 1,
            "team_a_id": 101,
            "team_b_id": 102,
            "match_date": datetime.now().isoformat(),
            "winner_team_id": 101,
            "game_patch": "1.8.44"
        })

        heroes = ["Zhuxin", "Chou", "Fanny", "Claude", "Yu Zhong"]
        
        for player in players:
            if player["team_id"] in [101, 102]:
                performances.append({
                    "performance_id": perf_id,
                    "match_id": match_id,
                    "player_id": player["player_id"],
                    "champion_hero_played": random.choice(heroes),
                    "kills": random.randint(0, 15),
                    "deaths": random.randint(0, 8),
                    "assists": random.randint(0, 20),
                    "gold_earned": random.randint(9000, 15000),
                    "damage_dealt": random.randint(40000, 100000)
                })
                perf_id += 1
                
        return matches, performances

    def save_to_json(self, data, filename_prefix):
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        
        filename = f"{filename_prefix}_{self.timestamp}.json"
        filepath = os.path.join(RAW_DATA_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✅ Tersimpan: {filepath}")

    def run_extraction(self):
        print("Memulai proses ekstraksi data (Mocking)...")
        
        tournaments = self.generate_tournaments()
        teams = self.generate_teams()
        players = self.generate_players()
        matches, performances = self.generate_matches_and_performance(players)
        
        self.save_to_json(tournaments, "tournaments")
        self.save_to_json(teams, "teams")
        self.save_to_json(players, "players")
        self.save_to_json(matches, "matches")
        self.save_to_json(performances, "player_performances")
        
        print("🎉 Ekstraksi selesai! Data mentah siap untuk ditransformasi.")

if __name__ == "__main__":
    generator = MockDataGenerator()
    generator.run_extraction()