from app import create_app
from app.models import db, Customer, Mechanic
from app.models import Inventory
import unittest


class TestServiceTicket(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.customer = Customer(name="Test Customer", email="cust@test.com", phone="123", password="pass")
            self.mechanic = Mechanic(name="Test Mechanic", email="mech@test.com", phone="123", salary=40000)
            db.session.add_all([self.customer, self.mechanic])
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_service_ticket(self):
        service_ticket_payload = {
            "VIN": "1234ABC",
            "service_date": "2025-05-07",
            "service_desc": "Oil change and tire rotation",
            "customer_id": 1,
            "mechanic_ids": [1]
            }


        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], "1234ABC")
    
    def test_invalid_creation(self):
        service_ticket_payload = {
            "VIN": "1234ABC"
            }


        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 400)

     
    def test_edit_service_ticket_add_and_remove_mechanics(self):
        customer_resp = self.client.post("/customers/", json={
            "name": "Alex",
            "email": "alex@example.com",
            "phone": "123-321-4567",
            "password": "secure123"
        })
        self.assertEqual(customer_resp.status_code, 201)
        customer_id = customer_resp.get_json()["id"]


        mech1_resp = self.client.post("/mechanics/", json={
            "name": "Mech One",
            "email": "mech1@example.com",
            "phone": "111-111-1111",
            "salary": 50000
        })
        mech2_resp = self.client.post("/mechanics/", json={
            "name": "Mech Two",
            "email": "mech2@example.com",
            "phone": "222-222-2222",
            "salary": 55000
        })
        self.assertEqual(mech1_resp.status_code, 201)
        self.assertEqual(mech2_resp.status_code, 201)

        mechanic1_id = mech1_resp.get_json()["id"]
        mechanic2_id = mech2_resp.get_json()["id"]

        ticket_resp = self.client.post("/service_tickets/", json={
            "VIN": "A1B2C3D4",
            "service_date": "2025-05-10",
            "service_desc": "Initial inspection",
            "customer_id": customer_id,
            "mechanic_ids": [mechanic1_id]
        })
        self.assertEqual(ticket_resp.status_code, 201)
        ticket_id = ticket_resp.get_json()["id"]

        payload = {
            "add_mechanic_ids": [mechanic2_id],
            "remove_mechanic_ids": [mechanic1_id]
        }

        response = self.client.put(f"/service_tickets/{ticket_id}", json=payload)
        self.assertEqual(response.status_code, 200)

        mechanic_list = [mech["id"] for mech in response.get_json()["mechanics"]]
        self.assertIn(mechanic2_id, mechanic_list)
        self.assertNotIn(mechanic1_id, mechanic_list)

    
    
    def test_get_all_service_ticket(self):
        self.test_create_service_ticket()
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['VIN'], '1234ABC')


    def test_delete_service_ticket(self):
        self.test_create_service_ticket()
        response = self.client.delete('/service_tickets/1')
        self.assertEqual(response.status_code, 200)


    def test_add_inventory_to_ticket(self):
        service_ticket_payload = {
            "VIN": "5678XYZ",
            "service_date": "2025-05-08",
            "service_desc": "Engine diagnostics",
            "customer_id": 1,
            "mechanic_ids": [1]
        }
        self.client.post('/service_tickets/', json=service_ticket_payload)
        with self.app.app_context():
            inventory_item = Inventory(name="Oil Filter", price=29.99)
            db.session.add(inventory_item)
            db.session.commit()


        response = self.client.post('/service_tickets/1/add-inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("added to service ticket", response.json["message"])
