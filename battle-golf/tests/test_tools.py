from tools import save_teams, load_teams
from models import Team

def test_save_and_load_teams():
    # Create some test teams
    team_a = Team("TestTeamA")
    
    # Save teams
    save_teams([team_a], "test_teams.json")
    
    # Load teams
    loaded_teams = load_teams("test_teams.json")
    
    # Here you would assert that the loaded_teams match what you expect
    assert loaded_teams[0].team_name == "TestTeamA"
    # ... more assertions or checks ...
