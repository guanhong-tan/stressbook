from datetime import datetime

# {
#     "_id": "transaction_id_001",
#     "user_id": "user_id_001",
#     "event_id": "event_id_001",
#     "seat_ids": ["seat_id_333", "seat_id_334"],  // Array of seat IDs from the Seating Collection
#     "amount": 420,                               // Total amount based on seat prices
#     "payment_status": "completed",               // Options: "completed", "pending", "failed"
#     "payment_method": "credit_card",             // E.g., "credit_card", "paypal"
#     "transaction_date": "2024-10-31T15:45:00Z"
# }

{
    "_id": "transaction_id_001",
    "booking_id": "booking_id_001",
    "user_id": "user_id_001",
    "event_id": "event_id_001",
    "amount": 200,
    "payment_status": "completed",
    "payment_method": "credit_card",
    "transaction_date": "2024-11-15T10:05:00Z",
    "receipt_url": "https://example.com/receipts/transaction_id_001",
    "payment_gateway_id": "txn_123456789",
    "notes": "Transaction completed successfully"
}
