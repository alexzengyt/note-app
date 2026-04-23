import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.models import Note

class TestNotes:

    def test_create_note(self, client, mock_db):
        # Arrange
        def fake_refresh(obj):
            obj.id = 1
            obj.user_id = 1
            obj.created_at = datetime(2024, 1, 1)
            obj.updated_at = datetime(2024, 1, 1)

        mock_db.refresh.side_effect = fake_refresh

        # Action
        response = client.post('/notes/', json={
            "title": "Test Note",
            "content": "Test Content"
        })

        # Assert
        assert response.status_code == 201
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_list_notes(self, client, mock_db):
        # Arrange
        mock_db.exec.return_value.all.return_value = []

        # Action
        response = client.get('/notes/')

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_get_note_found(self, client, mock_db):
        # Arrange
        mock_note = Note(
            id=1,
            title="Test Note",
            content="Test Content",
            user_id=1,
            created_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 1, 1)
        )
        mock_db.get.return_value = mock_note

        # Action
        response = client.get('/notes/1')

        # Assert
        assert response.status_code == 200
        assert response.json()['title'] == "Test Note"

    def test_get_note_not_found(self, client, mock_db):
        # Arrange
        mock_db.get.return_value = None

        # Action
        response = client.get('/notes/999')

        # Assert
        assert response.status_code == 404
    
    def test_root(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_validation_endpoint(self, client):
        response = client.post('/test-validation', json={
            "title": "Test",
            "content": "Content"
        })
        assert response.status_code == 200