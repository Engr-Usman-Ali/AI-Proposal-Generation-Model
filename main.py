# main.py

import random
from src.data_preprocessing import load_and_clean_data
from src.proposal_generator import generate_proposal
from src.utils import save_json, append_text
from src.evaluator import evaluate_all

def main():
    print("\n=== DevArion Smart Proposal Generator ===\n")

    # Step 1: Load dataset
    data = load_and_clean_data("data/client_briefs_dataset.csv")
    total_entries = len(data)

    # Step 2: Ask user for number of test cases
    while True:
        try:
            user_count = int(input(f"Enter number of test cases to run (min 10, max {total_entries}): "))
            if user_count < 10:
                print("⚠️ Please enter at least 10 test cases as per DevArion requirements.\n")
                continue
            if user_count > total_entries:
                print(f"⚠️ Maximum available test cases are {total_entries}. Running all available.")
                user_count = total_entries
            break
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value.\n")

    # Step 3: Ask user how to select test cases
    print("\nSelect test case mode:")
    print("1. Sequential (first N from dataset)")
    print("2. Random (select random N cases)")
    
    while True:
        mode = input("Enter choice (1 or 2): ").strip()
        if mode in ["1", "2"]:
            break
        print("❌ Invalid choice. Please enter 1 or 2.\n")

    # Step 4: Select data subset
    if mode == "1":
        selected_data = data.head(user_count)
        print(f"\n🧾 Selected first {user_count} client briefs for testing.\n")
    else:
        selected_data = data.sample(n=user_count, random_state=42)
        print(f"\n🎲 Randomly selected {user_count} client briefs for testing.\n")

    # Step 5: Generate proposals
    all_proposals = []
    for idx, row in selected_data.iterrows():
        print(f"Processing ID {row['id']} → {row['service_type']}")
        proposal = generate_proposal(row["text"])
        all_proposals.append(proposal)
        append_text(proposal["formatted_text"], "output/generated_proposals.txt")

    # Step 6: Save structured output
    save_json(all_proposals, "output/proposal_samples.json")

    # Step 7: Evaluate all proposals
    evaluate_all(all_proposals)

    print("\n✅ All proposals generated and evaluated successfully!")
    print(f"→ Total test cases: {user_count}")
    print("→ Outputs saved in /output folder.\n")

if __name__ == "__main__":
    main()
