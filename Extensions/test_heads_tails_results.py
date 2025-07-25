import unittest
import statistics
import random
import sys
from collections import defaultdict


class TestHeadsTailsResults(unittest.TestCase):
    def simulate_heads_tails_game(self, bet_side, num_simulations=10000):
        """Simulate the heads/tails game logic from Gambling.py"""
        wins = 0
        losses = 0
        net_results = []
        
        for _ in range(num_simulations):
            # Simulate the 5-roll system from the gambling code
            rolls = []
            max_rolls = 5
            
            for i in range(max_rolls):
                # Random choice between -1 (tails) and 1 (heads)
                roll_result = random.choice([-1, 1])
                rolls.append(roll_result)
                
                current_sum = sum(rolls)
                rolls_remaining = max_rolls - (i + 1)
                
                if rolls_remaining > 0:
                    max_possible_change = rolls_remaining
                    min_possible_change = -rolls_remaining
                    
                    # Early termination logic from original code
                    if (current_sum + min_possible_change > 0) or (current_sum + max_possible_change <= 0):
                        break
            
            # Calculate net result
            net_result = sum(rolls)
            net_results.append(net_result)
            
            # Determine winner based on net result
            if net_result > 0:
                # Heads wins
                if bet_side == "heads":
                    wins += 1
                else:
                    losses += 1
            else:
                # Tails wins (net negative or zero)
                if bet_side == "tails":
                    wins += 1
                else:
                    losses += 1
        
        return wins, losses, net_results
    
    def test_heads_tails_statistics(self):
        """Test and analyze heads/tails game statistics"""
        num_simulations = 1000000
        
        print(f"\n=== HEADS/TAILS GAMBLING ANALYSIS ===")
        print(f"Simulations per test: {num_simulations:,}")
        
        # Test betting on heads
        heads_wins, heads_losses, heads_net_results = self.simulate_heads_tails_game("heads", num_simulations)
        heads_win_rate = heads_wins / num_simulations * 100
        
        # Test betting on tails
        tails_wins, tails_losses, tails_net_results = self.simulate_heads_tails_game("tails", num_simulations)
        tails_win_rate = tails_wins / num_simulations * 100
        
        print(f"\n--- BETTING ON HEADS ---")
        print(f"Wins: {heads_wins:,} ({heads_win_rate:.2f}%)")
        print(f"Losses: {heads_losses:,} ({100-heads_win_rate:.2f}%)")
        print(f"Average net result: {statistics.mean(heads_net_results):.3f}")
        print(f"Median net result: {statistics.median(heads_net_results):.3f}")
        print(f"Net result std dev: {statistics.stdev(heads_net_results):.3f}")
        
        print(f"\n--- BETTING ON TAILS ---")
        print(f"Wins: {tails_wins:,} ({tails_win_rate:.2f}%)")
        print(f"Losses: {tails_losses:,} ({100-tails_win_rate:.2f}%)")
        print(f"Average net result: {statistics.mean(tails_net_results):.3f}")
        print(f"Median net result: {statistics.median(tails_net_results):.3f}")
        print(f"Net result std dev: {statistics.stdev(tails_net_results):.3f}")
        
        # Expected value analysis
        print(f"\n--- EXPECTED VALUE ANALYSIS ---")
        # In the game, you bet 1 unit and win 2 units (net +1) or lose 1 unit (net -1)
        heads_expected_value = (heads_win_rate/100 * 1) + ((100-heads_win_rate)/100 * -1)
        tails_expected_value = (tails_win_rate/100 * 1) + ((100-tails_win_rate)/100 * -1)
        
        print(f"Expected value betting heads: {heads_expected_value:.4f} units per bet")
        print(f"Expected value betting tails: {tails_expected_value:.4f} units per bet")
        
        # Distribution analysis
        all_net_results = heads_net_results + tails_net_results
        net_result_distribution = defaultdict(int)
        for result in all_net_results:
            net_result_distribution[result] += 1
        
        print(f"\n--- NET RESULT DISTRIBUTION ---")
        for net_result in sorted(net_result_distribution.keys()):
            percentage = net_result_distribution[net_result] / len(all_net_results) * 100
            print(f"Net {net_result:+2d}: {net_result_distribution[net_result]:,} occurrences ({percentage:.2f}%)")
        
        # Verify the game is approximately fair
        combined_win_rate = (heads_wins + tails_wins) / (num_simulations * 2) * 100
        print(f"\n--- FAIRNESS CHECK ---")
        print(f"Overall win rate: {combined_win_rate:.2f}% (should be ~50% for fair game)")
        print(f"Deviation from 50%: {abs(combined_win_rate - 50):.2f}%")
        
        # Assert the game is reasonably fair (within 1% of 50%)
        self.assertLess(abs(combined_win_rate - 50), 1.0, "Game appears to be significantly unfair")


if __name__ == '__main__':
    # Redirect output to file for analysis
    try:
        with open("heads_tails_statistics.txt", 'w') as f:
            sys.stdout = f
            unittest.main(verbosity=2)
    except Exception as e:
        print(f'An error occurred while generating heads/tails stats: {e}')
    finally:
        sys.stdout = sys.__stdout__
        print("Heads/tails analysis complete. Check heads_tails_statistics.txt for results.")