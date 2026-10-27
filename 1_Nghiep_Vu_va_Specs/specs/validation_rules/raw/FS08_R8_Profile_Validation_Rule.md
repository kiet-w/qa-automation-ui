# My Details Validation

Page: `http://localhost:5174/profile`

## Field rules

| Field | Rule | Message |
|---|---|---|
| Full Name | Read-only | None |
| NRIC | Read-only | None |
| Residential Address | Read-only | None |
| Mobile Number | Required; exactly 8 digits; starts with 6, 8, or 9 | Blank: `MSG-0001` — “Enter your mobile number”. Invalid: `MSG-0805` — “Enter a mobile number in the correct format, like 9123 4567”. |
| Email | Required; valid email format; maximum 150 characters | Blank: `MSG-0001` — “Enter your email”. Invalid or over 150 characters: `MSG-0806` — “Enter an email address in the correct format, like name@example.com”. |
| Mailing Block | Optional; maximum 20 characters | Over limit: “Enter no more than 20 characters.” *(Assume message)* |
| Mailing Street | Required; maximum 100 characters | Blank: `MSG-0001` — “Enter your mailing street”. Over limit: “Enter no more than 100 characters.” *(Assume message)* |
| Mailing Unit | Optional; maximum 20 characters | Over limit: “Enter no more than 20 characters.” *(Assume message)* |
| Mailing Postal Code | Required; exactly 6 digits | Blank: `MSG-0001` — “Enter your mailing postal code”. Invalid: “Enter a valid 6-digit postal code.” *(Assume message)* |
| Mailing Country | Required; maximum 100 characters | Blank: `MSG-0001` — “Enter your mailing country”. Over limit: “Enter no more than 100 characters.” *(Assume message)* |

## Save behavior

- If a required field is blank or a value is invalid, show the message beside that field and do not submit the update.
- On successful update, show `MSG-0807`: “Your details have been updated.”
- If saving fails, show `MSG-0808`: “We could not update your details. Please try again.”
- If all linked children are 16 or older, show the profile in read-only mode.

## Notes

- `MSG-0001` is the required-field message: “Enter your <field>”.
- Messages marked *(Assume message)* are suggested copy because `message_R8.txt` does not define wording for those validation cases.
- The current frontend code checks email format on submit. Mobile format and the mailing field rules above may still need implementation.
