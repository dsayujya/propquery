import pytest

def test_support_ticket_lifecycle(client):
    # 1. Create a ticket
    create_response = client.post(
        "/api/v1/support/",
        json={
            "title": "Test Ticket",
            "description": "This is a test issue",
            "category": "system",
            "priority": "high",
            "status": "open"
        }
    )
    assert create_response.status_code == 201
    ticket = create_response.json()
    ticket_id = ticket["id"]
    assert ticket["status"] == "open"

    # 2. Verify initial update was created automatically
    get_response = client.get(f"/api/v1/support/{ticket_id}")
    assert get_response.status_code == 200
    ticket_data = get_response.json()
    updates = ticket_data["updates"]
    assert len(updates) == 1
    assert updates[0]["update_type"] == "created"

    # 3. Transition state to 'investigating'
    update_response = client.patch(
        f"/api/v1/support/{ticket_id}",
        json={"status": "investigating", "assigned_engineer": "Test Engineer"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "investigating"

    # 4. Verify state transition update was logged
    get_response = client.get(f"/api/v1/support/{ticket_id}")
    updates = get_response.json()["updates"]
    assert len(updates) == 2
    assert updates[1]["update_type"] == "status_change"
    assert updates[1]["old_status"] == "open"
    assert updates[1]["new_status"] == "investigating"

    # 5. Add a manual comment
    comment_response = client.post(
        f"/api/v1/support/{ticket_id}/updates",
        json={
            "update_type": "comment",
            "content": "Looking into this now.",
            "author": "Test Engineer"
        }
    )
    assert comment_response.status_code == 200

    # 6. Verify manual comment was added
    get_response = client.get(f"/api/v1/support/{ticket_id}")
    updates = get_response.json()["updates"]
    assert len(updates) == 3
    assert updates[2]["update_type"] == "comment"

    # 7. Resolve the ticket
    resolve_response = client.patch(
        f"/api/v1/support/{ticket_id}",
        json={
            "status": "resolved",
            "resolution_notes": "Fixed the underlying issue."
        }
    )
    assert resolve_response.status_code == 200

    # 8. Verify resolution logged
    get_response = client.get(f"/api/v1/support/{ticket_id}")
    updates = get_response.json()["updates"]
    # We expect 2 updates here: one for status_change, one for resolution_note_added
    assert len(updates) == 5
    assert updates[3]["update_type"] == "status_change"
    assert updates[4]["update_type"] == "resolution_note_added"
