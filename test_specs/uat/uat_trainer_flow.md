# Feature: UAT End-to-End User Journeys

## Scenario: UAT-01 Trainer Full Onboarding Flow @uat @journey
- Open: curricula_trainer_account.html
- Assert: Title contains "Curricula"
- Fill: #preferredName with "Dr. Alexandra Tan"
- Click: #cancelBtn
- Assert: Title contains "Curricula"
